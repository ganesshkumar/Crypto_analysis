import os
import time
from datetime import datetime
import pandas as pd
import json
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from requests import Request, Session

import streamlit as st
from tradingview_ta import TA_Handler, Interval, Exchange

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

class analysis:

    def __init__(self):
        self.all_crypto, self.crypto_changes = self.get_marketCap()
        self.buy = []
        self.sell = []
        self.strong_buy=[]
        self.strong_sell=[]
        self.data = {}
        self.info_mma = {}
        self.info_osc = {}
        self.recommanded_crypto=[]

    @st.cache(allow_output_mutation=True)
    def get_marketCap(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
        'start':'1',
        'limit':'100',
        'convert':'USDT'
        }
        headers = {
        'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '',
        }

        session = Session()
        session.headers.update(headers)

        try:
            crypto_data=[]
            changes={}
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            
            for d in data.keys():
                if d=="data":
                    for i in data[d]:
                        ticker=i["symbol"]
                        proc_1h = i["quote"]["USDT"]["percent_change_1h"]
                        proc_24h= i["quote"]["USDT"]["percent_change_24h"]
                        proc_7d = i["quote"]["USDT"]["percent_change_7d"]
                        crypto_data.append(ticker)
                        changes[ticker] = [proc_1h, proc_24h, proc_7d]
            
            return crypto_data,changes 
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return e

    #@st.cache
    def get_analysis_mma(self,tick,interval):
        try:
            ticker_summery = TA_Handler(
                symbol=tick,
                screener="crypto",  # "america"
                exchange="binance",  # "NASDAQ"
                interval=interval  # Interval.INTERVAL_1_DAY
            )
            analyse = ticker_summery.get_analysis().moving_averages
            if analyse is not None:
                return analyse 
        except:
            pass

    #@st.cache()
    def get_analysis_osc(self,tick,interval):
        try:
            ticker_summery = TA_Handler(
                symbol=tick,
                screener="crypto",  # "america"
                exchange="binance",  # "NASDAQ"
                interval=interval  # Interval.INTERVAL_1_DAY
            )
            analyse = ticker_summery.get_analysis().oscillators
            if analyse is not None: 
                return analyse 
        except:
            pass

    def crypto_analysis(self,info):
        
        for i in info:
            if info[i]["RECOMMENDATION"] == "BUY":
                self.buy.append(i.replace("USDT",""))
            if info[i]["RECOMMENDATION"] == "SELL":
                self.sell.append(i.replace("USDT", ""))
            if info[i]["RECOMMENDATION"] == "STRONG_BUY":
                self.strong_buy.append(i.replace("USDT",""))
            if info[i]["RECOMMENDATION"] == "STRONG_SELL":
                self.strong_sell.append(i.replace("USDT", ""))
        if self.strong_buy and self.strong_sell is not None:
            return self.buy, self.sell, self.strong_buy, self.strong_sell
        

    #supported_list = ["ADA","ATOM","BTT","DASH","DOGE","EOS","ETC","ICX","IOTA","NEO","OMG","ONT","QTUM","TRX","VET","XLM","XMR"]        
    #@st.cache
    def save_file(self, final_list):
        with open("supported_coin_list.txt", "w") as file:
            for coin in final_list:
                file.writelines(coin+'\n')
            file.close()
                          
    def do_job(self):

        st.sidebar.header("Crypto-Analysis")
        btn = st.sidebar.radio("Choose interval",(
            "1 minute", 
            "5 minutes",
            "15 minutes",
            "1 hour",
            "4 hours",
            "1 day",
            "1 week",
            "1 month"))

        t0=time.time()
        my_bar = st.progress(0)
        
        filtered_coins = [coin for coin in self.crypto_changes.keys() if self.crypto_changes[coin][0] and self.crypto_changes[coin][1] and self.crypto_changes[coin][2] > 0]
        percent_complete = 0
        
        for ticker in filtered_coins:
            ticker = ticker+"USDT"
            if btn=="1 minute":
                self.info_mma[ticker] = self.get_analysis_mma(ticker, Interval.INTERVAL_1_MINUTE)
            
            if btn=="5 minutes":
                self.info_mma[ticker] = self.get_analysis_mma(ticker, Interval.INTERVAL_5_MINUTES)
            
            if btn=="15 minutes":
                self.info_mma[ticker] = self.get_analysis_mma(ticker, Interval.INTERVAL_15_MINUTES)
            
            if btn=="1 hour":
                self.info_mma[ticker] = self.get_analysis_mma(ticker, Interval.INTERVAL_1_HOUR)
            
            if btn=="4 hours":
                self.info_mma[ticker] = self.get_analysis_mma(ticker, Interval.INTERVAL_4_HOURS)
            
            if btn=="1 day":
                self.info_mma[ticker] = self.get_analysis_mma(ticker, Interval.INTERVAL_1_DAY)
            
            if btn=="1 week":
                self.info_mma[ticker] = self.get_analysis_mma(ticker, Interval.INTERVAL_1_WEEK)
            
            if btn=="1 month":
                self.info_mma[ticker] = self.get_analysis_mma(ticker, Interval.INTERVAL_1_MONTH)
            percent_complete = percent_complete + 1
            my_bar.progress(percent_complete)
        

        info_filtered = {x: y for x, y in self.info_mma.items() if (y is not None and y != 0)}
        self.buy, self.sell, self.strong_buy, self.strong_sell = self.crypto_analysis(info_filtered)
        
        for ticker in self.strong_buy:
            ticker = ticker+"USDT"
            if btn=="1 minute":
                self.info_osc[ticker] = self.get_analysis_osc(ticker, Interval.INTERVAL_1_MINUTE)
            
            if btn=="5 minutes":
                self.info_osc[ticker] = self.get_analysis_osc(ticker, Interval.INTERVAL_5_MINUTES)
            if btn=="15 minutes":
                self.info_osc[ticker] = self.get_analysis_osc(
                    ticker, Interval.INTERVAL_15_MINUTES)
            if btn=="1 hour":
                self.info_osc[ticker] = self.get_analysis_osc(ticker, Interval.INTERVAL_1_HOUR)
            if btn=="4 hours":
                self.info_osc[ticker] = self.get_analysis_osc(ticker, Interval.INTERVAL_4_HOURS)
            if btn=="1 day":
                self.info_osc[ticker] = self.get_analysis_osc(
                    ticker, Interval.INTERVAL_1_DAY)
            if btn=="1 week":
                self.info_osc[ticker] = self.get_analysis_osc(ticker, Interval.INTERVAL_1_WEEK)
            if btn=="1 month":
                self.info_osc[ticker] = self.get_analysis_osc(ticker, Interval.INTERVAL_1_MONTH)
        
        

        info2_filtered = {x: y for x, y in self.info_osc.items() if (y is not None and y != 0)}
        
        for i in info2_filtered:
            if info2_filtered[i]["RECOMMENDATION"] == "BUY":
                self.recommanded_crypto.append(i.replace("USDT", ""))
        my_bar.progress(100)
        t1=time.time()
        total = round(t1-t0,2)

        st.write(f"{total} seconds")
        
        st.header("BUY/SELL")
        col1, col2,col3,col4,col5 = st.beta_columns(5)
        if self.strong_buy or self.strong_sell is not None:
            col1.success("recommanded")
            col2.success("Strong buy")
            col3.success("Buy")
            col4.error("Sell")
            col5.error("Strong sell")
            col1.table(self.recommanded_crypto)
            col2.table(self.strong_buy)
            col3.table(self.buy)
            col4.table(self.sell)
            col5.table(self.strong_sell)
        else:
            col2.success("Buy")
            col3.error("Sell")
            col2.table(self.buy)
            col3.table(self.sell)

        st.sidebar.subheader("Overwrite [supported_coin_list.txt] coin list")
        option = st.sidebar.radio("", (
            "Strong buy list",
            "Buy list","Recommanded list"))
        bt = st.sidebar.button("save")

        if bt:
            if option=="Strong buy list":
                self.save_file(self.strong_buy)
            if option=="Buy list":
                self.save_file(self.buy)
            if option == "Recommanded list":
                self.save_file(self.recommanded_crypto)
            directory_path = os.getcwd()
            st.sidebar.success(
                f"file [supported_coin_list.txt]\nfile_path: {directory_path}")
def main():
    crypto_analysis= analysis()
    crypto_analysis.do_job()
            
if __name__=="__main__":
    main()
