import pandas as pd
import numpy as np


def calc_idx_wgt(sw_code_dic_l1, start_date, end_date):
    # 利用行业指数权重计算指数特异性风险占比
    from we_factor_quad import data_api
    idx_wgt = data_api.load_stock_index_weight(sw_code_dic_l1, data_api.ths_a_share_code_map(),
                                               start_date, end_date, freq='BM')
    return idx_wgt


def calc_idx_weighted_signal(idx_wgt_dic, signal_frame):
    ind_signal_lst = []
    ind_code_lst = []
    for i, j in idx_wgt_dic.items():
        ind_signal_lst.append(
            (j.asfreq('D',method='pad').reindex(signal_frame.index) * signal_frame).dropna(how='all',
                                                                                                  axis=1).sum(
                axis=1))
        ind_code_lst.append(i)
    ind_signal_frame = pd.concat(ind_signal_lst, axis=1)
    ind_signal_frame.columns = ind_code_lst
    return ind_signal_frame


def concat_idx_wgt_signal(idx_wgt_dic, wgt_signal_dic):
    ind_signal_lst = []
    for signal_name,signal_frame in wgt_signal_dic.items():
        ind_signal_frame = calc_idx_weighted_signal(idx_wgt_dic, signal_frame).stack().reset_index()
        ind_signal_frame.columns = ['TD_DATE', 'INDEX_CODE', signal_name]
        ind_signal_lst.append(ind_signal_frame.set_index(['TD_DATE', 'INDEX_CODE']))
    res = pd.concat(ind_signal_lst,axis=1)
    return res


def get_sw_name_dic():
    import wiserdata as widata
    widata.login(username='admin', password='admin')
    # sw一级行业列表
    param = {
        'phylum': 'ths',
        'class': 'index_basic_info',
        'filters': {'INDEX_SECTOR_NAME': ["='申万一级行业指数'"]},
        'fields': [],
        'domain': 'sheet',
    }
    sw_l1 = widata.query(param)
    sw_code_dic_l1 = sw_l1.set_index('INDEX_ID')['INDEX_CODE'].to_dict()
    # sw二级行业列表
    param = {
        'domain': 'sheet',
        'phylum': 'ths',
        'class': 'index_basic_info',
        'filters': {'INDEX_SECTOR_NAME': ["='申万二级行业指数'"]},
        'fields': []
    }
    # 调用query函数
    sw_l2 = widata.query(param)
    sw_code_dic_l2 = sw_l2.set_index('INDEX_ID')['INDEX_CODE'].to_dict()
    sw_l2_list = list(sw_l2['INDEX_CODE'])
    sw_l1_list = list(sw_l1['INDEX_CODE'])

    # sw二级行业列表
    param = {
        'domain': 'sheet',
        'phylum': 'ths',
        'class': 'industry_classi_standard',
        'filters': {'INDUSTRY_CTGRY': ["='申万行业分类'"]},
        'fields': []
    }
    # 调用query函数
    sw_map = widata.query(param)

    s1 = sw_map[sw_map['INDUSTRY_LEVEL'] == 1][
        ['INDUSTRY_CLASSI_CODE', 'INDUSTRY_CLASSI_NAME', 'CORRESP_INDUSTRY_INDEX_ID']]
    s2 = sw_map[sw_map['INDUSTRY_LEVEL'] == 2][
        ['INDUSTRY_CLASSI_CODE', 'INDUSTRY_CLASSI_NAME', 'CORRESP_INDUSTRY_INDEX_ID']]
    s2['INDUSTRY_CLASSI_CODE'] = s2['INDUSTRY_CLASSI_CODE'].str[:3]
    s2 = s2.rename(columns={'INDUSTRY_CLASSI_NAME': 'INDUSTRY_CLASSI_NAME_l2',
                            'CORRESP_INDUSTRY_INDEX_ID': 'CORRESP_INDUSTRY_INDEX_ID_l2'})
    s = s1.merge(s2, on='INDUSTRY_CLASSI_CODE').merge(sw_l2[['INDEX_CODE', 'INDEX_NAME', 'INDEX_ID']],
                                                      left_on='CORRESP_INDUSTRY_INDEX_ID_l2', right_on='INDEX_ID',
                                                      how='outer')
    s['NAME_TOT'] = s['INDUSTRY_CLASSI_NAME'] + '#' + s['INDUSTRY_CLASSI_NAME_l2']
    sw_l2_name_dic = s.dropna().set_index('INDEX_CODE')['NAME_TOT'].to_dict()

    sw_l1_name_dic = sw_l1[['INDEX_CODE', 'INDEX_NAME']].set_index('INDEX_CODE')['INDEX_NAME'].to_dict()
    return sw_l1_name_dic, sw_l2_name_dic, sw_code_dic_l1, sw_code_dic_l2, s[
        ['INDUSTRY_CLASSI_NAME', 'INDEX_CODE', 'NAME_TOT']]


def get_index_quoation_data(sw_l1_list, sw_l2_list, use_local=True,start_date=20100101):  # 获取二级行业行情
    if use_local:
        sw_l1_price_frame = pd.read_csv(
            '../../we_factor_quad/we_factor_quad/workshop/industry_analysis/sw_l1_price_frame.csv', index_col=0)
        sw_l1_amount_frame = pd.read_csv(
            '../../we_factor_quad/we_factor_quad/workshop/industry_analysis/sw_l1_amount_frame.csv', index_col=0)
        sw_l2_price_frame = pd.read_csv(
            '../../we_factor_quad/we_factor_quad/workshop/industry_analysis/sw_l2_price_frame.csv', index_col=0)
        sw_l2_amount_frame = pd.read_csv(
            '../../we_factor_quad/we_factor_quad/workshop/industry_analysis/sw_l2_amount_frame.csv', index_col=0)
    else:
        import wiserdata as wedata
        wedata.login(username='admin', password='admin')

        param = {
            'domain': 'sheet',
            'phylum': 'ths',
            'class': 'index_daily_quotation',
            'filters': {'INDEX_CODE': [f"in {sw_l2_list}"]},
            'fields': [],
        }
        sw_l2_price = wedata.query(param)
        sw_l2_price_frame = sw_l2_price.pivot(index='TD_DATE', columns='INDEX_CODE', values='LATEST_INDEX')
        sw_l2_price_frame.index = pd.to_datetime(sw_l2_price_frame.index)
        sw_l2_amount_frame = sw_l2_price.pivot(index='TD_DATE', columns='INDEX_CODE', values='TRANS_AMT')
        sw_l2_amount_frame.index = pd.to_datetime(sw_l2_amount_frame.index)
        # 获取二级行业行情
        param = {
            'domain': 'sheet',
            'phylum': 'ths',
            'class': 'index_daily_quotation',
            'filters': {'INDEX_CODE': [f"in {sw_l1_list}"]},
            'fields': [],
        }
        sw_l1_price = wedata.query(param)
        sw_l1_price_frame = sw_l1_price.pivot(index='TD_DATE', columns='INDEX_CODE', values='LATEST_INDEX')
        sw_l1_price_frame.index = pd.to_datetime(sw_l1_price_frame.index)
        sw_l1_amount_frame = sw_l1_price.pivot(index='TD_DATE', columns='INDEX_CODE', values='TRANS_AMT')
        sw_l1_amount_frame.index = pd.to_datetime(sw_l1_amount_frame.index)
    return sw_l1_price_frame, sw_l2_price_frame, sw_l1_amount_frame, sw_l2_amount_frame


def get_select_lst(sw_l1_price_frame, sw_l2_price_frame, sw_l1_name_dic, s, start='2018-01-01'):
    sw_l1_list = list(sw_l1_price_frame.columns)
    l1_corr = sw_l1_price_frame.pct_change().rename(columns=sw_l1_name_dic).loc[start:].corr().unstack().replace(1,
                                                                                                                 np.nan).dropna().describe()
    l2_sep_lst = []
    l1_select_lst = []
    l1_corr_lst = []
    l2_corr_lst = []
    for i in sw_l1_list[:]:
        ind_name = sw_l1_name_dic[i]
        ind_name_lst = [i for i in sw_l2_price_frame.rename(columns=sw_l2_name_dic).columns if i.startswith(ind_name)]
        l2_corr = sw_l2_price_frame.pct_change().rename(columns=sw_l2_name_dic)[ind_name_lst].loc[start:].corr() \
            .unstack().replace(1, np.nan).dropna().describe()
        if l2_corr.loc['50%'] <= l1_corr.loc['75%']:
            l2_sep_lst.append(i)
            l2_corr_lst.append(l2_corr)
        else:
            l1_select_lst.append(i)
            l1_corr_lst.append(l2_corr)
    l2_select_lst = list(s[s.INDUSTRY_CLASSI_NAME.isin([sw_l1_name_dic[i] for i in l2_sep_lst])]['INDEX_CODE'].dropna())
    l1_corr_frame = pd.concat(l1_corr_lst, axis=1)
    l1_corr_frame.columns = l1_select_lst
    l2_corr_frame = pd.concat(l2_corr_lst, axis=1)
    l2_corr_frame.columns = l2_sep_lst
    return l1_select_lst, l2_select_lst, l1_corr_frame, l2_corr_frame


def calculate_signal(price_frame, amt_frame):
    n = 63
    inc_frame = price_frame.pct_change()[price_frame.pct_change() > 0].fillna(0).rolling(n).sum()
    dec_frame = price_frame.pct_change()[price_frame.pct_change() <= 0].fillna(0).rolling(n).sum()
    rsi = (inc_frame / (inc_frame - dec_frame)).stack().reset_index()
    rsi.columns=['TD_DATE', 'INDEX_CODE', 'rank_amt']

    price_frame_stack=price_frame.stack().reset_index()
    price_frame_stack.columns=['TD_DATE', 'INDEX_CODE', 'close']

    amt = amt_frame.ewm(span=20).mean()
    amt = ((amt - amt.rolling(252).mean()) / (amt.rolling(252).std())).stack().reset_index()
    amt.columns=['TD_DATE', 'INDEX_CODE', 'rank_amt']
    res = price_frame_stack.merge(rsi, on=['TD_DATE', 'INDEX_CODE']) \
        .merge(amt, on=['TD_DATE', 'INDEX_CODE'])
    res.columns = ['TD_DATE', 'INDEX_CODE'] + ['close', 'rsi', 'rank_amt']
    return res


def insert_table(res, table_name='IndustrySignal_L2',method='append'):
    from sqlalchemy import create_engine
    from urllib.parse import quote_plus as urlquote
    engine = create_engine(f"mysql+pymysql://root:{urlquote('dev-project@mysql.')}@172.16.127.213:3306/supersetdb")
    # res.to_sql(table_name, engine, if_exists='replace', chunksize=100000, index=None)
    res.to_sql(table_name, engine, if_exists=method, chunksize=100000, index=None)
    print('存入成功！')


def read_sql_table(table='StockRisk', start_date='2018-01-01'):
    from sqlalchemy import create_engine
    from urllib.parse import quote_plus as urlquote
    engine = create_engine(f"mysql+pymysql://root:{urlquote('dev-project@mysql.')}@172.16.127.213:3306/supersetdb")
    sql_query = f'select trade_date,code,msg_iVol_pct from {table} where trade_date> "{pd.to_datetime(start_date)}"'
    # 使用pandas的read_sql_query函数执行SQL语句，并存入DataFrame
    option_inf = pd.read_sql_query(sql_query, engine)
    return option_inf


def read_dwd_table(table, start_dt, end_dt):
    '''
    获取ths__fore_compre_info_rolling__mean_fore_np__fttm、ths__income_statement_ns__net_profit_atsopc__4q_dis_avg等数据
    '''
    import wiserdata as wedata
    start_dt = pd.to_datetime(start_dt).strftime('%Y%m%d')
    end_dt = pd.to_datetime(end_dt).strftime('%Y%m%d')
    param = {
        'domain': 'sheet',
        'phylum': 'direcct',
        'class': table,
        'fields': [],
        'start_date': start_dt,
        'end_date': end_dt,
    }
    df = wedata.extract(param)
    df = df.sort_values('TRADE_DT').set_index('TRADE_DT')
    df.index = pd.to_datetime(df.index.astype('str'))
    if 'OPDATE' in df.columns:
        del df['OPDATE']
    df.columns = [i[:6] + '.' + i[6:] for i in df.columns]

    return df


def get_stock_ivol_pct(start_date):
    sql_df = read_sql_table(table='StockRisk', start_date=start_date)
    ivol_pct = sql_df.pivot(index='trade_date', columns='code', values='msg_iVol_pct')
    return ivol_pct


if __name__ == '__main__':
    start_date = '2022-01-01'
    end_date = '2023-02-11'


    sw_l1_name_dic, sw_l2_name_dic, sw_code_dic_l1, sw_code_dic_l2, s = get_sw_name_dic()

    # sw_l1_price_frame, sw_l2_price_frame, sw_l1_amount_frame, sw_l2_amount_frame = get_index_quoation_data(
    #     list(sw_l1_name_dic.keys()) \
    #     , list(sw_l2_name_dic.keys()),use_local=True)
    #
    # l1_res = calculate_signal(sw_l1_price_frame, sw_l1_amount_frame)
    # # 行业信号结果入库
    # insert_table(l1_res, table_name='IndustrySignal_L1')

    sw_code_dic_l1_test = dict(zip(list(sw_code_dic_l1.keys())[:2], list(sw_code_dic_l1.values())[:2]))
    # sql_df = pd.read_csv('sql_df.csv')
    idx_weight_dic_l1 = calc_idx_wgt(sw_code_dic_l1, start_date, end_date)
    # sigle stock signal
    ivol_pct = get_stock_ivol_pct(start_date)
    earnings = read_dwd_table('ths__income_statement_ns__net_profit_atsopc__4q_dis_avg', start_date, end_date)
    earning_pred = read_dwd_table('ths__fore_compre_info_rolling__mean_fore_np__fttm', start_date, end_date).fillna(method='pad',limit=2)
    earning_pred=earning_pred.combine_first(earnings)
    wgt_signal_dic = {'ivol_pct':ivol_pct,'earning_pred': earning_pred,'earnings': earnings}
    # st signal concate to index signal
    # idx_wgt_signal = calc_idx_weighted_signal(idx_weight_dic_l1, wgt_signal_lst)
    idx_wgt_signal = concat_idx_wgt_signal(idx_weight_dic_l1, wgt_signal_dic).reset_index().dropna(subset='ivol_pct')
    # 行业信号结果入库
    insert_table(idx_wgt_signal, table_name='IndustryWgtSignal_L1_t1')
    idx_weight_dic_l2 = calc_idx_wgt(sw_code_dic_l1, start_date, end_date)
    # index basic signal
    sw_l1_price_frame, sw_l2_price_frame, sw_l1_amount_frame, sw_l2_amount_frame = get_index_quoation_data(
        list(sw_l1_name_dic.keys()) \
        , list(sw_l2_name_dic.keys()),use_local=True)

    l1_select_lst, l2_select_lst, l1_corr_frame, l2_corr_frame = get_select_lst(sw_l1_price_frame, sw_l2_price_frame,
                                                                                sw_l1_name_dic, s, start='2018-01-01')

    l1_res = calculate_signal(sw_l1_price_frame, sw_l1_amount_frame)
    l2_res = calculate_signal(sw_l2_price_frame, sw_l2_amount_frame)
    # 行业信号结果入库
    insert_table(l2_res, table_name='IndustrySignal_L2')
