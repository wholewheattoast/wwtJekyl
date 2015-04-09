import argparse
import pystache
import os
import time
import toast_tools

parser = argparse.ArgumentParser()
parser.add_argument("sb_name", help="The name of the sketchbook")

# Only old sketchbooks will start with ifc
# parser.add_argument("pages_start_on", help="Does the sketchbook start on 1 or ifc")
args = parser.parse_args()

sb_display_name = args.sb_name
sb_url_safe_name = args.sb_name.replace(" ", "-")

sb_image_dir = os.path.dirname(
    "../image/sketchbooks/{}/".format(sb_url_safe_name)
    )

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
                sb_numbers_only = strip_base.replace("-", " ").lstrip()
                sb_image_files.append(sb_numbers_only)

sorted_image_list = sorted(sb_image_files)

# Effectivaly send fc to front of list.
# This should leave bc (if exists) at end of list
sorted_image_list.insert(0, sorted_image_list.pop())

sb_directory = "../sketchbooks/{}".format(sb_url_safe_name)

print "-------------------- sb_dir is {}".format(sb_directory)

if not os.path.exists(sb_directory):
    os.makedirs(sb_directory)
    print "-------------------- Created  {}".format(sb_directory)

sb_dict = {}

spreads_list = []

for i, item in enumerate(sorted_image_list):
    temp_spread_dict = {}
    
    print "-------------------- i is {}".format(item)
    
    i_split = item.split()
    
    temp_spread_dict["sb_display_name"] = sb_display_name
    temp_spread_dict["sb_url_safe_name"] = sb_url_safe_name
    temp_spread_dict["spread"] = "{}".format(
        item.replace(" ", "-")
    )
    
    try:
        temp_spread_dict["next"] = "{}".format(
            (sorted_image_list[i + 1]).replace(" ", "-")
        )
    except IndexError:
        temp_spread_dict["next"] = "{}".format(
            (sorted_image_list[0]).replace(" ", "-")
        )

    try: 
        temp_spread_dict["prev"] = "{}".format(
            (sorted_image_list[i - 1]).replace(" ", "-")
        )
    except IndexError:
        print "woops index error on prev"
        
    
    temp_file_name = "{}-{}.html".format(
        sb_url_safe_name, item.replace(" ", "-")
    )
    
    toast_tools.write_out_template(
        temp_spread_dict, sb_directory, temp_file_name, "sb_page.mustache"
    )
    
    spreads_list.append(temp_spread_dict)


sb_dict["sb_display_name"] = sb_display_name
sb_dict["sb_url_safe_name"] = sb_url_safe_name
sb_dict["sb_spreads"] = spreads_list
sb_dict["image_dir"] = sb_image_dir
sb_dict["html_dir"] = sb_directory
# TODO count number of pages
#sb_dict["page_count"] = "?"
#sb_dict["sb_date_started"] = "?"
#sb_dict["sb_date_ended"] = "?"
#sb_dict["sb_dimensions"] = "?"


# Generate index file
# write_out_template(dictionary, path, file_name, template)

toast_tools.write_out_template(sb_dict, sb_directory, "index.html", "sb_index.mustache")
