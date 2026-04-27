 import pandas as pd
import streamlit as st

# This caches the data loading function!
@st.cache_data
def load_country_data(country_name):
    """Loads a single country's cleaned CSV given its name."""
    # Adjust the path to your data file
    file_path = f'data/{country_name}_clean.csv'
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        return None

def load_all_data():
    """Loads all five datasets, merges them, and adds a 'Country' column."""
    countries = ['ethiopia', 'kenya', 'sudan', 'tanzania', 'nigeria']
    all_dfs = []
    for country in countries:
        df = load_country_data(country)
        if df is not None:
            # Convert Year and DOY to datetime and extract Year
            df['Date'] = pd.to_datetime(df['YEAR'].astype(str) + df['DOY'].astype(str).str.zfill(3), format='%Y%j', errors='coerce')
            df['Year'] = df['Date'].dt.year
            df['Month'] = df['Date'].dt.month
            df['Country'] = country.capitalize()
            all_dfs.append(df)
        else:
            st.warning(f"Could not load data for {country}.")

    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    else:
        return pd.DataFrame()

def filter_data(df, countries, year_range):
    """Filters data based on selected countries and year range."""
    if df.empty:
        return df
    filtered_df = df[df['Country'].isin(countries)]
    filtered_df = filtered_df[(filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])]
    return filtered_df
