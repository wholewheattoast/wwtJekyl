from ConfigParser import SafeConfigParser

import datetime
import json
import os
import os.path
import requests

import toast_tools


parser = SafeConfigParser()
parser.read("instagram-sync.ini")

REDIRECT_URI = parser.get("instagram_api", "redirect_uri")
CLIENT_ID = parser.get("instagram_api", "client_id")
ACCESS_TOKEN = parser.get("instagram_api", "access_token")

BLOG_POSTS_DIR = parser.get('blog_setup', 'mount_point')
BLOG_IMG_DIR = parser.get('blog_setup', 'posts_img_dir')
POSTS_ARCHIVE = parser.get('blog_setup', 'posts_archive')


# TODO upgrade script to python 3


def munge_instagram_images(post, image):
    """
        formating urls to get paths
        save local path info to post
        initiate image download
    """
    # TODO it would be nice to read full_resolution img enough to get
    # dimensions and store these
    url = post["images"][image]["url"]
    # remove cache parameter
    clean_url = toast_tools.split_on_sep("?", url)
    filename, file_extension = os.path.splitext(clean_url)
    image_path = u"{}/instagram-{}-{}{}".format(
        BLOG_IMG_DIR,
        post["id"],
        image,
        file_extension)
    post["images"][image]["local"] = "instagram-{}-{}{}".format(
        post["id"],
        image,
        file_extension)
    toast_tools.get_img_from_url(image_path, clean_url)


def try_for_full_resolution_url(post):
    """
        Attempt to get full_resolution url from instagram.

        Instagram doesn't supply the full resolution image so I have to guess.
    """
    import os
    import requests

    insta_img_endpoint = "https://scontent.cdninstagram.com/t51.2885-15/"
    url = post["images"]["standard_resolution"]["url"]
    url_basename = os.path.basename(url)

    full_res_url = "{}{}".format(insta_img_endpoint, url_basename)
    r = requests.get(full_res_url)
    if r.status_code == 200:
        post["images"]["full_resolution"] = {}
        post["images"]["full_resolution"]["url"] = full_res_url
        munge_instagram_images(post, "full_resolution")
    else:
        print "!!!!!!!!!! HTTP {}".format(r.status_code)
        print ".......... Possibly Instagram has not provided a full res img"
        print "\n"


def create_image_post_from_instagram(post, file_name):
    """
        Iterate through images.
        Get each format, rename for clarity.
        Create a post for post.
    """

    # images taken inside instagram seem to be capped at 640 x 640 and
    # do not appear to get a "full_resolution" image.
    try_for_full_resolution_url(post)

    for image in post["images"]:
        munge_instagram_images(post, image)

    # Not sure ATM how to deal with unicode in liquid? str them for now.
    formated_tags = []
    for i in post["tags"]:
        formated_tags.append(str(i))
    post["formated_tags"] = formated_tags

    # save a copy of the edited json
    edited_post_archive_file_path = u"{}_edited/{}.json".format(
        POSTS_ARCHIVE, formated_file_name)
    with open(edited_post_archive_file_path, "w") as f:
        json.dump(post, f)

    toast_tools.write_out_template(
        post,
        BLOG_POSTS_DIR,
        file_name,
        "instagram_image_post.mustache"
    )


def format_post_title_and_dates(post):
    post_converted_dt = datetime.datetime.fromtimestamp(
        int(post["created_time"]))

    # TODO What timezone this is in?
    post["display_date"] = post_converted_dt.strftime('%Y-%m-%d %H:%M:%S')

    # remove tags from display title.
    # also removing quotation marks due to issues with yaml headers.
    # was issue where an emoji followed a quoted sting.
    title_wo_tags = toast_tools.split_on_sep(
        "#", post[u"caption"][u"text"]).replace('"', '').rstrip()

    # make a version of caption test w/o tags here
    # since i don't want 'id' for post caption
    if len(title_wo_tags) > 0:
        post[u"caption"][u"cleaned_text"] = title_wo_tags
    # if post has no title (for file name)
    if len(title_wo_tags) == 0:
        title_wo_tags = post["id"]

    post[u"title"] = title_wo_tags

    # clean up title
    # tumblr tunc-ed around 48 chars
    cleaned_title = toast_tools.clean_string(title_wo_tags).replace(" ", "-").lower()[0:48]

    formated_file_name = u"{}-{}.html".format(
        post_converted_dt.strftime('%Y-%m-%d'),
        cleaned_title
    )

    title_wo_tags, formated_file_name, post_converted_dt
    return post, formated_file_name


# get my recent posts
recent_posts = "https://api.instagram.com/v1/users/self/media/recent/?access_token={}".format(ACCESS_TOKEN)

get_recent_posts = requests.get(recent_posts)

# instagram api docs refer to this as an envelope
envelope = json.loads(get_recent_posts.content)


if envelope['meta']['code'] != 200:
    print "!!!!!!!!!! client returned {}".format(envelope['meta']['code'])
    if envelope['meta']['error_type']:
        print "!!!!!!!!!! {}".format(envelope['meta']['error_type'])
        print "!!!!!!!!!! {}".format(envelope['meta']['error_message'])
else:
    for post in envelope["data"]:
        updated_post, formated_file_name = format_post_title_and_dates(post)

        # save a copy of the original json
        # TODO consider adding a timestamp to title to keep historical records
        post_archive_file_path = u"{}/{}.json".format(
            POSTS_ARCHIVE, formated_file_name)
        with open(post_archive_file_path, "w") as f:
            json.dump(post, f)

        post_path = u"{}/{}".format(BLOG_POSTS_DIR, formated_file_name)

        if os.path.isfile(post_path):
            print u"========== Already exists: {} ".format(formated_file_name)
        else:
            if updated_post["type"] == "image":
                print u"========== Creating: {}".format(formated_file_name)
                create_image_post_from_instagram(
                    updated_post, formated_file_name)
            else:
                print "********** {} is unsupported.".format(
                    updated_post["type"])
