import os
import sys
import unittest
from numpy import number
import pandas as pd
import pandas.api.types as ptypes
from pandas.api import types

sys.path.append(os.path.abspath(os.path.join('..')))
from clean_tweets_dataframe import Clean_Tweets


class TestCleanTweetsDataframe(unittest.TestCase):
    """
                A class for unit-testing function in the clean_tweets_dataframe.py file

                Args:
        -----
                        unittest.TestCase this allows the new class to inherit
                        from the unittest module
        """

    def setUp(self) -> pd.DataFrame:
        self.df = pd.read_csv("../notebooks/clean_tweets.csv")
        self.ct = Clean_Tweets()

    def test_drop_duplicate(self):
        temp_df = self.df.copy(deep=True)
        temp_df.append([temp_df[temp_df['screen_name'] == True]]
                       * 5, ignore_index=True)
        self.assertTrue(not temp_df.duplicated().any())
        temp_df = self.ct.drop_duplicate(temp_df)
        self.assertTrue(not temp_df.duplicated().any())

    def test_convert_to_string(self):
        temp_df = self.ct.convert_to_string(self.df)
        print(temp_df['device'].dtype)
        print(pd.StringDtype)
        self.assertTrue(temp_df['device'].dtype == "string")
        self.assertTrue(temp_df['original_text'].dtype == "string")
        self.assertTrue(temp_df['original_author'].dtype == "string")
        self.assertTrue(temp_df['place'].dtype == "string")
        self.assertTrue(temp_df['hashtags'].dtype == "string")
        self.assertTrue(temp_df['hashtags_in_tweets'].dtype == "string")
        self.assertTrue(temp_df['screen_name'].dtype == "string")

    def test_convert_to_datetime(self):
        temp_df = self.ct.convert_to_datetime(self.df)
        self.assertTrue(types.is_datetime64_any_dtype(temp_df['created_at']))

    def test_convert_to_numbers(self):
        temp_df = self.ct.convert_to_numbers(self.df)
        self.assertTrue(types.is_float_dtype(temp_df['polarity']))
        self.assertTrue(types.is_float_dtype(temp_df['subjectivity']))
        self.assertTrue(types.is_numeric_dtype(temp_df['favorite_count']))
        self.assertTrue(types.is_numeric_dtype(temp_df['followers_count']))
        self.assertTrue(types.is_numeric_dtype(temp_df['friends_count']))
        self.assertTrue(types.is_numeric_dtype(temp_df['retweet_count']))

    def test_convert_to_boolean(self):
        temp_df = self.ct.convert_to_boolean(self.df)
        self.assertTrue(types.is_bool_dtype(temp_df['possibly_sensitive']))


if __name__ == '__main__':
    unittest.main()
