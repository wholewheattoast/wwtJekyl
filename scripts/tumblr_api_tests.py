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

    #dictionary_formated = json.dumps(dictionary, sort_keys=False, indent=4, separators=(',', ': '))

    html_path = "{}/{}".format(path, file_name)
    html_file = open(html_path,"w")

    results_template = open("../_templates/{}.mustache".format(template)).read()

    html_results = pystache.render(results_template, dictionary)
    html_file.write(html_results)

    html_file.close()


# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
  'NvpHTpkowzT3I4FqoYaYE5UfHguJTl5rMtUcCWyi5hiqJqAwPL',
  'QK10sUUoA6osskA3vVgIz0lUdMM6OgrHgpbMpuDqlfRwZu17m8',
  '3ojJTqCtP7apBR681FhSRJfpYSgtDoCr9hiXShTrJNVIZO9cbI',
  'W8BaOGaabnQUrgTVZAly2TLRWo4Rrjz7HjLmm7rqmu4x0x81nA'
)

# Make the request
client.blog_info('wholewheattoast.tumblr.com')

# Authenticate via API Key
#client = pytumblr.TumblrRestClient('NvpHTpkowzT3I4FqoYaYE5UfHguJTl5rMtUcCWyi5hiqJqAwPL')


# To do  store the json somewhere?

tumblr_request = client.posts('wholewheattoast.tumblr.com', limit=10, notes_info=True, filter='html')

file_names = []

for i in tumblr_request["posts"]:
    temp_tumblr_slug = i["slug"]
    temp_date = (i["date"].split())
    temp_tumblr_date = temp_date[0]

    temp_formated_file_name = "{}-{}.html".format(temp_tumblr_date, temp_tumblr_slug)
    file_names.append(temp_formated_file_name)

# look up file name
mount_point = "../_posts/"

for i in file_names:
    temp_path = "{}{}".format(mount_point, i)
    if os.path.isfile(temp_path):
        print "{}  Post exists.".format(i)
    else:
        for i in tumblr_request["posts"]:
            # TODO handle other types of tumblr posts.
            if i["type"] == "photo":
                #pdb.set_trace()
                temp_file_dict = {}
                temp_file_dict["title"] = (i["slug"].replace("-", " "))
                temp_file_dict["tags"] = i["tags"]
                temp_file_dict["tumblr_url"] = i["post_url"]
                temp_file_dict["date"] = i["date"]
                try:
                    temp_file_dict["source_url"] = i["link_url"]
                except:
                    try:
                        temp_file_dict["source_url"] = i["post_url"]
                    except:
                        print "dunno?"
                temp_file_dict["caption"] = i["caption"]

                # Get the image.
                # Only getting the original size at this time.
                # Need to make img a list of photos and iterate
                
                temp_file_dict["photos"] = []
                
                for photo in i["photos"]:
                    if photo["original_size"]:
                        distinct_photo = {}
                        distinct_photo_tumblr_img = (photo["original_size"])["url"]
                        
                        distinct_photo["tumblr_img_url"] = distinct_photo_tumblr_img
                        distinct_photo["img"] = os.path.basename(distinct_photo_tumblr_img)

                        temp_file_object = urllib.URLopener()
                        
                        temp_file_object.retrieve(distinct_photo_tumblr_img, "../image/posts/{}".format(os.path.basename(distinct_photo_tumblr_img)))
                        
                        temp_file_dict["photos"].append(distinct_photo)

                temp_formated_file_name = "{}-{}.html".format(((i["date"].split())[0]), i["slug"])
                    
                write_out_template(temp_file_dict, "../_posts/", 
                    temp_formated_file_name, "tumblr_photo_post")
                print "Created {}".format(temp_formated_file_name)
            else:
                "Not a photo?"
