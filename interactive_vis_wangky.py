import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

st.title('Disability Status and Types among Adults Over 18 Years Old in Each State in 2020')

# Description
st.write("The visualizations below together show the percentages and types of disabilities of citizens in different states.")
st.write("The upper graph shows the percentage of any disability the top 2 disability (cognative and mobility disability) population in each state.")
st.write("The bottom bar chart presents the total percentage of each disability type in the US.")
state_pop = data.population_engineers_hurricanes()[['state', 'id', 'population']]
state_id = state_pop['id'].tolist()
state_id.pop()

dataset = 'us_disability.csv'
df = pd.read_csv(dataset)
df = df.sort_values('State')
df['id'] = state_id

# Upper Vis: geographical chart
state_map = alt.topo_feature(data.us_10m.url, feature='states')
left = alt.Chart(state_map).mark_geoshape().transform_lookup(
    lookup='id',
    from_=alt.LookupData(df, key='id',fields=['Any Disability', 'State', 'Cognitive Disability', 'Mobility Disability'])
).encode(
    color='Any Disability:Q',
    tooltip=['State:N', 'Any Disability:Q', 'Cognitive Disability:Q', 'Mobility Disability:Q']
).project(
    'albersUsa'
)

cd = sum(df['Cognitive Disability'])
hd = sum(df['Hearing Disability'])
md = sum(df['Mobility Disability'])
vd = sum(df['Vision Disability'])
sd = sum(df['Self-care Disability'])
ild = sum(df['Independent Living Disability'])

df_disablility = pd.DataFrame({'Disability':['Cognitive Disability', 'Hearing Disability',
                                            'Mobility Disability', 'Vision Disability',
                                            'Self-care Disability', 'Independent Living Disability'],
                              'Sum':[cd, hd, md, vd, sd, ild]})

# Bottom Vis: bar chart
right = alt.Chart(df_disablility).transform_window(
    sort=[alt.SortField('Sum')],
    sum_rank='rank(Sum)'
).mark_bar().encode(
    x=alt.X('Sum:Q', title='Sum of Disable Percentage'),
    y=alt.Y('Disability:N',sort=alt.EncodingSortField(field="sum_rank",order="descending")),
    color='Sum:Q',
    tooltip=[alt.Tooltip('Sum')]
)
st.altair_chart(alt.vconcat(left, right).resolve_scale(color='independent'))
