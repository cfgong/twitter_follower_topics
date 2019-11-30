from twython import Twython

from nltk.tokenize import casual_tokenize
import nltk
nltk.download('averaged_perceptron_tagger')

import pandas as pd
import psycopg2

from auth import consumer_key, consumer_secret, access_token, access_token_secret
from aws import host as ahost, port as aport, user as auser, password as apassword, database as adatabase

twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
connection = psycopg2.connect(host = ahost,
                              port = aport,
                              user = auser,
                              password = apassword,
                              dbname = adatabase)
cursor = connection.cursor()

# FOLLOWER_SAMPLE_LIMIT = 100 # number of followers to randomly sample
WORD_FREQ_LIMIT = 10 # return this number of topics that are most freq

REGULAR_NOUN_WORD_TYPE = 0
PROPER_NOUN_WORD_TYPE = 1

def read_try(sql):
    try:
        df = pd.read_sql(sql, con=connection)
        return pd.DataFrame() if df.empty else df
    except Exception as e:
        #print("READ ERROR", e)
        return pd.DataFrame()

def write_try(sql):
    try:
        cursor.execute(sql)  # run a psql command
        return True
    except Exception as e:
        #print("WRITE ERROR: ", e)
        return False
    finally:
        connection.commit()

# get all the users from the users table
def read_all_users_from_db():
    sql = 'SELECT * FROM users'
    return read_try(sql)

# get all the follower, user pairs from the followers table
def read_all_followers_from_db():
    sql = 'SELECT * FROM followers'
    return read_try(sql)

# get all the tweets from tweets table
def read_all_tweets_from_db():
    sql = 'SELECT * FROM tweets'
    return read_try(sql)

# get all word counts of tweet text
def read_all_words_from_db():
    sql = 'SELECT * FROM words'
    return read_try(sql)

# get all hashtag counts
def read_all_hashtags_from_db():
    sql = 'SELECT * FROM hashtags'
    return read_try(sql)

def read_user_from_db(user):
    sql = 'SELECT * FROM users WHERE user_handle = \'{}\''.format(user)
    return read_try(sql)

# get list of followers for a user
def read_user_followers_from_db(user, limit = 'NULL'):
    sql = 'SELECT follower_handle FROM followers WHERE user_handle = \'{}\'LIMIT {}'.format(user, limit)
    return read_try(sql)

# see if tweet is already indexed in DB
def read_tweet_from_db(tweet_id):
    sql = ('SELECT tweet_date FROM tweets '
    'WHERE tweet_id = {}'.format(tweet_id)
    )
    return read_try(sql)

# get list of word counts for a user
def read_user_words_from_db(user, limit = 'NULL', date = ''):
    sql = ('SELECT word, SUM(count) as sum_count FROM followers '
    'JOIN tweets ON tweets.follower_handle = followers.follower_handle '
    'JOIN words ON words.tweet_id = tweets.tweet_id '
    'WHERE followers.user_handle = \'{}\' GROUP BY word ORDER BY sum_count desc LIMIT {}'.format(user, limit)
    )
    return read_try(sql)

# get list of word counts for a user
def read_user_proper_words_from_db(user, limit = 'NULL', date = ''):
    sql = ('SELECT word, SUM(count) as sum_count FROM followers '
    'JOIN tweets ON tweets.follower_handle = followers.follower_handle '
    'JOIN words ON words.tweet_id = tweets.tweet_id '
    'WHERE followers.user_handle = \'{}\' '.format(user))
    sql += 'GROUP BY word HAVING MAX(words.word_type) = {} '.format(PROPER_NOUN_WORD_TYPE)
    sql += 'ORDER BY sum_count desc LIMIT {} '.format(limit)
    return read_try(sql)

# get list of hashtag counts for a user
def read_user_hashtags_from_db(user, limit = 'NULL', date = ''):
    sql = ('SELECT word, SUM(count) as sum_count FROM followers '
    'JOIN tweets ON tweets.follower_handle = followers.follower_handle '
    'JOIN hashtags ON hashtags.tweet_id = tweets.tweet_id '
    'WHERE followers.user_handle = \'{}\' GROUP BY word ORDER BY sum_count desc LIMIT {}'.format(user, limit)
    )
    return read_try(sql)

def write_user_to_db(user):
    sql = 'INSERT INTO users VALUES (\'{}\');'.format(user)
    write_try(sql)

def write_user_followers_to_db(followers, user):
    for follower in followers:
        sql = 'INSERT INTO followers VALUES (\'{}\', \'{}\');'.format(follower, user)
        write_try(sql)

def write_tweets_words_hashtags_to_db(tweets_dictionary):
    for tweet in tweets_dictionary:
        follower = tweet['user']
        tweet_id = tweet['id']
        tweet_date = tweet['date']
        sql = 'INSERT INTO tweets VALUES ({},\'{}\',\'{}\');'.format(tweet_id, follower, tweet_date)

        # if writing tweet to database was sucessful, then we need to get write word count info
        if write_try(sql):
            words, tags = word_hashtag_extraction_noun_based(tweet)
            word_count = get_freq_map(words)
            hashtag_count = get_freq_map(tags)

            for w, c in word_count.items():
                word_type_int = words[w]
                sql2 = 'INSERT INTO words VALUES ({},\'{}\',{},{});'.format(tweet_id, w, c, word_type_int)
                write_try(sql2)

            for w, c in hashtag_count.items():
                sql2 = 'INSERT INTO hashtags VALUES ({},\'{}\',{});'.format(tweet_id, w, c)
                write_try(sql2)

def get_tweets_from(follower_name, results = []):
    try:
        result = twitter.get_user_timeline(screen_name = follower_name)
        results.extend(result)
        return results
    except:
        return results

def get_tweet_info_from_tweets(results):
    tweets = []
    for tweet in results:
        tweet_map = {'text': tweet['text']}
        tweet_map['id'] = tweet['id']
        tweet_map['date'] = tweet['created_at']
        tweet_map['user'] = tweet['user']['screen_name']
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

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
        return True if s.isalpha() else False
    except UnicodeDecodeError:
        return False

# noun based word extraction
def word_hashtag_extraction_noun_based(tweet_dictionary):
    text = tweet_dictionary['text']
    # skip over retweets
    if text[0:4] == 'RT @':
        return [], []
    text = casual_tokenize(tweet_dictionary['text'])
    result = nltk.pos_tag(text)

    hashtags = ['#' + s for s in tweet_dictionary['hashtags']]
    urls = tweet_dictionary['urls']
    user_mentions = ['@' + s for s in tweet_dictionary['user_mentions']]
    ignore = hashtags + urls + user_mentions

    all_noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
    proper_noun_tags = ['NNP', 'NNPS']

    cleaned_text = {}
    for t in result:
        word = t[0]
        tag = t[1]
        if (tag in all_noun_tags) and (not word in ignore) and isEnglish(word):
            if tag in proper_noun_tags:
                cleaned_text[word.lower()] = PROPER_NOUN_WORD_TYPE
            else:
                cleaned_text[word.lower()] = REGULAR_NOUN_WORD_TYPE

    return cleaned_text, set([h.lower() for h in hashtags])

def get_freq_map(my_list):
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    return freq

# TODO: add date filtering (filter tweets by date)
# TODO: add get from db only option (meaning no writing to db, just pull info from db)
def main(user='realDonaldTrump', only_get_info_from_db = True):
    # make sure user exists
    try:
        twitter.show_user(screen_name=user)
    except:
        return -1

    # pull more info and write to db
    # if we get only info flag is False or user not already in db
    if not only_get_info_from_db or read_user_from_db(user).empty:
        followers = twitter.get_followers_list(screen_name = user)['users']
        followers_list = []
        for follower in followers:
            followers_list.append(follower['screen_name'])
        # make sure user exists in db
        write_user_to_db(user)
        # write user followers to db
        write_user_followers_to_db(followers_list, user)

        results = []
        for f in followers_list:
            results = get_tweets_from(f, results)
        # pull relevant data from tweets and write and process data
        tweets_data = get_tweet_info_from_tweets(results)
        write_tweets_words_hashtags_to_db(tweets_data)

    # pull tweet count from db
    user_words_df = read_user_words_from_db(user, limit = WORD_FREQ_LIMIT)
    user_words_better_df = read_user_proper_words_from_db(user, limit = WORD_FREQ_LIMIT)
    user_hashtags_df = read_user_hashtags_from_db(user, limit = WORD_FREQ_LIMIT)

    word_results = word_count_results = tag_results = tag_count_results = []
    if user_words_df.size > 0:
        word_results = user_words_df["word"].tolist()
        word_count_results = user_words_df["sum_count"].tolist()
    if user_hashtags_df.size > 0:
        tag_results = user_hashtags_df["word"].tolist()
        tag_count_results = user_hashtags_df["sum_count"].tolist()

    final_results = {'token_labels': word_results,
            'token_counts': word_count_results,
            'hash_labels': tag_results,
            'hash_counts': tag_count_results}

    return final_results

if __name__ == "__main__":
    print(main())
