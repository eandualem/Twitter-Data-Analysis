from os import write
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
from add_data import db_execute_fetch

st.set_page_config(page_title="Day 5", layout="wide")

st.title("Database")


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


def QueryByPolarity(condition):
    query = f"select favorite_count, followers_count, friends_count from TweetInformation where {condition}"
    print(query)
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
