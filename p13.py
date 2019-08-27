import numpy as np
import pandas as pd
from sklearn import svm, preprocessing
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")



def Build_Data_Set(FEATURES =  ['DE Ratio',
             'Trailing P/E',
             'Price/Sales',
             'Price/Book',
             'Profit Margin',
             'Operating Margin',
             'Return on Assets',
             'Return on Equity',
             'Revenue Per Share',
             'Market Cap',
             'Enterprise Value',
             'Forward P/E',
             'PEG Ratio',
             'Enterprise Value/Revenue',
             'Enterprise Value/EBITDA',
             'Revenue',
             'Gross Profit',
             'EBITDA',
             'Net Income Avl to Common ',
             'Diluted EPS',
             'Earnings Growth',
             'Revenue Growth',
             'Total Cash',
             'Total Cash Per Share',
             'Total Debt',
             'Current Ratio',
             'Book Value Per Share',
             'Cash Flow',
             'Beta',
             'Held by Insiders',
             'Held by Institutions',
             'Shares Short (as of',
             'Short Ratio',
             'Short % of Float',
             'Shares Short (prior ']):
    data_df = pd.DataFrame.from_csv("key_stats.csv")
    # print data_df
    # data_df = data_df[:1000]

    X = np.array(data_df[FEATURES].values)#.tolist())

    y = (data_df["Status"]
         .replace("underperform", 0)
         .replace("outperform", 1)
         .values.tolist())

    X = preprocessing.scale(X)

    return X, y

def Analysis():
    test_size = 500
    X, y = Build_Data_Set()
    print len(X)
    # print X
    # print "y:\n", y
    clf = svm.SVC(kernel = "linear", C = 1.0)
    clf.fit(X[:-test_size],y[:-test_size])

    correct_count = 0
    predictions = clf.predict(X)
    print "predictions", predictions, "\n++++++++++"

    for x in range(1,test_size+1):
        print predictions[x], y[x], "\n =================="
        if predictions[x] == y[x]:
            correct_count += 1.0

    print "accuracy:" , (correct_count/test_size) * 100
    # print correct_count
    # w = clf.coef_[0]
    #
    # a = -w[0] / w[1]
    #
    # xx = np.linspace(min(X[:, 0]), max(X[:, 0]))
    #
    # yy = a * xx - clf.intercept_[0] / w[1]
    #
    # h0 = plt.plot(xx,yy,"k-", label = "non weighted")
    #
    # plt.scatter(X[:, 0], X[:, 1], c = y)
    # plt.ylabel("Trailing P/E")
    # plt.xlabel("DE Ratio")
    # plt.legend()
    # plt.savefig('Figure_13.png')
    # plt.show()

Analysis()