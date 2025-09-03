import ta
import pandas as pd


class TechnicalFeatures:

    def __init__(self,data):
        self.data = data

    def create_suffix(self,column,suffix):
        return column + '_'+suffix

    def rsi(self,window = 14,columns=[],suffix='rsi',inplace = True):

        data = self.data
        new_data = pd.DataFrame()
        
        for col in columns:
            name = self.create_suffix(col,suffix)
            if inplace == True:
                data[name] = ta.momentum.RSIIndicator(data[col], window=window).rsi()
            else:
                new_data[name] = ta.momentum.RSIIndicator(data[col], window=window).rsi()

        if inplace == True:
            return data
        else:
            return new_data


    def money_flow_index(self,window = 14,tickers=[],suffix='mfi',inplace = True):

        data = self.data
        new_data = pd.DataFrame()

        for i in tickers:

            high_column = i + "_" + "High"
            low_column = i + "_" + "Low"
            close_column = i + "_" + "Close"
            volume_column = i + "_" + "Volume"

            name = self.create_suffix(i,suffix)
            if inplace == True:
                data[name] =  ta.volume.money_flow_index(data[high_column],data[low_column],data[close_column],data[volume_column],window=window)
            else:
                new_data[name] = ta.volume.money_flow_index(data[high_column],data[low_column],data[close_column],data[volume_column],window=window)

        if inplace == True:
            return data
        else:
            return new_data
        

    def acc_dist_index(self,tickers=[],suffix='adi',inplace = True):

        data = self.data
        new_data = pd.DataFrame()

        for i in tickers:

            high_column = i + "_" + "High"
            low_column = i + "_" + "Low"
            close_column = i + "_" + "Close"
            volume_column = i + "_" + "Volume"

            name = self.create_suffix(i,suffix)
            if inplace == True:
                data[name] =  ta.volume.acc_dist_index(data[high_column],data[low_column],data[close_column],data[volume_column])
            else:
               new_data[name] = ta.volume.acc_dist_index(data[high_column],data[low_column],data[close_column],data[volume_column])

        if inplace == True:
            return data
        else:
            return new_data
        
    def volume_price_trend(self,tickers=[],suffix='vpt',inplace = True):

        data = self.data
        new_data = pd.DataFrame()

        for i in tickers:

            close_column = i + "_" + "Close"
            volume_column = i + "_" + "Volume"

            name = self.create_suffix(i,suffix)
            if inplace == True:
                data[name] =  ta.volume.volume_price_trend(data[close_column],data[volume_column])
            else:
               new_data[name] = ta.volume.volume_price_trend(data[close_column],data[volume_column])

        if inplace == True:
            return data
        else:
            return new_data
        

    def average_true_range(self,window = 14,tickers=[],suffix='atr',inplace = True):

        data = self.data
        new_data = pd.DataFrame()

        for i in tickers:

            high_column = i + "_" + "High"
            low_column = i + "_" + "Low"
            close_column = i + "_" + "Close"

            name = self.create_suffix(i,suffix)
            if inplace == True:
                data[name] =  ta.volatility.average_true_range(data[high_column],data[low_column],data[close_column],window=window)
            else:
               new_data[name] = ta.volatility.average_true_range(data[high_column],data[low_column],data[close_column],window=window)

        if inplace == True:
            return data
        else:
            return new_data
        
    

    def bollinger_mavg(self,window = 14,columns=[],suffix='bmavg',inplace = True):

        data = self.data
        new_data = pd.DataFrame()
        
        for col in columns:
            name = self.create_suffix(col,suffix)
            if inplace == True:
                data[name] = ta.volatility.bollinger_mavg(data[col], window=window)
            else:
                new_data[name] = ta.volatility.bollinger_mavg(data[col], window=window)
        if inplace == True:
            return data
        else:
            return new_data
        
    def average_directional_movement_index(self,window=14,tickers=[],suffix='adx',inplace=True):

        data = self.data
        new_data = pd.DataFrame()

        for i in tickers:

            high_column = i + "_" + "High"
            low_column = i + "_" + "Low"
            close_column = i + "_" + "Close"

            name = self.create_suffix(i,suffix)
            if inplace == True:
                data[name] =  ta.trend.adx(data[high_column],data[low_column],data[close_column],window=window)
            else:
               new_data[name] = ta.trend.adx(data[high_column],data[low_column],data[close_column],window=window)

        if inplace == True:
            return data
        else:
            return new_data

    def exponational_moving_average(self,window = 14,columns=[],suffix='ema',inplace = True):

        data = self.data
        new_data = pd.DataFrame()

        for col in columns:
            name = self.create_suffix(col,suffix)
            if inplace == True:
                data[name] = ta.trend.ema_indicator(data[col], window=window)
            else:
                new_data[name] = ta.trend.ema_indicator(data[col], window=window)
        if inplace == True:
            return data
        else:
            return new_data
        
    def log_return(self,columns=[],suffix="logrtn",inplace=True):

        data = self.data
        new_data = pd.DataFrame()

        for col in columns:
            name = self.create_suffix(col,suffix)
            if inplace == True:
                data[name] = ta.others.daily_log_return(data[col])
            else:
                new_data[name] = ta.others.daily_log_return(data[col])
                
        if inplace == True:
            return data
        else:
            return new_data
        