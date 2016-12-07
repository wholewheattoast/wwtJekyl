from ConfigParser import SafeConfigParser

import datetime
import json
import os
import os.path
import requests

import toast_tools

import pdb



parser = SafeConfigParser()
parser.read("instagram-sync.ini")

REDIRECT_URI = parser.get("instagram_api", "redirect_uri")
CLIENT_ID = parser.get("instagram_api", "client_id")
ACCESS_TOKEN = parser.get("instagram_api", "access_token")

BLOG_POSTS_DIR = parser.get('blog_setup', 'mount_point')
BLOG_IMG_DIR = parser.get('blog_setup', 'posts_img_dir')


def create_image_post_from_instagram(post):
    """
        Iterate through images.
        Get each format, rename for clarity.
        Create a post for post.
    """
    for image in post["images"]:
        url = post["images"][image]["url"]
        # remove cache paramiter
        clean_url = toast_tools.split_on_sep("?", url)
        filename, file_extension = os.path.splitext(clean_url)
        # instagram-{id}-{image}.jpg
        image_path = "{}/instagram-{}-{}{}".format(
            BLOG_IMG_DIR,
            post["id"],
            image,
            file_extension)
        toast_tools.get_img_from_url(image_path, clean_url)
    # TODO after getting images write out html with a template file
    # TODO check if I can use existing write_out_template()


# TODO set up some way on sever to re auth?
# I don't think i can automate this?

# 
# do_auth = request.get(auth_url)

# auth dace
# TODO will need to add scope to get likes
# https://www.instagram.com/developer/authorization/
# 1. Step One: Direct your user to our authorization URL
# auth_url = "https://api.instagram.com/oauth/authorize/?client_id=CLIENT-ID&redirect_uri=REDIRECT-URI&response_type=code"

# auth_url = "https://api.instagram.com/oauth/authorize/?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code".format(CLIENT_ID, REDIRECT_URI)

# https://api.instagram.com/oauth/authorize/?client_id=ff3becfe4fbf4097a044d4ab142d7b06&redirect_uri=https://www.wholewheattoast.com&response_type=code

# 2. Step Two: Receive the redirect from Instagram
redirect_code = parser.get("instagram_api", "redirect_code")

# 3. Step Three: Request the access_token
# curl -F 'client_id=CLIENT_ID' \
#     -F 'client_secret=CLIENT_SECRET' \
#     -F 'grant_type=authorization_code' \
#     -F 'redirect_uri=AUTHORIZATION_REDIRECT_URI' \
#     -F 'code=CODE' \
#     https://api.instagram.com/oauth/access_token

# get my recent posts
recent_posts = "https://api.instagram.com/v1/users/self/media/recent/?access_token={}".format(ACCESS_TOKEN)

get_recent_posts = requests.get(recent_posts)

# insta api docs refer to this as an envelope
envelope = json.loads(get_recent_posts.content)


if envelope['meta']['code'] != 200:
    print "!!!!!!!!!! client returned {}".format(envelope['meta']['code'])
    if envelope['meta']['error_type']:
        print "!!!!!!!!!! {}".format(envelope['meta']['error_type'])
        print "!!!!!!!!!! {}".format(envelope['meta']['error_message'])
else:
    for post in envelope["data"]:
        instagram_post_dict = {}
        
        # make a copy of everything
        for i in post:
            instagram_post_dict[i] = post[i]
        
        # make a title from post.title
        # TODO add to toast_tools ?
        # date is formated as unix timestamp
        formated_date = datetime.datetime.fromtimestamp(
            int(post["created_time"])
        ).strftime('%Y-%m-%d')
        
        post_date = (formated_date)

        # remove tags from display title
        title_wo_tags = toast_tools.split_on_sep(
            "#", post["caption"]["text"]).rstrip()
        # check if title
        if len(title_wo_tags) == 0:
            title_wo_tags = "untitled"

        post_formated_file_name = u"{}-{}.html".format(post_date, title_wo_tags)
        post_path = u"{}/{}".format(BLOG_POSTS_DIR, post_formated_file_name)
        
        # TODO how to format same as old tumblr posts???
        if os.path.isfile(post_path):
            print "========== Already exists: {} ".format(post_formated_file_name)
        else:
            if post["type"] == "image":
                create_image_post_from_instagram(post)
            else:
                print "********** {} is unsupported.".format(post["type"])

