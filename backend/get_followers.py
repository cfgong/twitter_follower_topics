from twython import Twython

from auth2 import (
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

def get_follower_handles(user):

    results = twitter.cursor(twitter.get_followers_list, screen_name=user, count=5, return_pages=True)
    handles = []
    last_page = None
    try:
        for page in results:
            last_page = page
            for result in page:
                handles.append(result['screen_name'])
            print("sleeping")
            time.sleep(60)
            print(len(set(handles)))
    except:
        pass
    print(len(set(handles)))

    return handles



for candidate in candidates:

	followers = get_follower_handles(candidate)