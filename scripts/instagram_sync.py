from ConfigParser import SafeConfigParser

import datetime
import json
import os
import os.path
import requests

from toast_tools import (
    get_img_from_url,
    split_on_sep,
)


parser = SafeConfigParser()
parser.read("instagram-sync.ini")

REDIRECT-URI = parser.get("instagram_api", "redirect_uri")
CLINET-ID = parser.get("instagram_api", "tumblr_consumer_key")
ACCESS_TOKEN = parser.get("instagram_api", "access_token")

BLOG_POSTS_DIR = parser.get('blog_setup', 'mount_point')
BLOG_IMG_DIR = parser.get('blog_setup', 'posts_img_dir')



# TODO will need to add scope to get likes
# https://www.instagram.com/developer/authorization/


def create_image_post_from_instagram(post):
    """
        Iterate through images.
        Get each format, rename for clarity.
        Create a post for post.
    """
    for image in post["images"]:
        url = post["images"][image]["url"]
        filename, file_extension = os.path.splitext('url')
        # remove cache paramiter
        clean_url = toast_tools.split_on_sep("?", url)
        # instagram-{id}-{image}.jpg
        image_title = "instagram-{}-{}{}".format(
            post["id"],
            image,
            file_extension)
        get_img_from_url(BLOG_IMG_DIR, image_title, clean_url)







# I don't think i can automate this?
auth_url = "https://api.instagram.com/oauth/authorize/?client_id={CLIENT-ID}&redirect_uri={REDIRECT-URI}&response_type=code".format(CLIENT-ID, REDIRECT-URI)

do_auth = request.get(auth_url)

# get my recent posts
recent_posts = "https://api.instagram.com/v1/users/self/media/recent/?access_token={}".format(ACCESS_TOKEN)

get_posts = response.get(recent_posts)

# insta api docs refer to this as an envelope
envelope = json.loads(get_posts.content)

for post in envelope["data"]:
    instagram_post_dict = {}
    
    # make a copy of everything
    for i in post:
        instagram_post_dict[i] = post[i]
    
    # make a title from post.title
    
    # TODO add to toast_tools
    # date is formated as unix timestamp
    formated_date = datetime.datetime.fromtimestamp(
        int(post["created_time"])
    ).strftime('%Y-%m-%d')
    
    post_date = (formated_date)

    # remove tags from display title
    title_wo_tags = toast_tools.split_on_sep("#", post["text"]).rstrip()

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

