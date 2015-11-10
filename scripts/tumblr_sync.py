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

# should i get filter='raw' instead? 
# No!!! use html and strip when needed.
# this gives me formating on captions
tumblr_request = authed_client.posts(
    BLOG_URL,
    limit=40,
    notes_info=True,
    filter='html'
)

def get_photo(photo):
    print "---------- Getting {}".format(photo)
    file_object = urllib.URLopener()
    file_object.retrieve(
        photo, 
        "{}/{}".format(
            BLOG_IMG_DIR,
            os.path.basename(photo)
        )
    )


def create_photo_post(post):
    print "*" * 10
    for i in post:
        print u"{} = {}".format(i, post[i])
        print "\n"
    print "*" * 10
    
    # TODO how am i referencing primary img in template?
    # TODO do I need to handle tags in a certian way?
    # .. I don't think so?
    
    for photo in post["photos"]:
        if photo["original_size"]:
            distinct_photo_tumblr_img = (photo["original_size"])["url"]
            get_photo(distinct_photo_tumblr_img)
            # Do i need to store this image for the mustache template?
            
        elif photo["alt_sizes"]:
            for i in photo["alt_sizes"]
                distinct_photo_tumblr_img = (photo["original_size"])["url"]
                get_photo(distinct_photo_tumblr_img)
    
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
    
    # What do I do here if slug is empty?
    # Not sure if this is a good way to do this?
    if post[u"slug"] == "":
        # TODO strip html from caption here !!!
        this_post_title = (post[u"caption"].replace(" ", "-"))
    else:
        this_post_title = post[u"slug"]
        
    post_formated_file_name = u"{}-{}.html".format(
        post_date,
        this_post_title,
    )
    
    post_path = u"{}{}".format(BLOG_POSTS_DIR, post_formated_file_name)
    
    # Test if post already exists if it does not do stuff
    # should i make this a function?
    
    if os.path.isfile(post_path):
        print "========== {} already exists".format(
            post_formated_file_name
        )
    else:
        # TODO handle other types of tumblr posts.
        # Each post type as a function?
        if post["type"] == "photo":
            print u"========== Creating {}".format(post_formated_file_name)
            create_photo_post(tumblr_post_dict)
        else:
            print "========== {} is unsupported.".format(post["type"])
    
    
    
    
