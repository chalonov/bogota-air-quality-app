import pickle
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

#  create dictionary for stations
stations_keys = ["Bolivia", "Carvajal - Sevillana", "CAR", "Colina", "Fontibón", "Guaymaral",
                 "Kennedy", "Las Ferias", "M.Ambiente", "Mov.Fontibón", "P.Aranda", "S.Cristobal",
                 "Suba", "Tunal", "Usaquen"]
stations_values = ["bolivia", "carvajal", "car", "colina", "fontibon", "guaymaral", 
                   "kennedy", "lasferias", "mambiente", "mfontibón", "paranda", "sancristobal",
                   "suba", "tunal", "usaquen"]

stations = dict(zip(stations_keys, stations_values))
station_to_view = st.sidebar.selectbox(
    "Escoja la estación a predecir",
    (stations_keys)
)

#  create dictionary for PM levels
pm_keys = ["PM2.5", "PM10"]
pm_values = ["_pm2.5", "_pm10"]

pms = dict(zip(pm_keys, pm_values))
nivel = st.sidebar.radio(
    "Nivel de concentración de PM",
    ('PM2.5', 'PM10'))

station = stations[station_to_view] + pms[nivel]

st.text(station)

if st.sidebar.button('Ejecutar'):
    # Load data (deserialize)
    with open('pickle/model_' + station, 'rb') as handle:
        df = pickle.load(handle)    

    ax = df.loc[(df.index > '06-01-2023 ') & (df.index < '06-15-2023')][station].plot(figsize=(12, 6))
    df.loc[(df.index > '06-01-2023') & (df.index < '06-15-2023')]['prediction'].plot(style='--')
    plt.title('Últimos 15 dias - ' + station_to_view)
    plt.xlabel("días")
    plt.ylabel("$ \mu g /m^3$")
    plt.legend(['Datos reales','Predicción'])
    plt.grid()
    st.pyplot(plt)

    with open('pickle/score_' + station, 'rb') as handle:
        score = pickle.load(handle)  
    
    st.text(f'RMSE Score on Test set: {score:0.2f}')