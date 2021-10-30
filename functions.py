from altair.vegalite.v4.schema.core import CsvDataFormat
import pandas as pd
import streamlit as st
import altair as alt
st.title('COVID Data Exploration')

data = pd.read_csv('owid-covid-data.csv')

cols = data.columns
x_var = st.sidebar.selectbox('Pick first stat', cols, index=5)
y_var = st.sidebar.selectbox('Pick second stat', cols, index=8)

countries = set(data['location'])
country = st.sidebar.selectbox('Pick your country', countries)


def filter_data(df, col_names, country_name):

    df = df[df['location'] == country_name]
    col_names = ['date'] + col_names
    df = df[col_names]
    df['date'] = pd.to_datetime(df['date'])

    return df


data_f = filter_data(data, [x_var] + [y_var], country)

source = data_f
base = alt.Chart(source).encode(
    alt.X('date', axis=alt.Axis(title=None))
)

line1 = base.mark_line(stroke='#57A44C', interpolate='monotone').encode(
    alt.Y(x_var,
          axis=alt.Axis(title=x_var, titleColor='#57A44C'))
)

line = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
    alt.Y(y_var,
          axis=alt.Axis(title=y_var, titleColor='#5276A7'))
)

c = alt.layer(line1, line).resolve_scale(
    y='independent'
)
st.altair_chart(c, use_container_width=True)

link = '[Download Data](https://covid.ourworldindata.org/data/owid-covid-data.csv)'
st.markdown(link, unsafe_allow_html=True)
