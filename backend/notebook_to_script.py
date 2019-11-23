import random
import re
import nltk
from twython import Twython
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
import psycopg2
import pandas as pd

from auth2 import consumer_key, consumer_secret, access_token, access_token_secret
from aws import host, port, user, password, database

connection = psycopg2.connect(host = host, port = port, user = user, password = password, dbname = database)
cursor=connection.cursor()

twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)

PRINT_LIMIT = 10
FOLLOWER_SAMPLE_LIMIT = 2 # number of followers to randomly sample (500)
WORD_FREQ_LIMIT = 10 # return this number of topics that are most freq
MIN_WORD_LEN = 3

STOPWORDS = stopwords.words('english') + stopwords.words('spanish')
# TODO: decide whether or not to remove tweets that are from retweets altogether
more_stop_words = ['rt']
STOPWORDS += more_stop_words

with open('top1000.txt', 'r') as f:
    mostFreqWords = [line.strip() for line in f]

STOPWORDS += mostFreqWords
STOPWORDS = set(STOPWORDS)

# Printing twitter account IDs

# limit = 0
# for follower_id in followers['ids']:
#     print('Follower Id: {0} '.format(follower_id))
#     limit += 1
#     if limit >= PRINT_LIMIT:
#         break

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def get_tweet_data(results):
    tweets = []
    for tweet in results:
        tweet_map = {"text": tweet['text']}
        tweet_hashtags = []
        tweet_urls = []
        tweet_user_mentions = []

        entities = tweet['entities']

        for hashtags in entities['hashtags']:
            tweet_hashtags.append(hashtags['text'])
        for urls in entities['urls']:
            tweet_urls.append(urls['url'])
        try:
            for media in entities['media']:
                tweet_urls.append(media['url'])
        except:
            pass
        for users in entities['user_mentions']:
            tweet_user_mentions.append(users['screen_name'])

        tweet_map["hashtags"] = tweet_hashtags
        tweet_map["urls"] = tweet_urls
        tweet_map["user_mentions"] = tweet_user_mentions
        tweets.append(tweet_map)

    return tweets


def get_tweets_data_from(user_id, results):
    try:
        result = twitter.get_user_timeline(user_id = user_id)
        results.extend(result)
        return get_tweet_data(result), results
    except:
        return [], results


def get_tweets_data_and_results(user_ids):
    tweets_data = []
    results = []

    samples = user_ids
    if len(user_ids) > FOLLOWER_SAMPLE_LIMIT:
        samples = random.sample(user_ids, FOLLOWER_SAMPLE_LIMIT)

    for f in samples:
        result, results = get_tweets_data_from(f, results)
        tweets_data.extend(result)

    return tweets_data, results


def word_extraction_tweet(tweet_dictionary, stopwords = STOPWORDS):
    sentence = tweet_dictionary['text']
    hashtags = ['#' + s for s in tweet_dictionary['hashtags']]
    urls = tweet_dictionary['urls']
    user_mentions = ['@' + s for s in tweet_dictionary['user_mentions']]

    ignore = hashtags + urls + user_mentions

    words = sentence.split()

    cleaned_text = []

    for word in words:
        cleaned_word = re.sub("[^\w]", "",  word)
        if (isEnglish(word)) and \
        (not word in ignore) and \
        (not word.lower() in stopwords) and \
        (word.isalpha()) and (len(cleaned_word) >= MIN_WORD_LEN):
            cleaned_text.append(cleaned_word.lower())
    return cleaned_text

def word_extraction_hashtag(tweet_dictionary, stopwords = STOPWORDS):
    hashtags = tweet_dictionary['hashtags']
    cleaned_text = []
    for tag in hashtags:
        if (isEnglish(tag)):
            cleaned_text.append(tag)
    return cleaned_text


def get_freq_map(my_list):
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    return freq


def get_top_freq(my_list, top_count):
    freq = get_freq_map(my_list)
    freq = sorted(freq.items(), key=lambda item: item[1], reverse = True)

    if len(freq) <= top_count:
        return freq
    else:
        return freq[:top_count]


# import maptlotlib.pyplot as plt
# def visualize_data(token_counts):
#     tokens = [tup[0] for tup in token_counts]
#     counts = [tup[1] for tup in token_counts]
#     plt.bar(range(len(tokens)), height=counts, tick_label=tokens)
#     plt.savefig()

# visualize_data(tweets_text_freq)

# methods for writing and reading to database
def read_try(sql):
    try:
        df = pd.read_sql(sql, con=connection)
        return pd.DataFrame() if df.empty else df
    except Exception as e:
        print("READ ERROR", e)
        return pd.DataFrame()

def write_try(sql):
    try:
        cursor.execute(sql)  # run a psql command
        connection.commit()  # commit to db
        return True
    except Exception as e:
        print("WRITE ERROR: ", e)
        return False

def read_user_from_db(user):
    sql = 'SELECT * FROM users WHERE user_handle = \'{}\''.format(user)
    return read_try(sql)

# get list of followers for a user
def read_user_followers_from_db(user):
    sql = 'SELECT follower_handle FROM followers WHERE user_handle = \'{}\''.format(user)
    return read_try(sql)

# get list of word counts for a user
def read_user_words_from_db(user, date = ''):
    sql = ('SELECT word, SUM(count) as sum_count FROM followers '
    'JOIN tweets ON tweets.follower_handle = followers.follower_handle '
    'JOIN words ON words.tweet_id = tweets.tweet_id '
    'WHERE followers.user_handle = \'{}\' GROUP BY word ORDER BY sum_count desc'.format(user)
    )
    return read_try(sql)

# get list of words for a user
def read_user_hashtags_from_db(user, date = ''):
    sql = ('SELECT word, SUM(count) as sum_count FROM followers '
    'JOIN tweets ON tweets.follower_handle = followers.follower_handle '
    'JOIN hashtags ON hashtags.tweet_id = tweets.tweet_id '
    'WHERE followers.user_handle = \'{}\' GROUP BY word ORDER BY sum_count desc'.format(user)
    )
    return read_try(sql)

def write_user_to_db(user):
    sql = 'INSERT INTO users VALUES (\'{}\');'.format(user)
    write_try(sql)

def write_user_followers_to_db(followers, user):
    for follower in followers:
        sql = 'INSERT INTO followers VALUES (\'{}\', \'{}\');'.format(follower, user)
        write_try(sql)

def write_follower_tweets_words_hashtags_to_db(follower, tweets):
    for tweet in tweets:
        tweet_id = tweet['id']
        tweet_date = tweet['created_at']
        sql = 'INSERT INTO tweets VALUES ({},\'{}\',\'{}\');'.format(tweet_id, follower, tweet_date)
        # if writing tweet to database was sucessful, then we need to get write word count info
        if write_try(sql):
            # calculate word and hashtag count of the tweet and insert that into database
            '''
            words = ...
            word_counts = ...
            for word, wcount in words, word_counts:
                sql2 = 'INSERT INTO words VALUES ({},\'{}\',{});'.format(tweet_id, word, wcount)
                word_try(sql2)

            hashtags = ...
            hashtag_counts = ...
            for hashtag, hcount in hashtags, hashtag_counts:
                sql2 = 'INSERT INTO words VALUES ({},\'{}\',{});'.format(tweet_id, hashtag, hcount)
                word_try(sql2)
            '''
            pass


def main(user='realDonaldTrump'):
    followers = []
    try:
        followers = twitter.get_followers_ids(screen_name = user)
    except:
        return -1

    # make sure user is in users db
    was_user_in_db = not read_user_from_db(user).empty
    if not was_user_in_db:
        write_user_to_db(user)

    tweets_data, results = get_tweets_data_and_results(followers['ids'])
    print(tweets_data)
    print(results)
    exit()
    tweets_text = []
    for tweet in tweets_data:
        tweets_text.extend(word_extraction_tweet(tweet))


    tweets_hashtags = []
    for tweet in tweets_data:
            tweets_hashtags.extend(word_extraction_hashtag(tweet))

    tweets_text_freq = get_top_freq(tweets_text, WORD_FREQ_LIMIT)
    tweets_hashtags_freq = get_top_freq(tweets_hashtags, WORD_FREQ_LIMIT)

    return {'token_labels': [t[0] for t in tweets_text_freq],
        'token_counts': [t[1] for t in tweets_text_freq],
        'hash_labels': [t[0] for t in tweets_hashtags_freq],
        'hash_counts': [t[1] for t in tweets_hashtags_freq]}


if __name__ == "__main__":
    print(main())
