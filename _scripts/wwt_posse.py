from ConfigParser import SafeConfigParser
# import json
import pytumblr
# import pystache
import os
import os.path
# import pdb
# import urllib

parser = SafeConfigParser()
parser.read("tumblr_jekyll.ini")

TUMBLR_BLOG = parser.get('tumblr_api', 'tumblr_blog')
CONSUMER_KEY = parser.get('tumblr_api', 'tumblr_consumer_key')
CONSUMER_SECRET = parser.get('tumblr_api', 'tumblr_consumer_secret')
OAUTH_TOKEN = parser.get('tumblr_api', 'tumblr_oauth_token')
OAUTH_SECRET = parser.get('tumblr_api', 'tumblr_oauth_secret')

mount_point = "../_posts/"

client = pytumblr.TumblrRestClient(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    OAUTH_TOKEN,
    OAUTH_SECRET,
)

tumblr_request = client.posts(
    TUMBLR_BLOG,
    limit=10,
    notes_info=True,
    filter='html'
)

local_posts = []

# 1. check recent posts os walk put last 10 filenames in a list?
for root, sub_dirs, files in os.walk(mount_point):
    for filename in files:
        if filename.endswith(('.html', '.md')):
            local_posts.append(filename)
    
print "---------- local_posts = {}".format(local_posts)

# 2. make call to tumblr to see if alreay published
for post in tumblr_request["posts"]:
    post_formated_file_name = "{}-{}.html".format(
        (post["date"].split())[0],
        post["slug"]
    )
    
    post_path = "{}{}".format(mount_point, post_formated_file_name)
    
    print "---------- tumblr on tumblr = {}".format(post_path)

# 3. if not then publish posts

# order should be
# 1. post from here
# 2. then check there for new posts (from instagram or what not)
