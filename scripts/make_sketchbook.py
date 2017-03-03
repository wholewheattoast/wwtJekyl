import argparse
import json
import mistune
import os
import yaml

import toast_tools


def make_image_list():
    """
        Find images for a given sketchbook.
        Make a sorted list of them.
    """
    sb_image_files = []

    # make a list of bad names
    bad_name_1 = "{}-front-cover-icon.jpg".format(sb_url_safe_name)
    bad_name_2 = "{}_cover_icon.jpg".format(sb_url_safe_name.replace("-", "_"))
    bad_name_list = [".DS_Store", bad_name_1, bad_name_2]

    for root, dirs, files in os.walk(sb_image_dir):
        for name in files:
            if root == sb_image_dir:
                if name in bad_name_list:
                    pass
                else:
                    strip_ext = name.replace(".jpg", "")
                    strip_base = strip_ext.replace(sb_url_safe_name, "")
                    sb_numbers_only = strip_base.replace("-", " ").lstrip()
                    sb_image_files.append(sb_numbers_only)

    sorted_image_list = toast_tools.sort_nicely(sb_image_files)

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


def assemble_spreads(sorted_image_list):
    """
        Put together spreads from a sorted_image_list
    """

    spreads_list = []

    for i, item in enumerate(sorted_image_list):
        temp_spread_dict = {}
        spread = {}

        print "---------- item is {}".format(item)

        spread_name = "{}-{}".format(sb_url_safe_name, item.replace(" ", "-"))
        item_split = item.split()

        if item_split[1] == "cover":
            spread[item] = item.replace(" ", "-")
        else:
            print "---------- item_split is {}".format(item_split)
            spread["verso"] = item_split[0]
            spread["recto"] = item_split[1]

        for key, value in spread.iteritems():
            page_name = "{}-{}".format(sb_url_safe_name, value.replace(" ", "-"))

            # open a file that matches name of current spread
            # file should contain any available 'metadata' for spread
            try:
                # YAML files are in image dir since images are staple and
                # build pages are not
                metadata_file_path = "{}/metadata/{}.yaml".format(
                    sb_image_dir,
                    page_name,
                )
                print ".......... metadata_file_path = {}".format(
                    metadata_file_path
                )
                with open(metadata_file_path, 'r') as metadata_file:
                    metadata_file_obj = yaml.load(metadata_file)
                    temp_spread_dict["{}_metadata".format(key)] = metadata_file_obj
                    # let's format the transcription if available
                    markdown = mistune.Markdown()
                    html_transcript = markdown.render(
                        metadata_file_obj["transcription"]
                    )
                    temp_spread_dict["{}_metadata".format(key)]['html-transcription'] = html_transcript
                    print ".......... found metadata for {}".format(page_name)
            except:
                print ".......... no metadata found for {}".format(page_name)

        temp_spread_dict["sb_display_name"] = sb_display_name.title()
        temp_spread_dict["sb_url_safe_name"] = sb_url_safe_name
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

        toast_tools.write_out_json(temp_spread_dict, sb_directory, spread_name)

#         import pdb
#         pdb.set_trace()
        spreads_list.append(temp_spread_dict)

    return spreads_list


def make_pages(spreads_list):
    # TODO break out writing pages till i have full spreads_list
    # write this into each page
    # Then I can use it to look for relationshitps in pages
    # like other days/location
    for item in spreads_list:
        spread_name = "{}-{}".format(
            sb_url_safe_name, item["spread"].replace(" ", "-")
        )
        temp_file_name = "{}.html".format(spread_name)

        # add full list to each pages item?
        # TODO break out "same as today" look up as a def
        # call it here and write out.
        item["all-data"] = spreads_list

        toast_tools.write_out_template(
            item,
            sb_directory,
            temp_file_name,
            "sb_page.mustache",
        )


def make_index(spreads_list):
    sb_dict = {}
    sb_dict["sb_display_name"] = sb_display_name
    sb_dict["sb_url_safe_name"] = sb_url_safe_name
    sb_dict["sb_spreads"] = spreads_list
    sb_dict["image_dir"] = sb_image_dir
    sb_dict["html_dir"] = sb_directory

    # grab top level metadata for index page
    try:
        # YAML files are in image dir. img dir is stable while built pages are not
        metadata_file_path = "{}/metadata/{}-index.yaml".format(
            sb_image_dir, sb_url_safe_name)
        print ".......... metadata_file_path = {}".format(metadata_file_path)
        with open(metadata_file_path, 'r') as metadata_file:
            metadata_file_obj = yaml.load(metadata_file)
            sb_dict["metadata"] = metadata_file_obj
            print ".......... found metadata for {} index".format(sb_url_safe_name)
    except:
        print ".......... no metadata found for {} index".format(sb_display_name)

    # TODO something about sb_dict is causing an error FIXME
#     toast_tools.write_out_json(
#         sb_dict,
#         sb_directory,
#         "{}-index".format(sb_url_safe_name),
#     )

    # Let's try to just write out as YAML
    toast_tools.write_out_yaml(
        sb_dict,
        sb_directory,
        "{}-index-full".format(sb_url_safe_name)
    )

    toast_tools.write_out_template(
        sb_dict,
        sb_directory,
        "index.html",
        "sb_index.mustache"
    )


parser = argparse.ArgumentParser()
parser.add_argument("sb_name", help="The name of the sketchbook")

# TODO add param for single page sketchbooks

# TODO add param to override sb name when not same as dir name
# For example "perdef"
# OR use a config file per sb
# Only old sketchbooks will start with ifc

# TODO logic to handle IFC
# parser.add_argument("pages_start_on", help="Does the sketchbook start on 1 or ifc")

args = parser.parse_args()

# set up
sb_display_name = args.sb_name.replace("-", " ")
sb_url_safe_name = (args.sb_name.replace(" ", "-")).lower()
sb_image_dir = os.path.dirname(
    "../image/sketchbooks/{}/".format(sb_url_safe_name)
)
sb_directory = "../sketchbooks/{}".format(sb_url_safe_name)

print "========== sb_display_name = {}".format(sb_display_name)
print "========== sb_url_safe_name = {}".format(sb_url_safe_name)
print "========== sb_image_dir = {}".format(sb_image_dir)
print "========== sb_directory is {}".format(sb_directory)

if not os.path.exists(sb_directory):
    os.makedirs(sb_directory)
    print "---------- Created  {}".format(sb_directory)

this_sorted_image_list = make_image_list()
this_spreads = assemble_spreads(this_sorted_image_list)
make_index(this_spreads)
make_pages(this_spreads)

print ".......... All Done!!!"
