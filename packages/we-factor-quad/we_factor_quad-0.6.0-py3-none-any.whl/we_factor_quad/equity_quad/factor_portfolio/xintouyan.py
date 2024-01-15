import pandas as pd
import numpy as np
import copy
import os
import seaborn.objects as so
from we_factor_quad.equity_quad.factor_portfolio.full_factor_mimicking_portfolio import FmpAnalyzer as Fmp
import we_factor_quad.data_api as dapi
from we_factor_quad.equity_quad.factor_quad_equity import FactorQuadEQ
from we_factor_quad.factor_quad import decompose_vcv
from we_factor_quad.equity_quad.factor_portfolio import corr_plot_helper as cplot
from we_factor_quad.equity_quad.factor_portfolio import compare_independency as cindep
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib
matplotlib.rc("font",family='DengXian')


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

def get_asset_decomposition(start: str = "20150101",
                            end: str = "20150101",
                            factor_system: str = "HF25_SRAM_DAILY_V0_monthly",
                            seadrive_localpath="D:\seadrive_cache_folder\zhouly\群组资料库") -> tuple:
    """

    Args:
        start:
        end:
        factor_system:
        seadrive_localpath:

    Returns:
    """
    if os.path.exists("msg_factor_return.csv") and os.path.exists("msg_sys.csv") and os.path.exists("msg_residual.csv"):
        factor_return = pd.read_csv("msg_factor_return.csv", index_col=0, parse_dates=True)
        sys = pd.read_csv("msg_sys.csv", index_col=0, parse_dates=True)
        residual = pd.read_csv("msg_residual.csv", index_col=0, parse_dates=True)
        return factor_return, sys, residual
    quad = FactorQuadEQ.create_factor_quad(start_date=start, end_date=end, factor_system="HF25_SRAM_DAILY_V0_monthly",
                                           from_src=3,
                                           local_path="D:\jiaochayuan_files\projects\we_factor_quad_\we_factor_quad\equity_quad/factor_portfolio")
    # quad = FactorQuadEQ.create_factor_quad(start_date=start, end_date=end, factor_system=factor_system,
    #                                        local_path=seadrive_localpath)
    analyzer = Fmp(quad)
    monthly_ret = dapi.wiser_get_stock_return(start=start,
                                              end=end,
                                              freq='BM',
                                              seadrive_localpath=seadrive_localpath)
    # monthly_ret['CN600519'].iloc[-1] += 0.0114
    monthly_ret.index = quad.date_list
    weights_df = analyzer.get_portfolio_weights(start_date=start, end_date=end)
    # factor_return = dapi.wiser_fetch_factor_return(start_date=start, end_date=end, factor_system="HF25_SRAM", seadrive_localpath=seadrive_localpath)
    factor_return = analyzer.construct_factor_return(ret=monthly_ret, weights_df=weights_df)
    # factor_return.index = list(factor_return2.index)[:-2]
    # factor_return = factor_return.combine_first(factor_return2)
    # factor_return.index.name = 'date'
    sys, residual = analyzer.factor_decompose_asset_return(stock_ret=monthly_ret, factor_return=factor_return)
    factor_return.to_csv("msg_factor_return.csv")
    sys.to_csv("msg_sys.csv")
    residual.to_csv("msg_residual.csv")
    return factor_return, sys, residual

def get_stock_return(start,
                     end,
                     code_map=False,
                     seadrive_local_path: str = "D:\seadrive_cache_folder\zhouly\群组资料库"):
    """

    Args:
        start:
        end:
        seadrive_local_path:

    Returns:

    """
    monthly_return = dapi.wiser_get_stock_return(start=start, end='20230331', freq='BM', seadrive_localpath=seadrive_localpath)
    if code_map:
        monthly_return.columns = [map_code(x) for x in monthly_return.columns]
    return monthly_return

def pick_stock_super_asset_decomposition(stock_code: str,
                                         start: str = "20150101",
                                         end: str = "20230331",
                                         seadrive_localpath: str = "D:\seadrive_cache_folder\zhouly\群组资料库"):
    """

    Args:
        stock_codes:
        sys_ret:
        resid_ret:

    Returns:
    """
    if os.path.exists(f"{stock_code}_stock_return.csv") and \
            os.path.exists(f"{stock_code}_beta_mul_factor.csv") and \
            os.path.exists(f"{stock_code}_stock_resid.csv"):

        stock_return = pd.read_csv(f"{stock_code}_stock_return.csv", index_col=0, parse_dates=True)

        beta_mul_factor = pd.read_csv(f"{stock_code}_beta_mul_factor.csv", index_col=0, parse_dates=True)
        stock_resid = pd.read_csv(f"{stock_code}_stock_resid.csv", index_col=0, parse_dates=True)
        return stock_return, beta_mul_factor, stock_resid
    quad = FactorQuadEQ.create_factor_quad(start_date=start, end_date=end, factor_system="HF25_SRAM_DAILY_V0_monthly",
                                           from_src=3,
                                           local_path="D:\jiaochayuan_files\projects\we_factor_quad_\we_factor_quad\equity_quad/factor_portfolio")
    quad.add_country_factor()
    stock_returns = dapi.wiser_get_stock_return(start=start, end=end, freq='BM', seadrive_localpath=seadrive_localpath)
    # stock_returns['CN600519'].iloc[-1] += 0.0114
    # stock_returns = stock_returns[stock_returns.index.isin(quad.date_list)]
    stock_returns.index = quad.date_list
    beta = quad.beta_withcountry_ts
    stock_beta = beta[beta['code'] == stock_code]
    stock_beta = stock_beta.drop(['code'], axis=1).set_index('date').sort_index()

    factor_return, _, resid_ret = get_asset_decomposition(start=start, end=end, factor_system="HF25_SRAM_DAILY_V0",
                                                          seadrive_localpath=seadrive_localpath)
    factor_return = factor_return[stock_beta.columns]
    # stock_beta = stock_beta[factor_return.columns]
    # stock_beta = stock_beta.shift(1).dropna(how='all')
    resid_cn_code = copy.deepcopy(resid_ret)
    resid_cn_code.columns = [map_code(x) for x in resid_ret.columns]
    stock_returns.columns = [map_code(x) for x in stock_returns.columns]
    stock_resid = resid_cn_code[[stock_code]]
    beta_mul_factor = stock_beta * factor_return
    nonzero_columns = beta_mul_factor.any()
    beta_mul_factor = beta_mul_factor.loc[:, nonzero_columns].dropna(how='all')
    stock_return = stock_returns[[stock_code]]
    stock_return = stock_return.reindex(index=stock_resid.index)
    stock_return.to_csv(f"{stock_code}_stock_return.csv")
    beta_mul_factor.to_csv(f"{stock_code}_beta_mul_factor.csv")
    stock_resid.to_csv(f"{stock_code}_stock_resid.csv")
    return stock_return, beta_mul_factor, stock_resid

def plot_return_decomposition(stock_code: str,
                              stock_name: str,
                              stock_return: pd.DataFrame,
                              beta_mul_factor: pd.DataFrame,
                              stock_resid: pd.DataFrame):
    """
    Args:
        stock_code:

    Returns:
    """

    _beta_mul_factor = copy.deepcopy(beta_mul_factor)
    _stock_return = copy.deepcopy(stock_return)
    _stock_resid = copy.deepcopy(stock_resid)
    _stock_return.index = _beta_mul_factor.index

    # beta_mul_factor_q = beta_mul_factor.groupby(pd.Grouper(freq='BQ')).sum()
    _beta_mul_factor = _beta_mul_factor[_beta_mul_factor.index > "20180101"]
    # stock_return_q = stock_return.iloc[1:, :].groupby(pd.Grouper(freq='BQ')).sum()
    _stock_return = _stock_return[_stock_return.index > "20180101"]
    # stock_resid_q = stock_resid.groupby(pd.Grouper(freq='BQ')).sum()
    _stock_resid = _stock_resid[_stock_resid.index > "20180101"]
    # _stock_return.iloc[-1] += 0.0114
    stacked_sub_return = copy.deepcopy(_beta_mul_factor)
    stacked_sub_return['residual'] = _stock_resid[stock_code]
    stacked_sub_return['total'] = _stock_return[stock_code]
    # stacked_sub_return.index = stacked_sub_return.index.to_period("Q")
    stacked_sub_return = stacked_sub_return.groupby(pd.Grouper(freq='Q')).sum()
    stock_return_q = stacked_sub_return[['total']]
    stacked_sub_return = stacked_sub_return.iloc[:, :-1]
    # 筛选因子
    stacked_sub_return = stacked_sub_return[['beta', "country", "gpm", "roe",
                                             "log_markcap", "residual"]]
    stacked_sub_return.columns = ['Beta', "市场因子", "gpm", "ROE", "市值", "residual"]
    stacked_sub_return = stacked_sub_return[["市场因子", "市值", "residual", "Beta", "ROE", "gpm"]]

    stacked_sub_return = stacked_sub_return.reset_index()
    stock_return_q = stock_return_q.reset_index()
    sns.set_context("paper", font_scale=1)
    sns.set_style('darkgrid')
    sns.set_theme(style="ticks")
    # palette = sns.color_palette("deep")
    fig, ax = plt.subplots(figsize=(18, 4))
    last_col = ""
    acc_bottom = 0.0
    for col_name in stacked_sub_return.columns[1:]:

        if last_col != "":
            if col_name == "residual":
                ax.bar(stacked_sub_return['date'], stacked_sub_return[col_name], label=col_name, width=35,
                       alpha=0.4, color='grey',
                       bottom=acc_bottom,
                       )
            else:
                ax.bar(stacked_sub_return['date'], stacked_sub_return[col_name], label=col_name, width=35,
                       bottom=acc_bottom,
                       alpha=0.7)
            acc_bottom = acc_bottom + stacked_sub_return[col_name]
        else:
            ax.bar(stacked_sub_return['date'], stacked_sub_return[col_name], label=col_name, width=35,
                   bottom=acc_bottom,
                   alpha=0.7)
            acc_bottom = acc_bottom + stacked_sub_return[col_name]
        last_col = col_name
    ax.scatter(x=stock_return_q['date'], y=stock_return_q['total'], label="total", color='black')

    ax.set_ylabel(f"{stock_code} return")
    ax.set_title(f"{stock_code} {stock_name}总收益分解", fontsize=16)
    ax.legend(fontsize=9)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=2))

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    close_price = pd.read_csv("close_price.csv", index_col=0, parse_dates=True)
    close_price.index.name = 'date'
    close_price = close_price.reset_index()
    close_price.columns = ['date', 'price']
    ax2 = ax.twinx()
    ax2 = sns.lineplot(data=close_price,
                       x='date',
                       y='price')
    ax2.fill_between(x=close_price['date'], y1=close_price['price'],
                     color='b', alpha=0.07)
    ax.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    plt.savefig(f"{stock_code} 贵州茅台总收益分解分上下副本.png", dpi=500)
    plt.show()
    plt.clf()

def plot_bar_on_latestdata(stock_code: str,
                           stock_name: str,
                           stock_return: pd.DataFrame,
                           beta_mul_factor: pd.DataFrame,
                           stock_resid: pd.DataFrame):

    _beta_mul_factor = copy.deepcopy(beta_mul_factor)
    _stock_return = copy.deepcopy(stock_return)
    _stock_resid = copy.deepcopy(stock_resid)
    _stock_return.index = _beta_mul_factor.index

    _beta_mul_factor = _beta_mul_factor[_beta_mul_factor.index > "20180101"]
    _stock_return = _stock_return[_stock_return.index > "20180101"]
    _stock_resid = _stock_resid[_stock_resid.index > "20180101"]

    stacked_sub_return = copy.deepcopy(_beta_mul_factor)
    stacked_sub_return['residual'] = _stock_resid[stock_code]

    stock_return_q = _stock_return[[stock_code]]
    last_stacked_sub_return = stacked_sub_return.iloc[-3, :]
    last_stock_return = stock_return_q.iloc[-3, :]

    last_stacked_sub_return['total'] = last_stock_return.values[0]
    last_stacked_sub_return.index.name = 'date'
    last_stacked_sub_return = last_stacked_sub_return.sort_values(ascending=False).reset_index()
    # last_stacked_sub_return = last_stacked_sub_return.iloc[:16, :]
    last_stacked_sub_return.columns = ['factor_name', "return"]
    factor_names_map = {'country': "市场因子",
                        'total': "总收益率",
                        "residual": "残差",
                        "beta": "Beta",
                        "log_st_mean": "log换手率",
                        "log_bp": "log净资产市值比",
                        "gpm": "毛利率",
                        'rstr': "相对强度",
                        "ceg": "资本支出增长率",
                        "dtop": "分红价格比",
                        "etop": "盈利价格比",
                        "mbs": "资产负债充裕度",
                        "tagr": "总资产增长率",
                        "roe": "ROE",
                        "log_std": "log日标准差",
                        "reversal_short": "短期反转",
                        "log_markcap": "市值",
                        "industry_Food_and_Beverage": "食品饮料行业因子"
                        }
    last_stacked_sub_return["factor_name"] = last_stacked_sub_return["factor_name"].map(factor_names_map)
    chinese_last_stacked_sub_return = last_stacked_sub_return[last_stacked_sub_return['factor_name'] != '总收益率']
    chinese_last_stacked_sub_return = chinese_last_stacked_sub_return[chinese_last_stacked_sub_return['factor_name'] != '残差']

    colors = ["steelblue", 'plum', "rosybrown", "chocolate", "olivedrab", "crimson", "slateblue",
              "indianred", "teal", "mediumpurple", "khaki", "tomato", "forestgreen", "maroon", "lightsalmon",
              "pink", "blue", "black"]
    color_map = dict(zip(factor_names_map.values(), colors))

    palette = sns.color_palette("deep")
    sns.set_context("paper", font_scale=1)
    sns.set_style('darkgrid')
    sns.set_theme(style="ticks")
    fig, ax = plt.subplots(figsize=(14, 8))
    ax = sns.barplot(
                     # palette=palette,
                     palette=color_map,
                     data=chinese_last_stacked_sub_return,
                     x="factor_name",
                     y='return',
                     # hue='factor_name',
                     # width=30,
                     alpha=0.7)
    residual = last_stacked_sub_return[last_stacked_sub_return['factor_name'] == '残差']['return'].iloc[0]
    total = last_stacked_sub_return[last_stacked_sub_return['factor_name'] == '总收益率']['return'].iloc[0]
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    ax.set_title(f"{stock_code}贵州茅台2023年一月总收益及因子总贡献(总收益{round(total * 100, 2)}%，"
                 f"因子收益{round((total - residual)*100, 2)}%，残差{round(residual*100, 2)}%)", fontsize=16)
    ax.set_ylabel(f"{stock_code} 因子收益贡献")
    ax.set_xlabel("")

    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=2))
    plt.xticks(rotation=40, fontsize=9)
    sns.despine()
    plt.savefig(f"{stock_code}贵州茅台总收益分解(最新数据).png", dpi=500)
    plt.show()
    plt.clf()


def plot_pairwise_return_corr_ts(stock_codes: list,
                                 start,
                                 end,
                                 stock_maps: dict,
                                 target: str = "600519.SH",
                                 add_rolling=False,
                                 seadrive_localpath="D:\zhouly\群组资料库"):
    """

    Args:
        stock_codes:
        stock_return: 全部股票的return时间序列

    Returns:

    """
    rolling_ms = pd.DataFrame([])
    if add_rolling:
        rolling_ms = pd.read_csv("茅台石化rolling.csv", index_col=0, parse_dates=True)
    if os.path.exists("all_dates_corrs.csv"):
        all_dates_corrs = pd.read_csv("all_dates_corrs.csv", index_col=[0, 1], parse_dates=True)
    else:
        quad = FactorQuadEQ.create_factor_quad(start_date=start, end_date=end, factor_system="HF25_SRAM",
                                               local_path=seadrive_localpath)

        beta_use = quad.beta_ts[quad.beta_ts['code'].isin(stock_codes)]
        systematic_cov = quad.get_systematic_cov(beta_exposure=beta_use)
        dates = quad.date_list
        all_dates_corrs = pd.DataFrame([])
        for date in dates:
            date_cov = systematic_cov[systematic_cov['date'] == date].set_index(['date', 'code'])
            _, one_date_corr = decompose_vcv(date_cov)
            all_dates_corrs = pd.concat([all_dates_corrs, one_date_corr], axis=0)

    list_corr_ts = []
    for stock_code in stock_codes:
        if stock_code == target:
            continue
        corr_temp = all_dates_corrs[all_dates_corrs.index.get_level_values(level=1) == target]
        corr = corr_temp[[stock_code]]
        corr.columns = [f"{stock_maps[target]} vs {stock_maps[stock_code]}"]
        corr = corr.droplevel(1)
        corr.index.name = 'date'
        list_corr_ts.append(corr)

    corr_tses = pd.concat([df for df in list_corr_ts], axis=1)
    if rolling_ms.shape[0] > 0:
        corr_tses['贵州茅台 vs 中国石化 rolling'] = rolling_ms

    sns.set_context("paper", font_scale=1)
    # sns.set_style('darkgrid')
    palette = sns.color_palette("dark")
    color_map = {"贵州茅台 vs 五粮液": "teal", "贵州茅台 vs 泸州老窖": "maroon", "贵州茅台 vs 舍得酒业": "olive",
                 "贵州茅台 vs 中国石化": "dimgray"}
    if rolling_ms.shape[0] > 0:
        color_map = {"贵州茅台 vs 五粮液": "teal", "贵州茅台 vs 泸州老窖": "maroon", "贵州茅台 vs 舍得酒业": "olive",
                     "贵州茅台 vs 中国石化": "dimgray", "贵州茅台 vs 中国石化 rolling": "darkorange"}

    fig, ax = plt.subplots(figsize=(15, 6))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    ax = sns.lineplot(data=corr_tses, palette=color_map, lw=2)
    ax.set_title("贵州茅台与对比对象的相关性时间序列", fontsize=16)
    sns.despine()
    plt.savefig(f"贵州茅台与对比对象的相关性时间序列.png", dpi=500)
    plt.show()
    print(1)


def plot_pairwise_return_corr_ts_expanding(stock_codes: list,
                                           # sys_return,
                                           stock_maps: dict,
                                           target: str = "600519.SH",
                                           return_rolling=False):
    """

    Args:
        stock_codes:
        stock_return: 全部股票的return时间序列

    Returns:

    """
    sys_return = pd.read_csv("msg_sys.csv", index_col=0, parse_dates=True)
    sys_return.columns = [map_code(x) for x in sys_return.columns]
    sys_return_use = sys_return[stock_codes]
    expanding_corrs = sys_return_use.rolling(24, min_periods=20).corr(pairwise=True)
    expanding_corrs = expanding_corrs[expanding_corrs.index.get_level_values(0) >= "20180101"]

    # all_dates_corrs = pd.DataFrame([])
    # for date in dates:
    #     date_cov = systematic_cov[systematic_cov['date'] == date].set_index(['date', 'code'])
    #     _, one_date_corr = decompose_vcv(date_cov)
    #     all_dates_corrs = pd.concat([all_dates_corrs, one_date_corr], axis=0)
    #
    list_corr_ts = []
    for stock_code in stock_codes:
        if stock_code == target:
            continue
        corr_temp = expanding_corrs[expanding_corrs.index.get_level_values(level=1) == target]
        corr = corr_temp[[stock_code]]
        corr.columns = [f"{stock_maps[target]} vs {stock_maps[stock_code]}"]
        corr = corr.droplevel(1)
        corr.index.name = 'date'
        list_corr_ts.append(corr)
    # print(1)
    corr_tses = pd.concat([df for df in list_corr_ts], axis=1)

    if return_rolling:
        res = corr_tses['贵州茅台 vs 中国石化']
        return res

    sns.set_context("paper", font_scale=1)
    # sns.set_style('darkgrid')
    palette = sns.color_palette("dark")
    color_map = {"贵州茅台 vs 五粮液": "teal", "贵州茅台 vs 泸州老窖": "maroon", "贵州茅台 vs 舍得酒业": "olive",
                 "贵州茅台 vs 中国石化": "dimgray"}

    fig, ax = plt.subplots(figsize=(15, 6))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    ax = sns.lineplot(data=corr_tses, palette=color_map, lw=2)
    ax.set_title("贵州茅台与对比对象的相关性时间序列_rolling", fontsize=16)
    sns.despine()
    plt.savefig(f"贵州茅台与对比对象的相关性时间序列_rolling.png", dpi=500)
    plt.show()
    print(1)



if __name__ == '__main__':
    start = "20171201"
    end = "20230331"
    stock_code = '601169.SH'
    stock_codes = ['600519.SH', '000858.SZ', "000568.SZ", "600702.SH", "600028.SH"]
    stock_maps = {'600519.SH': "贵州茅台",
                  '000858.SZ': "五粮液",
                  "000568.SZ": "泸州老窖",
                  "600702.SH": "舍得酒业",
                  "600028.SH": "中国石化"}
    seadrive_localpath="D:\seadrive_cache_folder\zhouly\群组资料库"

    stock_return, beta_mul_factor, stock_resid = pick_stock_super_asset_decomposition(start=start,
                                                                                      end=end,
                                                                                      stock_code=stock_code)
    # monthly_return = get_stock_return(start=start, end=end, code_map=True)
    plot_return_decomposition(stock_code=stock_code,
                              stock_name="北京银行",
                              stock_return=stock_return,beta_mul_factor=beta_mul_factor, stock_resid=stock_resid)

    # plot_bar_on_latestdata(stock_code=stock_code,
    #                        stock_name="贵州茅台",
    #                        stock_return=stock_return, beta_mul_factor=beta_mul_factor, stock_resid=stock_resid)
    # plot_pairwise_return_corr_ts(stock_codes=stock_codes, stock_maps=stock_maps, start=start,
    #                              end=end, seadrive_localpath=seadrive_localpath,
    #                              add_rolling=True)
    # plot_pairwise_return_corr_ts_expanding(stock_codes=stock_codes, stock_maps=stock_maps)
