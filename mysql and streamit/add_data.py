import os
import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error


def DBConnect(dbName=None):
    """

    Parameters
    ----------
    dbName :
        Default value = None)

    Returns
    -------

    """
    try:
        conn = mysql.connect(host='localhost', user=os.getenv("USER"), password=os.getenv("PASSWORD"),
                             database=dbName, buffered=True)
        cur = conn.cursor()
        return conn, cur
    except mysql.connector.Error as err:
        print("Database connection error: {}".format(err))


def emojiDB(dbName: str) -> None:

    try:
        conn, cur = DBConnect(dbName)
        dbQuery = f"ALTER DATABASE {dbName} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
        cur.execute(dbQuery)
        conn.commit()
    except mysql.connector.Error as err:
        print("Error : {}".format(err))


def createDB(dbName: str) -> None:
    """

    Parameters
    ----------
    dbName :
        str:
    dbName :
        str:
    dbName:str :


    Returns
    -------

    """
    try:
        conn, cur = DBConnect()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbName};")
        conn.commit()
        cur.close()
    except mysql.connector.Error as err:
        print("Error : {}".format(err))


def createTables(dbName: str) -> None:
    """

    Parameters
    ----------
    dbName :
        str:
    dbName :
        str:
    dbName:str :


    Returns
    -------

    """
    conn, cur = DBConnect(dbName)
    sqlFile = 'tweets_schema.sql'
    fd = open(sqlFile, 'r')
    readSqlFile = fd.read()
    fd.close()

    sqlCommands = readSqlFile.split(';')
    for command in sqlCommands:
        try:
            res = cur.execute(command)
        except Exception as ex:
            print("Command skipped: ", command)
            print(ex)
    conn.commit()
    cur.close()

    return


# def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
#     """

#     Parameters
#     ----------
#     df :
#         pd.DataFrame:
#     df :
#         pd.DataFrame:
#     df:pd.DataFrame :


#     Returns
#     -------

#     """
#     cols_2_drop = ['Unnamed: 0', 'timestamp', 'sentiment',
#                    'possibly_sensitive', 'original_text']
#     try:
#         df = df.drop(columns=cols_2_drop, axis=1)
#         df = df.fillna(0)
#     except KeyError as e:
#         print("Error:", e)

#     return df


def insert_to_tweet_table(dbName: str, df: pd.DataFrame, table_name: str) -> None:
    """

    Parameters
    ----------
    dbName :
        str:
    df :
        pd.DataFrame:
    table_name :
        str:
    dbName :
        str:
    df :
        pd.DataFrame:
    table_name :
        str:
    dbName:str :

    df:pd.DataFrame :

    table_name:str :


    Returns
    -------

    """
    conn, cur = DBConnect(dbName)

    # df = preprocess_df(df)

    for _, row in df.iterrows():
        sqlQuery = f"""INSERT INTO {table_name} (created_at, original_text, polarity, subjectivity,
                    favorite_count, retweet_count, original_author, followers_count, friends_count,
                    possibly_sensitive, hashtags, place, hashtags_in_tweets, screen_name, device)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11],
                row[12], row[13], row[14])

        try:
            # Execute the SQL command
            cur.execute(sqlQuery, data)
            # Commit your changes in the database
            conn.commit()
            print("Data Inserted Successfully")
        except Exception as e:
            conn.rollback()
            print("Error: ", e)
    return


def db_execute_fetch(*args, many=False, tablename='', rdf=True, **kwargs) -> pd.DataFrame:
    """

    Parameters
    ----------
    *args :

    many :
         (Default value = False)
    tablename :
         (Default value = '')
    rdf :
         (Default value = True)
    **kwargs :


    Returns
    -------

    """
    connection, cursor1 = DBConnect(**kwargs)
    if many:
        cursor1.executemany(*args)
    else:
        cursor1.execute(*args)

    # get column names
    field_names = [i[0] for i in cursor1.description]

    # get column values
    res = cursor1.fetchall()

    # get row count and show info
    nrow = cursor1.rowcount
    if tablename:
        print(f"{nrow} recrods fetched from {tablename} table")

    cursor1.close()
    connection.close()

    # return result
    if rdf:
        return pd.DataFrame(res, columns=field_names)
    else:
        return res


if __name__ == "__main__":
    createDB(dbName='tweets')
    emojiDB(dbName='tweets')
    createTables(dbName='tweets')

    df = pd.read_csv('../notebooks/clean_tweets.csv')

    print(df.info())

    insert_to_tweet_table(dbName='tweets', df=df,
                          table_name='TweetInformation')
