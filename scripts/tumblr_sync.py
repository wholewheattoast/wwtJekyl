from ConfigParser import SafeConfigParser

import os.path
import urllib

import pytumblr

from toast_tools import (
    auth_tumblr,
    write_out_template,
)

parser = SafeConfigParser()
parser.read("tumblr_jekyll.ini")

BLOG_URL = parser.get('blog_setup', 'tumblr_blog')
BLOG_POSTS_DIR = parser.get('blog_setup', 'mount_point')
BLOG_IMG_DIR = parser.get('blog_setup', 'posts_img_dir')

authed_client = auth_tumblr('tumblr_jekyll.ini')

tumblr_request = authed_client.posts(
    BLOG_URL,
    limit=40,
    notes_info=True,
    filter='html'
)

def get_photo(photo):
    photo_path = "{}/{}".format(
            BLOG_IMG_DIR,
            os.path.basename(photo)
        )
        
    if os.path.isfile(photo_path):
        print "---------- {} already downloaded.".format(photo)
    else:
        file_object = urllib.URLopener()
        file_object.retrieve(photo, photo_path)


def create_photo_post(post):
    for photo in post["photos"]:
        if photo["original_size"]:
            distinct_photo_tumblr_img = (photo["original_size"])["url"]
            get_photo(distinct_photo_tumblr_img)
            original_size_local = os.path.basename(distinct_photo_tumblr_img)
            post["img"] = original_size_local

    write_out_template(
        post,
        BLOG_POSTS_DIR,
        post_formated_file_name,
        "tumblr_photo_post"
    )


for post in tumblr_request["posts"]:
    tumblr_post_dict = {}
    
    # Let's store *everything*
    for i in post:
        tumblr_post_dict[i] = post[i]

    post_date = (post["date"].split())[0]

    if post[u"slug"] == "":
        tumblr_post_dict["title"] = post[u"id"]
    else:
        tumblr_post_dict["title"] = post[u"slug"]

    post_formated_file_name = u"{}-{}.html".format(
        post_date,
        tumblr_post_dict["title"],
    )
    
    post_path = u"{}/{}".format(BLOG_POSTS_DIR, post_formated_file_name)
    
    if os.path.isfile(post_path):
        print "========== {} already exists".format(post_formated_file_name)
    else:
        if post["type"] == "photo":
            print u"========== Creating {}".format(post_formated_file_name)
            create_photo_post(tumblr_post_dict)
        # TODO handle other types of tumblr posts.
        else:
            print "========== {} is unsupported.".format(post["type"])
            
            