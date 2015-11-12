from ConfigParser import SafeConfigParser
import json
import os.path
import pytumblr
import pystache
import urllib

def write_out_template(dictionary, path, file_name, template):
    """
        Read in json of a post.
        Render the template and save an html file.
    """

    html_path = "{}/{}".format(path, file_name)
    html_file = open(html_path,"w")

    results_template = open("../_templates/{}.mustache".format(template)).read()

    html_results = pystache.render(
        results_template, 
        dictionary, 
        string_encoding='utf-8', 
        file_encoding='utf-8'
    )
    
    html_file.write(html_results)

    html_file.close()

# Authenticate via OAuth
parser = SafeConfigParser()
parser.read("tumblr_jekyll.ini")

TUMBLR_BLOG = parser.get('tumblr_api', 'tumblr_blog')
CONSUMER_KEY = parser.get('tumblr_api', 'tumblr_consumer_key')
CONSUMER_SECRET = parser.get('tumblr_api', 'tumblr_consumer_secret')
OAUTH_TOKEN = parser.get('tumblr_api', 'tumblr_oauth_token')
OAUTH_SECRET = parser.get('tumblr_api', 'tumblr_oauth_secret')
MNT_PNT = parser.get('tumblr_api', 'mount_point')

client = pytumblr.TumblrRestClient(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    OAUTH_TOKEN,
    OAUTH_SECRET,
)

client.blog_info('wholewheattoast.tumblr.com')

tumblr_request = client.posts(
    'wholewheattoast.tumblr.com',
    limit=10,
    notes_info=True,
    filter='html'
)

for post in tumblr_request["posts"]:
    # Gather some useful information
    tumblr_post_type = post["type"]
    tumblr_post_id = post["id"]
    tumblr_post_tags = post["tags"]
    tumblr_post_date = post["date"]
    tumblr_post_format = post["format"]
    tumblr_post_slug = post["slug"]
    tumblr_post_date = (post["date"].split())[0]
    
    post_formated_file_name = "{}-{}.html".format(tumblr_post_date, tumblr_post_slug)
    
    post_path = "{}{}".format(MNT_PNT, post_formated_file_name)
    
    # Test if post already exists
    if os.path.isfile(post_path):
        print "Post exists:  {}".format(post_formated_file_name)
    else:
        # TODO handle other types of tumblr posts.
        # Each post type as a function?
        if post["type"] == "photo":
            temp_file_dict = {}
            
            temp_file_dict["title"] = (post["slug"].replace("-", " "))
            temp_file_dict["tumblr_url"] = post["post_url"]
            #temp_file_dict["img_permalink"] = post["image_permalink"]
            temp_file_dict["tumblr_post_type"] = post["type"]
            temp_file_dict["tumblr_post_id"] = post["id"]
            temp_file_dict["caption"] = post["caption"]
            temp_file_dict["date"] = post["date"]
            temp_file_dict["format"] = post["format"]
            temp_file_dict["tumblr_slug"] = post["slug"]
            
            # format tags
            formated_tags = []
            
            for i in post["tags"]:
                formated_tags.append(str(i))
                
            temp_file_dict["tags"] = formated_tags
                
            try:
                temp_file_dict["source_url"] = post["link_url"]
            except:
                try:
                    temp_file_dict["source_url"] = post["post_url"]
                except:
                    print "dunno?"
            
            temp_file_dict["photos"] = []
            
            for photo in post["photos"]:
                if photo["original_size"]:
                    distinct_photo = {}
                    distinct_photo_tumblr_img = (photo["original_size"])["url"]
                    
                    distinct_photo["tumblr_img_url"] = distinct_photo_tumblr_img
                    distinct_photo["img"] = os.path.basename(
                        distinct_photo_tumblr_img
                    )

                    temp_file_object = urllib.URLopener()
                    
                    temp_file_object.retrieve(
                        distinct_photo_tumblr_img, 
                        "../image/posts/{}".format(os.path.basename(distinct_photo_tumblr_img))
                    )
                    
                    temp_file_dict["photos"].append(distinct_photo)

            temp_formated_file_name = u'{}-{}.html'.format(
                ((post["date"].split())[0]), 
                post["slug"]
            )
                
            write_out_template(
                temp_file_dict,
                "../_posts/",
                temp_formated_file_name,
                "tumblr_photo_post"
            )
            
            print "Created:  {}".format(temp_formated_file_name)
        else:
            "Not a photo?"
