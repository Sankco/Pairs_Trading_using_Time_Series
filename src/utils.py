import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint



def find_cointegrated_pairs(data):
    n = data.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = {}
    for i in range(n):
        for j in range(i+1, n):
            S1 = data[keys[i]]
            S2 = data[keys[j]]
            result = coint(S1, S2)
            score = result[0]
            pvalue = result[1]
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            if pvalue < 0.05:
                pairs[(keys[i], keys[j])] = result
    return score_matrix, pvalue_matrix, pairs


def get_top_k_pairs(pairs,k):
    pairs_data = {key:value[1]  for (key, value) in pairs.items()}
    pairs_data = sorted(pairs_data.items(), key=lambda x: x[1])
    return pairs_data[0:k]


def get_cointergrated_coeff(y:pd.Series,x:pd.Series):

    """
    y = beta*x + e
    y-beta*x = e
    alpha = -beta


    Return: alpha
    """
    regress = sm.OLS(y,x)
    regress = regress.fit()
    alpha = -regress.params.iloc[0]
    return alpha



def buy_signal_plots(spread,S1,S2,window1=60,window2=5,upper=1,lower=-1,label="Actual"):

    # Plot the ratios and buy and sell signals from z score
  
    ma1 = spread.rolling(window=window1, center=False).mean()
    ma2 = spread.rolling(window=window2, center=False).mean()
    std = spread.rolling(window=window2, center=False).std()
    zscore = ((ma1 - ma2)/std)

    # Compute the z score for each day
    zscore.name = 'z-score'

    plt.figure(figsize=(15,7))
    zscore.plot()

    plt.scatter(list(zscore[zscore>upper].index),zscore[zscore>upper],color="red")
    plt.scatter(list(zscore[zscore<lower].index),zscore[zscore<lower],color="green")  #
    plt.axhline(0, color='black')
    plt.axhline(upper, color='red', linestyle='--')
    plt.axhline(lower, color='green', linestyle='--')
    plt.legend([f'Rolling Spread {label} z-score',f'{upper}', f'{lower}','Mean'])
    plt.show()




# def buy_signal_plots(spread,S1,S2,window1=5,window2=60,label="Actual",upper=1,lower=-1):

#     # Plot the ratios and buy and sell signals from z score
  
#     ma1 = spread.rolling(window=window1, center=False).mean()
#     ma2 = spread.rolling(window=window2, center=False).mean()
#     std = spread.rolling(window=window2, center=False).std()
#     zscore = ((ma1 - ma2)/std)

#     # Compute the z score for each day
#     zscore.name = 'z-score'

#     pyplot.figure(figsize=(15,7))
#     zscore.plot()

#     pyplot.scatter(list(zscore[zscore<lower].index),zscore[zscore<-1],color="red")  #
#     pyplot.scatter(list(zscore[zscore>upper].index),zscore[zscore>1],color="green")
#     pyplot.axhline(0, color='black')
#     pyplot.axhline(1.0, color='red', linestyle='--')
#     pyplot.axhline(-1.0, color='green', linestyle='--')
#     pyplot.legend([f'Rolling Spread {label} z-Score', 'Mean', f'{upper}', '{lower}'])
#     pyplot.show()


    # pyplot.figure(figsize=(15,7))

    # plt.figure(figsize=(15,7))
    # buy = spread.copy()
    # sell = spread.copy()
    # buy[np.array(zscore)>lower] = -100  ## will remove these points by limiting y axis.
    # sell[np.array(zscore)<upper] = -100

    # spread.plot()
    # buy.plot(color='g', linestyle='None', marker='^')
    # sell.plot(color='r', linestyle='None', marker='^')

    # x1,x2,y1,y2 = plt.axis()
    # plt.axis((x1,x2,spread.min(),spread.max()))
    # plt.legend(['Spread', 'Buy Signal', 'Sell Signal'])
    # plt.title(f' Residual buy/sell plot developed using {label} Next Day Residuals')
    # plt.show()


    # # Plot the prices and buy and sell signals from z score
    # pyplot.figure(figsize=(17,9))
    # S1[index:].plot(color='b')
    # S2[index:].plot(color='c')
    # buyR = 0*S1.copy()
    # sellR = 0*S1.copy()

    # # When buying the ratio, buy S1 and sell S2
    # buyR[buy!=-100] = S1[buy!=-100]
    # sellR[buy!=-100] = S2[buy!=-100]
    # # When selling the ratio, sell S1 and buy S2 
    # buyR[sell!=-100] = S2[sell!=-100]
    # sellR[sell!=-100] = S1[sell!=-100]

    # buyR[index:].plot(color='g', linestyle='None', marker='^')
    # sellR[index:].plot(color='r', linestyle='None', marker='^')
    # x1,x2,y1,y2 = pyplot.axis()
    # pyplot.axis((x1,x2,min(S1.min(),S2.min()),max(S1.max(),S2.max())))

    # pyplot.legend(['S1', 'S2', 'Buy Signal', 'Sell Signal'])
    # pyplot.show()


def trade_strategy(S1, S2, spread, window1, window2,sell_threshold,buy_threshold,clear_threshold):
    # If window length is 0, algorithm doesn't make sense, so exit
    if (window1 == 0) or (window2 == 0):
        return 0
    # Compute rolling mean and rolling standard deviation
    ma1 = spread.rolling(window=window1, center=False).mean()
    ma2 = spread.rolling(window=window2, center=False).mean()
    std = spread.rolling(window=window2, center=False).std()
    zscore = ((ma1 - ma2)/std)

    # Simulate trading
    # Start with no money and no positions
    money = 0
    countS1 = 0
    countS2 = 0
    for i in range(len(spread)-1):
        # Sell short if the z-score is > 1
        if zscore.iloc[i] > sell_threshold:
            money += S1.iloc[i] - S2.iloc[i] * spread.iloc[i]
            countS1 -= 1
            countS2 += spread.iloc[i]
        # Buy long if the z-score is < 1
        elif zscore.iloc[i] < buy_threshold:
            money -= S1.iloc[i] - S2.iloc[i]* spread.iloc[i]
            countS1 += 1
            countS2 -= spread.iloc[i]
        # Clear positions if the z-score between -.5 and .5
        elif abs(zscore.iloc[i]) < clear_threshold:
            money += countS1 * S1.iloc[i] + S2.iloc[i] * countS2
            countS1 = 0
            countS2 = 0
    # close position money
    return money + (countS1 * S1.iloc[i+1] + S2.iloc[i+1] * countS2)