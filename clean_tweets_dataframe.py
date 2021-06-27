import json
import re
import pandas as pd
from streamlit.errors import Error


class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """

    def drop_unwanted_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        unwanted_rows = df[df['retweet_count'] == 'retweet_count'].index
        df.drop(unwanted_rows, inplace=True)
        df = df[df['polarity'] != 'polarity']

        return df

    def drop_duplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        drop duplicate rows
        """
        df.drop_duplicates(inplace=True)

        return df

    def remove_non_english_tweets(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove non english tweets from lang
        """
        df = df.drop(df[df['lang'] != 'en'].index)

        return df

    def remove_links(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove links starting with http, https or www
        """
        df['original_text'] = df.original_text.replace(
            r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)

        return df

    def remove_special_characters(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove all characters except for [a-z, A-Z and #]
        """
        df['original_text'] = df['original_text'].str.replace(
            "[^a-zA-Z#]", " ")
        return df

    def convert_to_string(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert columns source, original_text, original_author, place, hashtags, 
        hashtags_in_tweets and screen_name to string        """
        df["source"] = df["source"].astype("string")
        df["original_text"] = df["original_text"].astype("string")
        df["original_author"] = df["original_author"].astype("string")
        df["place"] = df["place"].astype("string")
        df["hashtags"] = df["hashtags"].astype("string")
        df["hashtags_in_tweets"] = df["hashtags_in_tweets"].astype("string")
        df["screen_name"] = df["screen_name"].astype("string")
        return df

    def convert_to_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert column to datetime
        """
        df['created_at'] = pd.to_datetime(df["created_at"])
        return df

    def convert_to_numbers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df["polarity"] = pd.to_numeric(df["polarity"])
        df["subjectivity"] = pd.to_numeric(df["subjectivity"])
        df["favorite_count"] = pd.to_numeric(df["favorite_count"])
        df["followers_count"] = pd.to_numeric(df["followers_count"])
        df["retweet_count"] = pd.to_numeric(df["retweet_count"])
        df["friends_count"] = pd.to_numeric(df["friends_count"])

        return df

    def convert_to_boolean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        converts possibly_sensitive to boolean
        """
        df["possibly_sensitive"] = df["possibly_sensitive"].astype(
            'bool')
        return df

    def get_element_from_json(self, json_data, key, append):
        """
        returns specific element value from json file in list
        """
        hashtags = []
        try:
            res = json.loads(json_data.replace("'", "\""))
            for i in range(len(res)):
                hashtags.append(append+res[0][key])

            return hashtags
        except:
            return hashtags

    def array_to_string(self, data):
        """
        converts an array of into strings separated by comma
        """
        if len(data) == 0:
            return " "
        else:
            def res(x): return ', '.join([str(elem) for elem in x])
            return res(data)

    def find_hashtags(self, tweet):
        """
        finds hashtags in a give text
        """
        return re.findall('(#[A-Za-z]+[A-Za-z0-9-_]+)', str(tweet))
