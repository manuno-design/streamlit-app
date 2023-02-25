import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATA_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    def lowercase(x): return str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATA_COLUMN] = pd.to_datetime(data[DATA_COLUMN])
    return data


# loading data
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Done! (using st.cache_data)')

# raw data rendering
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# histogram rendering
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATA_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

# map rendering
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATA_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickup at {hour_to_filter}:00')
st.map(filtered_data)
