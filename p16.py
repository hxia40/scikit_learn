import numpy as np
import pandas as pd
import os
import time
from sklearn import svm, preprocessing
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
import quandl
quandl.ApiConfig.api_key = '1Wqwfvb_8P63_mcduPa4'




# data = quandl.get("WIKI/KO", trim_start = "2000-12-12", trim_end = "2014-12-30" )
# print data["Adj. Close"]
path = "/Users/huixia/Documents/ScikitLearn/intraQuarter"

def Stock_Prices():
    df = pd.DataFrame()
    statspath = path + "/_KeyStats"
    stock_list = [x[0] for x in os.walk(statspath)]

    for each_dir in stock_list[1:]:
        try:
            ticker = each_dir.split('/Users/huixia/Documents/ScikitLearn/intraQuarter/_KeyStats/')[1]
            print ticker
            name = "WIKI/" + ticker.upper()
            data = quandl.get(name,
                              trim_start = "2000-12-12",
                              trim_end = "2014-12-30")
            data[ticker.upper()] = data["Adj. Close"]
            df = pd.concat([df, data[ticker.upper()]], axis = 1)

            # ticker_list.append(ticker)
        except Exception as e1:
            print "error e1:", str(e1)
            time.sleep(10)
            try:
                ticker = each_dir.split('/Users/huixia/Documents/ScikitLearn/intraQuarter/_KeyStats/')[1]
                print ticker
                name = "WIKI/" + ticker.upper()
                data = quandl.get(name,
                                  trim_start="2000-12-12",
                                  trim_end="2014-12-30")
                data[ticker.upper()] = data["Adj. Close"]
                df = pd.concat([df, data[ticker.upper()]], axis=1)
            except Exception as e11:
                print "error e11:", str(e11)
    df.to_csv("stock_prices.csv")


Stock_Prices()