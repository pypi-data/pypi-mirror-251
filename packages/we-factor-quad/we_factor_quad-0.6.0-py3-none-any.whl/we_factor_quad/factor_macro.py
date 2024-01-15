import os.path
import pathlib as pl
import pickle
from typing import Dict, AnyStr, List
import numpy as np
import pandas as pd
from we_factor_quad.data_api import wiser_download_em_result


class FactorMacro(object):

    def __init__(self, raw_data: dict, factor_system: str = 'MACRO'):
        """
        不建议直接使用，建议使用create_factor_macro
        :param raw_data:
        :param factor_system:
        """
        self.factor_system = factor_system
        self.macro_beta = raw_data['characteristic_macro_exposure']

    @staticmethod
    def create_factor_macro(start_date: str,
                            end_date: str,
                            from_src: int = 1,
                            local_path: str = None,
                            factor_system: str = 'MACRO'):
        """
        创建中观对宏观回归结果数据的结构
        :param start_date: 数据开始日期
        :param end_date: 数据结束日期
        :param from_src: 数据来源，0代表remote下载，1代表 local seadrive
        :param local_path: 本地seadrive数据路径
        :param factor_system: 数据库中的case名，当前中观对宏观回归数据只有 MACRO 这一个case
        :return: 取中观对宏观回归结果数据的class
        """
        raw_data = FactorMacro.factor_macro_load(factor_system=factor_system,
                                                 start_date=start_date,
                                                 end_date=end_date,
                                                 from_src=from_src,
                                                 local_path=local_path)

        return FactorMacro(factor_system=factor_system, raw_data=raw_data)

    def get_macro_beta(self, sub_class: list = []):
        """
        取中观对宏观回归得到的敏感度数据表格
        :param sub_class: 一个中观因子/资产大类 名列表， 不在列表中的不取，但如果列表为空则全取
        :return: 中观对宏观回归得到的敏感度数据表格
        """
        df = self.macro_beta
        if bool(sub_class):
            df = df[df.meso_code.isin(sub_class)].copy()
        return df

    def diy_meso_forecast(self, macro_forecast: dict, sub_class: list = [], include_alpha=False, only_newest=False):
        """
        一个给定的宏观场景下，计算中观因子和资产大类的收益预测
        :param macro_forecast: 要计算的宏观数据场景，一个字典，key是宏观因子名(全小写)，value是宏观因子值；
         如果某个key不是模型中的宏观因子会被自动忽略，字典中没出现的宏观因子值，按照取0计算
        :param sub_class: 中观因子/资产大类 名的列表，不在列表中的计算与结果中会被忽略，只有列表非空时才会有忽略操作，否则计算全部
        :param include_alpha: 是否包含alpha贡献的收益
        :param only_newest: 是否只给出最新一期的收益预测
        :return: 一个dataframe, 包含日期、中观因子/资产大类名称，预测收益值 三列
        """
        df_beta = self.macro_beta
        if bool(sub_class):
            df_beta = df_beta[df_beta.meso_code.isin(sub_class)].copy()
        if only_newest:
            df_beta = df_beta[df_beta.date == df_beta.date.max()]
        df_macro = pd.DataFrame(data=[[0] * (len(df_beta.columns) - 3)], columns=df_beta.columns[3:], index=[0])
        for key in macro_forecast:
            if key in df_macro.columns:
                df_macro[key] = macro_forecast[key]
        if include_alpha:
            df_macro['alpha'] = 1
        ret_ts = df_beta[df_macro.columns].to_numpy().dot(df_macro.to_numpy().T)
        df_res = pd.DataFrame(data=ret_ts, columns=['return'], index=df_beta.index)
        return pd.concat([df_beta[['date', 'meso_code']], df_res], axis=1)

    @staticmethod
    def factor_macro_load(start_date: str,
                          end_date: str,
                          universe: list = [],
                          from_src: int = 1,
                          years_split: int = 1,
                          local_path=None,
                          factor_system: str = 'MACRO'):
        """
        提取中观对宏观回归结果数据
        :param start_date: 数据开始日期
        :param end_date: 数据截止日期
        :param universe: 资产的unvierse，这里不需要，默认为[]即可
        :param from_src: 数据来源，0代表remote下载，1代表 local seadrive
        :param years_split: 每次下载纪念数据
        :param local_path:  本地seadrive数据路径
        :param factor_system: 数据库中的case名，当前中观对宏观回归数据只有 MACRO 这一个case
        :return: 一个字典，key是数据表格名，value是数据表格
        """
        which_objs = ["characteristic_macro_exposure"]
        raw_data_dic = {}
        if from_src == 1:  # 从sea_drive 下载数据
            assert local_path is not None, "local_path (seadrive path) should not be None!"
            for x in which_objs:
                raw_data_dic[x] = wiser_download_em_result(case_name=factor_system,
                                                           which=x,
                                                           start_date=str(start_date),
                                                           end_date=str(end_date),
                                                           years_split=years_split,
                                                           universe=universe, mode="local",
                                                           seadrive_localpath=local_path)
        elif from_src == 0:  # 从remote origin 下载数据
            for x in which_objs:
                raw_data_dic[x] = wiser_download_em_result(case_name=factor_system,
                                                           which=x,
                                                           start_date=str(start_date),
                                                           end_date=str(end_date),
                                                           years_split=years_split,
                                                           universe=universe, mode="remote")
        else:
            raise ValueError("from_src not in [0, 1]")
        return raw_data_dic


def test_factor_macro():
    macro = FactorMacro.create_factor_macro(factor_system='MACRO',
                                            start_date='20200101',
                                            end_date='20220101',
                                            from_src=1,
                                            local_path='D://Seafile')

    sub_class = ['黄金', 'industry_Military', 'rstr']
    df_beta = macro.get_macro_beta(sub_class=sub_class)

    macro_forecast = {'growth': 0.1, 'inflation_cpi': 0.2}
    df_ret = macro.diy_meso_forecast(macro_forecast=macro_forecast, sub_class=sub_class,
                                     include_alpha=True, only_newest=True)

    return None


if __name__ == '__main__':
    test_factor_macro()
