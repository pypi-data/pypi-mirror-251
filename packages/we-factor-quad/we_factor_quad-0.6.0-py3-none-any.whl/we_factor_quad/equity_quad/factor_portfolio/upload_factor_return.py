import copy
import os
import pandas as pd
from we_factor_quad.equity_quad.factor_quad_equity import FactorQuadEQ
from we_factor_quad.equity_quad.factor_portfolio.full_factor_mimicking_portfolio import FmpAnalyzer
import we_factor_quad.data_api as dapi


def compute_and_save_fr_locally(start_date: str,
                                end_date: str,
                                factor_system='HF25_SRAM_DAILY_V0',
                                path_to_save="D:/jiaochayuan_files/projects"):
    """

    Args:
        start_date:
        end_date:

        factor_system:
        path_to_save:

    Returns:

    """
    factorquad = FactorQuadEQ.create_factor_quad(factor_system=factor_system,
                                                 start_date=start_date,
                                                 end_date=end_date,
                                                 from_src=1,
                                                 local_path="D:\seadrive_cache_folder\zhouly\群组资料库")
    analyzer = FmpAnalyzer(quad=factorquad)
    end_date_range = list(pd.DataFrame(factorquad.date_list).set_index([0]).to_period('M').to_timestamp('M').index)
    year_range = sorted(list(set([x.year for x in end_date_range])))
    weights_df = analyzer.get_portfolio_weights(start_date=start_date,
                                                end_date=end_date,
                                                freq='B')
    # ret = dapi.wiser_get_stock_return(start=start_date,
    #                                   end=end_date,
    #                                   sample_stk=[],
    #                                   seadrive_localpath="D:\seadrive_cache_folder\zhouly\群组资料库",
    #                                   freq='B')
    ret = dapi.get_stock_return(start=start_date,
                                end=end_date,
                                log_return=False,
                                sample_stk=[],
                                freq='B')
    factor_return = analyzer.construct_factor_return(weights_df=weights_df, ret=ret)
    # sys, resid = analyzer.factor_decompose_asset_return(factor_return=factor_return, stock_ret=ret)
    # factorquad.add_country_factor()
    # sigma_t = factorquad.sigma_withcountry_ts[factorquad.sigma_withcountry_ts[factorquad._time_col_name] == "20231031"] \
    #     .drop(labels=[factorquad._time_col_name], axis=1).set_index('source')
    # from we_factor_quad.factor_quad import decompose_vcv
    # sigma_vec, corr_mat = decompose_vcv(sigma_t)
    # corrs = []
    # for date in factorquad.date_list:
    #     sigma_t = factorquad.sigma_withcountry_ts[
    #         factorquad.sigma_withcountry_ts[factorquad._time_col_name] == date] \
    #         .drop(labels=[factorquad._time_col_name], axis=1).set_index('source')
    #     sigma_vec, corr_mat = decompose_vcv(sigma_t)
    #     corrs.append(corr_mat)
    # corrs_mean = sum(corrs) / len(corrs)
    # from we_factor_quad.equity_quad.factor_portfolio.corr_plot_helper import get_stock_all_factors_correlation, draw_corrs_hist
    # all_corrs = get_stock_all_factors_correlation(residual=resid, factor_return=factor_return)
    # draw_corrs_hist(all_corrs=all_corrs)
    save_dir = path_to_save + "/characteristic_return"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 生成一个小factor_quad，获取目前所有行业名字
    # latest_industries = FactorQuadEQ.create_factor_quad(factor_system=factor_system,
    #                                                     start_date=latest_start_date,
    #                                                     end_date=latest_end_date,
    #                                                     from_src=1,
    #                                                     local_path="D:\seadrive_cache_folder\zhouly\群组资料库").beta_ts.columns
    raw_data = FactorQuadEQ.factor_quads_download(factor_system=factor_system,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  from_src=1,
                                                  local_path="D:\seadrive_cache_folder\zhouly\群组资料库")
    latest_factor_number = list(set(raw_data['characteristic_exposure']['characteristic']))
    latest_industries = [x for x in latest_factor_number if x.split('_')[0] == 'industry']
    # assert len(latest_industries) == 35, "wrong number of industries!"
    factor_return_industries = [x for x in factor_return.columns if x.split('_')[0] == 'industry']
    industry_diff = list(set(latest_industries).difference(factor_return_industries))
    if len(industry_diff) != 0:
        factor_return = pd.concat([factor_return, pd.DataFrame(data=0.0, index=factor_return.index, columns=industry_diff)],
                                  axis=1)
    assert len(latest_factor_number) + 1 == len(factor_return.columns), "wrong number of factors!"
    stacked_factor_return = factor_return.stack(dropna=False).reset_index()
    stacked_factor_return.rename(columns=dict(zip(list(stacked_factor_return.columns),
                                                  ['date', 'characteristic', 'return'])), inplace=True)

    stacked_factor_return['date'] = stacked_factor_return['date'].apply(lambda x: x.strftime('%Y%m%d'))
    type_list = list(stacked_factor_return['characteristic'])
    for i in range(len(type_list)):
        if type_list[i].split("_")[0] == "industry":
            type_list[i] = "industry"
        elif type_list[i] == "country":
            pass
        else:
            type_list[i] = "style"
    stacked_factor_return['type'] = type_list
    filename = f"characteristic_return_{factor_system}_{str(year_range[0])}_{str(year_range[-1])}"

    path = f"{save_dir}/{filename}_.gzip.parquet"
    if not os.path.exists(path):
        stacked_factor_return.to_parquet(path=path)

def update_daily_factor_return(factor_system='HF25_SRAM_DAILY_V0',
                               output_path="D:/jiaochayuan_files/projects/characteristic_return",
                               date_of_running="20231114"):
    """
    因子收益日更。输出最新一天的factor_return到一个parquet文件。这个函数要在有了当天四元组数据，且有当天股价数据后才能跑。
    例：
    比如要跑20231110周五的，在有了20231110的四元组后，再来跑这个。如果没有当天的四元组(比如当天四元组日更还没跑，或者要跑的那天是节假日)，
    那么不会生成任何parquet文件，直接结束。如果数仓有当天的四元组数据，那么跑完会在output_path这个地址下生成对应的parquet文件。
    Args:
        factor_system: 日频的四元组文件夹名'HF25_SRAM_DAILY_V0'
        output_path: 储存文件的本地文件夹地址,这个文件夹必须已经存在
        date_of_running: 指需要跑的那一天的时间，比如要跑20231110周五的数据，就输入“20231110”，注意这不是指本机服务器的时间

    Returns:
    """
    import datetime
    import pathlib
    assert os.path.exists(output_path), "The output path does not exist!"
    datetime_of_running = datetime.datetime.strptime(date_of_running, "%Y%m%d")
    start_date = (datetime_of_running - datetime.timedelta(days=15)).strftime("%Y%m%d")
    factorquad = FactorQuadEQ.create_factor_quad(factor_system=factor_system,
                                                 start_date=start_date,
                                                 end_date=date_of_running,
                                                 from_src=0)
    if pd.Timestamp(factorquad.date_list[-1]).strftime("%Y%m%d") != date_of_running:
        print("当天还未跑四元组日更，或为节假日，本程序更新因子收益失败自动结束，请先运行四元组日更，或选择下一个交易日运行")
        return
    analyzer = FmpAnalyzer(quad=factorquad)
    end_date_range = list(pd.DataFrame(factorquad.date_list).set_index([0]).to_period('M').to_timestamp('M').index)
    year_range = sorted(list(set([x.year for x in end_date_range])))
    weights_df = analyzer.get_portfolio_weights(start_date=start_date,
                                                end_date=date_of_running,
                                                freq='B')
    ret = dapi.get_stock_return(start=start_date,
                                end=date_of_running,
                                freq='B')
    return_target_date = ret.index[-1].strftime("%Y%m%d")
    if return_target_date != date_of_running:
        print("当天股票收益或股票价格尚未更新，或为节假日，本程序更新因子收益失败自动结束，请先更新股票收益或股票价格，或选择下一个交易日运行")
        return
    factor_return = analyzer.construct_factor_return(weights_df=weights_df, ret=ret)
    latest_day_factor_return = factor_return.tail(1)
    factor_return_target_date = latest_day_factor_return.index[0].strftime("%Y%m%d")

    if factor_return_target_date != date_of_running:
        print("不存在需要更新的因子收益数据，可能是因为当天还未跑四元组日更，或为节假日。"
              "本程序更新因子收益失败自动结束，请先运行四元组日更，或选择下一个交易日运行")
        return
    stacked_factor_return = factor_return.stack(dropna=False).reset_index()
    stacked_factor_return.rename(columns=dict(zip(list(stacked_factor_return.columns),
                                                  ['date', 'characteristic', 'return'])), inplace=True)

    stacked_factor_return['date'] = stacked_factor_return['date'].apply(lambda x: x.strftime('%Y%m%d'))
    type_list = list(stacked_factor_return['characteristic'])
    for i in range(len(type_list)):
        if type_list[i].split("_")[0] == "industry":
            type_list[i] = "industry"
        elif type_list[i] == "country":
            pass
        else:
            type_list[i] = "style"
    stacked_factor_return['type'] = type_list
    filename = f"characteristic_return_{factor_system}_{factor_return_target_date}.gzip.parquet"
    path = pathlib.Path.joinpath(pathlib.Path(output_path), filename)
    # 如果文件已存在，则删除替换文件
    if path.is_file():
        path.unlink()
    stacked_factor_return.to_parquet(path=str(path))
    print(f"{date_of_running}因子收益更新成功，运行结束~")



if __name__ == "__main__":
    start_date = "20231201"
    end_date = "20231228"
    compute_and_save_fr_locally(start_date=start_date, end_date=end_date)
    # update_daily_factor_return()
    # g = os.walk("D:\jiaochayuan_files\projects\characteristic_return")
    # for path, dir_list, file_list in g:
    #     for file_name in file_list:
    #         fr_df = pd.read_parquet(path + "/" + file_name)[['date', 'characteristic', 'return']]
    #         pivoted = fr_df.pivot(index='date', columns='characteristic', values='return')
    #         num_nan = pd.isnull(pivoted).sum().sum()
    #         print(num_nan)
