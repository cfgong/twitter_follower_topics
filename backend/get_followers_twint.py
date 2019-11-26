import twint

twitter_handles = ['realDonaldTrump','ewarren','JoeBiden',
	'SenSanders','KamalaHarris','CoryBooker','AndrewYang']

for h in twitter_handles:
	c = twint.Config()
	c.Limit = 50
	c.Username = h
	c.Pandas = True

	twint.run.Followers(c)

	Followers_df = twint.storage.panda.Follow_df
	list_of_followers = Followers_df['followers'][h]

	print(Followers_df)

	break