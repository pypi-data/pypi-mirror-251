from typing import Dict, Union, List

import numpy as np
import pandas as pd

from we_factor_quad.factor_quad import FactorQuad


class FactorQuadNS(FactorQuad):
    # 适于本应用的最优lambda值
    GLOBAL_LAMBDA = 0.3383  # for tenor in years

    def __init__(self, factor_system: str, raw_data: Dict,
                 _code_col_name: str = "code",
                 _time_col_name: str = "date"):
        """
        默认取回来的 sigma, psi 量纲与股票等资产的 FactorQuad 一致。注意银行间市场交易日与股票市场有差异。
        :param factor_system:
        :param raw_data:
        :param _code_col_name: 默认变量名
        :param _time_col_name:
        """
        super().__init__(factor_system=factor_system,
                         raw_data=raw_data,
                         _code_col_name=_code_col_name,
                         _time_col_name=_time_col_name)
        self.psi_ts = self.psi_ts.drop(labels='var', axis='columns').merge(
            raw_data['characteristic_idiosyncratic_variance'].drop(
                labels=self._code_col_name, axis='columns').drop_duplicates(keep='last', ignore_index=True),
            on=self._time_col_name, how='inner')
        self.fmp_w = raw_data['factor_mimicking_portfolio_weights'].drop_duplicates() \
            .pivot(index=['date', 'code'], columns='factors', values='weight').reset_index(drop=False)

        self.fac_names = ['level_adj', 'slope_adj', 'curvature_adj']

    @staticmethod
    def create_factor_quad(factor_system: str,
                           start_date: str,
                           end_date: str,
                           from_src: int = 1,
                           local_path: str = None) -> "FactorQuadNS":
        """
        创建一个因子四要素数据结构;
        :param factor_system: 因子系统的名称，对应于数据库中的 case 名称
        :param start_date: 8 digits格式 日期
        :param end_date:
        :param from_src: 0 表示从网络sql提取数据，1表示从sea_drive提取数据，2表示从本地提取数据（2需要对应一个pkl文件）
        :param local_path: 当from_src == 2时，需要一个pkl文件；0表示remote，1表示 seadrive，所以默认为1；
        :return:
        """
        raw_data = FactorQuadNS.factor_quads_download(factor_system=factor_system,
                                                      start_date=start_date,
                                                      end_date=end_date,
                                                      incl_factor_weight=True,
                                                      from_src=from_src,
                                                      years_split=20,
                                                      local_path=local_path)
        return FactorQuadNS(factor_system, raw_data=raw_data)

    @classmethod
    def calc_nelson_siegel_exposure(cls, tenor_list, lbd):
        """
        给定待偿期限，计算Nelson-Siegel模型三因子暴露。
        :param tenor_list: 待偿期限列表，期限单位应与参数 lbd 相适应 (years)
        :param lbd: 模型参数，需指定。
        :return: 返回值列按level, slope, curvature顺序
        """

        if isinstance(tenor_list, pd.Series):
            tenor_list = tenor_list.values
        elif isinstance(tenor_list, list):
            tenor_list = np.array(tenor_list)

        if isinstance(tenor_list, np.ndarray):
            n_row = tenor_list.shape[0]
        else:
            raise ValueError('tenor_list 要为np.ndarray, pd.Series 或 list 类型')
        ns_expo = np.ones((n_row, 3))
        ns_expo[:, 1] = (1 - np.exp(-tenor_list * lbd)) / (tenor_list * lbd)
        ns_expo[:, 2] = ns_expo[:, 1] - np.exp(-tenor_list * lbd)

        zero_idx = tenor_list <= 0
        ns_expo[zero_idx, 1] = 1.
        ns_expo[zero_idx, 2] = 0.

        return ns_expo

    def get_sample_ptfl_w(self, horizon=10, asset_type='index'):
        """
        示例代码：构造规范的组合权重
        :param horizon: 组合权重时间长度，默认取FactorQuad.data_list最后10个值
        :param asset_type: index: 返回国债指数组合  curve: 返回利率组合
        """
        if self.date_list.shape[0] > horizon:
            dt = self.date_list[-horizon:]  # 取后h天
        else:
            dt = self.date_list

        if asset_type.lower() == 'index':
            sample_beta = self.beta_ts.set_index(self._time_col_name).loc[dt]
            sample_ptfl_w = sample_beta.groupby(sample_beta.index).apply(
                lambda x: pd.Series(1 / x.shape[0], index=x[self._code_col_name]))
            if isinstance(sample_ptfl_w, pd.Series):
                sample_ptfl_w = sample_ptfl_w.unstack(fill_value=0.)
            assert sample_ptfl_w.index.name == self._time_col_name
            assert sample_ptfl_w.columns.name == self._code_col_name
        elif asset_type.lower() == 'curve':
            tenor = [1, 3, 5, 7, 10]
            sample_ptfl_w = pd.DataFrame(1 / len(tenor), index=dt, columns=tenor)
        else:
            print(f'Unsupported asset type: f{asset_type}')
            sample_ptfl_w = pd.DataFrame()

        return sample_ptfl_w

    def get_curve_ptfl_beta(self, ptfl_w: pd.DataFrame) -> pd.DataFrame:
        """
        利率组合的 exposure
        :param ptfl_w: Dataframe: curve weights, T x N (panel of weights) with cols in years (float dtype)
        """

        exposure = pd.DataFrame(self.calc_nelson_siegel_exposure(ptfl_w.columns.values, lbd=self.GLOBAL_LAMBDA),
                                index=ptfl_w.columns, columns=self.fac_names)
        return ptfl_w.fillna(0.).dot(exposure)

    def get_curve_systematic_var(self, beta_exposure: pd.DataFrame) -> pd.DataFrame:
        """
        利率的 systematic variance
        :param beta_exposure: T x K wide panel
        """
        return beta_exposure.groupby(beta_exposure.index).apply(
            lambda x: np.diag(x.dot(self.get_sigma(x.index[0], drop_time=True)).dot(x.T))[0])

    def get_curve_ivar(self, start: str = None, end: str = None) -> pd.Series:
        """
        利率的 idiosyncratic variance
        :param start:
        :param end:
        """
        return self.psi_ts.set_index(self._time_col_name)['var'].drop_duplicates().truncate(before=start, after=end)

    def compute_curve_ptfl_var(self, ptfl_w: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
        """
        利率组合的波动
        """
        beta_exposure = self.get_curve_ptfl_beta(ptfl_w)

        sys_var = self.get_curve_systematic_var(beta_exposure)
        idio_var = self.get_curve_ptfl_ivar(ptfl_w)

        return sys_var + idio_var, sys_var, idio_var

    def get_curve_ptfl_ivar(self, ptfl_w: pd.DataFrame) -> pd.DataFrame:
        """
        利率组合的 idiosyncratic variance
        """
        return ptfl_w.apply(lambda x: (x ** 2).sum(), axis=1) * self.get_curve_ivar(start=ptfl_w.index[0],
                                                                                    end=ptfl_w.index[-1])

    def get_factor_mimicking_portfolio_weight(self):
        """
        获取FMP组合权重
        """
        return self.fmp_w.set_index(['date', 'code'])


if __name__ == '__main__':
    # 测试
    import warnings

    warnings.filterwarnings(action='ignore', category=FutureWarning)

    fq = FactorQuadNS.create_factor_quad(factor_system='Nelson_Siegel_HL21_W150_rho_0275',
                                         start_date='20020101', end_date='20230501',
                                         from_src=0, local_path=None)

    fq.info('Info')

    ptfl_w = fq.get_sample_ptfl_w(asset_type='curve')
    var, sys_var, idio_var = fq.compute_curve_ptfl_var(ptfl_w)
