# Parameter Optimization
import numpy as np
from mango.tuner import Tuner

class bayesianOpt:

    def __init__(self):
        self.optimize_results = None
       

    def optimize(self,spread,S1,S2,param_grid,conf_dict):
        """
        Optimization Function for classifier with data inputs and scoring function
        """
        def objective(args_list):
            all_money = []
            for params in args_list:

                window1 = params["window1"]
                window2 = params["window2"]
                sell_threshold = params["sell_threshold"]
                buy_threshold = params["buy_threshold"]
                clear_threshold = params["clear_threshold"]
                money = self.trade(spread,S1,S2,window1,window2,sell_threshold,buy_threshold,clear_threshold)
                all_money.append(money)
            return all_money

        tuner_user = Tuner(param_grid, objective, conf_dict)
        optimize_results = tuner_user.maximize()
        self.optimize_results = optimize_results
        return optimize_results
    
    def trade(self,spread,S1,S2,window1,window2,sell_thresold,buy_threshold,clear_threshold):
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
            if zscore.iloc[i] > sell_thresold:
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
