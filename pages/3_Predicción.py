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

fig, ax = plt.subplots(figsize=(12, 6))
train.plot(ax=ax, label='Training Set', title='Data Train/Test Split')
test.plot(ax=ax, label='Test Set')
ax.legend(['Training Set', 'Test Set'])
st.pyplot(fig)
