from typing import List
import copy

import pandas as pd

from ..param import Param
from ..client_local import BaseClient


class CharacteristicExposureParam(Param):

    base_columns = ["date", "code", "characteristic", "exposure", "type"]

    def __init__(self, param_dict: dict):
        super().__init__(param_dict)

    def check_table(self, param_dict: dict) -> bool:
        if param_dict.get("phylum") == "characteristic" and param_dict.get("class") == "characteristic_exposure":
            return True
        return False


class CharacteristicExposureQuery:

    @classmethod
    def pivot_on_characteristic_by_split_days_query(cls,
                                                    client: BaseClient,
                                                    param_dict: dict,
                                                    days: int = 300) -> pd.DataFrame:
        """
        将exposure表转化为characteristic列的宽表，通过分片查询减少内存
        """
        param = CharacteristicExposureParam.create_param(param_dict)
        date_list = param.get_split_date_by_days()
        every_param_dict = copy.deepcopy(param_dict)
        dfs = []
        for start, end in date_list:
            print(f"迭代查询，正在查询{start}-{end}数据")
            every_param_dict["start_date"] = start
            every_param_dict["end_date"] = end
            try:
                df = client.query(every_param_dict)
            except Exception as e:
                print("迭代查询失败")
                raise e
            if df.empty is True:
                continue
            pivot_index = list(df.columns)
            pivot_index.remove('characteristic')
            pivot_index.remove('exposure')
            pivot_index.remove('type')
            pivot_index.remove('case')
            try:
                df = df.pivot_table(columns="characteristic", values="exposure", index=pivot_index)
                df = df.reset_index()
            except Exception as e:
                print("窄表转换成宽表失败")
                raise e
            dfs.append(df)
        if not dfs:
            raise Exception("无查询结果无法转换成宽表")
        return pd.concat(dfs)


