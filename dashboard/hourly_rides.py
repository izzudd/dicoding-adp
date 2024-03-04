import streamlit as st
import plotly.express as px

def hourly_rides(dataset):
  all_day_cnt = dataset[['dteday', 'hr', 'casual', 'registered', 'cnt', 'temp', 'hum', 'windspeed']]
  
  min_date = dataset['dteday'].min()
  max_date = dataset['dteday'].max()
  
  col1, col2 = st.columns(2)
  with col1:
    st.subheader('Daily rides 🚲')
  with col2:
    date = st.date_input(
      'Date',
      min_value=min_date,
      max_value=max_date,
      value=min_date
    )

  filtered_day = all_day_cnt[all_day_cnt['dteday'] == str(date)]
  melted_filtered_day = filtered_day[['hr', 'casual', 'registered', 'cnt']].rename(columns={
    'hr': 'time (24 hour)',
    'cnt': 'total',
  })
  
  plot = px.line(melted_filtered_day, x='time (24 hour)', y=['casual', 'registered', 'total'])

  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric('Total registered', filtered_day['registered'].sum())
    st.metric('Avg. Temperature (°C)', round(filtered_day['temp'].mean(), 2))
  with col2:
    st.metric('Total casual', filtered_day['casual'].sum())
    st.metric('Avg. Humidity (%)', round(filtered_day['hum'].mean(), 2))
  with col3:
    st.metric('Total all', filtered_day['cnt'].sum())
    st.metric('Avg. Windspeed (knot)', round(filtered_day['windspeed'].mean(), 2))
    
  st.plotly_chart(plot)