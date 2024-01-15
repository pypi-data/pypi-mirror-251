import pandas as pd
import numpy as np
import copy
from we_factor_quad.equity_quad.factor_portfolio.full_factor_mimicking_portfolio import FmpAnalyzer as Fmp
import we_factor_quad.data_api as dapi
from we_factor_quad.equity_quad.factor_quad_equity import FactorQuadEQ
from we_factor_quad.equity_quad.factor_portfolio import corr_plot_helper as cplot
import seaborn as sns
from matplotlib import pyplot as plt

def get_barra_factor_return(start="20121101", end="20221031"):

    raw_data = pd.read_excel("factor_return_BARRA.xlsx", index_col=0)
    raw_data.index = [x - pd.offsets.BDay(1) for x in list(raw_data.index)]
    raw_data = raw_data[(raw_data.index >= start) & (raw_data.index <= end)]
    raw_data.index.name = "date"
    return raw_data

def wiser_get_barra_beta(start="20121101",
                         end='20221031',
                         seadrive_localpath="D:\zhouly\群组资料库",
                         factor_system: str = "202211_PRE_BARRA"):
    '''
    获取的beta一定跟barra的factor return日期是完全对齐的
    Args:

    Returns:

    '''
    from we_factor_quad.client_local import LocalClient
    client = LocalClient(f"{seadrive_localpath}")
    # wedata.login(username='admin', password='admin')
    param = {
        'domain': 'descriptor',
        'phylum': 'characteristic',
        'case': factor_system,
        'class': 'characteristic_exposure',
        'start_date': start,
        'end_date': end,
    }
    # quad = FactorQuadEQ.create_factor_quad(start_date=start, end_date=end, factor_system="202211_PRE_BARRA",
    #                                        local_path=seadrive_localpath)
    # barra_beta = quad.beta_ts
    barra_factor_return = get_barra_factor_return()
    date_list = list(barra_factor_return.index)
    barra_beta = client.query(param)[['date','code', "characteristic",'exposure']]
    barra_beta['date'] = pd.to_datetime(barra_beta['date']) + pd.offsets.BDay(1) - pd.offsets.BDay(1)
    barra_beta = barra_beta[barra_beta['date'].isin(date_list)]
    barra_beta = barra_beta.sort_values(['date', 'code'])
    barra_beta = barra_beta.pivot(index=['date', 'code'], columns='characteristic', values='exposure')
    # 将列名排成一样的
    barra_beta = barra_beta[barra_factor_return.columns]
    return barra_beta

def _get_stock_return(start: str,
                      end: str,
                      universe: list = [],
                      freq="BM",
                      seadrive_localpath="D:\zhouly\群组资料库"):
    """
    获取股票收益率
    Args:
        universe: 一个list，代表想获得股票收益的股票代码

    Returns:
    """
    stock_return = dapi.wiser_get_stock_return(sample_stk=universe,
                                               freq=freq,
                                               seadrive_localpath=seadrive_localpath,
                                               start=start,
                                               end=end)
    return stock_return

def get_barra_asset_decomposition(start="20121101",
                                  end='20221031',
                                  seadrive_localpath="D:\zhouly\群组资料库",
                                  factor_system: str = "202211_PRE_BARRA"
                                  ) -> (pd.DataFrame, pd.DataFrame):
    """
    获得barra的systematic return 和 residual return
    Returns:
    """
    barra_factor_return = get_barra_factor_return(start=start, end=end)
    barra_beta = wiser_get_barra_beta(start=start, end=end)
    all_stock_codes = sorted(list(set(barra_beta.index.get_level_values(1))))
    repeated_barra_factor_ret = pd.DataFrame(data=np.repeat(barra_factor_return.reset_index(drop=False).values,
                                                            repeats=len(all_stock_codes), axis=0),
                                             columns=[barra_factor_return.index.name] + list(barra_factor_return.columns))
    repeated_barra_factor_ret['code'] = barra_beta.index.get_level_values(1)
    repeated_barra_factor_ret = repeated_barra_factor_ret.set_index(['date', 'code'])
    stock_return = _get_stock_return(universe=all_stock_codes, start=start, end=end)
    stock_codes_in_return = sorted(list(set(stock_return.columns)))
    repeated_barra_factor_ret = \
        repeated_barra_factor_ret[repeated_barra_factor_ret.index.get_level_values(1).isin(stock_codes_in_return)]
    barra_beta = barra_beta[barra_beta.index.get_level_values(1).isin(stock_codes_in_return)]
    beta_to_use = barra_beta.shift(len(stock_codes_in_return)).dropna(how='all')
    sys_return = beta_to_use.groupby(level=[0]) \
        .apply(lambda x: (x * repeated_barra_factor_ret.loc[x.index]).sum(axis=1)).unstack() \
        .reset_index(level=1, drop=True)
    residual_return = stock_return.iloc[1:, :] - sys_return
    no_return_bool_condition = (stock_return.iloc[1:, :] != 0.0)
    no_return_bool_condition = no_return_bool_condition.replace(False, np.nan)
    residual_return = stock_return.iloc[1:, :] - sys_return
    residual_return = residual_return * no_return_bool_condition
    sys_return = sys_return * no_return_bool_condition
    # sys_return[sys_return.columns] = sys_return[sys_return.columns].astype('object')
    # residual_return[residual_return.columns] = residual_return[residual_return.columns].astype('object')
    return sys_return, residual_return


def get_we_asset_decomposition(start: str = "20121101",
                               end: str = "20221031",
                               seadrive_localpath="D:\zhouly\群组资料库"):
    quad = FactorQuadEQ.create_factor_quad(start_date=start, end_date=end, factor_system="HF25_SRAM",
                                           local_path=seadrive_localpath)
    analyzer = Fmp(quad)
    monthly_ret = dapi.wiser_get_stock_return(start=start,
                                              end=end,
                                              seadrive_localpath=seadrive_localpath,
                                              freq='BM')
    weights_df = dapi.wiser_fetch_fmp_weights(start_date=start, end_date=end,
                                              seadrive_localpath=seadrive_localpath)
    factor_return = analyzer.construct_factor_return(ret=monthly_ret, weights_df=weights_df)
    sys, residual = analyzer.factor_decompose_asset_return(stock_ret=monthly_ret, factor_return=factor_return)
    return sys, residual

def get_aligned_asset_decomposition(we_sys: pd.DataFrame=None,
                                    we_resid: pd.DataFrame=None,
                                    barra_sys: pd.DataFrame=None,
                                    barra_resid: pd.DataFrame=None,
                                    from_local=True):
    """
    输入we和barra的两套systematic return和residual return，返回时间上完全对齐的两套，包在一个字典里
    Args:
        we_sys:
        we_resid:
        barra_sys:
        barra_resid:

    Returns:
    """

    if from_local:
        barra_sys_adjed = pd.read_csv("barra_sys_adjed.csv", index_col=0, parse_dates=True)
        barra_resid_adjed = pd.read_csv("barra_resid_adjed.csv", index_col=0, parse_dates=True)
        we_sys_adjed = pd.read_csv("we_sys_adjed.csv", index_col=0, parse_dates=True)
        we_resid_adjed = pd.read_csv("we_resid_adjed.csv", index_col=0, parse_dates=True)
        return {"barra_sys": barra_sys_adjed,
                "we_sys": we_sys_adjed,
                "barra_resid": barra_resid_adjed,
                "we_resid": we_resid_adjed}
    # barra的beta比较少，所以sys和resid内的股票也比较少，所以we的两个dataframe也要缩小到跟barra对齐
    barra_codes = set(barra_sys.columns)
    we_codes = set(we_sys.columns)
    intersected_codes = sorted(list(barra_codes.intersection(we_codes)))
    barra_sys_adjed = barra_sys[intersected_codes]
    barra_resid_adjed = barra_resid[intersected_codes]
    we_sys_adjed = we_sys[intersected_codes]
    we_resid_adjed = we_resid[intersected_codes]

    return {"barra_sys": barra_sys_adjed,
            "we_sys": we_sys_adjed,
            "barra_resid": barra_resid_adjed,
            "we_resid": we_resid_adjed}

def get_sys_resid_corrs(sys_resid_dict: dict[str: pd.DataFrame],
                        use_tstats=False) -> (pd.DataFrame, pd.DataFrame):
    """
    分别获取barra和我们的系统性和residual return的correlation，返回一对dataframe
    Args:
        sys_resid_dict:

    Returns:
    """
    we_corr = cplot.get_df_corrs(df1=sys_resid_dict['we_sys'],
                                 df2=sys_resid_dict['we_resid'],
                                 tstats_corr=use_tstats)
    barra_corr = cplot.get_df_corrs(df1=sys_resid_dict['barra_sys'],
                                    df2=sys_resid_dict['barra_resid'],
                                    tstats_corr=use_tstats)
    we_corr.columns = ['sys_resid_corrs']
    barra_corr.columns = ['sys_resid_corrs']
    return we_corr, barra_corr


def get_summary_stats(ret_dict: pd.DataFrame):
    """
    Args:
        ret:

    Returns:
    """
    for k in ret_dict.keys():
        sum_stat = cplot.summary_stats(ret_dict[k])
        sum_stat.to_excel(f"{k}_sumstats.xlsx")

def get_resid_ar(lag_num: int,
                 resid_df: pd.DataFrame) -> pd.DataFrame:
    """
    Args:
        lag_num:
        resid:

    Returns:
    """
    shifted_resid_df = copy.deepcopy(resid_df).shift(lag_num)
    resid_df1 = copy.deepcopy(resid_df.iloc[lag_num:, :])
    resid_df2 = shifted_resid_df.dropna(how='all',axis=0)
    ar_lag = cplot.get_df_corrs(df1=resid_df1, df2=resid_df2)
    ar_lag.columns = ['AR1']
    return ar_lag

if __name__ == '__main__':
    start = "20121101"
    end = "20221031"
    # barra_fr = get_barra_factor_return()
    # barra_beta = wiser_get_barra_beta()
    # barra_sys, barra_resid = get_barra_asset_decomposition()
    # _get_stock_return()
    # we_sys, we_resid = get_we_asset_decomposition()
    # webarra_sys_resid = get_aligned_asset_decomposition(we_sys=we_sys, we_resid=we_resid,
    #                                                     barra_sys=barra_sys, barra_resid=barra_resid, from_local=False)
    webarra_sys_resid = get_aligned_asset_decomposition()
    # get_summary_stats(ret_dict=webarra_sys_resid)
    # quad = FactorQuadEQ.create_factor_quad(start_date="20121101", end_date="20221031", factor_system="HF25_SRAM",
    #                                        local_path="D:\seadrive_cache_folder\zhouly\群组资料库")
    # analyzer = Fmp(quad)
    # monthly_ret = dapi.wiser_get_stock_return(start="20121101",
    #                                           end="20221031",
    #                                           seadrive_localpath="D:\zhouly\群组资料库",
    #                                           freq='BM')
    # weights_df = dapi.wiser_fetch_fmp_weights(start_date="20121101", end_date="20221031",
    #                                           seadrive_localpath="D:\seadrive_cache_folder\zhouly\群组资料库")
    # factor_return = analyzer.construct_factor_return(ret=monthly_ret, weights_df=weights_df)

    # we_corr, barra_corr = get_sys_resid_corrs(webarra_sys_resid, use_tstats=False)
    # cplot.plot_we_barra_ret_corr(we_corrs=we_corr, barra_corrs=barra_corr)
    # all_corrs = cplot.get_stock_all_factors_correlation(residual=webarra_sys_resid["we_resid"], factor_return=factor_return)
    # cplot.draw_corrs_hist(all_corrs=all_corrs)
    # cplot.plot_return_decomposition(ret=monthly_ret,
    #                                 sys_ret=webarra_sys_resid["barra_sys"],
    #                                 resid_ret=webarra_sys_resid["barra_resid"],
    #                                 code="CN601398",
    #                                 stock_name="ICBC")
    # ar1_barra = get_resid_ar(lag_num=1, resid_df=webarra_sys_resid["barra_resid"])
    # ar1_igsm = get_resid_ar(lag_num=1, resid_df=webarra_sys_resid["we_resid"])
    cplot.plot_stock_rolling_corrs(we_sys_ret=webarra_sys_resid['we_sys'],
                                   we_resid_ret=webarra_sys_resid['we_resid'],
                                   barra_sys_ret=webarra_sys_resid['barra_sys'],
                                   barra_resid_ret=webarra_sys_resid['barra_resid'],
                                   code="CN300359",
                                   stock_name="Quantong Education",
                                   chinese_name="全通教育")











