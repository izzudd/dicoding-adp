import streamlit as st
import plotly.express as px

def daily_rides(dataset):
  all_day_cnt = dataset.groupby('dteday')[['casual', 'registered', 'cnt']].sum().reset_index()
  
  min_date = dataset['dteday'].min()
  max_date = dataset['dteday'].max()
  start_date, end_date = min_date, max_date
  
  col1, col2 = st.columns(2)
  st.subheader('Total daily rides 🎯')
  
  col1, col2, col3 = st.columns(3)
  with col3:
    start_date, end_date = st.date_input(
      'Range',
      min_value=min_date,
      max_value=max_date,
      value=[min_date, max_date]
    )
    filtered_day = all_day_cnt[(all_day_cnt['dteday'] <= str(end_date)) & (all_day_cnt['dteday'] >= str(start_date))].rename(columns={
      'dteday': 'date',
      'cnt': 'total'
    })
  with col1:
    st.metric('Total', filtered_day['total'].sum())
  with col2:
    st.metric('Daily Avg.', round(filtered_day['total'].mean(), 2))
  
  plot = px.line(filtered_day, x='date', y=['casual', 'registered', 'total'])

  st.plotly_chart(plot)