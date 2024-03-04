import streamlit as st
import plotly.graph_objects as go


def alltime_stats(dataset):
  dataset = dataset[['dteday', 'mnth', 'yr', 'cnt', 'season']]
  
  st.subheader('All Time Stats 📈')
  
  daily = dataset.groupby('dteday')['cnt'].sum().reset_index()
  monthly = dataset.groupby(['mnth', 'yr'])['cnt'].sum().reset_index()
  seasonal = dataset.groupby(['season', 'yr'])['cnt'].sum().reset_index()
  
  col1, col2, col3 = st.columns(3)
  with col1:
    busy_day = daily[daily['cnt'] == daily['cnt'].max()].iloc[0]
    st.metric(f"Most Busy Day ({busy_day['cnt']} bikes rode)", busy_day['dteday'].strftime('%d %b %Y'))
  with col2:
    busy_month = monthly[monthly['cnt'] == monthly['cnt'].max()].iloc[0]
    st.metric(f"Most Busy Month ({busy_month['cnt'] // 1000}k bikes rode)", f"{busy_month['mnth']:.3s} {busy_month['yr']}")
  with col3:
    busy_season = seasonal[seasonal['cnt'] == seasonal['cnt'].max()].iloc[0]
    st.metric(f"Most Busy Season ({busy_season['cnt'] // 1000}k bikes rode)", f"{busy_season['season'].title()} {busy_season['yr']}")
    
  col1, col2, col3 = st.columns(3)
  with col1:
    slow_day = daily[daily['cnt'] == daily['cnt'].min()].iloc[-1]
    st.metric(f"Slowest Day ({slow_day['cnt']} bikes rode)", slow_day['dteday'].strftime('%d %b %Y'))
  with col2:
    slow_month = monthly[monthly['cnt'] == monthly['cnt'].min()].iloc[-1]
    st.metric(f"Slowest Month ({slow_month['cnt'] // 1000}k bikes rode)", f"{slow_month['mnth']:.3s} {slow_month['yr']}")
  with col3:
    slow_season = seasonal[seasonal['cnt'] == seasonal['cnt'].min()].iloc[-1]
    st.metric(f"Slowest Season ({slow_season['cnt'] // 1000}k bikes rode)", f"{slow_season['season'].title()} {slow_season['yr']}")