"""Create sketchbook files from a list of images."""

import argparse
import os
import yaml

import toast_tools

# TODO add tests


def sort_image_list(list_to_sort):
    """Sort sketchbook images from 'make_image_list' to return."""
    sorted_image_list = toast_tools.sort_nicely(list_to_sort)

    # sort the various cover images properly
    # for example, back cover should be last

    if sorted_image_list[0] == "back cover":
        temp_item = sorted_image_list[0]
        sorted_image_list.pop(0)
        sorted_image_list.append(temp_item)

    if sorted_image_list[-1] == "ifc 001":
        temp_item = sorted_image_list[-1]
        sorted_image_list.pop(-1)
        sorted_image_list.insert(0, temp_item)

    if sorted_image_list[-1] == "front cover":
        temp_item = sorted_image_list[-1]
        sorted_image_list.pop(-1)
        sorted_image_list.insert(0, temp_item)

    return sorted_image_list


def make_image_list():
    """
    Find images for a given sketchbook and make a sorted list of them.

    Ignored names are files that will exist in the directory, that we don't
    want to include.
    """
    sb_image_files = []

    # make a list of ignored names
    ignored_name_1 = "{}-front-cover-icon.jpg".format(SB_URL_SAFE_NAME)
    ignored_name_2 = "{}_cover_icon.jpg".format(
        SB_URL_SAFE_NAME.replace("-", "_")
    )

    ignored_name_list = [".DS_Store", ignored_name_1, ignored_name_2]

    for root, dirs, files in os.walk(SB_IMAGE_DIR):
        for name in files:
            if root == SB_IMAGE_DIR:
                if name in ignored_name_list:
                    pass
                else:
                    # format the name before appending
                    strip_ext = name.replace(".jpg", "")
                    strip_base = strip_ext.replace(SB_URL_SAFE_NAME, "")
                    sb_numbers_only = strip_base.replace("-", " ").lstrip()
                    sb_image_files.append(sb_numbers_only)
    if len(sb_image_files) == 0:
        print "!!!!!!!!!!!! Nothing here?  Maybe a typo?"
        pass
    else:
        sorted_image_list = sort_image_list(sb_image_files)
        return sorted_image_list


def assemble_spreads(sorted_image_list):
    """Assemble spreads from a sorted_image_list."""
    spreads_list = []

    for i, item in enumerate(sorted_image_list):
        temp_spread_dict = {}
        spread = {}

        item_split = item.split()

        if item_split[1] == "cover":
            spread[item] = item.replace(" ", "-")
        else:
            print "---------- item_split is {}".format(item_split)
            spread["verso"] = item_split[0]
            spread["recto"] = item_split[1]

        temp_spread_dict["sb_display_name"] = SB_DISPLAY_NAME.title()
        temp_spread_dict["sb_url_safe_name"] = SB_URL_SAFE_NAME
        temp_spread_dict["spread"] = "{}".format(item.replace(" ", "-"))

        # build pagination
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

        spreads_list.append(temp_spread_dict)

    return spreads_list


def make_pages(spreads_list):
    """Build pages from a 'spreads_list'."""
    for item in spreads_list:
        spread_name = "{}-{}".format(
            SB_URL_SAFE_NAME, item["spread"].replace(" ", "-")
        )
        file_name = "{}.html".format(spread_name)

        item["all-data"] = spreads_list

        toast_tools.write_out_template(
            item,
            SB_DIR,
            file_name,
            "sb_page.mustache",
        )


def make_index(spreads_list):
    """Build index from a 'spreads_list'."""
    sb_dict = {}
    sb_dict["SB_DISPLAY_NAME"] = SB_DISPLAY_NAME
    sb_dict["SB_URL_SAFE_NAME"] = SB_URL_SAFE_NAME
    sb_dict["sb_spreads"] = spreads_list
    sb_dict["image_dir"] = SB_IMAGE_DIR
    sb_dict["html_dir"] = SB_DIR

    # grab top level metadata for index page
    try:
        # YAML files are in image dir. this is stable while built pages are not
        metadata_file_path = "{}/metadata/{}-index.yaml".format(
            SB_IMAGE_DIR, SB_URL_SAFE_NAME)
        print ".......... metadata_file_path = {}".format(metadata_file_path)
        with open(metadata_file_path, 'r') as metadata_file:
            metadata_file_obj = yaml.load(metadata_file)
            sb_dict["metadata"] = metadata_file_obj
            print ".......... found metadata for {} index".format(SB_URL_SAFE_NAME)
    except:
        print ".......... no metadata found for {} index".format(SB_DISPLAY_NAME)

    toast_tools.write_out_template(
        sb_dict,
        SB_DIR,
        "index.html",
        "sb_index.mustache"
    )


parser = argparse.ArgumentParser()
parser.add_argument("sb_name", help="The name of the sketchbook")

# TODO add param for single page sketchbooks

# TODO add param to override sb name when not same as dir name
# For example "perdef"
# OR use a config file per sb ?

# TODO logic to handle IFC
# Only old sketchbooks will start with ifc
# parser.add_argument("pages_start_on", help="Does the sketchbook start on 1 or ifc")

args = parser.parse_args()

# set up
SB_DISPLAY_NAME = args.sb_name.replace("-", " ")
SB_URL_SAFE_NAME = (args.sb_name.replace(" ", "-")).lower()
SB_IMAGE_DIR = os.path.dirname(
    "../image/sketchbooks/{}/".format(SB_URL_SAFE_NAME)
)

SB_DIR = "../sketchbooks/{}".format(SB_URL_SAFE_NAME)

print "========== SB_DISPLAY_NAME = {}".format(SB_DISPLAY_NAME)
print "========== SB_URL_SAFE_NAME = {}".format(SB_URL_SAFE_NAME)
print "========== SB_IMAGE_DIR = {}".format(SB_IMAGE_DIR)
print "========== SB_DIR is {}".format(SB_DIR)

if not os.path.exists(SB_DIR):
    os.makedirs(SB_DIR)
    print "---------- Created  {}".format(SB_DIR)

this_sorted_image_list = make_image_list()
this_spreads = assemble_spreads(this_sorted_image_list)
make_index(this_spreads)
make_pages(this_spreads)

print ".......... All Done!!!"
