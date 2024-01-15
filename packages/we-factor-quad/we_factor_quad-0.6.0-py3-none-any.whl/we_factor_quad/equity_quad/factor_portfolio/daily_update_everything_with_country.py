import os
import sys
import logging
import argparse
from logging.handlers import TimedRotatingFileHandler
import copy
import os
import pandas as pd
import wiserdata

from we_factor_quad.equity_quad.factor_quad_equity import FactorQuadEQ
from we_factor_quad.equity_quad.factor_portfolio.full_factor_mimicking_portfolio import FmpAnalyzer
import we_factor_quad.data_api as dapi
import datetime
import pathlib


def setup_logger(logger_name: str = __name__, log_level: str = None,
                 formatter=None, log_file_name=None, log_path='log'):

    level_map = {
        'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING,
        'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL
    }

    if log_level.upper() in level_map:
        log_level = level_map[log_level.upper()]
    else:
        log_level = logging.WARNING

    if formatter is None:
        formatter = logging.Formatter("%(asctime)s %(pathname)s(%(lineno)d): %(levelname)s %(message)s [%(name)s]")

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    consl_handler = logging.StreamHandler(sys.stdout)
    consl_handler.setFormatter(formatter)

    if log_file_name is None:
        log_file_name = 'mylog'
    if not os.path.isdir(log_path):
        os.mkdir(log_path)
    log_file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_path, log_file_name), when='MIDNIGHT', interval=1, backupCount=3)
    log_file_handler.setFormatter(formatter)

    logger.addHandler(consl_handler)
    logger.addHandler(log_file_handler)
    logger.propagate = False

    return logger


logger = setup_logger(log_level='INFO', log_file_name='everything_with_country.log', log_path='./')

def daily_update_everything_with_country(date_of_running: str,
                                         seadrive_local_path: str = "D:\seadrive_cache_folder\zhouly\群组资料库",
                                         factor_system='HF25_SRAM_DAILY_V0',
                                         factor_system_name_wc='HF25_SRAM_DAILY_V1',
                                         output_path="D:/jiaochayuan_files/projects/everything_with_country"):
    """
    将所有的四元组和因子收益(本身就有国家因子)，加上国家因子，传到V1这个case里

    Args:
        date_of_running:

    Returns:
    """
    assert os.path.exists(output_path), "The output path does not exist!"
    # logger = setup_logger(log_level='INFO', log_file_name='带国家因子的四元组和因子收益.log', log_path='./')
    logger.info(f"开始更新{date_of_running}带国家因子的四元组和因子收益")
    try:
        factor_return = dapi.wiser_fetch_factor_return(start_date=date_of_running,
                                                       end_date=date_of_running,
                                                       seadrive_localpath=seadrive_local_path)
    except FileNotFoundError:
        logger.info(f"{date_of_running}本日没有因子收益数据，说明为节假日或尚未日更原始四元组，程序自动结束")
        return

    if factor_return.shape[0] == 0:
        logger.info(f"{date_of_running}本日没有因子收益数据，说明为节假日或尚未日更原始四元组，程序自动结束")
        return

    stacked_factor_return = factor_return.stack(dropna=False).reset_index()
    stacked_factor_return.rename(columns=dict(zip(list(stacked_factor_return.columns),
                                                  ['date', 'characteristic', 'return'])), inplace=True)

    stacked_factor_return['date'] = stacked_factor_return['date'].apply(lambda x: x.strftime('%Y%m%d'))
    type_list = list(stacked_factor_return['characteristic'])
    for i in range(len(type_list)):
        if type_list[i].split("_")[0] == "industry":
            type_list[i] = "industry"
        elif type_list[i] == "country":
            pass
        else:
            type_list[i] = "style"
    stacked_factor_return['type'] = type_list
    raw_data = FactorQuadEQ.factor_quads_download(factor_system=factor_system,
                                                  start_date=date_of_running,
                                                  end_date=date_of_running,
                                                  from_src=1,
                                                  local_path=seadrive_local_path)

    # 四元组转宽表
    beta_wc = copy.deepcopy(raw_data['characteristic_exposure'])
    beta_wc['date'] = pd.to_datetime(beta_wc['date'])
    beta_wc = beta_wc.pivot(index=['date', 'code'], columns='characteristic', values='exposure').reset_index()
    beta_wc['country'] = 1

    factorquad = FactorQuadEQ.create_factor_quad(factor_system=factor_system,
                                                 start_date=date_of_running,
                                                 end_date=date_of_running,
                                                 from_src=0)

    sigma_wc, _ = factorquad.add_country_factor()
    scale = raw_data['characteristic_scale']
    psi = raw_data['characteristic_idiosyncratic_variance']

    # sigma和beta再转回窄表
    stacked_beta = beta_wc.set_index(['date', 'code']).stack(dropna=True).reset_index()
    stacked_beta.columns = ['date', 'code', 'characteristic', 'exposure']
    stacked_beta['type'] = stacked_beta['characteristic'].apply(lambda x: "industry" if x.split("_")[0] == 'industry' else "style")
    stacked_beta.loc[stacked_beta['characteristic'] == "country", "type"] = "country"
    stacked_beta['date'] = stacked_beta['date'].apply(lambda x: x.strftime("%Y%m%d"))

    stacked_sigma = sigma_wc.set_index(['date', 'source']).stack(dropna=True).reset_index()
    stacked_sigma.columns = ['date', 'source', 'target', 'cov']
    stacked_sigma['date'] = stacked_sigma['date'].apply(lambda x: x.strftime("%Y%m%d"))
    stacked_sigma["case"] = factor_system_name_wc
    stacked_beta['case'] = factor_system_name_wc

    filename1 = f"characteristic_return_wc_{factor_system_name_wc}_{date_of_running}.gzip.parquet"
    filename2 = f"characteristic_covariance_wc_{factor_system_name_wc}_{date_of_running}.gzip.parquet"
    filename3 = f"characteristic_exposure_wc_{factor_system_name_wc}_{date_of_running}.gzip.parquet"
    filename4 = f"characteristic_scale_{factor_system_name_wc}_{date_of_running}.gzip.parquet"
    filename5 = f"characteristic_idiosyncratic_variance_{factor_system_name_wc}_{date_of_running}.gzip.parquet"
    output_dict = {filename1: stacked_factor_return,
                   filename2: stacked_sigma,
                   filename3: stacked_beta,
                   filename4: scale,
                   filename5: psi}
    for filename in output_dict.keys():
        path = pathlib.Path.joinpath(pathlib.Path(output_path), filename)
        if path.is_file():
            path.unlink()
        output_dict[filename].to_parquet(path=str(path))
        # f = pd.read_parquet(str(path))
    logger.info(f"{date_of_running}_{factor_system_name_wc}带国家因子的四元组和因子收益更新成功，运行结束~")


def upload_file(path):
    for time in range(5):
        res = wiserdata.update(factor_system, [path], daemon=False)
        logger.info(f"Uploading {path}")
        if res:
            os.remove(path)
            logger.info('Success')
            return
    logger.error(f'Error: File upload failure: {path}')


if __name__ == '__main__':
    # 跑历史数据的时候 start_date 要指定前一天
    # parser = argparse.ArgumentParser(description='This is the we_factor_return start shell')
    # parser.add_argument("--factor_system", required=True)
    # parser.add_argument("--output_path", required=True)
    # parser.add_argument("--date_of_running", required=True)
    # parser.add_argument("--factor_system_name_wc", required=True)

    #
    # args = parser.parse_args()
    #
    # factor_system = args.factor_system
    # output_path = args.output_path
    # start_date = args.date_of_running
    # end_date = args.factor_system_name_wc

    daily_update_everything_with_country(date_of_running='20140108')