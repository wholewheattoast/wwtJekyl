import pytumblr
import os.path

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

tumblr_request = client.posts('wholewheattoast.tumblr.com', limit=10, notes_info=True, filter='html')

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
        # make the entry
        print "False"