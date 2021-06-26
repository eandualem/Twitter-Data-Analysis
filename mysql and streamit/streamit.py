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

st.set_page_config(page_title="Day 5", layout="wide")

header("Database")
"""
1. Here I have loaded the whole data from the database and 
Filtered the data using pandas.
"""


def loadData():
    query = "select * from TweetInformation"
    df = db_execute_fetch(query, dbName="tweets", rdf=True)
    return df


def hashtag(df):
    hashtag = st.sidebar.multiselect(
        "Hashtag column", list(df['hashtags'].unique()))

    return hashtag


def hashtagInTweets(df):
    hashtag = st.sidebar.multiselect(
        "Hashtags in tweets", list(df['hashtags_in_tweets'].unique()))

    return hashtag


def selectHashTag(df):
    hashTags = st.sidebar.selectbox(
        "Select Hashtag from", (["Hashtag Column", "Hashtags in tweet"]))
    if hashTags == "Hashtag Column":
        return hashtag(df)
    else:
        return hashtagInTweets(df)


df = loadData()
hashtag = selectHashTag(df)
temp_df = df[np.isin(df, hashtag).any(axis=1)]
st.write(temp_df)

"""
2. Here I have written a query that selects specific data I want.
   This is good for example if the data is too large.
"""


def QueryByPolarity(condition):
    query = f"select favorite_count, followers_count, friends_count from TweetInformation where {condition}"
    df = db_execute_fetch(query, dbName="tweets", rdf=True)
    return df


def selectByPolarity():
    pol = st.sidebar.selectbox(
        "Select Polarity", (["Positive", "Negative", "Neutral"]))
    filt = st.selectbox("Order By", ([
        "favorite_count DESC",
        "favorite_count ASC",
        "followers_count DESC",
        "followers_count ASC",
        "friends_count DESC",
        "friends_count ASC"]))
    if pol == "Positive":
        return QueryByPolarity('polarity>0 Order by ' + filt)
    elif pol == "Negative":
        return QueryByPolarity('polarity<0 Order by ' + filt)
    else:
        return QueryByPolarity('polarity=0 Order by ' + filt)


st.write(selectByPolarity())


header("Visualization")
"""
3. Here I have created a bar chart for a selected column,
   with select number of elements
"""


def selectColumn(df):
    column = st.sidebar.selectbox(
        "Select column from", (["original_author", "hashtags", "favorite_count"]))

    dfCount = pd.DataFrame({'Tweet_count': df.groupby(
        [column])[column].count()}).reset_index()
    dfCount[column] = dfCount[column].astype(str)
    dfCount = dfCount.sort_values("Tweet_count", ascending=False)

    num = st.slider("Select number of Rankings", 0, 50, 5)
    title = f"Top {num} Ranking By Number of tweets"
    barChart(dfCount.head(num), title, "original_author", "Tweet_count")

df = loadData()
selectColumn(df)
# fig = ff.create_distplot([df['original_author'].head(num)], [
#                          "love"])
# st.plotly_chart(fig, use_container_width=True)
