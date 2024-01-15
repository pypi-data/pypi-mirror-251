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


logger = setup_logger(log_level='INFO', log_file_name='we_factor_return.log', log_path='./logs')


def update_daily_factor_return(factor_system='HF25_SRAM_DAILY_V0',
                               output_path="D:/jiaochayuan_files/projects/characteristic_return",
                               date_of_running="20231215"):
    """
    因子收益日更。输出最新一天的factor_return到一个parquet文件。这个函数要在有了当天四元组数据，且有当天股价数据后才能跑。
    例：
    比如要跑20231110周五的，在有了20231110的四元组后，再来跑这个。如果没有当天的四元组(比如当天四元组日更还没跑，或者要跑的那天是节假日)，
    那么不会生成任何parquet文件，直接结束。如果数仓有当天的四元组数据，那么跑完会在output_path这个地址下生成对应的parquet文件。
    Args:
        factor_system: 日频的四元组文件夹名'HF25_SRAM_DAILY_V0'
        output_path: 储存文件的本地文件夹地址,这个文件夹必须已经存在
        date_of_running: 指需要跑的那一天的时间，比如要跑20231110周五的数据，就输入“20231110”，注意这不是指本机服务器的时间

    Returns:
    """
    assert os.path.exists(output_path), "The output path does not exist!"
    datetime_of_running = datetime.datetime.strptime(date_of_running, "%Y%m%d")
    start_date = (datetime_of_running - datetime.timedelta(days=15)).strftime("%Y%m%d")
    factorquad = FactorQuadEQ.create_factor_quad(factor_system=factor_system,
                                                 start_date=start_date,
                                                 end_date=date_of_running,
                                                 from_src=0)
    logger = setup_logger(log_level='INFO', log_file_name='因子收益日更日志.log', log_path='./')
    logger.info(f"开始更新{date_of_running}因子收益")
    if pd.Timestamp(factorquad.date_list[-1]).strftime("%Y%m%d") != date_of_running:
        logger.info("当天还未跑四元组日更，或为节假日，本程序更新因子收益失败自动结束，请先运行四元组日更，或选择下一个交易日运行")
        return
    analyzer = FmpAnalyzer(quad=factorquad)
    end_date_range = list(pd.DataFrame(factorquad.date_list).set_index([0]).to_period('M').to_timestamp('M').index)
    year_range = sorted(list(set([x.year for x in end_date_range])))
    weights_df = analyzer.get_portfolio_weights(start_date=start_date,
                                                end_date=date_of_running,
                                                freq='B')
    ret = dapi.get_stock_return(start=start_date,
                                end=date_of_running,
                                freq='B')
    return_target_date = ret.index[-1].strftime("%Y%m%d")
    if return_target_date != date_of_running:
        logger.info(
            "当天股票收益或股票价格尚未更新，或为节假日，本程序更新因子收益失败自动结束，请先更新股票收益或股票价格，或选择下一个交易日运行")
        return
    factor_return = analyzer.construct_factor_return(weights_df=weights_df, ret=ret)

    raw_data = FactorQuadEQ.factor_quads_download(factor_system=factor_system,
                                                  start_date=start_date,
                                                  end_date=date_of_running,
                                                  from_src=0)
    latest_factor_number = list(set(raw_data['characteristic_exposure']['characteristic']))
    latest_industries = [x for x in latest_factor_number if x.split('_')[0] == 'industry']
    # assert len(latest_industries) == 35, "wrong number of industries!"
    factor_return_industries = [x for x in factor_return.columns if x.split('_')[0] == 'industry']
    industry_diff = list(set(latest_industries).difference(factor_return_industries))
    if len(industry_diff) != 0:
        factor_return = pd.concat(
            [factor_return, pd.DataFrame(data=0.0, index=factor_return.index, columns=industry_diff)],
            axis=1)
    assert len(latest_factor_number) + 1 == len(factor_return.columns), "wrong number of factors!"

    latest_day_factor_return = factor_return.tail(1)
    factor_return_target_date = latest_day_factor_return.index[0].strftime("%Y%m%d")

    if factor_return_target_date != date_of_running:
        # print("不存在需要更新的因子收益数据，可能是因为当天还未跑四元组日更，或为节假日。"
        #       "本程序更新因子收益失败自动结束，请先运行四元组日更，或选择下一个交易日运行")
        logger.info(
            "不存在需要更新的因子收益数据，可能是因为当天还未跑四元组日更，或为节假日。"
              "本程序更新因子收益失败自动结束，请先运行四元组日更，或选择下一个交易日运行")

        return
    stacked_factor_return = latest_day_factor_return.stack(dropna=False).reset_index()
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
    filename = f"characteristic_return_{factor_system}_{factor_return_target_date}.gzip.parquet"
    path = pathlib.Path.joinpath(pathlib.Path(output_path), filename)
    # 如果文件已存在，则删除替换文件
    if path.is_file():
        path.unlink()
    stacked_factor_return.to_parquet(path=str(path))
    logger.info(f"{date_of_running}_{factor_system}因子收益更新成功，运行结束~")


def update_historical_factor_return(start_date: str,
                                    end_date: str,
                                    factor_system='HF25_SRAM_DAILY_V0',
                                    output_path="D:/jiaochayuan_files/projects/characteristic_return"):
    """
    跑历史因子收益
    Args:
        start_date: 起始日期，注意跑出来的因子收益的日期会滞后一期。比如start date如果是20210101，则跑出来的因子收益是从start date的下一个
        交易日开始的。
        end_date: 结束日期
        factor_system:
        output_path: 储存文件的本地文件夹地址,这个文件夹必须已经存在

    Returns:

    """
    logger = setup_logger(log_level='INFO', log_file_name='因子收益日更日志.log', log_path='./')
    factorquad = FactorQuadEQ.create_factor_quad(factor_system=factor_system,
                                                 start_date=start_date,
                                                 end_date=end_date,
                                                 from_src=3,
                                                 local_path="D:\jiaochayuan_files\projects\we_factor_analysis\we_factor_analysis/factor_validation/factor_return")
    analyzer = FmpAnalyzer(quad=factorquad)
    # end_date_range = list(pd.DataFrame(factorquad.date_list).set_index([0]).to_period('M').to_timestamp('M').index)
    # year_range = sorted(list(set([x.year for x in end_date_range])))
    weights_df = analyzer.get_portfolio_weights(start_date=start_date,
                                                end_date=end_date,
                                                freq='B')
    ret = dapi.get_stock_return(start=start_date,
                                end=end_date,
                                freq='B')
    factor_return = analyzer.construct_factor_return(weights_df=weights_df, ret=ret)
    for i in range(1, len(factorquad.date_list)):
        if pd.Timestamp(factorquad.date_list[i]) != factor_return.index[i - 1]:
            logger.info(f"beta日期与factor_return日期不匹配，{factorquad.date_list[i]} 不等于 factor_return.index[i]， 更新历史失败")
            raise ValueError("日期不匹配，更新历史失败")

    raw_data = FactorQuadEQ.factor_quads_download(factor_system=factor_system,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  from_src=0)
    latest_factor_number = list(set(raw_data['characteristic_exposure']['characteristic']))
    latest_industries = [x for x in latest_factor_number if x.split('_')[0] == 'industry']
    # assert len(latest_industries) == 35, "wrong number of industries!"
    factor_return_industries = [x for x in factor_return.columns if x.split('_')[0] == 'industry']
    industry_diff = list(set(latest_industries).difference(factor_return_industries))
    if len(industry_diff) != 0:
        factor_return = pd.concat(
            [factor_return, pd.DataFrame(data=0.0, index=factor_return.index, columns=industry_diff)],
            axis=1)
    assert len(latest_factor_number) + 1 == len(factor_return.columns), "wrong number of factors!"

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
    fr_start_date_str = factor_return.index[0].strftime("%Y%m%d")
    fr_end_date_str = factor_return.index[-1].strftime("%Y%m%d")
    filename = f"characteristic_return_{factor_system}_{fr_start_date_str}_{fr_end_date_str}.gzip.parquet"
    path = pathlib.Path.joinpath(pathlib.Path(output_path), filename)
    # 如果文件已存在，则删除替换文件
    if path.is_file():
        path.unlink()
    stacked_factor_return.to_parquet(path=str(path))
    logger.info(f"{fr_start_date_str}_{fr_end_date_str}_{factor_system}历史因子收益更新成功，运行结束~")



def upload_file(path):
    for time in range(5):
        res = wiserdata.update(factor_system, [path], daemon=False)
        logger.info(f"Uploading {path}")
        if res:
            os.remove(path)
            logger.info('Success')
            return
    logger.error(f'Error: File upload failure: {path}')


def run():
    if start_date == end_date:
        update_daily_factor_return(factor_system, output_path, start_date)
    else:
        update_historical_factor_return(start_date, end_date, factor_system, output_path)

if __name__ == "__main__":
    # start_date = "20091220"
    # end_date = "20091231"
    # # 跑历史数据的时候 start_date 要指定前一天
    # parser = argparse.ArgumentParser(description='This is the we_factor_return start shell')
    # parser.add_argument("--factor_system", required=True)
    # parser.add_argument("--output_path", required=True)
    # parser.add_argument("--start_date", required=True)
    # parser.add_argument("--end_date", required=True)
    #
    # args = parser.parse_args()
    #
    # factor_system = args.factor_system
    # output_path = args.output_path
    # start_date = args.start_date
    # end_date = args.end_date
    #
    # run()
    update_daily_factor_return(date_of_running="20140102")