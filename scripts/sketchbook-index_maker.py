#
# Output a sketchbook index page
#
# Inputs
import os
import time
#
# Gather sketchbook name and file paths.
working_directory_path = "/Users/shawn/Dropbox/Sites/wwtJekyl/_posts/sketchbooks/"
output_directory_path = "."
sketchbook_name = raw_input('Enter sketchbook name: ')
sketchbook_url_name = raw_input("Enter the sketchbook's url name: ")
name_of_index = working_directory_path + sketchbook_url_name + "/" + "index.html"
title_string_prepend = """title: """ + str(sketchbook_name) + " Index"
stub = "sketchbooks/" + sketchbook_url_name + "/" + "index.html"
directory = working_directory_path + sketchbook_url_name
img_dir_location = "/image/sketchbooks/" + str(sketchbook_url_name) + "/"
#
# Page Setup
pages_start_on_input = raw_input('Page starts on 1 or ifc?  ')
pages_start_on = str(pages_start_on_input)
pagesInput = raw_input('How many total pages (including front and back covers)? ')
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
sketchbook_size = raw_input('size? ')
start_iso = raw_input('iso start date? ')
start_english = raw_input('English start date? ')
end_iso = raw_input('iso end date? ')
end_english = raw_input('English end date? ')
#
# Images
# different
thumb_img_width = 'width="' + raw_input('Thumbnail Image width? ') + '"'
thumb_img_height = 'height="' + raw_input('Thumbnail Image height? ') + '"'
# /different
#
## init
counter = 1
#
def write_index_yaml(name_of_index, title_string_prepend, description):
    """ Setup the meatadata yaml for the index """
    f = open(name_of_index, 'w+')
    f.write("---")
    f.write('\n')
    f.write("layout: sketchbook_index")
    f.write('\n')
    f.write(title_string_prepend)
    f.write('\n')
    f.write("description: " + description)
    f.write('\n')
    f.write("date: " +  time.strftime("%Y-%m-%d"))
    f.write('\n')
    f.write("stub: " + stub)
    f.write('\n')
    f.write("iso_time_start: " + start_iso)
    f.write('\n')
    f.write("time_start: " + start_english)
    f.write('\n')
    f.write("iso_time_end: " + end_iso)
    f.write('\n')
    f.write("time_end: " + end_english)
    f.write('\n')
    f.write("dimensions: " + sketchbook_size)
    f.write('\n')
    f.write("---")
    f.write('\n')
    f.write('\n')
    f.write('<ol class="list-unstyled">')
    f.write('\n')
    f.write('\n')
    f.close()

def finish_index_yaml(name_of_index):
    f = open(name_of_index, 'a')
    f.write('\n')
    f.write('</ol>')
    f.write('\n')

def write_to_index(name_of_index, sketchbook_page_url, thumbnail_img_url, this_entry_title):
    """ Write out each item to the index """
    f = open(name_of_index, 'a')
    f.write('<li class="col-xs-4 col-md-3"> <a href="' + sketchbook_page_url + '"><img src="' + thumbnail_img_url + '" alt="Thumbnail image for ' + this_entry_title + '" ' + 'title="' + this_entry_title + '" ' + thumb_img_width + ' ' + thumb_img_height  + """ /></a></li>""")
    f.write('\n')
    f.write('\n')
    f.close()

##create directory if it does not already exist
if not os.path.exists(directory):
    os.makedirs(directory)

initial_index_write = write_index_yaml(name_of_index, title_string_prepend, description, )

if pages_start_on == "1":
    while counter == 1:
        sketchbook_page_url = "/sketchbooks/" + sketchbook_url_name + "/" + sketchbook_url_name + "-front-cover.html"
        thumbnail_img_url = img_dir_location + "thumbs/" + sketchbook_url_name + """-front-cover.jpg"""
        this_entry_title = sketchbook_url_name + "/" + sketchbook_url_name + "-front-cover"
        front_cover_entry = write_to_index(name_of_index, sketchbook_page_url, thumbnail_img_url, this_entry_title)
        counter += 1
    while counter > 1 and counter <= (spreads):
        sketchbook_page_url = "/sketchbooks/" + sketchbook_url_name + "/" + sketchbook_url_name + "-pp-" + str(left_page) + "-" + str(right_page) + ".html"
        thumbnail_img_url = img_dir_location + "thumbs/" + sketchbook_url_name + """-pp-""" + str(left_page) + "-" + str(right_page) + """.jpg"""
        this_entry_title = sketchbook_url_name + "-pp-" + str(left_page) + "-" + str(right_page)
        body_pages = write_to_index(name_of_index, sketchbook_page_url, thumbnail_img_url, this_entry_title)
        left_page += 2
        right_page += 2
        counter += 1
    while counter == (spreads + 1):
        sketchbook_page_url = "/sketchbooks/" + sketchbook_url_name + "/" + sketchbook_url_name + "-back-cover.html"
        thumbnail_img_url = img_dir_location + "thumbs/" + sketchbook_url_name + """-back-cover.jpg"""
        this_entry_title = sketchbook_url_name + "/" + sketchbook_url_name + "-back-cover"
        front_cover_entry = write_to_index(name_of_index, sketchbook_page_url, thumbnail_img_url, this_entry_title)
        counter += 1
elif pages_start_on == "ifc":
    while counter == 1:
        sketchbook_page_url = "/sketchbooks/" + sketchbook_url_name + "/" + sketchbook_url_name + "-front-cover.html"
        thumbnail_img_url = img_dir_location + "thumbs/" + sketchbook_url_name + """-front-cover.jpg"""
        this_entry_title = sketchbook_url_name + "-front-cover"
        front_cover_entry = write_to_index(name_of_index, sketchbook_page_url, thumbnail_img_url, this_entry_title)
        counter += 1
    while counter == 2:
        sketchbook_page_url = "/sketchbooks/" + sketchbook_url_name + "/" + sketchbook_url_name + "-pp-" + str(ifc_page) + "-" + str(ifc_right_page) + ".html"
        thumbnail_img_url = img_dir_location + "thumbs/" + sketchbook_url_name + """_pp_""" + str(ifc_page) + "_" + str(ifc_right_page) + """.jpg"""
        this_entry_title = sketchbook_url_name + "-pp-" + str(ifc_page) + "-" + str(ifc_right_page) + ".html"
        body_pages = write_to_index(name_of_index, sketchbook_page_url, thumbnail_img_url, this_entry_title)
        ifc_right_page += 2
        counter += 1
    while counter > 2 and counter < (spreads):
        sketchbook_page_url = "/sketchbooks/" + sketchbook_url_name + "/" + sketchbook_url_name + "-pp-" + str(ifc_left_page) + "-" + str(ifc_right_page) + ".html"
        thumbnail_img_url = img_dir_location + "thumbs/" + sketchbook_url_name + """_pp_""" + str(ifc_left_page) + "_" + str(ifc_right_page) + """.jpg"""
        this_entry_title = sketchbook_url_name + "-pp-" + str(ifc_left_page) + "-" + str(ifc_right_page)
        body_pages = write_to_index(name_of_index, sketchbook_page_url, thumbnail_img_url, this_entry_title)
        ifc_left_page += 2
        ifc_right_page += 2
        counter += 1
    while counter == (spreads):
        sketchbook_page_url = "/sketchbooks/" + sketchbook_url_name + "/" + sketchbook_url_name + "-pp-" + str(ifc_left_page) + "-" + str(ibc_page) + ".html"
        thumbnail_img_url =  img_dir_location + "thumbs/" + sketchbook_url_name + """_pp_""" + str(ifc_left_page) + "_" + str(ibc_page) + """.jpg"""
        this_entry_title = sketchbook_url_name + "-pp-" + str(ifc_left_page) + "-" + str(ibc_page)
        body_pages = write_to_index(name_of_index, sketchbook_page_url, thumbnail_img_url, this_entry_title)
        counter += 1
    while counter == (spreads + 1):
        sketchbook_page_url = "/sketchbooks/" + sketchbook_url_name + "/" + sketchbook_url_name + "-back-cover.html"
        thumbnail_img_url = img_dir_location + "thumbs/" + sketchbook_url_name + """-back-cover.jpg"""
        this_entry_title = sketchbook_url_name + "-back-cover"
        front_cover_entry = write_to_index(name_of_index, sketchbook_page_url, thumbnail_img_url, this_entry_title)
        counter += 1
else:
    print "woops"

final_index_write = finish_index_yaml(name_of_index)

print "all done with " + sketchbook_name
