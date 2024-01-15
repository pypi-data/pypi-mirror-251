import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import ticker
from math import sqrt
import copy


def get_stock_single_factor_correlation(factor_name: str,
                                        residual: pd.DataFrame,
                                        factor_return: pd.DataFrame,
                                        min_period=50) -> pd.DataFrame:
    """

    Args:
        min_period:
        factor_name:
        residual:
        factor_return:
    Returns:
    """
    corrs = []
    single_factor_return = factor_return.loc[:, factor_name]
    for col in residual.columns:
        corr = residual.loc[:, col].corr(other=single_factor_return, min_periods=min_period)
        corrs.append(corr)
    single_corr_df = pd.DataFrame(data=np.array(corrs), index=residual.columns, columns=[factor_name])
    return single_corr_df

def get_df_corrs(df1: pd.DataFrame,
                 df2: pd.DataFrame,
                 tstats_corr: bool = False,
                 min_period=50):
    """
    计算两个index和column完全一致dataframe每一列对每一列的correlation
    Args:
        sys_return:
        resid_return:

    Returns:
    """
    all_codes = list(df1.columns)
    corrs = []
    for col in all_codes:
        if tstats_corr:
            sample_size = (~pd.isnull(df1[col])).sum()
            corr = df2[col].astype("float").corr(other=df1[col].astype("float"), min_periods=min_period) * np.sqrt(sample_size)
        else:
            corr = df2[col].astype("float").corr(other=df1[col].astype("float"), min_periods=min_period)
        corrs.append(corr)
    corr_df = pd.DataFrame(data=np.array(corrs).reshape(1, -1), columns=all_codes)
    corr_df = corr_df.T
    return corr_df


def get_stock_all_factors_correlation(residual: pd.DataFrame,
                                      factor_return: pd.DataFrame) -> pd.DataFrame:
    """

    Args:
        residual:
        factor_return:

    Returns:
    """
    all_corrs = pd.DataFrame([])
    for factor_name in factor_return.columns:
        single_factor_corr = get_stock_single_factor_correlation(factor_name=factor_name,
                                                                 residual=residual,
                                                                 factor_return=factor_return)
        all_corrs = pd.concat([all_corrs, single_factor_corr], axis=1)
    return all_corrs


def draw_corrs_hist(all_corrs: pd.DataFrame):
    """

    Args:
        all_corrs:个股， 因子在所有时间上的correlation的dataframe

    Returns:
    """
    for i in range(all_corrs.shape[1]):
        print(f"Ploting Residual_{all_corrs.columns[i]}_corr")
        single_factor_stock_corr = all_corrs.iloc[:, i]
        print(f"count is {single_factor_stock_corr.count()}")
        print(f"mean is {single_factor_stock_corr.mean()}")
        ax1 = sns.histplot(data=single_factor_stock_corr, bins=60)
        # ax1.set(xticklabels=[])
        ax1.set_title(f"Residual_{all_corrs.columns[i]}_corr")
        hist_figure = ax1.get_figure()
        hist_figure.savefig(f"IGSM_Residual_{all_corrs.columns[i]}_corr.png", dpi=500)
        plt.clf()


def summary_stats(ret, compounding=0, sampling_freq='BM', annual_fac=12.0):
    """
    return summary stats
    :param ret: DataFrame or Series of Returns
    :param compounding:
    :param sampling_freq:
    :param annual_fac: annualization factor for the corresponding frequency
    :return:
    """
    if isinstance(ret, pd.Series):
        ret = pd.DataFrame({'ret': ret})
    if compounding:
        ret_m = ret.cumprod().asfreq(sampling_freq, method='pad').pct_change()
    else:
        ret_m = ret.cumsum().asfreq(sampling_freq, method='pad').diff()

    summary = {'count': ((ret_m != 0.0) & (~pd.isnull(ret_m))).sum(),
               '0Mean': ret_m.mean() * annual_fac,
               '1Vol': ret_m.std() * np.sqrt(annual_fac),
               '2Sharpe': ret_m.mean() / ret_m.std() * np.sqrt(annual_fac),
               '3Skewness': (100.0 * ret_m).skew(),
               '4Kurt': (100.0 * ret_m).kurt(),
               '5AR(1)': ret_m.corrwith(ret_m.shift(1))}
    return pd.DataFrame(summary).T


def plot_residual_vols(all_residual: pd.DataFrame,
                       annual_fac=12.0):
    """

    Args:
        all_residual:
        annual_fac:

    Returns:

    """
    residual_vols = all_residual.std() * np.sqrt(annual_fac)
    plt.clf()
    ax1 = sns.histplot(data=residual_vols, bins=100)
    ax1.set_title(f"Residual_vols")
    hist_figure = ax1.get_figure()
    hist_figure.savefig(f"Residual_vols.png", dpi=500)

def plot_we_barra_ret_corr(we_corrs: pd.DataFrame,
                           barra_corrs: pd.DataFrame):
    """
    传入两个行列完全一致的correlation dataframe，列名表示计算的是什么correlation，列名是股票代码，画出的correlation分布，画在一张图里
    Args:
        we_corr:
        barra_corr:

    Returns:
    """
    _we_corrs = copy.deepcopy(we_corrs)
    _barra_corrs = copy.deepcopy(barra_corrs)
    # _we_corrs.columns = ['sys_resid_corrs']
    # _barra_corrs.columns=['sys_resid_corrs']
    col_name = _we_corrs.columns[0]
    _we_corrs['type'] = 'igsm'
    _barra_corrs['type'] = 'barra'
    _barra_corrs.index = [f"{x}_barra" for x in _barra_corrs.index]
    concated_corrs = pd.concat([_we_corrs, _barra_corrs])
    sns.set_context("paper", font_scale=0.9)
    ax1 = sns.histplot(palette=sns.color_palette("colorblind",2),
                       data=concated_corrs,
                       bins=60,
                       x=col_name,
                       hue='type',
                       alpha = 0.3)
    # ax1.set(xticklabels=[])
    ax1.set_title(f"igsm_vs_barra_{col_name}")
    # plt.legend(loc='upper right')
    hist_figure = ax1.get_figure()
    hist_figure.savefig(f"igsm_vs_barra_{col_name}.png", dpi=500)
    plt.clf()

def plot_return_decomposition(ret: pd.DataFrame,
                              sys_ret: pd.DataFrame,
                              resid_ret: pd.DataFrame,
                              code: str,
                              stock_name: str,
                              model_name: str = "igsm"):
    """
    画图，三条线，分别代表总return，系统性return和residual return的time series，画到一张图里
    Args:
        ret:
        sys_ret:
        resid_ret:
        code: 股票代码

    Returns:
    """
    cols = ["date", code]
    code_return = ret[code].reset_index()
    code_sys_return = sys_ret[code].reset_index()
    code_resid_return = resid_ret[code].reset_index()
    code_return = code_return[code_return.index.isin(code_sys_return.index)]
    code_return.columns = cols
    code_sys_return.columns = cols
    code_resid_return.columns = cols
    code_return['return_type'] = "total_ret"
    code_sys_return['return_type'] = "sys_ret"
    code_resid_return['return_type'] = "resid_ret"
    concated_df = pd.concat([code_return, code_sys_return, code_resid_return], axis=0)
    sns.set_context("paper", font_scale=0.7)
    ax1 = sns.lineplot(palette=sns.color_palette("deep",3), data=concated_df, x='date', y=code, hue='return_type', alpha=0.6)
    ax1.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=2))
    # ax1.set(xticklabels=[])
    ax1.set_title(f"{code} {stock_name} return decomposition {model_name}")
    plt.legend(loc='upper right', prop={'size': 6})
    plt.ylabel(f"{code} return")
    hist_figure = ax1.get_figure()
    hist_figure.savefig(f"{code} return decomposition {model_name}", dpi=500)
    plt.clf()

def plot_stock_rolling_corrs(we_sys_ret: pd.DataFrame,
                             we_resid_ret: pd.DataFrame,
                             barra_sys_ret: pd.DataFrame,
                             barra_resid_ret: pd.DataFrame,
                             code: str,
                             stock_name: str,
                             chinese_name='',
                             rolling_period: int = 12):
    """
    选择一支股票，将我们和barra的rolling的correlation画在一张图里，两条线

    Args:
        sys_ret:
        resid_ret:
        code:
        rolling_period: rolling多少个月
        stock_name:

    Returns:

    """
    we_stock_sys = we_sys_ret[code]
    we_stock_resid = we_resid_ret[code]
    barra_stock_sys = barra_sys_ret[code]
    barra_stock_resid = barra_resid_ret[code]
    we_rolling_corrs = we_stock_sys.rolling(rolling_period).corr(other=we_stock_resid).dropna().to_frame()
    barra_rolling_corrs = barra_stock_sys.rolling(rolling_period).corr(other=barra_stock_resid).dropna().to_frame()
    we_rolling_corrs['model_name'] = 'igsm'
    barra_rolling_corrs['model_name'] = 'barra'
    concated = pd.concat([we_rolling_corrs, barra_rolling_corrs], axis=0).reset_index()

    sns.set_context("paper", font_scale=0.7)
    sns.set_style('darkgrid')
    ax1 = sns.lineplot(palette=sns.color_palette("dark", 2),
                       data=concated,
                       x="date",
                       y=code,
                       style="model_name",
                       markers=True,
                       hue='model_name',
                       alpha=0.6)
    ax1.set_title(f"{code} {stock_name} sys_resid {rolling_period}m rolling_corrs")
    plt.legend(loc='upper right', prop={'size': 6})
    plt.ylabel(f"{code} corrs")
    hist_figure = ax1.get_figure()
    hist_figure.savefig(f"{code}_{chinese_name}_{rolling_period}m rolling_corrs", dpi=500)
    plt.clf()



