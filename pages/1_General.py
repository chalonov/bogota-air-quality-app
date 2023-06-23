import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Análisis General",
    page_icon="⛅",
)

st.write("""
#  Calidad de aire en Bogotá
Material particulado PM10 y PM2.5
""")

# DATOS
df = pd.read_csv("data/AirQuality_Bogota_Estaciones_20210101_20230614.csv", sep = ";", decimal = ',')
df["datetime"] = pd.date_range('2021-01-01 01:00:00', periods=len(df), freq='H')
df["month"] = df["datetime"].dt.month

stations_keys = ["Bolivia", "Carvajal - Sevillana", "CAR", "Colina", "Fontibón", "Guaymaral",
                 "Kennedy", "Las Ferias", "M.Ambiente", "Mov.Fontibón", "P.Aranda", "S.Cristobal",
                 "Suba", "Tunal", "Usaquen"]


st.header("Estaciones de la ciudad")

fig, axs = plt.subplots(figsize=(12, 6))
df.groupby(df["datetime"].dt.hour)["bolivia_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
df.groupby(df["datetime"].dt.hour)["carvajal_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
df.groupby(df["datetime"].dt.hour)["car_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
df.groupby(df["datetime"].dt.hour)["colina_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
df.groupby(df["datetime"].dt.hour)["fontibon_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
df.groupby(df["datetime"].dt.hour)["guaymaral_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
df.groupby(df["datetime"].dt.hour)["kennedy_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
df.groupby(df["datetime"].dt.hour)["lasferias_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
df.groupby(df["datetime"].dt.hour)["mambiente_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
df.groupby(df["datetime"].dt.hour)["mfontibon_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
df.groupby(df["datetime"].dt.hour)["paranda_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
df.groupby(df["datetime"].dt.hour)["sancristobal_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
df.groupby(df["datetime"].dt.hour)["suba_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
df.groupby(df["datetime"].dt.hour)["tunal_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
df.groupby(df["datetime"].dt.hour)["usaquen_pm2.5"].mean().plot(style="-o", rot=0, ax=axs)
plt.title('Media PM2.5 por cada hora del dia [enero 2021 - junio 2023]')
plt.xlabel("Hora del dia");
plt.ylabel("$ \mu g /m^3$");
plt.legend(stations_keys, bbox_to_anchor = (1.21, 0.6), loc='center right')
plt.xticks(range(0, 24, 1))
plt.grid()
st.pyplot(fig)