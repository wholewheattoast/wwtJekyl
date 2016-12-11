from ConfigParser import SafeConfigParser

import os.path
import pystache
import pytumblr
import re
import requests


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


def write_out_template(dictionary, path, file_name, template):
    """
        Render the dictionary using the given template
        Save the file with file_name
        to the location specified by the path
    """
    html_path = "{}/{}".format(path, file_name)
    results_template = open("../_templates/{}".format(template)).read()
    html_results = pystache.render(results_template, dictionary)
    # need to encode to pass to write()
    html_results_encoded = html_results.encode(
        encoding='UTF-8', errors='strict'
    )

    with open(html_path, "w") as html_file:
        html_file.write(html_results_encoded)


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
