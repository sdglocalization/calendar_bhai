import streamlit as st
import pandas as pd
import numpy as np
import calendar
# import plotly.graph_objs as go

import plotly.graph_objects as go

def create_calendar(year, month):
    # Find the first and last days of the selected month
    first_day = pd.Timestamp(year, month, 1)
    last_day = (first_day + pd.DateOffset(months=1)) - pd.DateOffset(days=1)

    # Create a range of dates for the selected month
    date_range = pd.date_range(first_day, last_day)

    # Create an array to store the calendar
    cal_array = np.full((6, 7), '', dtype=object)

    # Populate the calendar array with the days of the month
    for day in date_range:
        week_number = (day.day - 1 + calendar.weekday(year, month, 1)) // 7
        cal_array[week_number, day.weekday()] = day.day

    # Create font color array
    font_color_array = np.full((6, 7), 'black', dtype=object)
    font_color_array[:, 5] = 'red'
    font_color_array[:, 6] = 'red'

    # Create the calendar table using Plotly
    trace = go.Table(
        header=dict(
            values=list(calendar.day_abbr),
            align="center",
            font=dict(size=22, color=['black']*5 + ['red']*2),
            fill_color="white",
            height=60
        ),
        cells=dict(
            values=cal_array.T,
            align="center",
            font=dict(size=19, color=font_color_array.T),
            fill_color="white",
            line_color="black",
            height=60
        )
    )

    layout = go.Layout(
        title=f"{calendar.month_name[month]} {year}",
        margin=dict(l=30, r=30, t=30, b=30),
    )

    fig = go.Figure(data=[trace], layout=layout)

    return fig

st.title("Monthly Calendar")

# Creating the widgets in the sidebar
with st.sidebar:
    st.header("Select Year and Month")
    year = st.selectbox("Select Year", list(range(2020, 2024)))
    month = st.selectbox("Select Month", list(range(1, 13)), format_func=lambda x: calendar.month_name[x])

# Call the function to create the calendar table
calendar_table = create_calendar(year, month)

# Display the calendar table
st.plotly_chart(calendar_table)
