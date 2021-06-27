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
   1. **Query all tweets in database** \n
   Here I have loaded the whole data from the database and 
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
   2. **Query specific data** \n
   Here I have written a query that selects specific tweets based on condition. 
   It is good when the data we load is too large to load at once.
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
3. **Display barchart for selected column** \n
   Here I have created a bar chart for a selected column,
   with select number of elements
"""


def selectColumn(df):
    column = st.sidebar.selectbox(
        "Select column from", (["original_author",
                                "hashtags",
                                "hashtags_in_tweets",
                                "favorite_count",
                                "followers_count",
                                "friends_count",
                                "place", ]))

    if(column == "hashtags" or column == "hashtags_in_tweets"):
        df = flatten(df, column)
        print(type(df))

    dfCount = pd.DataFrame({'Tweet_count': df.groupby(
        [column])[column].count()}).reset_index()
    dfCount[column] = dfCount[column].astype(str)
    dfCount = dfCount.sort_values("Tweet_count", ascending=False)
    num = st.slider("Select number of Rankings", 0, 50, 5)
    title = f"Top {num} Ranking By Number of tweets"
    barChart(dfCount.head(num), title, column, "Tweet_count")


df = loadData()
selectColumn(df)

"""
4. **Tweet Text Word Cloud** \n
   Here I have created world cloud for, positive, negative, neutral tweets,
   and all tweets
"""


def wordCloud(df):
    choice = st.sidebar.selectbox(
        "Select polarit of tweets from", (["all tweets",
                                           "positive",
                                           "neutral",
                                           "negative"]))

    if(choice == "all tweets"):
        tweets_df = df['original_text']
    else:
        df["score"] = df["polarity"].apply(text_category)
        df.groupby("score")["polarity"].count()
        tweets_df = df[df['score'] == choice]['original_text']

    cleanText = ''
    for text in tweets_df:
        tokens = str(text).lower().split()

        cleanText += " ".join(tokens) + " "

    wc = WordCloud(width=650, height=450, background_color='white',
                   min_font_size=5).generate(cleanText)
    st.image(wc.to_array())


df = loadData()
wordCloud(df)
