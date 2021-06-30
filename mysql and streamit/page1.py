from clean_tweets_dataframe import *
import sys
import os
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud, STOPWORDS
from add_data import db_execute_fetch
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from streamlit_helper import *
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
sys.path.append(os.path.abspath(os.path.join('..')))


def loadData():
    query = "select * from TweetInformation"
    df = db_execute_fetch(query, dbName="tweets", rdf=True)
    return df


def place(df):
    hashtag = st.sidebar.multiselect(
        "Place column", list(df['place'].unique()))

    return hashtag


def device(df):
    hashtag = st.sidebar.multiselect(
        "Device used", list(df['device'].unique()))

    return hashtag


def screen_name(df):
    hashtag = st.sidebar.multiselect(
        "Screen Name column", list(df['screen_name'].unique()))

    return hashtag


def hashtag(df):
    hashtag = st.sidebar.multiselect(
        "Hashtag column", list(df['hashtags'].unique()))

    return hashtag


def hashtagInTweets(df):
    hashtag = st.sidebar.multiselect(
        "Hashtags in tweets", list(df['hashtags_in_tweets'].unique()))

    return hashtag


def select_column_for_filter(df):
    hashTags = st.sidebar.selectbox(
        "Select column from ", (["Place", "Device", "Screen Name", "Hashtags in tweet", "Hashtag Column"]))
    if hashTags == "Place":
        return place(df)
    elif hashTags == "Device":
        return device(df)
    elif hashTags == "Screen Name":
        return screen_name(df)
    elif hashTags == "Hashtag Column":
        return hashtag(df)
    else:
        return hashtagInTweets(df)


def QueryByPolarity(condition):
    query = f"select favorite_count, followers_count, friends_count from TweetInformation where {condition}"
    df = db_execute_fetch(query, dbName="tweets", rdf=True)
    return df


def selectByPolarity():
    pol = st.sidebar.selectbox(
        "Select from polarity", (["Positive", "Negative", "Neutral"]))
    filt = st.sidebar.selectbox("Order rows by", ([
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


def selectColumn(df, ct):
    column = st.selectbox(
        "Select a column for a barchart", (["original_author",
                                            "screen_name",
                                            "hashtags",
                                            "hashtags_in_tweets",
                                            "favorite_count",
                                            "followers_count",
                                            "friends_count",
                                            "place", ]))

    if(column == "hashtags" or column == "hashtags_in_tweets"):
        df[column] = df[column].apply(ct.string_to_array)
        df.dropna(inplace=True)
        df = ct.get_flattened_dataframe(df, column, 'score')

    num = st.slider("Select number of Rankings", 0, 50, 5)
    title = f"Top {num} Ranking By Number of tweets"
    df = df.groupby([column, 'score']).size().reset_index(name='counts')
    fig = px.histogram(df.nlargest(num, "counts"),
                       x=column, y="counts", color="score", title=title)
    fig.update_layout(width=1200, height=600)
    st.plotly_chart(fig)


def wordCloud(df):
    choice = st.selectbox(
        "Select polarit of tweets from", (["all tweets",
                                           "positive",
                                           "neutral",
                                           "negative"]))

    df['original_text'] = df['original_text'].astype(str)
    df['original_text'] = df['original_text'].apply(lambda x: x.lower())

    if(choice == "all tweets"):
        tweets_df = df['original_text']
    else:
        df["score"] = df["polarity"].apply(text_category)
        df.groupby("score")["polarity"].count()
        tweets_df = df[df['score'] == choice]['original_text']

    cleanText = ''
    for text in tweets_df:
        tokens = text.split()
        cleanText += " ".join(tokens) + " "

    custom_stopwords = ['t', 'rt', 'ti', 'vk', 'to', 'co',
                        'dqlw', 'z', 'nd', 'm', 's', 'kur', 'u', 'o', 'd']
    STOP_WORDS = STOPWORDS.union(custom_stopwords)

    wc = WordCloud(width=1000, height=600, background_color='white', stopwords=STOP_WORDS).generate(
        ' '.join(df.original_text.values))
    st.image(wc.to_array())


def pie(df, column):
    specs = [[{'type': 'domain'}, {'type': 'domain'}],
             [{'type': 'domain'}, {'type': 'domain'}]]
    fig = make_subplots(rows=2, cols=2, specs=specs)

    fig.add_trace(go.Pie(labels=df[column],
                         values=df["retweet_count"], name='retweet_count'), 1, 1)
    fig.add_trace(go.Pie(labels=df[column],
                         values=df["favorite_count"], name='favorite_count',), 1, 2)
    fig.add_trace(go.Pie(labels=df[column],
                         values=df["followers_count"], name='followers_count',), 2, 1)
    fig.add_trace(go.Pie(labels=df[column],
                         values=df["friends_count"], name='friends_count',), 2, 2)
    # Tune layout and hover info
    fig.update(layout_title_text=f'Tweet popularity vs their {column}')

    fig = go.Figure(fig)
    fig.update_layout(width=900, height=600)
    st.plotly_chart(fig)


def corelation(df, column):
    fig = px.scatter_matrix(df, dimensions=[
        "retweet_count",
        "favorite_count",
        "followers_count",
        "friends_count",
    ],  color=column)
    fig.update_layout(width=1200, height=600)
    st.plotly_chart(fig)


def select_pie(df):
    column = st.selectbox("Choice", ([
        "polarity",
        "subjectivity", ]), key=2)
    if column == "polarity":
        return ([pie(df, "score"), corelation(df, "score")])
    else:
        return ([pie(df, "subjectivity_score"), corelation(df, "subjectivity_score")])


def scatter(df):
    col1, col2, col3, col4 = st.beta_columns(4)
    color = col1.selectbox("Select column for color", ([
        "polarity",
        "subjectivity", ]), key=5)
    x = col2.selectbox("Select x axis", ([
        "created_at",
        "retweet_count",
        "favorite_count",
        "followers_count",
        "friends_count", ]), key=6)

    y = col3.selectbox("Select column for y-axis", ([
        "created_at",
        "retweet_count",
        "favorite_count",
        "followers_count",
        "friends_count", ]), key=7)

    z = col4.selectbox("Select column for size", ([
        "retweet_count",
        "favorite_count",
        "followers_count",
        "friends_count", ]), key=8)

    fig = px.scatter(df, x=x, y=y,
                     color=color, size=z)
    fig.update_layout(width=900, height=600)
    st.plotly_chart(fig)


def app():
    ct = Clean_Tweets()
    header("Database")
    st.write(
        """
    1. **Query all tweets in database** \n
    Here I have loaded the whole data from the database and 
    Filtered the data using pandas.
    """)

    df = loadData()
    hashtag = select_column_for_filter(df)
    temp_df = df[np.isin(df, hashtag).any(axis=1)]
    st.write(temp_df)
    st.write(
        """
    2. **Query specific data** \n
    Here I have written a query that selects specific tweets based on condition. 
    It is good if the data is too large to load at once.
    """)
    st.write(selectByPolarity())

    header("Visualization")
    st.write(
        """
    3. **Display barchart for selected column** \n
    Here I have created a bar chart for a selected column,
    it will split each bar based on their polarity or subjectivity
    and show them in different colors.
    """)

    df = loadData()
    df["score"] = df["polarity"].apply(ct.polarity_category)
    df["subjectivity_score"] = df["subjectivity"].apply(
        ct.subjectivity_category)
    selectColumn(df, ct)

    st.write(
        """
    4. **Tweet Text Word Cloud** \n
    Here I have created world cloud for, positive, negative, neutral tweets,
    or all tweets
    """)
    df = loadData()
    wordCloud(df)

    st.write(
        """
    5. **Popularity of tweets** \n
    Here we try to find if there is corelation between retweet_count, favorite_count,
    followers_count, friends_count and polarity and subjectivity
    """)

    df = loadData()
    df["score"] = df["polarity"].apply(ct.polarity_category)
    df["subjectivity_score"] = df["subjectivity"].apply(
        ct.subjectivity_category)
    select_pie(df)

    st.write(
        """
    6. **Trend over time** \n
    Here I try there is a trend over time in polarity and subjectivity of tweets and
    and theme being liked
    """)

    df = loadData()
    df["score"] = df["polarity"].apply(ct.polarity_category)
    df["subjectivity_score"] = df["subjectivity"].apply(
        ct.subjectivity_category)
    scatter(df)
