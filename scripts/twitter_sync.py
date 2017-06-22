from ConfigParser import SafeConfigParser

import twitter

# import toast_tools

parser = SafeConfigParser()
parser.read("twitter-sync.ini")

CONSUMER_KEY = parser.get('twitter_api', 'api_key')
CONSUMER_SECRET = parser.get('twitter_api', 'api_secret')
ACCESS_TOKEN = parser.get('twitter_api', 'access_token')
ACCESS_TOKEN_SECRET = parser.get('twitter_api', 'access_token_secret')

USER = 'wholewheattoast'

api = twitter.Api(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token_key=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# could store the id of last entry somewhere and check against that?
# For now don't include rt's
statuses = api.GetUserTimeline(
    screen_name=USER, include_rts=False, count=100
)
# print([s.text for s in statuses])
for s in statuses:
    # I'm already getting instagram content elsewhere
    if not s.source == '<a href="http://instagram.com" rel="nofollow">Instagram</a>':
        print s.created_at
        print s.text

# TODO grab details of tweet
# and then export to a template like insta and tumblr
