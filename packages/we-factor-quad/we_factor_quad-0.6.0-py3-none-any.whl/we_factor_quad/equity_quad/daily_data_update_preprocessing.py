import os
from copy import copy, deepcopy
import pandas as pd
import numpy as np
from we_factor_quad.equity_quad.factor_quad_equity import FactorQuadEQ
from we_factor_quad.factor_quad import FactorQuad
from we_factor_quad.equity_quad.factor_portfolio.full_factor_mimicking_portfolio import FmpAnalyzer
import we_factor_quad.data_api as dapi
from we_factor_quad.factor_quad_settings import FmpUniverseConfig, settings


def get_filled_psi(start_date,
                   end_date,
                   daily_return: pd.DataFrame = pd.DataFrame([]),
                   factor_system: str = "HF25_SRAM_DAILY_V0",
                   from_src: int = 3,
                   local_path: str = 'D:\jiaochayuan_files\projects\we_factor_quad_',
                   seadrive_localpath='D:\seadrive_cache_folder\zhouly\群组资料库'):
    """
    应该是输入一个要更新日期+前5个工作日(共6天)的asset return和用要更新日期+前一天的factorquad，然后输出一个填过的psi
    Args:
        local_path: 用来存放csv新增四元组数据的根文件夹地址，比如HF25_SRAM_DAILY这个文件夹的所在文件夹
        from_src: 3指用csv版本四元组数据生成factorquad
        factor_system: 用来存放csv新增四元组数据的根文件夹名字，比如“HF25_SRAM_DAILY”
        end_date: 生成factorquad的结束日期
        start_date:生成factorquad的起始日期
        daily_return: 当日和前6日的日股票收益率，必须是宽表，行为日期，列为股票。如果这个参数是None，那么将会自动从数据库里取return数据
        seadrive_localpath:

    Returns:
    """
    delta_time = (pd.Timestamp(end_date) - pd.Timestamp(start_date)).days
    # ====================================这里日后要改成通过csv生成factorquad================================================
    quad = FactorQuadEQ.create_factor_quad(start_date=start_date,
                                           end_date=end_date,
                                           factor_system=factor_system,
                                           from_src=from_src,
                                           local_path=local_path)
    # quad.capped_psi_adjustment()
    # ==================================================================================================================
    beta_ts, psi_ts = deepcopy(quad.beta_ts), deepcopy(quad.psi_ts)
    beta_ts["code"] = ["CN" + x.split(".")[0] for x in beta_ts["code"]]
    psi_ts["code"] = ["CN" + x.split(".")[0] for x in psi_ts["code"]]
    beta = beta_ts.sort_values(by=["date", "code"])[["date", "code"] +
                                                    settings.msg_factors_name].set_index(["date", "code"])
    psi = psi_ts[["date", "code", 'var']].sort_values(by=["date", "code"]).set_index(["date", "code"])

    status = ((beta != 0.0).sum(axis=1)) == 0.0
    # 已上市股票的beta和psi
    valid_index = list(status[status == 0.0].index)
    valid_psi = psi[psi.index.isin(valid_index)]
    valid_beta = beta[beta.index.isin(valid_index)]

    # 去除当天beta和psi股票日期组合的差，因为现在填充的实际上是用5天前beta算出来的
    beta_universe_5ago = get_beta_universe_5ago(start=start_date,
                                                end=end_date,
                                                from_src=from_src,
                                                local_path=local_path,
                                                factor_system=factor_system,
                                                original_beta_dates=quad.date_list)

    # 看风格因子是否三个以上为0
    condition = (valid_beta == 0).sum(axis=1) >= 3
    condition_index = condition[condition == True].index
    nan_psi = valid_psi[valid_psi.index.isin(condition_index)]
    need_fill_index = nan_psi[nan_psi['var'].isna()]
    need_fill_index = need_fill_index[need_fill_index.index.isin(beta_universe_5ago)]

    # 如果没有psi需要被填，那么直接返回一个空Dataframe
    if len(list(need_fill_index.index)) == 0:
        print("No missing psi to be filled!")
        return pd.DataFrame([])
    # =================================================================================================================
    ret_start = (quad.date_list[0] - pd.offsets.BDay(15)).strftime('%Y%m%d')
    ret_end = pd.Timestamp(quad.date_list[-1]).strftime('%Y%m%d')

    if daily_return.shape[0] == 0 or daily_return[daily_return.index <= quad.date_list[0]].shape[0] < 5:
        _return = dapi.get_stock_return(start=ret_start,
                                        end=ret_end,
                                        sample_stk=[],
                                        freq='B')
        # _return2 = pd.read_csv("D:\jiaochayuan_files\projects\we_factor_quad_\we_factor_quad\equity_quad/return.csv",
        #                       index_col=0, parse_dates=True)
        # _return2 = _return2.reindex(columns=sorted(list(set(_return.columns))), index=_return.index)
        # _return = _return2
        # _return = _return.fillna(0.0)
        # print(1)
    else:
        _return = deepcopy(daily_return)
    latest_date_return = _return.iloc[(-delta_time-1):, :]
    latest_date_return.index.name = "date"
    loc_noreturn = pd.isnull(latest_date_return)
    fmp_obj = FmpAnalyzer(quad=quad)
    weights = fmp_obj.get_portfolio_weights(start_date=start_date,
                                            end_date=end_date,
                                            freq='B',
                                            universe_conf=FmpUniverseConfig.universe_config['default_universe'])

    _return = _return.fillna(0.0).rolling(5).sum()
    _return = _return.reindex(index=quad.date_list)
    total_return_filter = loc_noreturn
    factor_return = fmp_obj.construct_factor_return(weights_df=weights, ret=_return)

    revive_beta_with_scale(quad=quad, hetero_adj=False)
    _return = revive_stock_ret_with_scale(quad=quad, ret=_return)
    total_return_filter = total_return_filter.replace(True, np.nan).replace(False, 1.0)
    sys_return, res_return = fmp_obj.factor_decompose_asset_return(factor_return=factor_return,
                                                                   stock_ret=_return)
    total_return_filter = total_return_filter.reindex(columns=res_return.columns, index=res_return.index)
    res_return = res_return * total_return_filter
    all_psi = ((res_return ** 2 * 52).ewm(com=0.003).mean()).stack(dropna=False)

    filled_nan_psi = all_psi[all_psi.index.isin(need_fill_index.index)]
    filled_nan_psi = filled_nan_psi.replace(0.0, np.nan).dropna()
    filled_nan_psi.index.names = ['date', 'code']

    multi_index_psi = psi_ts[['date', 'code', 'var']].set_index(['date', 'code'])

    all_nan_psi = multi_index_psi[multi_index_psi['var'].isna()]

    # 求每天市场psi中位数
    date_mean_psi = multi_index_psi.groupby(level=[0]).transform('median')
    filled_nan_psi = filled_nan_psi.to_frame()
    filled_nan_psi.columns = ['var']
    _filled_nan_psi = all_nan_psi.combine_first(filled_nan_psi)
    filled_nan_psi = _filled_nan_psi.combine_first(date_mean_psi[date_mean_psi.index.isin(_filled_nan_psi.index)])['var']

    # final_psi = filled_nan_psi.reset_index()
    # final_psi.columns = ['date', 'code', 'var']
    # final_psi['date'] = [x.strftime('%Y%m%d') for x in final_psi['date']]
    # final_psi['code'] = [map_code(x) for x in final_psi['code']]
    # min_date = final_psi['date'].min()
    # max_date = final_psi['date'].max()
    # path = f"D:/jiaochayuan_files/projects/filled_psi/filled_psi_{min_date}_{max_date}.gzip.parquet"
    # final_psi.to_parquet(path=path)

    if filled_nan_psi.shape[0] == 0:
        return pd.DataFrame([])
    else:
        return filled_nan_psi.unstack()


def revive_beta_with_scale(quad: FactorQuadEQ,
                           hetero_adj=False):
    """
    将beta除以1/scale的平均值，以还原beta
    Args:
        hetero_adj:
        quad:

    Returns:
    """
    scale_inverse = deepcopy(quad.scale_ts)
    scale_inverse['scale'] = 1 / scale_inverse['scale']
    ave_scale_inverse = scale_inverse.groupby(by='date').transform("mean")
    reviving_beta = quad.beta_ts.set_index(['date', 'code'])
    ave_scale_inverse.index = reviving_beta.index
    # ==========================
    if not hetero_adj:
        np_operation = reviving_beta.values / ave_scale_inverse.values.reshape(-1, 1)
    else:
        np_operation = reviving_beta.values / scale_inverse['scale'].values.reshape(-1, 1)
    # =========================
    quad.beta_ts = pd.DataFrame(data=np_operation,
                                index=reviving_beta.index,
                                columns=reviving_beta.columns).reset_index(drop=False)


def revive_stock_ret_with_scale(quad: FactorQuadEQ,
                                ret: pd.DataFrame):
    """
    将stock return除以1/scale的平均值
    Args:
     quad:
     ret:

    Returns:
    """
    scale_inverse = (1 / deepcopy(quad.scale_ts)[['date', 'code', 'scale']].pivot(index='date',
                                                                                  columns='code',
                                                                                  values='scale'))
    scale_inverse.sort_index(inplace=True)
    scale_inverse.columns = ["CN" + x.split(".")[0] for x in scale_inverse.columns]
    scale_inverse = scale_inverse.reindex(columns=ret.columns)
    np_operation = ret.values / scale_inverse.values
    new_ret = pd.DataFrame(data=np_operation,
                           index=ret.index,
                           columns=ret.columns)
    return new_ret


def map_code(code_cn: str):
    """
    将CNxxxxxx形式的股票代码转成xxxxxx.xx形式
    Args:
        code_cn:

    Returns:
    """
    if code_cn[2] == "6":
        new_code = f"{code_cn[2:]}.SH"
    elif code_cn[2] == "0" or "3":
        new_code = f"{code_cn[2:]}.SZ"
    elif code_cn[2] == "8":
        new_code = f"{code_cn[2:]}.BJ"
    else:
        raise ValueError("stock code does not exist!")
    return new_code

def get_beta_universe_5ago(start,
                           end,
                           original_beta_dates: list[str],
                           from_src: int = 3,
                           local_path='D:\jiaochayuan_files\projects\we_factor_quad_',
                           factor_system = "HF25_SRAM_DAILY"):
    """
    获取5天前beta的universe，用于后续筛选填过的psi
    Args:

    Returns:
    """
    path_for_dates = os.path.join(local_path, factor_system)
    repo_list = sorted(os.listdir(path_for_dates))
    if start not in repo_list:
        # 寻找最小的比start_date大的位置
        min_gt_start = min(x for x in repo_list if int(x) > int(start))
        index_start = repo_list.index((min_gt_start))
    else:
        index_start = repo_list.index(start)

    if end not in repo_list:
        # 寻找最大的比end_date小的位置
        max_less_end = max(x for x in repo_list if int(x) < int(end))
        index_end = repo_list.index((max_less_end))
    else:
        index_end = repo_list.index(end)
    start_5ago = repo_list[index_start - 5]
    end_5ago = repo_list[index_end - 5]
    quad_raw = FactorQuad.factor_quads_download(start_date=start_5ago,
                                                end_date=end_5ago,
                                                factor_system=factor_system,
                                                local_path=local_path,
                                                from_src=from_src,
                                                obj_need=['characteristic_exposure'])
    beta_dates_5ago = sorted(list(set(pd.to_datetime(quad_raw['characteristic_exposure']['date'].astype(str)))))
    dates_mapping = dict(zip(beta_dates_5ago, original_beta_dates))
    beta = deepcopy(quad_raw['characteristic_exposure'])
    beta['date'] = pd.to_datetime(beta['date'].astype(str).map(dates_mapping))
    beta['code'] = ["CN" + x.split(".")[0] for x in quad_raw['characteristic_exposure']['code']]
    beta_universe_5ago = beta.set_index(['date', 'code'])
    return beta_universe_5ago.index



if __name__ == "__main__":

    get_filled_psi(start_date="20231007",
                   end_date="20240105",
                   daily_return=pd.DataFrame([]),
                   factor_system="HF25_SRAM_DAILY_V0")
