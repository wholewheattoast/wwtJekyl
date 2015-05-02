import pytumblr
import os.path
import pystache
import json
import urllib
import pdb

def write_out_template(dictionary, path, file_name, template):
    """
        Read in json of a post.
        Render the template and save an html file.
    """

    html_path = "{}/{}".format(path, file_name)
    html_file = open(html_path,"w")

    results_template = open("../_templates/{}.mustache".format(template)).read()

    html_results = pystache.render(results_template, dictionary)
    html_file.write(html_results)

    html_file.close()

pdb.set_trace()

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
  'NvpHTpkowzT3I4FqoYaYE5UfHguJTl5rMtUcCWyi5hiqJqAwPL',
  'QK10sUUoA6osskA3vVgIz0lUdMM6OgrHgpbMpuDqlfRwZu17m8',
  '3ojJTqCtP7apBR681FhSRJfpYSgtDoCr9hiXShTrJNVIZO9cbI',
  'W8BaOGaabnQUrgTVZAly2TLRWo4Rrjz7HjLmm7rqmu4x0x81nA'
)

client.blog_info('wholewheattoast.tumblr.com')

# TODO store the json somewhere?

tumblr_request = client.posts(
    'wholewheattoast.tumblr.com',
    limit=10,
    notes_info=True,
    filter='html'
)

mount_point = "../_posts/"

for post in tumblr_request["posts"]:

    # Test if post already exists
    tumblr_post_slug = post["slug"]
    tumblr_post_date = (post["date"].split())[0]
    post_formated_file_name = "{}-{}.html".format(tumblr_post_date, tumblr_post_slug)
    post_path = "{}{}".format(mount_point, post_formated_file_name)
    if os.path.isfile(post_path):
        print "Post exists:  {}".format(post_formated_file_name)
    else:
        # TODO handle other types of tumblr posts.
        # Each post type as a function?
        if post["type"] == "photo":
            temp_file_dict = {}
            temp_file_dict["title"] = (post["slug"].replace("-", " "))
            temp_file_dict["tags"] = post["tags"]
            temp_file_dict["tumblr_url"] = post["post_url"]
            temp_file_dict["date"] = post["date"]
            try:
                temp_file_dict["source_url"] = post["link_url"]
            except:
                try:
                    temp_file_dict["source_url"] = post["post_url"]
                except:
                    print "dunno?"
            temp_file_dict["caption"] = post["caption"].encode("utf-8")
            
            temp_file_dict["photos"] = []
            
            for photo in post["photos"]:
                if photo["original_size"]:
                    distinct_photo = {}
                    distinct_photo_tumblr_img = (photo["original_size"])["url"]
                    
                    distinct_photo["tumblr_img_url"] = distinct_photo_tumblr_img
                    distinct_photo["img"] = os.path.basename(distinct_photo_tumblr_img)

                    temp_file_object = urllib.URLopener()
                    
                    temp_file_object.retrieve(distinct_photo_tumblr_img, "../image/posts/{}".format(os.path.basename(distinct_photo_tumblr_img)))
                    
                    temp_file_dict["photos"].append(distinct_photo)

            temp_formated_file_name = "{}-{}.html".format(((post["date"].split())[0]), post["slug"])
                
            write_out_template(temp_file_dict, "../_posts/", 
                temp_formated_file_name, "tumblr_photo_post")
            print "Created:  {}".format(temp_formated_file_name)
        else:
            "Not a photo?"
