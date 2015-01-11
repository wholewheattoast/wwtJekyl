import argparse
import pystache
import os
import time
import toast_tools

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
            elif name == "{}_cover_icon.jpg".format(sb_url_safe_name.replace("-", "_")):
                pass
            else:
                strip_ext = name.replace(".jpg", "")
                strip_base = strip_ext.replace(sb_url_safe_name, "")
                
                sb_numbers_only = strip_base.replace("-pp-", "")
                sb_image_files.append(sb_numbers_only)

print len(sb_image_files)
print ""
# may not need to do this
# though need to pad file numbers?
# to do so use zfill(3)
sorted_image_list = sorted(sb_image_files)
print sorted_image_list

# create sb dir
sb_directory = os.path.dirname("../sketchbooks/{}".format(sb_url_safe_name))

if not os.path.exists(sb_directory):
    os.makedirs(sb_directory)
    
    
# build pages
# Iterate through and build a dictionary
# make it json
# render with pystache, keep the template out of here
# one template for pages, one for index
# may only need a single dict

sb_dict = {}

spreads_list = []

for i in sorted_image_list:
    temp_spread_dict = {}
    
    i_without_dash = i.format("-", " ")
    i_split = i.split()
    
    temp_spread_dict["spread_name"] = "{}-pp-{}".format(sb_url_safe_name,i)
    # need to be able to deal w fc and bc images here
    temp_spread_dict["left_page_number"] = i_split[0]
    temp_spread_dict["right_page_numer"] = i_split[1]
#    temp_spread_dict["prev_spread"] = ?
#    temp_spread_dict["next_spread"] = ?
    spreads_list.append(temp_spread_dict)

# Flesh out sb_dict

sb_dict["sb_name"] = sb_url_safe_name
sb_dict["sb_spreads"] = spreads_list
sb_dict["page_count"] = "?"
#sb_dict["sb_date_started"] = "?"
#sb_dict["sb_date_ended"] = "?"
#sb_dict["sb_dimensions"] = "?"


# generate index

# write_out_template(dictionary, path, file_name, template)

sb_index_template = "../_templates/sb_index.mustache"

toast_tools.write_out_template(sb_dict, sb_directory, index, sb_index_template)


