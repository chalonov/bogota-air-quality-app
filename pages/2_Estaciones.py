import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Análisis Estaciones",
    page_icon="⛅",
)

# DATOS
df = pd.read_csv("data/AirQuality_Bogota_Estaciones_20210101_20230614.csv", sep = ";", decimal = ',')
df["datetime"] = pd.date_range('2021-01-01 01:00:00', periods=len(df), freq='H')
df["month"] = df["datetime"].dt.month

st.write("""
#  Análisis por estaciones
Material particulado PM10 y PM2.5
""")

# st.title('Parámetros')

stations_keys = ["Bolivia", "Carvajal - Sevillana", "CAR", "Colina", "Fontibón", "Guaymaral",
                 "Kennedy", "Las Ferias", "M.Ambiente", "Mov.Fontibón", "P.Aranda", "S.Cristobal",
                 "Suba", "Tunal", "Usaquen"]
stations_values = ["bolivia", "carvajal", "car", "colina", "fontibon", "guaymaral", 
                   "kennedy", "lasferias", "mambiente", "mfontibón", "paranda", "sancristobal",
                   "suba", "tunal", "usaquen"]

#  create dictionary for stations
stations = dict(zip(stations_keys, stations_values))
station_to_view = st.selectbox(
    "Escoja la estación a analizar",
    (stations_keys)
)

tab1, tab2, tab3, tab4 = st.tabs(["Hora","Diario","Semanal","Mensual"])

with tab1:
    st.header("Estación de monitoreo: " + station_to_view)

    station = stations[station_to_view]

    station_pm10 = station + '_pm10'
    station_pm25 =  station + '_pm2.5'
    df = df[['datetime', station_pm10, station_pm25]]
    fig, axs = plt.subplots(figsize=(12, 6))
    df.groupby(df["datetime"].dt.hour)[station_pm10].mean().plot(style="-o", rot=0, ax=axs)
    df.groupby(df["datetime"].dt.hour)[station_pm25].mean().plot(style="-o", rot=0, ax=axs)
    plt.title(station_to_view + ' - Media PM por cada hora del día [enero 2021 - junio 2023] ')
    plt.xlabel("Hora del dia");
    plt.ylabel("$ \mu g /m^3$");
    plt.legend([station_to_view + ' PM10', station_to_view + ' PM2.5'])
    plt.xticks(range(0, 24, 1))
    plt.grid()
    st.pyplot(fig)

with tab2:
    st.header("Estación de monitoreo: " + station_to_view)

    station = stations[station_to_view]

    station_pm10 = station + '_pm10'
    station_pm25 =  station + '_pm2.5'
    df = df[['datetime', station_pm10, station_pm25]]
    fig, axs = plt.subplots(figsize=(12, 6))
    df.groupby(df["datetime"].dt.day)[station_pm10].mean().plot(style="-o", rot=0, ax=axs)
    df.groupby(df["datetime"].dt.day)[station_pm25].mean().plot(style="-o", rot=0, ax=axs)
    plt.title(station_to_view + ' - Media PM por cada dia del mes [enero 2021 - junio 2023] ')
    plt.xlabel("Dia del mes");
    plt.ylabel("$ \mu g /m^3$");
    plt.legend([station_to_view + ' PM10', station_to_view + ' PM2.5'])
    plt.xticks(range(1, 32, 1))
    plt.grid()
    st.pyplot(fig)

with tab3:
    st.header("Estación de monitoreo: " + station_to_view)

    station = stations[station_to_view]

    station_pm10 = station + '_pm10'
    station_pm25 =  station + '_pm2.5'
    df = df[['datetime', station_pm10, station_pm25]]
    fig, axs = plt.subplots(figsize=(12, 6))
    df.groupby(df["datetime"].dt.dayofweek)[station_pm10].mean().plot(style="-o", rot=0, ax=axs)
    df.groupby(df["datetime"].dt.dayofweek)[station_pm25].mean().plot(style="-o", rot=0, ax=axs)
    plt.title(station_to_view + ' - Media PM por cada dia de la semana [enero 2021 - junio 2023] ')
    plt.xlabel("Dia de la semana");
    plt.ylabel("$ \mu g /m^3$");
    plt.legend([station_to_view + ' PM10', station_to_view + ' PM2.5'])
    plt.grid()
    st.pyplot(fig)

with tab4:
    st.header("Estación de monitoreo: " + station_to_view)

    station = stations[station_to_view]

    station_pm10 = station + '_pm10'
    station_pm25 =  station + '_pm2.5'
    df = df[['datetime', station_pm10, station_pm25]]
    fig, axs = plt.subplots(figsize=(12, 6))
    df.groupby(df["datetime"].dt.month)[station_pm10].mean().plot(style="-o", rot=0, ax=axs)
    df.groupby(df["datetime"].dt.month)[station_pm25].mean().plot(style="-o", rot=0, ax=axs)
    plt.title(station_to_view + ' - Media PM por cada mes del año [enero 2021 - junio 2023] ')
    plt.xlabel("Mes del año");
    plt.ylabel("$ \mu g /m^3$");
    plt.legend([station_to_view + ' PM10', station_to_view + ' PM2.5'])
    plt.xticks(range(1, 13, 1))
    plt.grid()
    st.pyplot(fig)
