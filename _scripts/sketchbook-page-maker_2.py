# LEGACY output sketchbook page
#
import os
#
# Sketchbook name and file paths
working_directory_path = "/Users/shawn/Dropbox/Sites/wwtJekyl/_posts/sketchbooks/"
output_directory_path = "."
sketchbook_name = raw_input('Enter sketchbook name: ')
sketchbook_url_name = raw_input("Enter the sketchbook's url name: ")
title_string_prepend = "title: {}".format(sketchbook_name)
directory = working_directory_path + sketchbook_url_name
img_dir_location = "/image/sketchbooks/{}/".format(sketchbook_url_name)
#
# Page Setup
pages_start_on_input = raw_input('Page starts on 1 or ifc?  ')
pages_start_on = pages_start_on_input
pagesInput = raw_input('How many pages? ')
pages = int(pagesInput)
spreads = pages // 2
left_page = 1
right_page = 2
ifc_page = "ifc"
ibc_page = "ibc"
ifc_left_page = 2
ifc_right_page = 1
#
# Other Metadata
description = raw_input('Enter a description: ')
#
# Images
img_width = 'width="' + raw_input('Image width? ') + '"'
img_height = 'height="' + raw_input('Image height? ') + '"'
#
## init
counter = 1
#
# Could i pass all this in as a dict instead?
#
def write_to_file(name_of, title_string, this_page_meta, next_page_meta, prev_page_meta, img_url, img_width, img_height):
    with open(name_of, 'w+') as f:
        f.write("---")
        f.write('\n')
        f.write("layout: sketchbook_page")
        f.write('\n')
        f.write(title_string)
        f.write('\n')
        f.write("description: {}".format(description))
        f.write('\n')
        f.write("tags: sketchbook")
        f.write('\n')
        f.write("index-page: index.html")
        f.write('\n')
        f.write("this-page: {}".format(this_page_meta))
        f.write('\n')
        f.write("next-page: {}".format(next_page_meta))
        f.write('\n')
        f.write("prev-page: {}".format(prev_page_meta))
        f.write('\n')
        f.write("img_url: {}".format(img_url))
        f.write('\n')
        f.write("image-width: {}".format(img_width))
        f.write('\n')
        f.write("image-height: {}".format(img_height))
        f.write('\n')
        f.write("---")

# Create directory if it does not already exist
if not os.path.exists(directory):
    os.makedirs(directory)

if pages_start_on == "1": 
	# TODO use str formating instead of concating here.
	while counter == 1:
		img_url = "{}{}-front-cover.jpg".format(img_dir_location, sketchbook_url_name)
		name_of = "{}{}/{}-front-cover.html".format(working_directory_path, sketchbook_url_name, sketchbook_url_name)
		this_page_meta = "{}/{}-front-cover".format(sketchbook_url_name, sketchbook_url_name)
		next_page_meta = "{}/{}-pp-{}-{}.html".format(output_directory_path, sketchbook_url_name, left_page, right_page)
		prev_page_meta = "index.html"
		title_string = "{} Front Cover".format(title_string_prepend)
		front_cover = write_to_file(name_of, title_string, this_page_meta, next_page_meta, prev_page_meta, img_url, img_width, img_height)
		counter += 1
	while counter == 2:
		img_url = "{}{}-pp-{}{}.jpg".format(img_dir_location,sketchbook_url_name, left_page, right_page)
		name_of = "{}{}/{}-pp-{}-{}.html".format(working_directory_path, sketchbook_url_name, sketchbook_url_name, left_page, right_page)
		this_page_meta = "{}-pp-{}-{}".format(sketchbook_url_name, left_page, right_page)
		next_page_meta = "{}/{}-pp-{}-{}.html".format(output_directory_path, sketchbook_url_name, (left_page + 2), (right_page + 2))
		prev_page_meta = "{}/{}-front-cover.html".format(output_directory_path, sketchbook_url_name)
		title_string = "{} pp {}-{}".format(title_string_prepend, left_page, right_page)
		body_pages = write_to_file(name_of, title_string, this_page_meta, next_page_meta, prev_page_meta, img_url, img_width, img_height)
		left_page += 2
		right_page += 2
		counter += 1
	while counter > 2 and counter <= (spreads):
		img_url = "{}{}-pp-{}-{}.jpg".format(img_dir_location, sketchbook_url_name, left_page, right_page)
		name_of = "{}{}/{}-pp-{}-{}.html".format(working_directory_path, sketchbook_url_name, sketchbook_url_name, left_page, right_page)
		this_page_meta = "{}-pp-{}-{}".format(sketchbook_url_name, left_page, right_page)
		next_page_meta = "{}/{}-pp-{}-{}.html".format(output_directory_path, sketchbook_url_name, (left_page + 2), (right_page + 2))
		prev_page_meta = "{}/{}-pp-{}-{}.html".format(output_directory_path, sketchbook_url_name, (left_page - 2), (right_page - 2))
		title_string = "{} pp {} - {}".format(title_string_prepend, left_page, right_page)
		body_pages = write_to_file(name_of, title_string, this_page_meta, next_page_meta, prev_page_meta, img_url, img_width, img_height)
		left_page += 2
		right_page += 2
		counter += 1
	while counter == (spreads + 1):
		img_url = "{}{}-pp-{}-{}.jpg".format(img_dir_location, sketchbook_url_name, left_page, right_page)
		name_of = "{}{}/{}-pp-{}-{}.html".format(working_directory_path, sketchbook_url_name, sketchbook_url_name, left_page, right_page)
		this_page_meta = "{}-pp-{}-{}".format(sketchbook_url_name, left_page, right_page)
		next_page_meta = "{}/{}-back-cover.html".format(output_directory_path, sketchbook_url_name)
		prev_page_meta = "{}/{}-pp-{}-{}.html".format(output_directory_path, sketchbook_url_name, (left_page - 2), (right_page - 2))
		title_string = "{} pp {}-{}".format(title_string_prepend, left_page, right_page)
		body_pages = write_to_file(name_of, title_string, this_page_meta, next_page_meta, prev_page_meta, img_url, img_width, img_height)
		counter += 1
	while counter == (spreads + 2):
		img_url =img_dir_location + sketchbook_url_name + """-back-cover.jpg"""
		name_of = working_directory_path + sketchbook_url_name + "/" + sketchbook_url_name + "-back-cover" + ".html"
		this_page_meta = sketchbook_url_name + "-back-cover"
		next_page_meta = output_directory_path + "/index.html"
		prev_page_meta = output_directory_path + "/" + sketchbook_url_name + """-pp-""" + str(left_page) + """-""" + str(right_page) +  """.html"""
		title_string = title_string_prepend + " " + "Back Cover"
		back_cover = write_to_file(name_of, title_string, this_page_meta, next_page_meta, prev_page_meta, img_url, img_width, img_height)
		counter +=1
elif pages_start_on == "ifc":
	while counter == 1:
		img_url = img_dir_location + sketchbook_url_name + """-front-cover.jpg"""
		name_of = working_directory_path + sketchbook_url_name + "/" + sketchbook_url_name + "-front-cover" + ".html"
		this_page_meta = sketchbook_url_name + "/" + sketchbook_url_name + "-front-cover"
		next_page_meta = output_directory_path + "/" + sketchbook_url_name + """-pp-""" + str(ifc_page) + """-""" + str(ifc_right_page) +  """.html"""
		prev_page_meta = "index.html"
		title_string = title_string_prepend + " " + "Front Cover"
		front_cover = write_to_file(name_of, title_string, this_page_meta, next_page_meta, prev_page_meta, img_url, img_width, img_height)
		counter += 1
	while counter == 2:
		img_url = img_dir_location + sketchbook_url_name + """-pp-""" + str(ifc_page) + "-" + str(ifc_right_page) + """.jpg"""
		name_of = working_directory_path + sketchbook_url_name + "/" + sketchbook_url_name + "-pp-" + str(ifc_page) + "-" + str(ifc_right_page) + ".html"
		this_page_meta = sketchbook_url_name + "-pp-" + str(ifc_page) + "-" + str(ifc_right_page)
		next_page_meta = output_directory_path + "/" + sketchbook_url_name + """-pp-""" + str((ifc_left_page)) + """-""" + str((ifc_right_page + 2)) +  """.html"""
		prev_page_meta = output_directory_path + "/" + sketchbook_url_name + "-front-cover" + ".html"
		title_string = title_string_prepend + " " + "pp " + str(ifc_page) + """-""" + str(ifc_right_page)
		body_pages = write_to_file(name_of, title_string, this_page_meta, next_page_meta, prev_page_meta, img_url, img_width, img_height)
		ifc_right_page += 2
		counter += 1
	while counter == 3:
		img_url = img_dir_location + sketchbook_url_name + """-pp-""" + str(ifc_left_page) + "-" + str(ifc_right_page) + """.jpg"""
		name_of = working_directory_path + sketchbook_url_name + "/" + sketchbook_url_name + "-pp-" + str(ifc_left_page) + "-" + str(ifc_right_page) + ".html"
		this_page_meta = sketchbook_url_name + "-pp-" + str(ifc_left_page) + "-" + str(ifc_right_page)
		next_page_meta = output_directory_path + "/" + sketchbook_url_name + """-pp-""" + str((ifc_left_page + 2)) + """-""" + str((ifc_right_page + 2)) +  """.html"""
		prev_page_meta = output_directory_path + "/" + sketchbook_url_name + """-pp-""" + str((ifc_page)) + """-""" + str((ifc_right_page - 2)) +  """.html"""
		title_string = title_string_prepend + " " + "pp " + str(ifc_left_page) + """-""" + str(ifc_right_page)
		body_pages = write_to_file(name_of, title_string, this_page_meta, next_page_meta, prev_page_meta, img_url, img_width, img_height)
		ifc_left_page += 2
		ifc_right_page += 2
		counter += 1
	while counter > 3 and counter <= (spreads):
		img_url = img_dir_location + sketchbook_url_name + """-pp-""" + str(ifc_left_page) + "-" + str(ifc_right_page) + """.jpg"""
		name_of = working_directory_path + sketchbook_url_name + "/" + sketchbook_url_name + "-pp-" + str(ifc_left_page) + "-" + str(ifc_right_page) + ".html"
		this_page_meta = sketchbook_url_name + "-pp-" + str(ifc_left_page) + "-" + str(ifc_right_page)
		next_page_meta = output_directory_path + "/" + sketchbook_url_name + """-pp-""" + str((ifc_left_page + 2)) + """-""" + str((ifc_right_page + 2)) +  """.html"""
		prev_page_meta = output_directory_path + "/" + sketchbook_url_name + """-pp-""" + str((ifc_left_page - 2)) + """-""" + str((ifc_right_page - 2)) +  """.html"""
		title_string = title_string_prepend + " " + "pp " + str(ifc_left_page) + """-""" + str(ifc_right_page)
		body_pages = write_to_file(name_of, title_string, this_page_meta, next_page_meta, prev_page_meta, img_url, img_width, img_height)
		ifc_left_page += 2
		ifc_right_page += 2
		counter += 1
	while counter == (spreads + 1):
		img_url = img_dir_location + sketchbook_url_name + """-pp-""" + str(ifc_left_page) + "-" + str(ibc_page) + """.jpg"""
		name_of = working_directory_path + sketchbook_url_name + "/" + sketchbook_url_name + "-pp-" + str(ifc_left_page) + "-" + str(ibc_page) + ".html"
		this_page_meta = sketchbook_url_name + "-pp-" + str(ifc_left_page) + "-" + str(ibc_page)
		next_page_meta = output_directory_path + "/" + sketchbook_url_name + "-back-cover" + ".html"
		prev_page_meta = output_directory_path + "/" + sketchbook_url_name + """-pp-""" + str((ifc_left_page - 2)) + """-""" + str((ifc_right_page - 2)) +  """.html"""
		title_string = title_string_prepend + " " + "pp " + str(ifc_left_page) + """-""" + str(ibc_page)
		body_pages = write_to_file(name_of, title_string, this_page_meta, next_page_meta, prev_page_meta, img_url, img_width, img_height)
		counter += 1
	while counter == (spreads + 2):
		img_url =img_dir_location + sketchbook_url_name + """-back-cover.jpg"""
		name_of = working_directory_path + sketchbook_url_name + "/" + sketchbook_url_name + "-back-cover.html"
		this_page_meta = sketchbook_url_name + "-back-cover"
		next_page_meta = output_directory_path + "/index.html"
		prev_page_meta = output_directory_path + "/" + sketchbook_url_name + """-pp-""" + str(ifc_left_page) + """-""" + str(ibc_page) +  """.html"""
		title_string = title_string_prepend + " " + "Back Cover"
		back_cover = write_to_file(name_of, title_string, this_page_meta, next_page_meta, prev_page_meta, img_url, img_width, img_height)
		counter +=1
else:
	print "---------- woops"

print "---------- All done with {}".format(sketchbook_name)
print "---------- Created {} pages".format(counter)
