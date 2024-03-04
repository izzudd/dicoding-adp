import streamlit as st
import pandas as pd
import os

from pandas.api.types import CategoricalDtype

def prepare_dataset():
  df = pd.read_csv(os.path.join(os.getcwd(), 'dashboard', 'main_data.csv'))
  cat_weekday = CategoricalDtype(categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
  cat_season = CategoricalDtype(categories=['winter', 'spring', 'summer', 'fall'], ordered=True)
  cat_month = CategoricalDtype(categories=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)
  clean_df = df.copy()
  clean_df['dteday'] = pd.to_datetime(df['dteday'])
  clean_df['yr'] = clean_df['dteday'].dt.year

  clean_df['mnth'] = clean_df['dteday'].dt.month_name().astype(cat_month)
  clean_df['weekday'] = clean_df['dteday'].dt.day_name().astype(cat_weekday)
  clean_df['season'] = clean_df['season'].map({1:'winter', 2:'spring', 3:'summer', 4:'fall'}).astype(cat_season)

  clean_df['holiday'] = clean_df['holiday'].astype(bool)
  clean_df['workingday'] = clean_df['workingday'].astype(bool)

  clean_df['temp'] = clean_df['temp'] * (39 + 8) - 8
  clean_df['atemp'] = clean_df['atemp'] * (50+16) - 16
  clean_df['windspeed'] = clean_df['windspeed'] * 67
  clean_df['hum'] = clean_df['hum'] * 100

  return clean_df

dataset = prepare_dataset()

from daily_rides import daily_rides
from hourly_rides import hourly_rides
from seasonal_scatter import seasonal_scatter
from alltime_stats import alltime_stats

st.write("""
# Bike Sharing Dataset Dashboard 🚀

- **Name:** Rahmatulloh Daffa Izzuddin Wahid
- **Dicoding ID:** zudd_in
""")

st.divider()
alltime_stats(dataset)
st.divider()
daily_rides(dataset)
st.divider()
hourly_rides(dataset)
st.divider()
seasonal_scatter(dataset)
