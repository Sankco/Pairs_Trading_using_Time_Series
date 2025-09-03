import numpy as np
import pandas as pd
import statsmodels.api as sm
from pydmd import HODMD
from pydmd.preprocessing import hankel_preprocessing

class PredictionModeling:

    def __init__(self,data,column_name,test_size=0.40,forcast_period=2):
        self.data = data.copy()
        self.base_column = column_name
        self.forcast_period = forcast_period
        self.train_end_index = int(len(data[column_name])*(1-test_size))
        self.add_actual_forecast_values()
        self.add_actual_forecast()
        self.add_actual_forecast_mean()

    def add_actual_forecast(self):
        column_name = self.base_column + "_" + "Actual_value" + f"_fore_perod_{self.forcast_period}"
        self.data[column_name] = self.data[self.base_column].shift(-self.forcast_period)

    def add_actual_forecast_mean(self):
        column_name = self.base_column + "_" + "Actual_mean" + f"_fore_perod_{self.forcast_period}"
        def custom_rolling_mean(window):
            return window.mean()
        indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=self.forcast_period)
        self.data[column_name] = self.data[self.base_column].shift(-1).rolling(window=indexer).apply(custom_rolling_mean)

    def add_actual_forecast_values(self):
        column_name = self.base_column + "_" + "Actual" + f"_fore_perod_{self.forcast_period}"
        self.data[column_name] = [self.data[self.base_column].iloc[i+1:i+1+self.forcast_period].tolist() for i in range(len(self.data) - self.forcast_period + 1)] + [[]] * (self.forcast_period - 1)
     
    def add_arima_forecast(self,column,order=(1,1,0)):
        
        self.ARIMA_forecast_value = []
        self.ARIMA_forecast_values = []
        train_end_index = self.train_end_index
        for i in range(train_end_index, len(self.data[column])):
            forecast_value,forecast_values= self.arima_prediciton(self.data[column].iloc[:i],order)
            self.ARIMA_forecast_value.append(forecast_value)
            self.ARIMA_forecast_values.append(list(forecast_values))
        self.data[f"{column}_ARIMA_forecast_{self.forcast_period}"]  =  np.NaN
        self.data[f"{column}_ARIMA_forecasts_{self.forcast_period}"] = np.NaN

        self.data[f"{column}_ARIMA_forecast_{self.forcast_period}"].iloc[train_end_index:] = self.ARIMA_forecast_value
        self.data[f"{column}_ARIMA_forecasts_{self.forcast_period}"] = self.data[f"{column}_ARIMA_forecasts_{self.forcast_period}"].astype(object)
        self.data[f"{column}_ARIMA_forecasts_{self.forcast_period}"].iloc[train_end_index:]= self.ARIMA_forecast_values
 
    def arima_prediciton(self,train_data,order):
        model = sm.tsa.arima.ARIMA(train_data, order=order)
        model_fit = model.fit()
        forcecast_values = np.array((model_fit.forecast(steps=self.forcast_period)))
        forecast_value = forcecast_values[-1]
        return forecast_value,forcecast_values
    

    def add_dmd_forecast(self,column,svd_rank=0,hanckel_d=5):

        self.DMD_forecast_value = []
        self.DMD_forecast_values = []
        train_end_index = self.train_end_index
        for i in range(train_end_index, len(self.data[column])):
            train_data = self.data[column].iloc[:i].values
            train_data = train_data.transpose()
            forecast_value,forecast_values= self.hodmd_predict(train_data,d=len(train_data),svd_rank = svd_rank,hankel_d=hanckel_d)
            self.DMD_forecast_value.append(forecast_value)
            self.DMD_forecast_values.append(list(forecast_values))
            
        self.data[f"{column}_DMD_forecast_{self.forcast_period}"]  =  np.NaN
        self.data[f"{column}_DMD_forecasts_{self.forcast_period}"] = np.NaN

        self.data[f"{column}_DMD_forecast_{self.forcast_period}"].iloc[train_end_index:] = self.DMD_forecast_value

        self.data[f"{column}_DMD_forecasts_{self.forcast_period}"] = self.data[f"{column}_DMD_forecasts_{self.forcast_period}"].astype(object)
        self.data[f"{column}_DMD_forecasts_{self.forcast_period}"].iloc[train_end_index:]= self.DMD_forecast_values
   
    def hodmd_predict(self,dmd_data,d=None,svd_rank=None,hankel_d=None):
    
        hodmd = HODMD(svd_rank=svd_rank, exact=False, opt=True,d=d-150)
        hodmd = hankel_preprocessing(hodmd, d=hankel_d)
        hodmd.fit(dmd_data[None])
        x = np.arange(0,len(dmd_data))
        hodmd.original_time["dt"] = hodmd.dmd_time["dt"] = x[1] - x[0]
        hodmd.original_time["t0"] = hodmd.dmd_time["t0"] = x[0]
        hodmd.original_time["tend"] = hodmd.dmd_time["tend"] = x[-1]
        hodmd.dmd_time["tend"] = x[-1]+ self.forcast_period
        forcecast_values = hodmd.reconstructed_data.real[0,-self.forcast_period:]
        forecast_value = forcecast_values[-1]
        return forecast_value,forcecast_values
        
