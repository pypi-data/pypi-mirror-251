# 总体思路：先基于数仓已有四元组的日期跑出来每个日期的weights，存在本地。
# 上传的时候读本地文件，一个一个上传(鉴于中间有可能出现502或者500，这样比较保险)
import os
import operator
import pandas as pd
import numpy as np
import time
import warnings
from pyinstrument import Profiler
import pytest
import wiserdata as wi
from wiserdata.uploader import Uploader
from wiserdata.uploader import CaseTypeEnum
from we_factor_analysis.factor_validation.factor_return.factor_mimicking_ptfl_def import EQ_LIQ_HF25_SRAM
import copy
from we_factor_analysis.factor_regression.em.em_data_util import decompose_vcv
from we_factor_analysis.factor_validation.factor_quad.factor_quad_eq \
    import FactorQuadEQ, TIME_COL_NAME, CODE_COL_NAME
from we_factor_analysis.factor_validation.factor_return.full_factormimicking_portfolio import get_portfolio_weights
from we_factor_analysis.factor_validation.factor_return.universe_filter import apply_universe_filter

from we_factor_analysis.factor_validation.factor_return.return_generator \
    import factor_decompose_asset_return, construct_factor_return
from we_factor_analysis.factor_validation.factor_return.corr_plot \
    import draw_corrs_hist, get_stock_all_factors_correlation, plot_residual_vols
import we_factor_analysis.factor_validation.factor_return.universe_api as u_api
from we_factor_quad.equity_quad.factor_quad_equity import FactorQuadEQ
from we_factor_quad.equity_quad.factor_portfolio.full_factor_mimicking_portfolio import FmpAnalyzer
warnings.filterwarnings('ignore')



def compute_and_save_fmp_locally(start_date: str,
                                 end_date: str,
                                 factor_system='HF25_SRAM_DAILY',
                                 path_to_save="D:/jiaochayuan_files/projects",
                                 freq="B"):
    factorquad = FactorQuadEQ.create_factor_quad(factor_system=factor_system,
                                                 start_date=start_date,
                                                 end_date=end_date,
                                                 from_src=3,
                                                 local_path="D:\jiaochayuan_files\projects\we_factor_quad_")
    analyzer = FmpAnalyzer(quad=factorquad)
    end_date_range = list(pd.DataFrame(factorquad.date_list).set_index([0]).to_period('M').to_timestamp('M').index)
    year_range = sorted(list(set([x.year for x in end_date_range])))
    weights_df = analyzer.get_portfolio_weights(start_date=start_date,
                                                end_date=end_date,
                                                freq='B')

    save_dir = path_to_save + "/fmp_weights"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for i in range(len(year_range)):
        batch_weights_df = weights_df[weights_df[TIME_COL_NAME].dt.year == year_range[i]].reset_index(drop=True)
        batch_weights_df_stacked = batch_weights_df.set_index([TIME_COL_NAME, 'factors']).stack(dropna=False).reset_index()
        batch_weights_df_stacked.columns = [TIME_COL_NAME, 'factors', CODE_COL_NAME, 'weight']
        batch_weights_df_stacked['case'] = factor_system
        # 转成窄表上传，取下来的时候还要转成宽表
        batch_weights_df_stacked[TIME_COL_NAME] = batch_weights_df_stacked[TIME_COL_NAME].apply(lambda x: x.strftime('%Y%m%d'))
        filename = f"factor_mimicking_portfolio_weights_{factor_system}_{str(year_range[i])}"
        # if batch_weights_df_stacked.shape[0] != 255900:
        #     print("wrong")
        path = f"{save_dir}/{filename}_.gzip.parquet"
        if not os.path.exists(path):
            batch_weights_df_stacked.to_parquet(path=path)


def upload_one_case_to_database(path="D:/jiaochayuan_files/projects",
                                case_name='HF25_SRAM'):
    """
    upload all parquet files in the given directory
    Args:
        path_to_read:

    Returns:
    """
    path_to_read = f"{path}/fmp_weights"
    parquet_files = os.listdir(path_to_read)
    copied_parquet_files = copy.deepcopy(parquet_files)
    for file in parquet_files:
        if (len(file) < 8 or file[-8:] != ".parquet") or (not operator.contains(file, case_name + "_")):
            # 删除掉不是parquet的文件
            copied_parquet_files.remove(file)
    files = [f"{path_to_read}/{file}" for file in copied_parquet_files]
    # param = {
    #     'domain': 'descriptor',
    #     'phylum': 'factor_mimicking_portfolio_weights',
    #     'class': 'factor_mimicking_portfolio_weights',
    #     'fields': ["factor_mimicking_portfolio_weights"],
    #     'start_date': start_date,
    #     'end_date': end_date,
    #     'case': case_name
    # }
    wi.login('admin', 'admin')
    # case_name_ = 'case_' + case_name
    wi.update(case_name, files, daemon=False)
    print(1)


def one_step_compute_and_upload_all(start_date: str,
                                    end_date: str,
                                    factor_systems=['HF25_SRAM_DAILY'],
                                    path_to_save="D:/jiaochayuan_files/projects"):
    """
    从数据库里提取所有的四元组数据，创建fmp weights然后将fmp weights上传数仓
    Args:
        start_date:
        end_date:
        factor_systems:
        path_to_save:

    Returns:
    """
    for case in factor_systems:
        print(f"Saving fmp_weights for case {case} locally...")
        compute_and_save_fmp_locally(start_date=start_date,
                                     end_date=end_date,
                                     factor_system=case,
                                     path_to_save=path_to_save)
        print(f"Uploading fmp_weights for case {case}...")
        upload_one_case_to_database(path_to_save, case_name=case)



if __name__ == '__main__':
    one_step_compute_and_upload_all(start_date='20100101', end_date='20101231')
