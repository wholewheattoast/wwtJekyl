"""Tools for making sketchbooks."""
import os

from toast_tools import (
    sort_nicely,
)


def create_dir_if_not_exists(sketchbook):
    """Create a directory to place sketchbook files into if necessary."""
    dir_path = "../sketchbooks/{}".format(
        sb_url_safe_name(sketchbook)
    )

    img_path = sb_image_dir(sketchbook)

    if not os.path.exists(dir_path) and os.path.exists(img_path):
        os.makedirs(dir_path)
        print("---------- Created  {}".format(dir_path))
    elif os.path.exists(dir_path) and not os.path.exists(img_path):
        print("!!!!!!!!!!!! No images img_path?  Maybe a typo?")
    else:
        print("!!!!!!!!!!!! yay??? what should this say or do?")


def sb_url_safe_name(name):
    """Return a url safe version of `name`."""
    return name.replace(" ", "-").lower()


def sb_display_name(name):
    """Return version of `name` meant for visual presentation."""
    return name.replace("-", " ").title()


def sb_image_dir(name):
    """Return the path to the sketchbook of `name`."""
    return os.path.dirname(
        "../image/sketchbooks/{}/".format(name)
    )


def sort_image_list(list_to_sort):
    """
    Sort sketchbook images from 'list_to_sort' and return.

    This uses `sort_nicely` and then handles sketchbook related edge cases.
    """
    sorted_image_list = sort_nicely(list_to_sort)

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


def assemble_spreads(sb_name, sorted_image_list):
    """Assemble spreads from a sorted_image_list."""
    spreads_list = []

    for i, item in enumerate(sorted_image_list):
        temp_spread_dict = {}
        spread = {}

        item_split = item.split()

        if item_split[1] == "cover":
            spread[item] = item.replace(" ", "-")
        else:
            print("---------- item_split is {}".format(item_split))
            spread["verso"] = item_split[0]
            spread["recto"] = item_split[1]

        temp_spread_dict["sb_display_name"] = sb_display_name(sb_name)
        temp_spread_dict["sb_url_safe_name"] = sb_url_safe_name(sb_name)
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
            print("woops index error on prev")

        spreads_list.append(temp_spread_dict)

    return spreads_list
