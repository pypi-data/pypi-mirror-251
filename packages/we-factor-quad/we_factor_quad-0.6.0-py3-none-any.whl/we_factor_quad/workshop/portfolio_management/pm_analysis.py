import numpy as np
import pandas as pd

import pm_library as lib

CODE_COL = 'code'
DATE_COL = 'date'


class PortfolioManagement:

    def __init__(self, df_exposure, df_sigma, code_col=CODE_COL, date_col=DATE_COL, start_date=None,
                 end_date=None):
        self.df_exposure = df_exposure
        self.df_sigma = df_sigma
        if start_date is not None:
            self.df_exposure = self.df_exposure[self.df_exposure[date_col] >= start_date]
            self.df_sigma = self.df_sigma[self.df_sigma[date_col] >= start_date]
        if end_date is not None:
            self.df_exposure = self.df_exposure[self.df_exposure[date_col] <= end_date]
            self.df_sigma = self.df_sigma[self.df_sigma[date_col] <= end_date]
        self.code_col = code_col
        self.date_col = date_col

    def in_opt(self, current_values, add_assets, add_value, key_styles=None, key_industries=None,
               date=None):
        """
        加仓优化
        :param current_values: 字典格式，当前股票持仓，key是股票代码，value是个股当前持仓金额
        :param add_assets:  list格式，候选加仓的个股代码
        :param add_value: float格式，考虑加仓的金额
        :param key_styles:  list格式，包含要尽可能保持暴露的风格因子名
        :param key_industries: list格式，包含要尽可能保持暴露的行业名
        :param date: string格式，日期
        :return: 字典，key是要加仓的个股代码，value是加仓金额
        """
        df_exposure = self.df_exposure.copy()
        df_sigma = self.df_sigma.copy()
        if date is None:
            date = df_exposure[self.date_col].max()
        df_exposure = df_exposure[df_exposure[self.date_col] == date]
        df_sigma = df_sigma[df_sigma[self.date_col] == date]
        df_exposure = df_exposure.drop(columns=[self.date_col])
        df_sigma = df_sigma.drop(columns=[self.date_col])

        if key_styles is None:
            key_styles = [i for i in df_exposure.columns if not i.startswith('industry') and i != self.code_col]
        if key_industries is None:
            key_industries = [i for i in df_exposure.columns if i.startswith('industry')]
        factor_list = key_styles + key_industries
        df_sigma = df_sigma[df_sigma.source.isin(factor_list)]
        df_sigma = df_sigma[['source'] + factor_list]
        df_sigma = df_sigma.set_index('source')
        df_sigma = df_sigma.loc[factor_list]
        df_exposure = df_exposure[[self.code_col] + factor_list]
        df_exposure = df_exposure[df_exposure[self.code_col].isin(list(current_values.keys()) + add_assets)]
        return lib.in_optimization(df_exposure=df_exposure, df_sigma=df_sigma, code_col=self.code_col,
                                   current_values=current_values, add_assets=add_assets, add_value=add_value)

    def in_opt_with_init(self, current_values, init_distribution, bound_ratio=0.5, key_styles=None,
                         key_industries=None, date=None):
        """

        :param current_values:
        :param init_distribution:
        :param bound_ratio:
        :param key_styles:
        :param key_industries:
        :param date:
        :return:
        """
        df_exposure = self.df_exposure.copy()
        df_sigma = self.df_sigma.copy()
        if date is None:
            date = df_exposure[self.date_col].max()
        df_exposure = df_exposure[df_exposure[self.date_col] == date]
        df_sigma = df_sigma[df_sigma[self.date_col] == date]
        df_exposure = df_exposure.drop(columns=[self.date_col])
        df_sigma = df_sigma.drop(columns=[self.date_col])

        if key_styles is None:
            key_styles = [i for i in df_exposure.columns if not i.startswith('industry') and i != self.code_col]
        if key_industries is None:
            key_industries = [i for i in df_exposure.columns if i.startswith('industry')]
        factor_list = key_styles + key_industries
        df_sigma = df_sigma[df_sigma.source.isin(factor_list)]
        df_sigma = df_sigma[['source'] + factor_list]
        df_sigma = df_sigma.set_index('source')
        df_sigma = df_sigma.loc[factor_list]
        df_exposure = df_exposure[[self.code_col] + factor_list]
        df_exposure = df_exposure[
            (df_exposure[self.code_col].isin(current_values)) | (df_exposure[self.code_col].isin(init_distribution))]
        return lib.in_opt_with_init(df_exposure=df_exposure, df_sigma=df_sigma, code_col=self.code_col,
                                    current_values=current_values, init_distribution=init_distribution,
                                    bound_ratio=bound_ratio)

    def out_opt(self, current_values, minus_assets, minus_value, key_styles=None, key_industries=None,
                date=None):
        """
        减仓优化
        :param current_values: 字典格式，当前股票持仓，key是股票代码，value是个股当前持仓金额
        :param minus_assets: list格式，候选减仓的个股代码
        :param minus_value: float格式，考虑减仓的金额
        :param key_styles: list格式，包含要尽可能保持暴露的风格因子名
        :param key_industries: list格式，包含要尽可能保持暴露的行业名
        :param date: string格式，日期
        :return: 字典，key是要减仓的个股代码，value是加仓金额
        """
        df_exposure = self.df_exposure.copy()
        df_sigma = self.df_sigma.copy()
        if date is None:
            date = df_exposure[self.date_col].max()
        df_exposure = df_exposure[df_exposure[self.date_col] == date]
        df_sigma = df_sigma[df_sigma[self.date_col] == date]
        df_exposure = df_exposure.drop(columns=[self.date_col])
        df_sigma = df_sigma.drop(columns=[self.date_col])

        if key_styles is None:
            key_styles = [i for i in df_exposure.columns if not i.startswith('industry') and i != self.code_col]
        if key_industries is None:
            key_industries = [i for i in df_exposure.columns if i.startswith('industry')]

        factor_list = key_styles + key_industries
        df_sigma = df_sigma[df_sigma.source.isin(factor_list)]
        df_sigma = df_sigma[['source'] + factor_list]
        df_sigma = df_sigma.set_index('source')
        df_sigma = df_sigma.loc[factor_list]
        df_exposure = df_exposure[[self.code_col] + factor_list]
        df_exposure = df_exposure[df_exposure[self.code_col].isin(current_values)]
        return lib.out_optimization(df_exposure=df_exposure, df_sigma=df_sigma, code_col=self.code_col,
                                    current_values=current_values, minus_assets=minus_assets, minus_value=minus_value)

    def out_opt_with_init(self, current_values, init_distribution, bound_ratio=0.5,
                          key_styles=None, key_industries=None, date=None):
        """

        :param current_values:
        :param init_distribution:
        :param bound_ratio:
        :param key_styles:
        :param key_industries:
        :param date:
        :return:
        """
        df_exposure = self.df_exposure.copy()
        df_sigma = self.df_sigma.copy()
        if date is None:
            date = df_exposure[self.date_col].max()
        df_exposure = df_exposure[df_exposure[self.date_col] == date]
        df_sigma = df_sigma[df_sigma[self.date_col] == date]
        df_exposure = df_exposure.drop(columns=[self.date_col])
        df_sigma = df_sigma.drop(columns=[self.date_col])

        if key_styles is None:
            key_styles = [i for i in df_exposure.columns if not i.startswith('industry') and i != self.code_col]
        if key_industries is None:
            key_industries = [i for i in df_exposure.columns if i.startswith('industry')]

        factor_list = key_styles + key_industries
        df_sigma = df_sigma[df_sigma.source.isin(factor_list)]
        df_sigma = df_sigma[['source'] + factor_list]
        df_sigma = df_sigma.set_index('source')
        df_sigma = df_sigma.loc[factor_list]
        df_exposure = df_exposure[[self.code_col] + factor_list]
        df_exposure = df_exposure[df_exposure[self.code_col].isin(current_values)]
        return lib.out_opt_with_init(df_exposure=df_exposure, df_sigma=df_sigma, code_col=self.code_col,
                                     current_values=current_values, init_distribution=init_distribution,
                                     bound_ratio=bound_ratio)

    def adj_opt(self, current_values, adj_value, add_assets=[], minus_assets=[], key_styles=[], key_industries=[],
                date=None):
        """
        调仓优化
        :param current_values: 字典格式，当前股票持仓，key是股票代码，value是个股当前持仓金额
        :param adj_value: float格式，考虑调仓的金额（调仓前后总持仓金额不变，调仓金额等于调出或调入的金额绝对值）
        :param add_assets: list格式，候加减仓的个股代码
        :param minus_assets: list格式，候选减仓的个股代码
        :param key_styles: list格式，包含要尽可能保持暴露的风格因子名
        :param key_industries: list格式，包含要尽可能保持暴露的行业名
        :param date: string格式，日期
        :return: 字典，key是要调仓的个股代码，value是金额，正代表加仓，负代表减仓
        """
        add_dic = {}
        minus_dic = {}
        if len(add_assets) > 0:
            add_dic = self.in_opt(current_values=current_values, add_assets=add_assets, add_value=adj_value,
                                  key_styles=key_styles, key_industries=key_industries, date=date)
        if len(minus_assets) > 0:
            minus_dic = self.out_opt(current_values=current_values, minus_assets=minus_assets, minus_value=adj_value,
                                     key_styles=key_styles, key_industries=key_industries, date=date)
        res_dic = {}
        for asset in add_dic:
            res_dic[asset] = add_dic[asset]
        for asset in minus_dic:
            if asset in res_dic:
                res_dic[asset] += minus_dic[asset]
            else:
                res_dic[asset] = minus_dic[asset]
        return res_dic

    def adj_with_init(self, current_values, init_distribution, bound_ratio=0.5, key_styles=[], key_industries=[],
                      date=None):
        """

        :param current_values:
        :param init_distribution:
        :param bound_ratio:
        :param key_styles:
        :param key_industries:
        :param date:
        :return:
        """
        add_distribution = {}
        minus_distribution = {}
        for asset in init_distribution:
            if init_distribution[asset] > 0:
                add_distribution[asset] = init_distribution[asset]
            else:
                minus_distribution[asset] = init_distribution[asset]
        add_dic = {}
        minus_dic = {}
        if len(add_distribution) > 0:
            add_dic = self.in_opt_with_init(current_values=current_values, init_distribution=add_distribution,
                                            bound_ratio=bound_ratio, key_styles=key_styles,
                                            key_industries=key_industries, date=date)
        if len(minus_distribution) > 0:
            minus_dic = self.out_opt_with_init(current_values=current_values, init_distribution=minus_distribution,
                                               bound_ratio=bound_ratio, key_styles=key_styles,
                                               key_industries=key_industries, date=date)
        res_dic = {}
        for asset in add_dic:
            res_dic[asset] = add_dic[asset]
        for asset in minus_dic:
            if asset in res_dic:
                res_dic[asset] += minus_dic[asset]
            else:
                res_dic[asset] = minus_dic[asset]
        return res_dic

    def factor_ret_display(self, df_factor_ret, factor_list=None, start_date=None, end_date=None):
        """

        :param df_factor_ret:
        :param factor_list:
        :param start_date:
        :param end_date:
        :return:
        """
        df = df_factor_ret.copy()
        if start_date is not None:
            df = df[df[self.date_col] >= start_date]
        if end_date is not None:
            df = df[df[self.date_col] <= end_date]
        if factor_list is not None:
            df = df[[self.date_col] + factor_list]
        return df

    def factor_exposure_display(self, df_values, code_col, start_date=None, end_date=None, multiple=100):
        """

        :param df_values:
        :param start_date:
        :param end_date:
        :param code_col:
        :param multiple:
        :return:
        """

        df_exposure = self.df_exposure.copy()
        df_sigma = self.df_sigma.copy()
        if start_date is not None:
            df_exposure = df_exposure[
                (df_exposure[self.date_col] >= start_date) & (df_exposure[self.date_col] <= end_date)]
            df_sigma = df_sigma[(df_sigma[self.date_col] >= start_date) & (df_sigma[self.date_col] <= end_date)]
        factor_list = list(df_sigma.columns)[2:]

        df_res = pd.DataFrame({})

        for date in df_exposure[self.date_col].unique():
            df_v = df_values[df_values[self.date_col] == date].copy()
            if len(df_v) == 0:
                continue
            df_v.drop(columns=[self.date_col], inplace=True)
            df_v.set_index(code_col, inplace=True)
            df_v = df_v / df_v.sum(axis=0)
            value = df_v.to_numpy()

            df_e = df_exposure[df_exposure[self.date_col] == date].copy()
            df_e.drop(columns=[self.date_col], inplace=True)
            df_e = df_e[[self.code_col] + factor_list]
            df_e.set_index(self.code_col, inplace=True)
            df_e = df_e.reindex(df_v.index)
            exposure = df_e.to_numpy()

            df_s = df_sigma[df_sigma[self.date_col] == date].copy()
            df_s.drop(columns=[self.date_col], inplace=True)
            df_s.set_index('source', inplace=True)
            sigma = df_s.to_numpy()
            sigma = np.sqrt(np.diag(np.diag(sigma)))

            w = value.T.dot(exposure).dot(sigma) * multiple
            df_slice = pd.DataFrame(data=w, columns=factor_list)
            df_slice.insert(0, self.date_col, date)
            if df_res.empty:
                df_res = df_slice
            else:
                df_res = pd.concat([df_res, df_slice], axis=0, ignore_index=True)

        return df_res

    def factor_exposure_alert(self, values, thresholds, current_date=None, multiple=100):
        """

        :param values:
        :param thresholds:
        :param multiple:
        :param current_date:
        :return:
        """
        if current_date is None:
            current_date = self.df_exposure[self.date_col].max()
        df_values = pd.DataFrame(values, index=['value']).T
        df_values.reset_index(inplace=True)
        df_values.rename(columns={'index': self.code_col}, inplace=True)
        df_values.insert(0, self.date_col, current_date)
        df_exposure = self.factor_exposure_display(df_values=df_values, code_col=self.code_col, multiple=multiple)
        exposure_dict = df_exposure.iloc[0,].to_dict()

        res_dict = {}
        for factor in thresholds:
            if abs(exposure_dict[factor]) > thresholds[factor]:
                res_dict[factor] = exposure_dict[factor]
        return res_dict

    def adjustment_mimic(self, values1, values2, current_date=None, multiple=100):
        """

        :param values1:
        :param values2:
        :param current_date:
        :param multiple:
        :return:
        """
        for key in values1:
            if key not in values2:
                values2[key] = 0
        for key in values2:
            if key not in values1:
                values1[key] = 0
        values_diff = {}
        for key in values1:
            values_diff[key] = values2[key] - values1[key]

        if current_date is None:
            current_date = self.df_exposure[self.date_col].max()

        df_v1 = pd.DataFrame(values1, index=['value']).T
        df_v1.reset_index(inplace=True)
        df_v1.rename(columns={'index': self.code_col}, inplace=True)
        df_v1.insert(0, self.date_col, current_date)
        df_e1 = self.factor_exposure_display(df_values=df_v1, code_col=self.code_col, multiple=multiple)
        df_e1.insert(0, 'order', 'before')

        df_v2 = pd.DataFrame(values2, index=['value']).T
        df_v2.reset_index(inplace=True)
        df_v2.rename(columns={'index': self.code_col}, inplace=True)
        df_v2.insert(0, self.date_col, current_date)
        df_e2 = self.factor_exposure_display(df_values=df_v2, code_col=self.code_col, multiple=multiple)
        df_e2.insert(0, 'order', 'after')

        df_vdiff = pd.DataFrame(values_diff, index=['value']).T
        df_vdiff.reset_index(inplace=True)
        df_vdiff.rename(columns={'index': self.code_col}, inplace=True)
        df_vdiff.insert(0, self.date_col, current_date)
        df_ediff = self.factor_exposure_display(df_values=df_vdiff, code_col=self.code_col, multiple=multiple)
        df_ediff.insert(0, 'order', 'diff')

        return pd.concat([df_e1, df_e2, df_ediff], axis=0)
