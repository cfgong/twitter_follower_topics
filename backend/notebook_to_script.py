import random
import re
import nltk
from twython import Twython
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)


PRINT_LIMIT = 50
FOLLOWER_SAMPLE_LIMIT = 20 # number of followers to randomly sample
WORD_FREQ_LIMIT = 10 # return this number of topics that are most freq

STOPWORDS = stopwords.words('english') + stopwords.words('spanish')
# TODO: decide whether or not to remove tweets that are from retweets altogether
more_stop_words = ['rt']
STOPWORDS += more_stop_words

# Printing twitter account IDs

# limit = 0
# for follower_id in followers['ids']:
#     print('Follower Id: {0} '.format(follower_id))
#     limit += 1
#     if limit >= PRINT_LIMIT:
#         break


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


def word_extraction(tweet_dictionary, stopwords = STOPWORDS):
    sentence = tweet_dictionary['text']
    hashtags = ['#' + s for s in tweet_dictionary['hashtags']]
    urls = tweet_dictionary['urls']
    user_mentions = ['@' + s for s in tweet_dictionary['user_mentions']]

    ignore = hashtags + urls + user_mentions

    words = sentence.split()

    cleaned_text = []

    for word in words:
        cleaned_word = re.sub("[^\w]", "",  word)
        if (not word in ignore) and (not word.lower() in stopwords) and (word.isalpha()) and (len(cleaned_word) > 0):
            cleaned_text.append(cleaned_word.lower())
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
        return freq[:10]


# import maptlotlib.pyplot as plt
# def visualize_data(token_counts):
#     tokens = [tup[0] for tup in token_counts]
#     counts = [tup[1] for tup in token_counts]
#     plt.bar(range(len(tokens)), height=counts, tick_label=tokens)
#     plt.show()

# visualize_data(tweets_text_freq)


def main():
    user = "AndrewYang"
    followers = twitter.get_followers_ids(screen_name = user)

    tweets_data, results = get_tweets_data_and_results(followers['ids'])

    tweets_text = []
    for tweet in tweets_data:
        tweets_text.extend(word_extraction(tweet))


    tweets_hashtags = []
    for tweet in tweets_data:
            tweets_hashtags.extend(tweet['hashtags'])

    tweets_text_freq = get_top_freq(tweets_text, WORD_FREQ_LIMIT)
    tweets_hashtags_freq = get_top_freq(tweets_hashtags, WORD_FREQ_LIMIT)    

    return {'labels': [t[0] for t in tweets_text_freqs],
        'counts': [t[1] for t in tweets_text_freqs]}


    # return {'data': [{'token': t[0], 'count': t[1]} for t in tweets_text_freq]}


if __name__ == "__main__":
    print(main())
