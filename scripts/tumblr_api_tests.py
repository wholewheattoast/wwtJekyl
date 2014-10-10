import pytumblr
import os
import os.path
import pystache
import json
import urllib
import tempfile

import pdb

# Write out the template
def write_out_template(dictionary, path, file_name, template):
    dictionary_formated = json.dumps(dictionary, sort_keys=False, indent=4, separators=(',', ': '))

    print "formated****"
    print dictionary_formated

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

tumblr_request = client.posts('wholewheattoast.tumblr.com', limit=1, notes_info=True, filter='html')

file_names = []

for i in tumblr_request["posts"]:
    temp_tumblr_slug = i["slug"]
    temp_date = (i["date"].split())
    temp_tumblr_date = temp_date[0]

    temp_formated_file_name = "{}-{}.html".format(temp_tumblr_date, temp_tumblr_slug)
    file_names.append(temp_formated_file_name)

print file_names

# look up file name
mount_point = "../_posts/"
for i in file_names:
    temp_path = "{}{}".format(mount_point, i)
    print temp_path
    if os.path.isfile(temp_path):
        print "Post exists"
    else:
        # TODO Get the relevent parts
        for i in tumblr_request["posts"]:
            if i["type"] == "photo":
                temp_file_dict = {}
                temp_file_dict["title"] = (i["slug"].replace("-", " "))
                temp_file_dict["tags"] = i["tags"]
                temp_file_dict["tumblr_url"] = i["post_url"]
                temp_file_dict["date"] = i["date"]
                temp_file_dict["source_url"] = i["link_url"]
                temp_file_dict["caption"] = i["caption"]

                # Get the image
                for thing in i["photos"]:
                    if thing["original_size"]:
                        temp_tumblr_org_img_url = (thing["original_size"])["url"]
                        temp_file_dict["tumblr_img_url"] =(thing["original_size"])["url"]
                        temp_tumblr_img = os.path.basename(temp_tumblr_org_img_url)
                        temp_file_dict["img"] = os.path.basename(temp_tumblr_org_img_url)
                        temp_file_object = urllib.URLopener()
                        temp_file_object.retrieve(temp_tumblr_org_img_url, "../image/posts/{}".format(temp_tumblr_img))

                print temp_file_dict

                # write file
                temp_formated_file_name = "{}-{}.html".format(((i["date"].split())[0]), i["slug"])
                write_out_template(temp_file_dict, "../_posts/", temp_formated_file_name, "tumblr_photo_post")
            else:
                "Not a photo?"
