import argparse
import pystache
import os
import time
import toast_tools

parser = argparse.ArgumentParser()
parser.add_argument("sb_name", help="The name of the sketchbook")

# Only old sketchbooks will start with ifc
parser.add_argument("pages_start_on", help="Does the sketchbook start on 1 or ifc")
args = parser.parse_args()

sb_url_safe_name = args.sb_name.replace(" ", "-")

sb_image_dir = os.path.dirname("../image/sketchbooks/{}/".format(sb_url_safe_name))

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
                
                # I plan on dropping this pp nonsesense
                sb_numbers_only = strip_base.replace("-pp-", "")
                sb_image_files.append(sb_numbers_only)


sorted_image_list = sorted(sb_image_files)
print sorted_image_list

sb_directory = "../sketchbooks/{}".format(sb_url_safe_name)

print "-------------------- sb_dir is {}".format(sb_directory)

if not os.path.exists(sb_directory):
    os.makedirs(sb_directory)
    print "-------------------- Created  {}".format(sb_directory)

sb_dict = {}

spreads_list = []

for i in sorted_image_list:
    temp_spread_dict = {}
    
    i_without_dash = i.replace("-", " ")
    
    i_split = i_without_dash.split()
    
    # Drop the pp ???
    # sketchbook_name-6-7 is clear enough
    # will need to rename images to match for existing
    temp_spread_dict["spread_name"] = "{}-pp-{}".format(sb_url_safe_name,i)
    
    try:
        temp_spread_dict["left_page_number"] = i_split[0]
        temp_spread_dict["right_page_numer"] = i_split[1]
    except IndexError:
        # TODO test for fc, ifc, ibc, bc
        print "is this fc or ???"
    except:
        print "error"
    
    # Maybe I can just render the pages here and only iterate once
    spreads_list.append(temp_spread_dict)

# Flesh out sb_dict metadata

sb_dict["sb_name"] = sb_url_safe_name
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

sb_index_template = "sb_index.mustache"

toast_tools.write_out_template(sb_dict, sb_directory, "index.html", sb_index_template)

# TODO write out individual pages
# use spreads_list
