import numpy as np
import pandas as pd
import we_factor_quad.fi_quad.risk_control as risk_util

from we_factor_quad.data_api import load_treasury_idx_return
from we_factor_quad.fi_quad.factor_quand_ns import FactorQuadNS

if __name__ == '__main__':
    import warnings

    warnings.simplefilter(action='ignore', category=FutureWarning)
    start = '20200101'
    end = '20230531'
    # 构造5个单一指数组合，控制其波动率为10%
    # 取四元组
    fq = FactorQuadNS.create_factor_quad(factor_system='Nelson_Siegel_HL21_W150_rho_0275', start_date=start,
                                         end_date=end, from_src=0)

    # 构造指数的组合 {ptfl name: pd.DataFrame weights}
    cols = ['1-3年', '3-5年', '5-7年', '7-10年', '10年以上']
    date_range = pd.to_datetime(fq.date_list)

    ptfl_lo = {}
    for n, tenor in enumerate(cols):
        tmp = pd.DataFrame(0.0, index=date_range, columns=cols)
        tmp.columns.name = 'code'
        tmp.index.name = 'date'
        tmp.loc[:, tenor] = 1.0
        ptfl_lo[cols[n]] = tmp

    # 目标波动率
    target_vol = 0.1

    # 指数 excess returns
    trea_ret = load_treasury_idx_return(date_range[0].strftime('%Y%m%d'), date_range[-1].strftime('%Y%m%d'))
    trea_ret = trea_ret.reindex(columns=cols)

    # model predicted ptfl volatility
    model_vol = pd.DataFrame({k: np.sqrt(fq.compute_ptfl_var(w)[0]) for k, w in ptfl_lo.items()})

    # risk managed ptfl_w
    ptfl_w_const_vol = {k: risk_util.risk_manage_ptfl(v, model_vol[k], target_vol=target_vol)
                        for k, v in ptfl_lo.items()}

    # Compute return
    ptfl_ret = pd.DataFrame({k: risk_util.compute_ptfl_ret(v, trea_ret) for k, v in ptfl_w_const_vol.items()})

    # Compute VoV and VaR
    rmv, vov, VaR, vov_ts = risk_util.compute_vov_var(ptfl_ret, target_vol=target_vol, alpha=.99)

    print('########## RMV ##########:\n', rmv)
    print('########## VoV ##########:\n', vov)
    print('########## VaR ##########:\n', VaR)
