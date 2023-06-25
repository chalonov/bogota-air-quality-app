import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.metrics import mean_squared_error
color_pal = sns.color_palette()

df = pd.read_csv("data/AirQuality_Bogota_Estaciones_20210101_20230614.csv", sep = ";", decimal = ',')
df["datetime"] = pd.date_range('2021-01-01 01:00:00', periods=len(df), freq='H')
df["month"] = df["datetime"].dt.month

df_mean = df.fillna(df.mean())
df_mean.isna().sum()

# Modificar estacion y periodo a analizar
#--------------------------------------
station = 'fontibon' 
date_to_train = '01-01-2023'
#--------------------------------------

station_pm10 = station + '_pm10'
station_pm25 =  station + '_pm2.5'
df = df_mean[['datetime', station_pm10, station_pm25]]
df = df.set_index('datetime')
df.index = pd.to_datetime(df.index)

train = df.loc[df.index < date_to_train]
test = df.loc[df.index >= date_to_train]

#fig, ax = plt.subplots(figsize=(14, 5))
#train.plot(ax=ax, label='Training Set', title='Data Train/Test Split')
#test.plot(ax=ax, label='Test Set')
#ax.legend(['Training Set', 'Test Set'])
#plt.show()

def create_features(df):
    """
    Create time series features based on time series index.
    """
    df = df.copy()
    df['hour'] = df.index.hour
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day
    df['weekofyear'] = df.index.isocalendar().week
    return df

df = create_features(df)

train = create_features(train)
test = create_features(test)

FEATURES = ['dayofyear', 'hour', 'dayofweek', 'quarter', 'month', station_pm25]
TARGET = station_pm10

X_train = train[FEATURES]
y_train = train[TARGET]

X_test = test[FEATURES]
y_test = test[TARGET]

reg = xgb.XGBRegressor(base_score=0.5, booster='gbtree',    
                       n_estimators=1000,
                       early_stopping_rounds=50,
                       objective='reg:linear',
                       max_depth=3,
                       learning_rate=0.01)
reg.fit(X_train, y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)],
        verbose=100)
# Feature importance
#fi = pd.DataFrame(data=reg.feature_importances_,
#             index=reg.feature_names_in_,
#             columns=['importance'])
#fi.sort_values('importance').plot(kind='barh', title='Feature Importance')
#plt.grid()
#plt.show()

test['prediction'] = reg.predict(X_test)
df = df.merge(test[['prediction']], how='left', left_index=True, right_index=True)

#ax = df.loc[(df.index > '06-01-2023 ') & (df.index < '06-15-2023')][station_pm10].plot(figsize=(15, 5), title='Últimos 15 dias')
#df.loc[(df.index > '06-01-2023') & (df.index < '06-15-2023')]['prediction'].plot(style='--')
#plt.legend(['Truth Data','Prediction'])
#plt.grid()
#plt.show()

score = np.sqrt(mean_squared_error(test[station_pm10], test['prediction']))
print(f'RMSE Score on Test set: {score:0.2f}')

test['error'] = np.abs(test[TARGET] - test['prediction'])
test['date'] = test.index.date
test.groupby(['date'])['error'].mean().sort_values(ascending=False).head(10)

# Store data (serialize)
with open('pickle/model_' + station_pm10, 'wb') as handle:
    pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('pickle/score_' + station_pm10, 'wb') as handle:
    pickle.dump(score, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('pickle/reg_' + station_pm10, 'wb') as handle:
    pickle.dump(reg, handle, protocol=pickle.HIGHEST_PROTOCOL)