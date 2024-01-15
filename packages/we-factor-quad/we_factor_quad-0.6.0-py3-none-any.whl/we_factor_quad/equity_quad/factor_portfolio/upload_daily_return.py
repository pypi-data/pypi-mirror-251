import copy
import os
import operator
import pandas as pd
import numpy as np
import wiserdata as wi


def compute_daily_excess_return(start: str,
                                end: str):
    import we_factor_analysis.data_api.return_api as return_api

    returns = return_api.load_prerequisite_stk_data(start=start, end=end, if_scale=False, if_clean_suspen=False,
                                                    src='wedata_ths')
    cash_ti = return_api.load_cash_ti(start, end)

    returns['CODE_ID'] = returns['CODE_ID'].apply(lambda x: 'CN' + x.split('.')[0])
    returns = returns.drop_duplicates(['TRADE_DT', 'CODE_ID'])
    px_close = returns.pivot(index='TRADE_DT', columns='CODE_ID', values='S_DQ_ADJCLOSE')
    px_close = px_close.dropna(how='all')
    status = returns.pivot(index='TRADE_DT', columns='CODE_ID', values='S_DQ_TRADESTATUS')
    status = status.asfreq('B')
    idx_halt = (status == '停牌').asfreq('B').reindex(index=status.index)
    excess_daily_ret = px_close.asfreq('B', method='pad').pct_change()
    excess_daily_ret[(excess_daily_ret == 0.0) & idx_halt] = np.nan
    excess_daily_ret = (excess_daily_ret.sub(cash_ti.asfreq('B', method='pad').pct_change(), axis=0)
                   * (~pd.isnull(status))).dropna(how='all')

    # make monthly_ex_ret
    excess_daily_ret.index = [x.strftime('%Y%m%d') for x in list(excess_daily_ret.index)]
    stacked_excess_daily_ret = excess_daily_ret.stack(dropna=False).reset_index()
    stacked_excess_daily_ret.rename(columns=dict(zip(list(stacked_excess_daily_ret.columns),
                                                     ['date', 'code', "daily_return"])),
                                    inplace=True)
    # pivoted = stacked_excess_daily_ret.pivot(index='date', columns='code', values='daily_return')
    return stacked_excess_daily_ret


def upload_daily_excess_return(start: str,
                               end: str,
                               path_to_save="D:/jiaochayuan_files/projects"):

    save_dir = path_to_save + "/stock_daily_excess_returns"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    daily_excess_return = compute_daily_excess_return(start=start, end=end)
    filename = f"daily_excess_returns_{start}_{end}"
    path = f"{save_dir}/{filename}.gzip.parquet"
    parquet_file = os.listdir(save_dir)
    if os.path.exists(path):
        for file in parquet_file:
            os.remove(file)
    daily_excess_return.to_parquet(path=path)


def compute_monthly_return(start,
                           end) -> pd.DataFrame:
    daily_returns = pd.read_parquet("D:/jiaochayuan_files/projects/stock_daily_excess_returns/daily_excess_returns_20100101_20221031.gzip.parquet")
    pivoted_daily_returns = daily_returns.pivot(index='date', columns='code', values='daily_return')
    pivoted_daily_returns.index = pd.to_datetime(list(pivoted_daily_returns.index))

    resampled_daily_return = copy.deepcopy(pivoted_daily_returns)
    resampled_daily_return.index = resampled_daily_return.index.to_period("M")
    monthly_return = pivoted_daily_returns.groupby(level=0).apply(lambda x: x.cumsum(skipna=True).iloc[-1, :])
    monthly_return = monthly_return.to_timestamp('M')
    monthly_return.index = pd.date_range(start=start, end=end, freq='BM')
    monthly_return.iloc[0, :] = np.nan
    return monthly_return



if __name__ == '__main__':
    # daily_excess_return = compute_daily_excess_return(start="20100101", end="20221031")
    # compute_monthly_return(start="20100101", end="20221031", daily_excess_return=daily_excess_return)
    upload_daily_excess_return(start="20091231", end="20231221")
    # compute_monthly_return(start="20220101", end="20221231")
