import streamlit as st
import plotly.express as px

def seasonal_scatter(dataset):
  all_day_cnt = dataset[['cnt', 'temp', 'hum', 'windspeed', 'season']].rename(columns={
    'cnt': 'bike rides',
    'temp': 'temperature',
    'hum': 'humidity'
  })
  
  col1, col2 = st.columns(2)
  with col1:
    st.subheader('Seasonal Scatter 🧨')
  with col2:
    filter_opts = st.selectbox('Influenced by', ['humidity', 'windspeed', 'temperature'], index=2)

  filtered_ds = all_day_cnt[['bike rides', 'season', filter_opts]]
  
  plot = px.scatter(filtered_ds, x=filter_opts, y='bike rides', color='season')
    
  st.plotly_chart(plot)