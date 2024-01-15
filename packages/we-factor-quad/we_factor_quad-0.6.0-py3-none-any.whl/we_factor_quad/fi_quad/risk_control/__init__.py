import numpy as np


def risk_manage_ptfl(ptfl_w, ptfl_vol, target_vol=0.1):
    """
    投资组合风控，将每个周期都调整到target volatility
    :param ptfl_w: T x N Dataframe, portfolio weight
    :param ptfl_vol: T x 1 Series, annualized volatility of the portfolio at each point
    :param target_vol: float, target annualized volatility
    :return:
    """
    return ptfl_w.div(ptfl_vol, axis=0) * target_vol


def compute_ptfl_ret(ptfl_w, ex_ret):
    """
    计算一个利率投资组合的收益
    :param ptfl_w: T x N Dataframe, portfolio weight
    :param ex_ret: T x M Dataframe, asset excess returns
    :return: T x 1 Series
    """
    ex_ret_w = ex_ret.reindex(columns=ptfl_w.columns, index=ptfl_w.index, fill_value=0.0)

    # Check if return is missing
    idx_nan = (np.isnan(ex_ret_w) & (~ np.isnan(ptfl_w.shift(1))))
    if idx_nan.sum().sum() > 0:
        print("Missing return for some assets of this portfolio!")
        print(ex_ret_w.loc[idx_nan.sum(1) > 0, idx_nan.sum(0) > 0])

    res = (ptfl_w.shift(1) * ex_ret_w).sum(1)
    return res


def compute_vov_var(ptfl_ret, overlap=5, rolling_win=61, target_vol=0.1, ann_factor=252,
                    alpha=0.99):
    """
    Compute VoV and Value at risk for a risk managed return series
    :param ptfl_ret: daily return dataframe: T x N portfolio
    :param overlap: estimation horizon ( by default = 5, use weekly return)
    :param rolling_win: number of periods to compute realized volatility
    :param target_vol: float: targeted volatility, in annualized terms
    :param ann_factor: annualization factor of returns (number of days in a year)
    :param alpha: the quantile threshold to compute VaR
    :return:
    """
    ptfl_ret_d = ptfl_ret.cumsum().diff(overlap)
    realized_vol = ptfl_ret_d.rolling(window=rolling_win, min_periods=int(0.5 * rolling_win)).std()
    realized_vol = realized_vol * np.sqrt(ann_factor) / np.sqrt(overlap)

    vov_ts = np.sqrt((realized_vol - target_vol) ** 2)
    value_at_risk = (ptfl_ret_d * np.sqrt(ann_factor / overlap) / target_vol).abs() \
        .quantile(alpha, axis=0)
    return ptfl_ret_d.std() * np.sqrt(ann_factor / overlap), vov_ts.mean(), value_at_risk, vov_ts
