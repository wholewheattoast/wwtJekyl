import argparse
import json
import os
import yaml
import toast_tools

# from argh import (
#    safe_input,
# )

# safe_input()

parser = argparse.ArgumentParser()
parser.add_argument("sb_name", help="The name of the sketchbook")

# TODO Add param to override sb name when not same as dir name
# For example "perdef"
# OR use a config file per sb
# Only old sketchbooks will start with ifc
# TODO logic to handle IFC
# parser.add_argument("pages_start_on", help="Does the sketchbook start on 1 or ifc")
args = parser.parse_args()

sb_display_name = args.sb_name.replace("-", " ")
sb_url_safe_name = (args.sb_name.replace(" ", "-")).lower()

print "========== sb_display_name = {}".format(sb_display_name)
print "========== sb_url_safe_name = {}".format(sb_url_safe_name)

sb_image_dir = os.path.dirname(
    "../image/sketchbooks/{}/".format(sb_url_safe_name)
)

print "========== sb_image_dir = {}".format(sb_image_dir)

sb_directory = "../sketchbooks/{}".format(sb_url_safe_name)

print "========== sb_directory is {}".format(sb_directory)

if not os.path.exists(sb_directory):
    os.makedirs(sb_directory)
    print "---------- Created  {}".format(sb_directory)


# TODO break page creation out into function

sb_image_files = []

for root, dirs, files in os.walk(sb_image_dir):
    for name in files:
        if root == sb_image_dir:
            if name == ".DS_Store":
                pass
            elif name == "{}-front-cover-icon.jpg".format(
                sb_url_safe_name
            ):
                pass
            elif name == "{}_cover_icon.jpg".format(
                sb_url_safe_name.replace("-", "_")
            ):
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

if sorted_image_list[-2] == "pp ifc 1":
    temp_item = sorted_image_list[-2]
    sorted_image_list.pop(-2)
    sorted_image_list.insert(1, temp_item)

sb_dict = {}

spreads_list = []

for i, item in enumerate(sorted_image_list):
    temp_spread_dict = {}

    spread = {}

    print "---------- item is {}".format(item)

    # TODO At some point this logic needs a check.
    # Bigger sketchbooks may have img of each page?

    spread_name = "{}-{}".format(
        sb_url_safe_name,
        item.replace(" ", "-")
    )
    item_split = item.split()

    if item_split[1] == "cover":
        spread[item] = item.replace(" ", "-")
    else:
        print "---------- item_split is {}".format(item_split)
        spread["verso"] = item_split[0]
        spread["recto"] = item_split[1]

    # this stips leading zeros out, might be useful
    # display_split = []
    # try:
    #     striped_split = re.sub("^0+", "", split)
    #     display_split.append(striped_split)
    # except:
    #     pass
    # print "----------  display_split is now {}".format(display_split)

    for key, value in spread.iteritems():
        page_name = "{}-{}".format(
            sb_url_safe_name,
            value.replace(" ", "-")
        )

        # Open a file that matches name of current spread
        # File should contain any available 'metadata' for spread
        try:
            metadata_file_path = "{}/metadata/{}.yaml".format(
                sb_image_dir,
                page_name,
            )
            print ".......... metadata_file_path = {}".format(
                metadata_file_path
            )
            with open(metadata_file_path, 'r') as metadata_file:
                # load yaml file
                metadata_file_obj = yaml.load(metadata_file)
                temp_spread_dict["{}_metadata".format(key)] = metadata_file_obj
                print ".......... found metadata for {}".format(page_name)
        except:
            print ".......... no metadata found for {}".format(page_name)

    temp_spread_dict["sb_display_name"] = sb_display_name.title()
    temp_spread_dict["sb_url_safe_name"] = sb_url_safe_name
    temp_spread_dict["spread"] = "{}".format(
        item.replace(" ", "-")
    )

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

    # Write file
    temp_file_name = "{}.html".format(spread_name)

    # write out a json file of results
    results_path = "{}/json".format(sb_directory)
    results_json = "{}.json".format(spread_name)
    if not os.path.exists(results_path):
        os.makedirs(results_path)
        print "---------- Created  {}".format(results_path)

    loaded_json = json.dumps(temp_spread_dict)
    with open("{}/{}".format(
        results_path, results_json
    ), "w") as json_results_file:
        json_results_file.write(loaded_json)
    # end results json

    toast_tools.write_out_template(
        temp_spread_dict,
        sb_directory,
        temp_file_name,
        "sb_page.mustache",
    )

    spreads_list.append(temp_spread_dict)

# Write Index
# TODO break out into function
sb_dict["sb_display_name"] = sb_display_name
sb_dict["sb_url_safe_name"] = sb_url_safe_name
sb_dict["sb_spreads"] = spreads_list
sb_dict["image_dir"] = sb_image_dir
sb_dict["html_dir"] = sb_directory

# TODO grab top level metadata for index page
# Perhaps have a metadata file for index
# and grab it in similar maner as pages

# Generate index file
toast_tools.write_out_template(
    sb_dict,
    sb_directory,
    "index.html",
    "sb_index.mustache"
)
