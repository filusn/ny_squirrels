import streamlit as st
import pandas as pd
import altair as alt


data = pd.read_csv(r"data\2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
ny_opendata = "(https://data.cityofnewyork.us/Environment/2018-Central-Park-Squirrel-Census-Squirrel-Data/vfnx-vebw)"

st.title("Central Park Squirrel Census")
st.markdown(
    f"Short analysis and visualisation of [Central Park squirrels data]{ny_opendata} made to try out the Streamlit."
)


"""
### Number of squirrels
"""
st.write(
    f'The dataset contains {str(len(data))} records of \
    {str(len(data["Unique Squirrel ID"].unique()))} unique squirrel sightings.'
)


"""
### Squirrels on hectares
"""
st.write(
    "In our data Central Park is divided into hectare grid and numbered from '01A' to '42I' with numerical axis running north-to-south and alphabetical running east-to-west. Squirrels sightings from dataset take place only on 339 of 378 (350 'countable') of these hectares."
)

squirrels_per_hectare = data["Hectare"].value_counts()
max_squirrels_hec = squirrels_per_hectare.index[0]
max_squirrels_hec_nr = squirrels_per_hectare[0]
min_squirrels_hec = squirrels_per_hectare.index[-1]
min_squirrels_hec_nr = squirrels_per_hectare[-1]
st.write(
    f"Most squirrels were seen on hectare number {max_squirrels_hec} - {max_squirrels_hec_nr}. Least squirrels were on hectare {min_squirrels_hec} - {min_squirrels_hec_nr}."
)


"""
### Time of squirrels sightings
"""
st.write(
    f'Squirrels were seen more in the afternoons - {len(data.loc[data["Shift"] == "PM"])} times. In the morning shifts researchers have met the squirrels {len(data.loc[data["Shift"] == "AM"])} times.'
)

data["Normal Date"] = [f"{str(x)[-4:]}-{str(x)[:2]}-{str(x)[2:4]}" for x in data["Date"]]
date_counts = pd.DataFrame(data["Normal Date"].value_counts()).reset_index()
date_counts.columns = ["Date", "Number of squirrel meetings"]
date_chart = (
    alt.Chart(date_counts)
    .mark_bar()
    .encode(x=alt.X("Date"), y="Number of squirrel meetings",)
    .properties(title="Squirrel meetings by date", width=400, height=400)
)
st.altair_chart(date_chart, width=-1)


"""
### Age of the squirrels
"""
data["Age"].replace("?", "Unknown", inplace=True)
data["Age"].fillna("Unknown", inplace=True)
age_counts = data["Age"].value_counts().reset_index()

age_chart = (
    alt.Chart(age_counts)
    .mark_bar()
    .encode(x="Age", y="index")
    .properties(title="Squirrels by age", width=300, height=300)
)
st.altair_chart(age_chart, width=-1)
st.write(
    "It is difficult to define squirrel age, just by looking at it. This is the reason of a lot of unknown values."
)


"""
### Fur colors
"""
data["Primary Fur Color"].fillna("Unknown", inplace=True)
data["Highlight Fur Color"].fillna("Unknown", inplace=True)

primary_color_scale = alt.Scale(
    domain=["Black", "Cinnamon", "Gray", "Unknown"],
    range=["black", "#D2691E", "gray", "blue"],
)
primary_color_chart = (
    alt.Chart(data)
    .mark_bar()
    .encode(
        x=alt.X("Primary Fur Color"),
        y="count()",
        color=alt.Color("Primary Fur Color", scale=primary_color_scale, legend=None),
    )
    .properties(title="Squirrels by primary fur color", height=250, width=250)
)
high_color_chart = (
    alt.Chart(data)
    .mark_bar()
    .encode(x=alt.X("Highlight Fur Color"), y="count()")
    .properties(title="Squirrels by highlight fur color", height=250, width=250)
)
st.altair_chart(primary_color_chart | high_color_chart, width=-1)


"""
### Squirrel activity
"""
# All activity
activity_data = (
    data[["Running", "Chasing", "Climbing", "Eating", "Foraging"]].sum().reset_index()
)
activity_data.columns = ["Activity", "Count"]
activity_chart = (
    alt.Chart(activity_data)
    .mark_bar()
    .encode(x="Activity:O", y="Count:Q")
    .properties(height=250, width=180)
)

# Activity by shift
activity_by_shift = data.groupby("Shift")[
    ["Running", "Chasing", "Climbing", "Eating", "Foraging"]
].sum()
activity_by_shift = activity_by_shift.reset_index()
activity_by_shift = activity_by_shift.melt(
    "Shift", var_name="Activity", value_name="Count"
)

activity_shifts_chart = (
    alt.Chart(activity_by_shift)
    .mark_bar()
    .encode(x=alt.X("Activity:N"), y="Count", column="Shift:N")
    .properties(title="Squirrel's activity", width=180, height=250)
)
st.altair_chart(activity_chart | activity_shifts_chart, width=-1)

# Are young squirrels foraging more often?
foraging_data = data.groupby("Age")["Foraging"].value_counts().reset_index(level=0)
foraging_data.columns = ["Age", "Foraging Counts"]
foraging_data.reset_index(inplace=True)
foraging_data["Foraging"] = [
    "foraging" if value == 1 else "not foraging" for value in foraging_data["Foraging"]
]

"Let's check if young squirrels are more likely to forage for food"
foraging_age_chart = (
    alt.Chart(foraging_data)
    .mark_bar()
    .encode(
        x=alt.X("sum(Foraging Counts)", stack="normalize", axis=alt.Axis(format="%")),
        y="Age",
        color="Foraging",
    )
    .properties(width=300, height=300)
)
st.altair_chart(foraging_age_chart, width=-1)
"It's really interesting what we see in the chart above. In the observed squirrel meetings, the squirrel adults far often beg for food. The reason for this is probably that the young squirrels have not learned yet, that people can feed them and are more afraid of humans. Obviously, we don't have enough records to be sure, so let's leave that to squirrel researchers."


"""
### Map of squirrels
"""
"You might need to get API token"
# FILTERS
filters = st.sidebar.markdown("### Map filters")
date_selectbox = st.sidebar.selectbox(
    "Date", ["All dates"] + sorted(data["Normal Date"].unique())
)
shifts = st.sidebar.markdown("Day-shifts")
shift_am_checkbox = st.sidebar.checkbox("AM", True)
shift_pm_checkbox = st.sidebar.checkbox("PM", True)
checked_shifts = list()
if shift_am_checkbox:
    checked_shifts.append("AM")
if shift_pm_checkbox:
    checked_shifts.append("PM")

age = st.sidebar.markdown("Age of the squirrels")
age_checkbox_adult = st.sidebar.checkbox("Adult", True)
age_checkbox_juvenile = st.sidebar.checkbox("Juvenile", True)
age_checkbox_unknown = st.sidebar.checkbox("Unknown", True, key="unknown_age")
checked_ages = [
    age
    for age, is_checked in dict(
        Adult=age_checkbox_adult,
        Juvenile=age_checkbox_juvenile,
        Unknown=age_checkbox_unknown,
    ).items()
    if is_checked
]

colors = st.sidebar.markdown("Fur colors")
color_black = st.sidebar.checkbox("Black", True)
color_cin = st.sidebar.checkbox("Cinnamon", True)
color_gray = st.sidebar.checkbox("Gray", True)
color_unknown = st.sidebar.checkbox("Unknown", True, key="unknown_color")
checked_colors = [
    color
    for color, is_checked in dict(
        Black=color_black, Cinnamon=color_cin, Gray=color_gray, Unknown=color_unknown
    ).items()
    if is_checked
]

activity = st.sidebar.markdown("Activity")
activity_chasing = st.sidebar.checkbox("Chasing", False)
activity_climbing = st.sidebar.checkbox("Climbing", False)
activity_eating = st.sidebar.checkbox("Eating", False)
activity_foraging = st.sidebar.checkbox("Foraging", False)
activity_running = st.sidebar.checkbox("Running", False)

# DATA FILTERING
map_data = (
    data.loc[data["Normal Date"] == date_selectbox]
    if date_selectbox != "All dates"
    else data
)
map_data = map_data.loc[map_data["Shift"].isin(checked_shifts)]
map_data = map_data.loc[map_data["Primary Fur Color"].isin(checked_colors)]
map_data = map_data.loc[map_data["Age"].isin(checked_ages)]

if activity_chasing:
    map_data = map_data.loc[map_data["Chasing"] == 1]
if activity_climbing:
    map_data = map_data.loc[map_data["Climbing"] == 1]
if activity_eating:
    map_data = map_data.loc[map_data["Eating"] == 1]
if activity_foraging:
    map_data = map_data.loc[map_data["Foraging"] == 1]
if activity_running:
    map_data = map_data.loc[map_data["Running"] == 1]

default_value = 10 if len(map_data) >= 10 else len(map_data)
squirrels_number_slider = st.sidebar.slider(
    "Number of squirrels", min_value=0, max_value=len(map_data), value=default_value
)

# DRAW THE MAP
map_data = map_data[["X", "Y"]]
map_data.columns = ["lon", "lat"]
st.map(map_data, zoom=12)
