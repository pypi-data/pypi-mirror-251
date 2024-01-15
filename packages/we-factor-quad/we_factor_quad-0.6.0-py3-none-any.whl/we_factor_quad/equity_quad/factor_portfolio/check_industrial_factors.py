import copy
import os
import pandas as pd
from we_factor_quad.equity_quad.factor_quad_equity import FactorQuadEQ
from we_factor_quad.equity_quad.factor_portfolio.full_factor_mimicking_portfolio import FmpAnalyzer
import we_factor_quad.data_api as dapi


def load_industrial_indices() -> pd.DataFrame:
    """
    load所有跟行业因子具有可比性的指数点位
    Returns: 所有行业指数，一个DataFrame
    """
    sw_l1_name_dic, sw_l2_name_dic, sw_code_dic_l1, sw_code_dic_l2, s = dapi.get_sw_name_dic()
    sw_l1_list, sw_l2_list = list(sw_l1_name_dic.keys()), list(sw_l2_name_dic.keys())
    indices_quotations = dapi.get_index_quoation_data(sw_l1_list=sw_l1_list, use_local=False)
    return indices_quotations

def get_indices_code_name_map():
    """
    指数代码和名字的mapping
    Returns:
    """
    sw_l1_name_dic, sw_l2_name_dic, sw_code_dic_l1, sw_code_dic_l2, s = dapi.get_sw_name_dic()
    names = [
        'industry_Agriculture_Forestry_Farming_Fishing',
        'industry_Mineral',
        'industry_Chemical',
        'industry_Steel',
        'industry_Non_Ferrous_Metal',
        '已退市_建筑建材',
        'industry_Mechanical_Equipment',
        'industry_Electronic',
        'industry_Transport_Equipment',
        'industry_Information_Device',
        'industry_Home_appliance',
        'industry_Food_and_Beverage',
        'industry_Textile_and_Clothing',
        'industry_Light_manufacturing',
        'industry_Biological',
        'industry_Public_Utility',
        'industry_Transportation',
        'industry_Real_Estate',
        'industry_Financial',
        'industry_Trade_and_Business',
        'industry_Community_Service',
        'industry_Information_Service',
        'industry_Other',
        'industry_Communication',
        'industry_Car',
        'industry_Bank',
        'industry_Non_Bank_Financial',
        'industry_Building_Material',
        'industry_Building_Decoration',
        'industry_Electric_Equipment',
        '重复_机械设备',
        'industry_Military',
        'industry_Computer',
        'industry_Media',
        '已退市_煤炭',
        'industry_Petroleum_and_Petrochemical',
        'industry_Environment',
        'industry_Beauty_Care'
    ]
    mapping = dict(zip(sw_l1_name_dic.keys(), names))
    return mapping


def rearrange_frames(factor_return: pd.DataFrame):
    """

    Args:
        factor_return:

    Returns:
    """
    indices = load_industrial_indices()
    indices_monthly = indices.reindex(index=factor_return.index)
    indices_return = indices_monthly.pct_change()
    mapping = get_indices_code_name_map()
    mapped_columns = (indices_return.columns.to_series().map(mapping)).tolist()
    indices_return.columns = mapped_columns
    intersection = sorted(list(set(mapped_columns).intersection(factor_return.columns)))
    indices_return = indices_return[intersection]
    industry_factor_names = [x for x in list(factor_return.columns) if x.split('_')[0] == 'industry']
    factor_return_only_industry = factor_return[industry_factor_names]
    country = factor_return['country']
    return factor_return_only_industry, indices_return, country


def get_industry_corrs(factor_return: pd.DataFrame):
    """
    Returns:

    """
    industry_factor_returns, indices_returns, country = rearrange_frames(factor_return)
    corrs = {}
    for ind in industry_factor_returns.columns:
        fr_plus_country = industry_factor_returns[ind] + country
        corr = fr_plus_country.corr(indices_returns[ind])
        corrs[ind] = corr
    corrs_df = pd.DataFrame.from_dict(corrs, orient='index', columns=['corr'])
    return corrs_df


def get_barra_factor_return(start="20100201", end="20221031"):

    raw_data = pd.read_excel("factor_return_BARRA.xlsx", index_col=0)
    raw_data.index = [x - pd.offsets.BDay(1) for x in list(raw_data.index)]
    raw_data = raw_data[(raw_data.index >= start) & (raw_data.index <= end)]
    raw_data.index.name = "date"
    return raw_data


def get_msg_barra_fr_corrs(msg_fr):
    """

    Args:
        msg_fr:
        barra_fr:

    Returns:
    """
    barra_factor_return = get_barra_factor_return()
    msg_factor_return = msg_fr.reindex(index=barra_factor_return.index)
    beta_corr = barra_factor_return['Beta'].corr(msg_factor_return['beta'])
    market_cap_corr = barra_factor_return['Size'].corr(msg_factor_return['log_markcap'])
    country_corr = barra_factor_return['Country'].corr(msg_factor_return['country'])
    rstr_corr = barra_factor_return['Momentum'].corr(msg_factor_return['rstr'])
    bp_corr = barra_factor_return['Book-to-Price'].corr(msg_factor_return['log_bp'])
    print(1)




if "__main__" == __name__:
    # factor_return = pd.read_csv("factor_return_logreturn.csv", index_col=0, parse_dates=True)
    # factor_return_onlysimplereturn = pd.read_csv("factor_return_onlysimplereturn.csv", index_col=0, parse_dates=True)
    factor_return_onlysimplereturn = dapi.wiser_fetch_factor_return(start_date="20100101", end_date="20221131",
                                                                    freq='BM', seadrive_localpath="D:\seadrive_cache_folder\zhouly\群组资料库")
    barra_factor_return = pd.read_excel("factor_return_BARRA.xlsx", index_col=0, parse_dates=True)
    get_msg_barra_fr_corrs(factor_return_onlysimplereturn)
    # log_return_version = get_industry_corrs(factor_return)
    simple_return_version = get_industry_corrs(factor_return_onlysimplereturn)
    print(1)
    # rearrange_frames(factor_return)
    # indices_return = get_indices_return()
    # mapping = get_indices_code_name_map()