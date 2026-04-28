import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_all_data, filter_data

st.set_page_config(layout="wide")
st.title("🌍 Climate Analysis Dashboard: Africa's Journey to COP32")


with st.spinner("Loading data..."):
    df = load_all_data()

if not df.empty:
   
    st.sidebar.header("Configure Your View")
    all_countries = sorted(df['Country'].unique())
    selected_countries = st.sidebar.multiselect(
        "🌍 Select Countries", all_countries, default=all_countries
    )
    min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
    year_range = st.sidebar.slider(
        "📅 Select Year Range", min_year, max_year, (min_year, max_year)
    )
    
  
    filtered_df = filter_data(df, selected_countries, year_range)
    

    st.header("📈 Temperature Trends")
    temp_check = st.checkbox("Show Temperature Trends", value=True)
    if temp_check and not filtered_df.empty:
        monthly_temp = filtered_df.groupby(['Country', 'Year', 'Month'])['T2M'].mean().reset_index()
        monthly_temp['Date'] = pd.to_datetime(monthly_temp['Year'].astype(str) + '-' + monthly_temp['Month'].astype(str))
        fig, ax = plt.subplots(figsize=(12, 6))
        for country in monthly_temp['Country'].unique():
            country_data = monthly_temp[monthly_temp['Country'] == country]
            ax.plot(country_data['Date'], country_data['T2M'], label=country, linewidth=2)
        ax.set_title('Monthly Average Temperature Comparison', fontsize=16)
        ax.set_xlabel('Date'); ax.set_ylabel('Temperature (°C)')
        ax.legend(); ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    else:
        st.info("No data available for the selected filters.")
    
   
    st.header("☔ Precipitation Patterns")
    if st.checkbox("Show Precipitation Boxplot", value=True) and not filtered_df.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(data=filtered_df, x='Country', y='PRECTOTCORR', ax=ax)
        ax.set_title('Daily Precipitation Distribution by Country', fontsize=16)
        ax.set_xlabel('Country'); ax.set_ylabel('Precipitation (mm/day)')
        plt.xticks(rotation=45)
        st.pyplot(fig)
else:
    st.error("No climate data could be loaded.")