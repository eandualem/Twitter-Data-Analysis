# Twitter-Data-Analysis

**Table of content**

- [Overview](##abstract)
- [Requirements](#setup)
- [Install](#install)
- [Features](#features)
  - [Data Extraction](#dataExtraction)
  - [Data Preprocessing](#dataPreprocessing)
  - [Data Exploration and Visualzation](#dataExplorationAndVisualization)
  - [Test](#testing)
  - [Travis CI](#travisCI)
  - [Dashboard](#dashboard)

## Overview
Beginning from December 2019, the whole world is confronting an infectious disease called coronavirus. With restrictions on movement and stay-at-home orders in place, social media platforms such as Twitter have become the only means for users to keep in touch with one another and an outlet to express their concerns, opinions, and feelings about the pandemic. During these challenging times, people have used Twitter to appreciate frontline health workers and uplift each other through difficult times. On the other hand, Twitter has also been a place for massive misinformation and negative Tweets, creating unnecessary anxiety towards this disease.

This repository explores the impact of COVID19 on people's livelihoods via a dashboard using Twitter data. The data is collected using keywords `covide19` and `Africa`. There is a fully automated MLOps pipeline that analyses Twitter application data, using sentiments of the tweets and the topic discussed in tweets. There is a dashboard that will allow exploring the findings using Streamlit.

## Requirements
Python 3.5 and above, Pip and MYSQL
## Install
```
git clone https://github.com/eandualem/Twitter-Data-Analysis.git
cd Catch-Tweet-with-Keyword
pip install -r requirements.txt
```
## Features

### Data Extraction
  - There are JSON data that is collected using keywords `covide19` and `Africa` from Twitter.
  - There is a file called `extract_data_frame.py` which is used to extracts the data from data/covid19.json and construct a data frame called `processed_tweet_data.csv`. 
  - If there is no change to the data, `processed_tweet_data.csv` is already generated.


### Data Preprocessing
  - For data preprocessing the class Clean_Tweets which is in clean_tweets_dataframe.py is used. 
  - The notebook for preprocessing is inside the notebooks folder in the file preprocessing.ipynb.

### Data Exploration and Visualization
  - The notebook for Data Exploration and Visualization is inside the notebooks folder in the file preprocessing.ipynb.

### Test
  - There are two tests inside the tests folder.

### Travis CI
  - The file .travis.yml contains the configuration for Travis.

### Dashboard
  - The code for the dashboard and database are inside MySQL and streamlit folder
