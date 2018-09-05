"""Create sketchbook files from a list of images."""

import argparse
import os
import yaml

from sketchbook_tools import (
    assemble_spreads,
    create_dir_if_not_exists,
    sb_display_name,
    sb_url_safe_name,
    sort_image_list,
    sb_image_dir,
)

from toast_tools import (
    write_out_template,
)


THE_BIG_LIST = [
    "garbage-filter",
    "pci",
    "pretty-lady",
    "sausage-barrier",
]


def make_sorted_image_list(sb_img_dir_path, url_safe_name):
    """
    Walk `sb_img_dir_path` and build a sorted list of image page numbers.

    sb_img_dir_path: Path where images are stored
    url_safe_name: Name of sketchbook as it's represented in file name
    Ignored names are files that will exist in the directory, that we don't
    want to include.
    """
    # make a list of ignored names
    # TODO can i put this somewhere else?  feels sloppy?
    # TODO I could convert these if i use a filter below
    # if thing_to_ignore not in name append(name)
    ignored_name_1 = "{}-front-cover-icon.jpg".format(url_safe_name)
    ignored_name_2 = "{}_cover_icon.jpg".format(
        url_safe_name.replace("-", "_")
    )

    ignored_name_list = [".DS_Store", ignored_name_1, ignored_name_2]

    sb_image_files = []
    # change to `strip` on '.' offloads need for template to understand format
    for root, dirs, files in os.walk(sb_img_dir_path):
        for name in files:
            if root == sb_img_dir_path and name not in ignored_name_list:
                # format the name before appending
                sb_numbers_only = name.split(".")[0] \
                                      .replace(url_safe_name, "") \
                                      .replace("-", " ") \
                                      .lstrip()
                sb_image_files.append(sb_numbers_only)
            else:
                pass
    # sanity check output
    if len(sb_image_files) == 0:
        print("!!!!!!!!!!!! Nothing here?  Maybe a typo?")
        pass
    else:
        # TODO when i'm less tired rewrite with filter
        # TODO should I do this above?
        filtered_list = []
        for item in sb_image_files:
            if " thumb" not in item and "@2x" not in item:
                filtered_list.append(item)
        sorted_image_list = sort_image_list(filtered_list)
        return sorted_image_list


def make_pages(sketchbook, spreads_list):
    """Build pages for sb named `sketchbook`from a 'spreads_list'."""
    for item in spreads_list:
        spread_name = "{}-{}".format(
            sb_url_safe_name(sketchbook),
            item["spread"].replace(" ", "-")
        )
        file_name = "{}.html".format(spread_name)

        item["all-data"] = spreads_list

        write_out_template(
            item,
            "../sketchbooks/{}".format(sb_url_safe_name(sketchbook)),
            file_name,
            "sb_page.mustache",
        )


def make_index(sketchbook, spreads_list):
    """
    Build a sketchbook's index page.

    sketchbook: Name of sketchbook
    spreads_list: list of sketchbook page spreads in order
    """
    sb_dict = {}
    sb_dict["sb_display_name"] = sb_display_name(sketchbook)
    sb_dict["sb_url_safe_name"] = sb_url_safe_name(sketchbook)
    sb_dict["sb_spreads"] = spreads_list
    sb_dict["image_dir"] = sb_image_dir(sketchbook)
    sb_dict["html_dir"] = "../sketchbooks/{}".format(sb_url_safe_name(sketchbook))

    # attempt to grab top level metadata for index page
    try:
        # YAML files are in image dir. this is stable while built pages are not
        metadata_file_path = "{}/metadata/{}-index.yaml".format(
            sb_image_dir(sketchbook),
            sb_url_safe_name(sketchbook)
        )
        print(".......... Metadata_file_path = {}".format(metadata_file_path))
        with open(metadata_file_path, 'r') as metadata_file:
            metadata_file_obj = yaml.load(metadata_file)
            sb_dict["metadata"] = metadata_file_obj
            print(".......... Found metadata for {} index".format(
                sb_url_safe_name(sketchbook)
            ))
    except IOError:
        print(".......... No metadata found for {} index".format(
            sb_display_name(sketchbook)
        ))

    write_out_template(
        sb_dict,
        "../sketchbooks/{}".format(sb_url_safe_name(sketchbook)),
        "index.html",
        "sb_index.mustache"
    )


parser = argparse.ArgumentParser()
parser.add_argument("sb_name", help="The name of the sketchbook")

# TODO add param for single page sketchbooks

# TODO add param to override sb name when not same as dir name
# For example "perdef"
# OR use a config file per sb ?
# would need to change use of args.sb_name and use a variable instead

# TODO logic to handle IFC
# Only old sketchbooks will start with ifc
# parser.add_argument("pages_start_on", help="Does the sketchbook start on 1 or ifc")

args = parser.parse_args()

sketchbooks_to_process = []

if args.sb_name == "ALL":
    sketchbooks_to_process = THE_BIG_LIST
else:
    sketchbooks_to_process = [args.sb_name]
    print("========== SB_DISPLAY_NAME = {}".format(sb_display_name(args.sb_name)))
    print("========== SB_URL_SAFE_NAME = {}".format(sb_url_safe_name(args.sb_name)))
    print("========== SB_IMAGE_DIR = {}".format(sb_image_dir(args.sb_name)))
    print("========== SB_DIR is {}".format("../sketchbooks/{}".format(
        sb_url_safe_name(args.sb_name)
    )))


for sketchbook in sketchbooks_to_process:
    print(("========== Processing {}").format(sketchbook))

    create_dir_if_not_exists(sketchbook)

    this_sorted_image_list = make_sorted_image_list(
        sb_image_dir(sketchbook),
        sb_url_safe_name(sketchbook)
    )

    this_spreads = assemble_spreads(sketchbook, this_sorted_image_list)
    make_index(sketchbook, this_spreads)
    make_pages(sketchbook, this_spreads)
    print(("========== Finished {}").format(sketchbook))

print(".......... All Done!!!")
