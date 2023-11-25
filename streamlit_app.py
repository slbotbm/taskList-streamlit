import streamlit as st
import pandas as pd
import numpy as np
from datetime import time, datetime

st.header("st.slider")

st.subheader("Slider")

age = st.slider("How old are you?", 0, 130, 25)

st.subheader("Range slider")

values = st.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))
st.write("Values: ", values)

st.subheader("Range time slider")

appointment = st.slider("Schedule you appointment:", value=(time(11, 30), time(12, 45)))
st.write("You're scheduled for:", appointment)

st.subheader("Datetime slider")

start_time = st.slider(
    "When do you start?", value=datetime(2020, 1, 1, 9, 30), format="MM/DD/YY - hh:mm"
)
st.write("Start time:", start_time)

st.header("Line chart")

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.line_chart(chart_data)

st.header("st.selectbox")
option = st.selectbox("What is your favourite color?", ("Blue", "Red", "Green"))

st.write("Your favourite color is", option)

st.header("st.multiselect")

options = st.multiselect(
    "What are your favorite colors",
    ["Green", "Yellow", "Red", "Blue"],
    ["Yellow", "Red"],
)

st.write("You selected:", options)

st.header("st.checkbox")

st.write("What would you like to order?")

icecream = st.checkbox("Ice cream")
coffee = st.checkbox("Coffee")
cola = st.checkbox("Cola")

if icecream:
    st.write("Great! Here's some more 🍦")

if coffee:
    st.write("Okay, here's some coffee ☕")

if cola:
    st.write("Here you go 🥤")

st.header("streamlit_pandas_profiling")
df = pd.read_csv(
    "https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv"
)

pr = df.profile_report()
st.write(pr)
