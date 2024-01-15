import pandas as pd

from we_factor_quad.equity_quad.factor_quad_equity import FactorQuadEQ
from pm_analysis import PortfolioManagement


def test_make_port():
    myquad = FactorQuadEQ.create_factor_quad(factor_system='HF25_SRAM_DAILY',
                                             start_date='20220501',
                                             end_date='20220601',
                                             from_src=1,
                                             universe=['600519.SH', '300750.SZ', '601318.SH', '600036.SH', '000858.SZ',
                                                       '000333.SZ', '002594.SZ'],
                                             local_path='D:/Seafile')
    myquad.add_country_factor()
    myopt = PortfolioManagement(df_exposure=myquad.beta_withcountry_ts, df_sigma=myquad.sigma_withcountry_ts)
    return myopt


def test_add():
    myopt = test_make_port()
    current_values = {
        '600519.SH': 200,
        '300750.SZ': 50,
        '601318.SH': 70,
        '600036.SH': 40
    }
    add_assets = ['600036.SH', '000858.SZ']
    add_value = 50
    key_styles = ['log_markcap', 'beta']
    add_values = myopt.in_opt(current_values=current_values, add_assets=add_assets, add_value=add_value,
                              key_styles=key_styles)
    pass


def test_add_with_init():
    myopt = test_make_port()
    current_values = {
        '600519.SH': 200,
        '300750.SZ': 50,
        '601318.SH': 70,
        '600036.SH': 40
    }
    init_distirbution = {
        '600036.SH': 30,
        '000858.SZ': 30
    }
    key_styles = ['log_markcap', 'beta']
    add_values = myopt.in_opt_with_init(current_values=current_values, init_distribution=init_distirbution,
                                        key_styles=key_styles)
    pass


def test_minus():
    myopt = test_make_port()
    current_values = {
        '600519.SH': 100,
        '300750.SZ': 50,
        '601318.SH': 60,
        '600036.SH': 30,
        '000858.SZ': 40,
        '000333.SZ': 20,
        '002594.SZ': 35
    }
    minus_assets = ['600519.SH', '000858.SZ', '000333.SZ', '002594.SZ']
    minus_value = 80
    key_styles = ['log_markcap', 'beta', 'rstr']
    minus_values = myopt.out_opt(current_values=current_values, minus_assets=minus_assets, minus_value=minus_value,
                                 key_styles=key_styles)
    pass


def test_minus_with_init():
    myopt = test_make_port()
    current_values = {
        '600519.SH': 100,
        '300750.SZ': 50,
        '601318.SH': 60,
        '600036.SH': 30,
        '000858.SZ': 40,
        '000333.SZ': 20,
        '002594.SZ': 35
    }
    init_distribution = {
        '600519.SH': 30,
        '000858.SZ': 10,
        '000333.SZ': 10,
        '002594.SZ': 15
    }
    key_styles = ['log_markcap', 'beta', 'rstr']
    minus_values = myopt.out_opt_with_init(current_values=current_values, init_distribution=init_distribution,
                                           key_styles=key_styles)
    pass


def test_adj():
    myopt = test_make_port()
    current_values = {
        '600519.SH': 100,
        '300750.SZ': 50,
        '601318.SH': 70,
        '600036.SH': 80
    }
    add_assets = ['600036.SH', '002594.SZ']
    minus_assets = ['600519.SH', '601318.SH']
    adj_value = 10
    key_styles = ['log_markcap', 'beta', 'rstr']
    key_industries = []
    adj_values = myopt.adj_opt(current_values=current_values, adj_value=adj_value, add_assets=add_assets,
                               minus_assets=minus_assets, key_styles=key_styles, key_industries=key_industries)
    pass


def test_adj_with_init():
    myopt = test_make_port()
    current_values = {
        '600519.SH': 100,
        '300750.SZ': 50,
        '601318.SH': 70,
        '600036.SH': 80
    }
    init_distribution = {
        '002594.SZ': 20,
        '600036.SH': 25,
        '600519.SH': -20,
        '601318.SH': -25
    }
    key_styles = ['log_markcap', 'beta', 'rstr']
    key_industries = []
    adj_values = myopt.adj_with_init(current_values=current_values, init_distribution=init_distribution,
                                     bound_ratio=0.5, key_styles=key_styles)
    pass


def test_factor_display():
    myopt = test_make_port()
    df_values = pd.DataFrame({'date': ['20220510', '20220510', '20220510', '20220511', '20220511', '20220511',
                                       '20220512', '20220512', '20220512'],
                              'code': ['600519.SH', '300750.SZ', '601318.SH', '600519.SH', '300750.SZ', '600036.SH',
                                       '600519.SH', '300750.SZ', '601318.SH'],
                              'value': [50, 20, 30, 45, 30, 25, 20, 40, 40]})
    df_values['date'] = pd.to_datetime(df_values['date'])
    df = myopt.factor_exposure_display(df_values=df_values, code_col='code')
    pass


def test_factor_exposure_alert():
    myopt = test_make_port()
    values = {'600519.SH': 100,
              '300750.SZ': 50,
              '601318.SH': 70,
              '600036.SH': 80
              }
    thresholds = {
        'industry_Food_and_Beverage': 5,
        'rstr': 1,
        'log_markcap': 5
    }
    res = myopt.factor_exposure_alert(values=values, thresholds=thresholds)
    pass


def test_adj_mimic():
    myopt = test_make_port()
    values1 = {'600519.SH': 100,
               '300750.SZ': 50,
               '601318.SH': 70,
               '600036.SH': 80
               }
    values2 = {'600519.SH': 80,
               '300750.SZ': 75,
               '601318.SH': 55,
               '600036.SH': 80
               }
    df = myopt.adjustment_mimic(values1=values1, values2=values2)
    pass


if __name__ == '__main__':
    # test_add()
    # test_add_with_init()
    # test_minus_with_init()
    # test_minus()
    # test_adj()
    # test_adj_with_init()
    # test_factor_display()
    test_factor_exposure_alert()
    # test_adj_mimic()
