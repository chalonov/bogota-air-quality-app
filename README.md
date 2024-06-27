# Bogotá Air Quality App

## Overview

This Streamlit application analyzes and predicts air quality in Bogotá, Colombia, focusing on particulate matter concentrations (PM10 and PM2.5) across various monitoring stations in the city. The app uses XGBoost for prediction and provides visualizations for data analysis.

## Features

1. **General Analysis**: Displays PM10 and PM2.5 concentrations across all monitoring stations in Bogotá.
2. **Station-specific Analysis**: Allows users to select a specific station and view hourly, daily, weekly, and monthly air quality trends.
3. **Prediction**: Utilizes XGBoost to predict PM10 and PM2.5 levels for selected stations.

## Files in the Repository

- `Inicio.py`: The main entry point of the Streamlit app.
- `1_General.py`: Provides a general overview of air quality across all stations.
- `2_Estaciones.py`: Offers detailed analysis for individual monitoring stations.
- `3_Predicción.py`: Implements the prediction feature using XGBoost.
- `dicts.py`: Contains dictionaries for stations, PM levels, and time periods.
- `requirements.txt`: Lists all the Python dependencies required for the project.
- `utils.py`: Contains utility functions for plotting and data visualization.
- `data.py`: Handles data loading and initial preprocessing.

## How to Use

1. Install the required dependencies: `pip install -r requirements.txt`
2. Run the Streamlit app using `streamlit run Inicio.py`.
3. Navigate through different pages using the sidebar:
- General Analysis
- Station Analysis
- Prediction

4. In the General Analysis, select between PM2.5 and PM10 to view citywide data.
5. In the Station Analysis, choose a specific station and explore data across different time periods.
6. In the Prediction section, select a station and PM level to view forecasts and model performance metrics.

## Dependencies

The main dependencies for this project are:
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- XGBoost
- Scikit-learn

For a complete list of dependencies and their versions, refer to `requirements.txt`.

## Data

The app uses air quality data from various monitoring stations in Bogotá. The data is loaded and preprocessed in `data.py`. It includes hourly measurements from January 1, 2021, to June 14, 2023.

## Utilities

The `utils.py` file contains helper functions for creating various plots used throughout the application, including:
- Station plots: Visualizing PM levels across different stations
- Period plots: Showing PM trends over different time periods (hourly, daily, weekly, monthly)

## Model

The prediction feature uses XGBoost, a gradient boosting framework. The models are trained separately for each station and PM level, and their performance is evaluated using RMSE (Root Mean Square Error).

## Creator

This app was created by Gonzalo Novoa.

## Note

Make sure to have all the required dependencies installed and the necessary data files in the correct directories before running the app. The data file should be located at `data/AirQuality_Bogota_Estaciones_20210101_20230614.csv`.
