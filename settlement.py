# -*- coding: utf-8 -*-
from __future__ import division

import datetime as dt
import logging
import re
import time
from io import StringIO

import numpy as np
import pandas as pd
import requests
from flask import Flask
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route("/")
def index():
    return "Hello world"


@app.route('/SMP/hourly_kmos')
def api_read_kpx_smp_hourly_kmos():
    logger.debug("kmos SMP api starts")
    table = read_hourly_smp_prices_from_kmos_website()
    today_year = dt.datetime.today().year
    table.columns = pd.to_datetime('{}.'.format(today_year) + table.columns.str[:5])
    table.index = [pd.Timedelta(i, unit='h') for i in table.index]
    table.index -= pd.Timedelta('1hour')
    table = table.stack()
    table.index = table.index.get_level_values(0) + table.index.get_level_values(1)
    table.sort_index(inplace=True)
    df_smp_hourly = table.to_frame("SMP_hourly")
    return df_smp_hourly.to_json()


def get_fixed_price_table():
    df = read_hourly_smp_prices_from_kmos_website()
    columns_to_drop = df.columns[:6]
    df_today_smp = df.drop(columns_to_drop, axis=1)
    today_datetimeindex = pd.date_range(start=dt.datetime.today().date(), periods=24, freq='1H') \
                          + pd.Timedelta(hours=1)
    today_timestampindex = datetimeindex_to_timestamp(today_datetimeindex)
    df_today_smp.index = today_timestampindex
    df_today_smp.columns = ['KPX_SMP']
    return df_today_smp


def read_hourly_smp_prices_from_kmos_website():
    """
    read_hourly_smp_prices_from_kmos_website()

    신재생원스톱 사업정보 통합포털 웹사이트에서 최근 1주일치 시간대별 SMP를 크롤링 하는 함수

   :return:
   type: pandas.DataFrame
   column: "SMP_hourly"
   dimension: 168x1
   unit: KRW/kWh
    """
    html = requests.get('http://onerec.kmos.kr/portal/rec/selectRecSMPList.do?key=1965').text
    df = pd.read_html(html, index_col=0)[1].head(24).dropna(1, 'all')
    return df


def datetimeindex_to_timestamp(datetimeindex):
    return datetimeindex.astype(np.int64)


@app.route('/REC/realtime')
def api_read_kpx_rec_spot():
    logger.debug("REC spot market api starts")
    df_rec_realtime = get_spot_market_table()
    return df_rec_realtime.to_json()


def get_spot_market_table():
    [table, timestamp] = read_realtime_rec_data_from_spotmarket_website()
    df_rec_realtime = convert_rec_spot_raw_to_df(table, timestamp)
    return df_rec_realtime


def read_realtime_rec_data_from_spotmarket_website(chrome_driver_path=None):
    """
    .. todo:: html Implementation 해야됨 ('http://rec.kmos.kr:8090/trade/popup_b.html#')

    :return:
    """
    logger.debug("Start to read realtime rec data from spotmarket website")
    if chrome_driver_path is None:
        chrome_driver_path = ChromeDriverManager().install()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_experimental_option("prefs",
                                    {"download.default_directory": "~/", "download.prompt_for_download": False})
    driver = webdriver.Chrome(chrome_driver_path, options=options)
    driver.get("http://rec.kmos.kr:8090/trade/popup_b.html#")
    time_stamp = time.mktime(dt.datetime.now().timetuple())
    max_number_of_retries = 10

    for k in range(max_number_of_retries):
        table = driver.find_element_by_css_selector((".t02")).text
        table = re.split(' |\n', table)
        if str(table[6]) == '-':
            logger.warning("The page is not loaded completely. Trying again. Wait three seconds...")
            time.sleep(3)
        else:
            break

    driver.quit()
    return table, time_stamp


def convert_rec_spot_raw_to_df(table, time_stamp):
    data = table[6:11] + table[18:23]
    datetime = dt.datetime.fromtimestamp(time_stamp)
    data.insert(0, datetime)
    data = list(map(lambda x: x.replace(",", "") if isinstance(x, str) else x, data))
    index = ['price_time', 'present_price', 'diff_money', 'highest_price', 'upper_limit_price', 'accum_trading_vol',
             'open_price', 'diff_percent', 'lowest_price', 'lower_limit_price', 'accum_trading_val']
    df_rec_realtime = pd.DataFrame(data, index, ['REC_today'])
    return df_rec_realtime


@app.route('/SMP/hourly_maleum')
def api_read_kpx_smp_hourly_maleum():
    logger.debug("maleum SMP api starts")
    df = read_hourly_smp_prices_from_maleum_website()
    df.columns = ['time', 'jeju', 'mainland']
    datetime_index = pd.date_range(pd.datetime.today(), periods=24, freq='H', tz='Asia/Seoul',
                                   normalize=True) + pd.Timedelta(days=1, hours=1)
    timestamp_index = datetime_index.values.astype(np.int64) // 10 ** 9
    df.index = timestamp_index
    df.drop('time', 1, inplace=True)
    return df.to_json(orient='index')


def read_hourly_smp_prices_from_maleum_website(chrome_driver_path=None):
    if chrome_driver_path is None:
        chrome_driver_path = ChromeDriverManager().install()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_experimental_option("prefs",
                                    {"download.default_directory": "~/", "download.prompt_for_download": False})
    driver = webdriver.Chrome(chrome_driver_path, options=options)
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow', 'downloadPath': '~/'}}
    driver.execute("send_command", params)
    driver.get('https://www.mal-eum.com/smp/trend/daily')
    time.sleep(3)
    csv = StringIO(driver.find_element_by_class_name("google-visualization-table-table").text)
    driver.quit()
    df = pd.read_csv(csv, ' ')
    return df


@app.route('/SMP/monthly')
def api_read_kpx_smp_monthly():
    logger.debug("Monthly SMP api starts")
    df = read_monthly_weighted_mean_prices_of_smp_from_kepco_website()
    df.drop('NO', 1, inplace=True)
    df.sort_index(inplace=True)
    df.columns = ['SMP_monthly']
    return df.to_json()


def read_monthly_weighted_mean_prices_of_smp_from_kepco_website():
    """
    read_monthly_weighted_mean_prices_of_smp_from_kepco_website()

    한전 웹페이지로부터 올해 월별 가중평균 SMP 값을 받아옴

    :return:
   type: pandas.DataFrame
   column: "SMP_monthly"
   dimension: depends on current month
   unit: KRW/kWh
    """
    html = requests.get('http://home.kepco.co.kr/kepco/CO/D/E/CODEPP002/list.do').text
    df = pd.read_html(html, index_col=1, parse_dates=True)[0]
    return df


@app.route('/REC/thismonth')
def api_read_kpx_rec_thismonth():
    logger.debug("Monthly REC api starts")
    df = read_rec_thismonth_from_kmos_website()
    df.drop(['비태양광', '거래량 합계'], 1, inplace=True)
    df.columns = ['rec_transaction', 'rec_price']
    df.index = ['spot', 'contract', 'total']
    return df.to_json()


def read_rec_thismonth_from_kmos_website():
    """
    read_rec_thismonth_from_kmos_website()

    신재생원스톱 사업정보 통합포털 웹페이지로부터 이번달 REC 시장 종합정보 값을 받아옴.

    :return:
   type: pandas.DataFrame
   column: "REC_transactions", "REC_price"
   dimension: depends on current month
   unit: KRW/kWh
    """
    html = requests.get('http://onerec.kmos.kr/portal/rec/selectRecReport_SMPList.do?key=1971').text
    df = pd.read_html(html, index_col=0, parse_dates=True)[0]
    return df


if __name__ == "__main__":
    read_realtime_rec_data_from_spotmarket_website()
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, host='0.0.0.0', port=5000)