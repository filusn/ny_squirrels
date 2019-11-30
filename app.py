import streamlit as st
import pandas as pd
import numpy as np
import arrow
import altair as alt

st.title('Central Park Squirrel Census')
'Short analysis and visualisation of Central Park squirrels data.'

"""
### Number of squirrels
"""
data = pd.read_csv(r'data\2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv')
st.write(data.head())
st.write(f'The dataset contains {str(len(data))} records of \
    {str(len(data["Unique Squirrel ID"].unique()))} unique squirrel sightings.')


"""
### Squirrels on hectares
"""
st.write('In our data Central Park is divided into hectare grid and numbered from \
    \'01A\' to \'42I\' with numerical axis running north-to-south and alphabetical \
    running east-to-west. Squirrels sightings from dataset take place only on \
    339 of 378 (350 \'countable\') of these hectares.')

squirrels_per_hectare = data['Hectare'].value_counts()
max_squirrels_hec = squirrels_per_hectare.index[0]
max_squirrels_hec_nr = squirrels_per_hectare[0]
min_squirrels_hec = squirrels_per_hectare.index[-1]
min_squirrels_hec_nr = squirrels_per_hectare[-1]
st.write(f'Most squirrels were seen on hectare number {max_squirrels_hec} - \
    {max_squirrels_hec_nr}. Least squirrels were on hectare {min_squirrels_hec} - \
    {min_squirrels_hec_nr}.')


"""
### Time of squirrels sightings
"""
st.write(f'Squirrels were seen more in the afternoons - \
    {len(data.loc[data["Shift"] == "PM"])} times. In the mornings shift there were \
    {len(data.loc[data["Shift"] == "AM"])} sightings.')

data['Normal Date'] = [f'{str(x)[-4:]}-{str(x)[:2]}-{str(x)[2:4]}' for x in data['Date']]
date_counts = pd.DataFrame(data['Normal Date'].value_counts())
date_counts['Counts'] = date_counts.index

date_chart = alt.Chart(date_counts).mark_bar().encode(
    x='Counts',  
    y='Normal Date',
)
st.altair_chart(date_chart, width=-1)


"""
### Age of the squirrels
"""
data['Age'].replace('?', 'Unknown', inplace=True)
data['Age'].fillna('Unknown', inplace=True)
age_counts = data['Age'].value_counts().reset_index()

age_chart = alt.Chart(age_counts).mark_bar().encode(
    x='Age',
    y='index'
)
st.altair_chart(age_chart, width=-1)
st.write('It is difficult to define squirrel age, just by looking at it. This is the reason there is a lot of unknown values.')


"""
### Fur colors
"""
st.write(data['Primary Fur Color'].unique())
st.write(data['Highlight Fur Color'].unique())

color_chart = alt.Chart(data[['Primary Fur Color', 'Highlight Fur Color']]).mark_bar().encode(
    x=alt.X('Primary Fur Color'),
    y='count()',
)
st.altair_chart(color_chart, width=-1)



# DO MAPY:
# - slider z datą
# st.write(data['Date'].value_counts())
# add_checkbox = st.sidebar.checkbox(
    # 'Choose a shift of '
# )

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

# map_data = data.loc[data['Primary Fur Color'] == str(option)]
map_data = data.loc[data['Hectare'] == '01E']
map_data = map_data[['X', 'Y']]
map_data.columns = ['lon', 'lat']

st.map(map_data)

st.write(data['Primary Fur Color'].value_counts())