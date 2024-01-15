from typing import List, Tuple
import time
from datetime import datetime, timedelta
# from .checker import Checker
from .constants import Constants
class Param():
    date_format = "%Y%m%d"

    def __init__(self, param_dict: dict):
        if self.check_table(param_dict) is not True:
            raise Exception("参数错误, 请检查参数")
        self.param_dict = param_dict
    @classmethod
    def create_param(cls, param_dict: dict):
        return cls(param_dict)

    def check_table(self, param_dict):
        return True

    def get_start_date(self) -> str:
        if self.param_dict.get('start_date'):
            return self.param_dict.get('start_date')
        return Constants.MIN_START_DATE_STR

    def get_end_date(self) -> str:
        if self.param_dict.get("end_date"):
            return self.param_dict.get("end_date")
        return self.date_to_str(datetime.today())
    @classmethod
    def date_to_str(self, date: datetime):
        return date.strftime(self.date_format)
    @classmethod
    def str_to_date(self, str):
        return datetime.strptime(str, self.date_format,)

    def get_split_date_by_days(self, days: int = 300) -> List[Tuple[str, str]]:
        if days <= 0:
            raise Exception("invalid param,  days")
        start_date = self.str_to_date(self.get_start_date())
        end_date = self.str_to_date(self.get_end_date())
        date_list = []
        current_start_date = start_date
        if start_date > end_date:
            raise Exception("invalid param, start_date > end_date")
        if start_date == end_date:
            return [(self.get_start_date(), self.get_start_date())]
        while current_start_date <= end_date:
            # 左闭合右闭合区间
            current_end_date = current_start_date + timedelta(days=days)
            date_list.append((current_start_date, min(current_end_date - timedelta(days = 1), end_date)))
            current_start_date = current_end_date
        date_list = [(self.date_to_str(start), self.date_to_str(end)) for start, end in date_list]
        date_list[-1] = (date_list[-1][0], self.get_end_date())
        return date_list
