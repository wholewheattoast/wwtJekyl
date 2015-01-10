import argparse
import pystache
import os
import time

import pdb
#pdb.set_trace()

# get values
parser = argparse.ArgumentParser()
parser.add_argument("sb_name", help="The name of the sketchbook")
parser.add_argument("pages_start_on", help="Does the sketchbook start on 1 or ifc")
args = parser.parse_args()

sb_url_safe_name = args.sb_name.replace(" ", "-")

# How to tell number of pages?
sb_image_dir = os.path.dirname("../image/sketchbooks/{}/".format(sb_url_safe_name))

# Going to have to remove bullshit files
# NAME_cover_icon.jpg
# NAME -cover-icon.jpg

# this may need to be a dict for order?
sb_image_files = []

for root, dirs, files in os.walk(sb_image_dir):
    for name in files:
        if root == sb_image_dir:
            if name == ".DS_Store":
                pass
            elif name == "{}-front-cover-icon.jpg".format(sb_url_safe_name):
                pass
            #egyptian_bun_cover_icon
            elif name == "{}_cover_icon.jpg".format(sb_url_safe_name.replace("-", "_")):
                pass
            else:
                striped_name = name.replace(".jpg", "")
                sb_image_files.append(striped_name)

print len(sb_image_files)
print ""
# may not need to do this
# though need to pad file numbers?
# to do so use zfill(3)
sorted_image_list = sorted(sb_image_files)
print sorted_image_list

# build directory
sb_directory = os.path.dirname("../sketchbooks/{}".format(sb_url_safe_name))

if not os.path.exists(sb_directory):
    os.makedirs(sb_directory)
    
    
# build pages
# build index