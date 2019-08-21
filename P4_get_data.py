import pandas as pd
import os
import time
import re
from datetime import datetime

from time import mktime
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import style
style.use("dark_background")

path = "/Users/huixia/Documents/ScikitLearn/intraQuarter"


def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path+'/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]     #x[0] is directory len=561, x[1] is folder name len = 561, x[2] is html file name, len = 561
    # print len(stock_list)
    # print stock_list
    df = pd.DataFrame(columns = ['Date',
                                 'Unix',
                                 'Ticker',
                                 'DE Ratio',
                                 'Price',
                                 'stock_p_change',
                                 'SP500',
                                 'sp500_p_change',
                                 'Difference'
                                 ])

    sp500_df = pd.read_csv('ALPHAVANTAGE-INDEX.csv', index_col = None)
    # print sp500_df.index

    ticker_list = []

    for each_dir in stock_list[1:]:
        print "\neach_dir:"+ each_dir
        each_file = os.listdir(each_dir)
        # print(each_file)
        # time.sleep(15)
        # ticker = each_dir.split("\\")[1]
        ticker = each_dir.split('/Users/huixia/Documents/ScikitLearn/intraQuarter/_KeyStats/')[1]
        ticker_list.append(ticker)
        starting_stock_value = False
        starting_sp500_value = False

        if len(each_file) > 0:
            for file in each_file:

                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                # print date_stamp,unix_time
                full_file_path = each_dir+'/'+file
                # print full_file_path
                source = open(full_file_path, 'r').read()  #normally this will be a urllib.urlopen if this is a url
                # print source

                try:
                    try:
                        # print "source b4 removal\n", source
                        # source = source.replace("\n", "")
                        # print "source after removal\n", source
                        # time.sleep(5)
                        value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    except Exception as ex11:
                        # print "ticker:", ticker, file, "problem ex11:", str(ex11)
                        try:
                            value = source.split(gather + ':</td>')[1].split('</td>')[0]
                            # print "value b4:", value
                            value = float(re.search('(\d+\.\d+)', value).group(0))
                            # print "value after:", value
                        except Exception as ex111:
                            # print "ticker:", ticker, file, "value:", value, "problem ex111:", str(ex111)
                            pass

                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df['Date'] == sp500_date)]
                        sp500_value = float(row["Adj Close"])
                        # print "==================="
                    except:
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df['Date'] == sp500_date)]
                        sp500_value = float(row["Adj Close"])
                        # print "+++++++++++++++++"

                    try:
                        # print "stock_price b4 treatment:\n", stock_price
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>&')[0])
                        # print "stock_price after treatment:\n", stock_price
                        # print 'stock price:', stock_price, "ticker:", ticker
                        # time.sleep(5)
                    except Exception as ex13:
                        # print "ticker:", ticker, file, "problem ex13:", str(ex13)
                        try:
                            stock_price = (source.split('</small><big><b>')[1].split('</b></big>&')[0])
                            # print "Hui's split000:", stock_price
                            stock_price = float(re.search('(\d+\.\d+)',stock_price).group(0))
                            # print "Hui's split050505:", stock_price
                            # stock_price = float(stock_price.group(1))

                        except Exception as ex131:
                            # print "ticker:", ticker, file, "problem ex131:", str(ex131)
                            try:
                                # print "stock_price b4 treatment:\n", stock_price
                                stock_price = re.search('<span id="yfs_''\D+''\d+''\D+''">''(\d+\.\d+)''</span>', source).group(0)

                                # print "Hui's split111:", stock_price
                                # stock_price = re.search('(\d+\.\d+)', stock_price)
                                stock_price = float(re.search('(\d+\.\d+)', stock_price).group(0))
                                # print "Hui's split222:", stock_price
                                # stock_price = float(stock_price.group(1))


                            except Exception as ex1311:
                                print "ticker:", ticker, file, "problem ex1311:", str(ex1311)





                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value

                    # print "starting_stock_value:======================", starting_stock_value, stock_price
                    stock_p_change = (stock_price - starting_stock_value) / starting_stock_value * 100.0
                    # print "stock_p_change:+++++++++++++++++++++++++", stock_p_change
                    sp500_p_change = (sp500_value - starting_sp500_value) / starting_sp500_value * 100.0

                    df = df.append({'Date':date_stamp,
                                    'Unix':unix_time,
                                    'Ticker':ticker,
                                    'DE Ratio':value,
                                    'Price':stock_price,
                                    'stock_p_change': stock_p_change,
                                    'SP500':sp500_value,
                                    'sp500_p_change': sp500_p_change,
                                   'Difference': stock_p_change - sp500_p_change
                                    },
                                   ignore_index = True)
                except Exception as e:
                    pass
                    # print str(e)
                    # print full_file_path
                    # value = float('nan')
    print "ticker_list:", ticker_list
    for each_ticker in ticker_list:
        try:
            plot_df = df[(df['Ticker']) == each_ticker]
            # print "checker 00000000\n", plot_df
            plot_df.set_index(['Date'], inplace = True)
            # print "checker 1111111\n",  plot_df

            plot_df['Difference'].plot(label = each_ticker)
            # plt.plot(plot_df['Difference'],label='Strategy Learner Portfolio', color='B')
            # print "checker 22222222\n", plot_df
            plt.legend()
        except Exception as ex2:
            print "ticker is:", each_ticker, "reason is:", str(ex2)
            pass
    plt.savefig('Figure.png')
    # plt.show()

    save = gather.replace(' ', '').replace(')', '').replace('(', '').replace('/', '') + str('.csv')
    print "save:", save
    df.to_csv(save)
                # print(ticker+":",value)




Key_Stats()
