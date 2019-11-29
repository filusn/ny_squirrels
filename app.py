import streamlit as st
import pandas as pd
import numpy as np

st.title('Central Park Squirrel Census')

data = pd.read_csv(r'data\2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv')
st.write(data.head())
st.write(data.columns)
st.write(data.describe())
st.write(len(data['Unique Squirrel ID'].unique()))

data['Primary Fur Color'] = data['Primary Fur Color'].fillna('Unknown')
primary_fur_colors = data['Primary Fur Color'].unique()

option = st.selectbox(
    'Pick a squirrel color',
    sorted(primary_fur_colors)
)
'You selected: ', option

map_data = data.loc[data['Primary Fur Color'] == str(option)]
map_data = map_data[['X', 'Y']][:10]
map_data.columns = ['lon', 'lat']

st.map(map_data)

st.write(data['Primary Fur Color'].value_counts())