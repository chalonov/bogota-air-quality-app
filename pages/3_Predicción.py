import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.metrics import mean_squared_error
color_pal = sns.color_palette()

st.set_page_config(
    page_title="Predicción PM - Bogotá Air Quality",
    page_icon="⛅",
)

st.write("""
#  Predicción de la calidad de aire en Bogotá
Material particulado PM10 y PM2.5
""")

st.markdown(
    """
    Se utiliza un modelo de árbol de decisión XGBoost para predecir la concentración de PM10 y PM2.5
    """
)

# DATOS
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

#fig, ax = plt.subplots(figsize=(12, 6))
#train.plot(ax=ax, label='Training Set', title='Data Train/Test Split')
#test.plot(ax=ax, label='Test Set')
#ax.legend(['Training Set', 'Test Set'])
#st.pyplot(fig)

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

test['prediction'] = reg.predict(X_test)
df = df.merge(test[['prediction']], how='left', left_index=True, right_index=True)

ax = df.loc[(df.index > '06-01-2023 ') & (df.index < '06-14-2023')][station_pm10].plot(figsize=(12, 6), title='Últimos 15 días')
df.loc[(df.index > '06-01-2023') & (df.index < '06-14-2023')]['prediction'].plot(style='--')
plt.xlabel("días");
plt.ylabel("$ \mu g /m^3$");
plt.legend(['Datos reales','Predicción'])
plt.grid()
st.pyplot(plt)