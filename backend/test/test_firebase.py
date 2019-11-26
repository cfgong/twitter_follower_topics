import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.Certificate("topic-tracker-e06e8-firebase-adminsdk-w30sj-17a4df2b46.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
# doc_ref = db.collection(u'trump').document(u'test')
# doc_ref.set({
#     u'count': 1,
# })



## List of Collections
twitter_handles = ['realDonaldTrump','ewarren','JoeBiden',
	'SenSanders','KamalHarris','CoryBooker','AndrewYang']

for h in twitter_handles:
	doc_ref = db.collection(h).document(u'test')
	doc_ref.set({
		u'count': 1
		})
