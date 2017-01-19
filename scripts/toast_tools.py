from ConfigParser import SafeConfigParser

import json
import os
import os.path
import pystache
import pytumblr
import re
import requests
import sys


def auth_tumblr(config):
    # Authenticate via OAuth
    parser = SafeConfigParser()
    parser.read("tumblr_jekyll.ini")

    CONSUMER_KEY = parser.get('tumblr_api', 'tumblr_consumer_key')
    CONSUMER_SECRET = parser.get('tumblr_api', 'tumblr_consumer_secret')
    OAUTH_TOKEN = parser.get('tumblr_api', 'tumblr_oauth_token')
    OAUTH_SECRET = parser.get('tumblr_api', 'tumblr_oauth_secret')

    client = pytumblr.TumblrRestClient(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        OAUTH_TOKEN,
        OAUTH_SECRET,
    )

    return client


def write_out_json(thing, directory, fn):
    """
        JSON Load a 'thing'
        Write to 'dir'/'filename'
    """
    results_path = "{}/json".format(directory)
    results_json = "{}.json".format(fn)
    fullpath = "{}/{}".format(results_path, results_json)

    if not os.path.exists(results_path):
        os.makedirs(results_path)
        print ".......... Created  {}".format(results_path)

    try:
        loaded_json = json.dumps(thing)
        with open(fullpath, "w") as json_results_file:
            json_results_file.write(loaded_json)
            print ".......... Wrote out {}".format(results_json)
    except ValueError as e:
        print ".......... ValueError {}".format(e)
        print "!!!!!!!!!! {}".format(thing)
    except:
        print ".......... Unexpected error:", sys.exc_info()[0]


def write_out_template(dictionary, path, fn, template):
    """
        Render the dictionary using the given template
        Save the file with file_name
        to the location specified by the path
    """
    html_path = u"{}/{}".format(path, fn)
    results_template = open("../_templates/{}".format(template)).read()
    html_results = pystache.render(results_template, dictionary)
    # need to encode to pass to write()
    html_results_encoded = html_results.encode(
        encoding='UTF-8', errors='strict'
    )

    with open(html_path, "w") as html_file:
        html_file.write(html_results_encoded)
        print ".......... Wrote out  {}".format(html_path)


def sort_nicely(l):
    """
        Sort the given list in the way that humans expect.
        From http://nedbatchelder.com/blog/200712.html#e20071211T054956
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    l.sort(key=alphanum_key)

    return l


def split_on_sep(seperator, thing):
    result = thing.split(seperator, 1)[0]
    return result


def get_img_from_url(image_path, url):
    if os.path.isfile(image_path):
        print "---------- Already downloaded {}".format(url)
    else:
        print "---------- Downloading {}".format(url)
        with open(image_path, 'w') as f:
            f.write(requests.get(url).content)


def clean_string(dirty_string):
    import string
    import re

    chars = re.escape(string.punctuation)
    clean_string = re.sub(r'['+chars+']', '', dirty_string)
    clean_string.lstrip().rstrip()
    return clean_string
