import numpy as np
import pandas as pd
import we_factor_quad.fi_quad.risk_control as risk_util
from we_dms.wiser_data_api.basic_info_api import load_calendar

from we_factor_quad.data_api import get_zero_rate, load_treasury_idx_return
from we_factor_quad.fi_quad.factor_quand_ns import FactorQuadNS

if __name__ == '__main__':
    import warnings

    warnings.simplefilter(action='ignore', category=FutureWarning)
    start = '20200101'
    end = '20230531'
    # 构造5个单一期限利率组合，控制其波动率为10%
    # 取四元组
    fq = FactorQuadNS.create_factor_quad(factor_system='Nelson_Siegel_HL21_W150_rho_0275', start_date=start,
                                         end_date=end, from_src=0)

    tenor_list = np.array([2, 3, 5, 7, 10])

    # 构造curve组合 {tenor: pd.DataFrame weights}
    date_range = pd.to_datetime(fq.date_list)
    ptfl_lo = {}
    for tenor in tenor_list:
        tmp = pd.DataFrame(0.0, index=date_range, columns=tenor_list)
        tmp.columns.name = 'code'
        tmp.index.name = 'date'
        tmp.loc[:, tenor] = 1.0
        ptfl_lo[tenor] = tmp

    # 目标波动率
    target_vol = 0.1

    # load zero rates
    zero_curves = get_zero_rate(start, end)
    zero_curves = zero_curves.filter(items=tenor_list, axis='columns')

    trading_days = pd.to_datetime(load_calendar(start=start, end=end, exchmarket='银行间债券市场'),
                                  format='%Y%m%d')
    zero_curves = zero_curves.filter(items=trading_days, axis='rows')

    # model predicted ptfl volatility
    model_vol = pd.DataFrame({k: np.sqrt(fq.compute_curve_ptfl_var(w)[0]) for k, w in ptfl_lo.items()})

    # risk managed ptfl_w
    ptfl_w_const_vol = {k: risk_util.risk_manage_ptfl(v, model_vol[k], target_vol=target_vol)
                        for k, v in ptfl_lo.items()}

    # Compute return, treat "returns" as change in yield
    ptfl_ret = pd.DataFrame({k: risk_util.compute_ptfl_ret(v, zero_curves.diff(1)) for k, v in ptfl_w_const_vol.items()})

    # Compute VoV and VaR
    rmv, vov, VaR, vov_ts = risk_util.compute_vov_var(ptfl_ret, target_vol=target_vol, alpha=.99)

    print('########## RMV ##########:\n', rmv)
    print('########## VoV ##########:\n', vov)
    print('########## VaR ##########:\n', VaR)
