from os import write
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
from add_data import db_execute_fetch
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from streamlit_helper import *


def header(text):
    st.sidebar.title(text)
    st.title(text)


def barChart(data, title, X, Y):
    title = f'{title.title()} Chart'
    st.write(title)

    msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                order='ascending')), y=f"{Y}:Q"))
    st.altair_chart(msgChart, use_container_width=True)


def wordCloud():
    df = loadData()
    cleanText = ''
    for text in df['original_text']:
        tokens = str(text).lower().split()

        cleanText += " ".join(tokens) + " "

    wc = WordCloud(width=650, height=450, background_color='white',
                   min_font_size=5).generate(cleanText)
    st.title("Tweet Text Word Cloud")
    st.image(wc.to_array())


def string_to_array(data):
    if data == ' ':
        return None
    else:
        return data.split(' ')


def flatten(df, column):
    df[column] = df[column].apply(string_to_array)
    df.dropna(inplace=True)
    df = pd.DataFrame(
        [hashtag for hashtags_list in df[column]
         for hashtag in hashtags_list],
        columns=[column])

    return df


def text_category(p):
    if p > 0:
        return "positive"
    elif p < 0:
        return "negative"
    else:
        return "neutral"
