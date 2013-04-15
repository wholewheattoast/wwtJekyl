#output sketchbook page

import os

#name and path
working_directory_path = "/Users/shawn/Dropbox/Sites/wwtJekyl/_posts/sketchbooks/"
output_directory_path = "."
output_domain = "http://www.wholewheattoast.com/"
sketchbook_name = raw_input('Enter sketchbook name: ')
title_string_prepend = """title: """ + str(sketchbook_name)
directory = working_directory_path + sketchbook_name


#pages
pagesInput = raw_input('How many pages? ')
#198
pages = int(pagesInput)
spreads = pages // 2
left_page = 1
right_page = 2

index_meta = "index-page: " + str(sketchbook_name) + "-index.html"

#images
img_width = 'width="' + raw_input('Image width? ') + '"'
#'width="900"'
#img_height = 'height="713"'
img_height = 'height="' + raw_input('Image height? ') + '"'
img_classes = """class="img-rounded" """

## init
counter = 1

def write_to_file(name_of, title_string, next_page_url, next_page_meta, prev_page_meta, img_url):
	f = open(name_of, 'w+')
	f.write("---")
	f.write('\n')
	f.write("layout: sketchbook")
	f.write('\n')
	f.write(title_string)
	f.write('\n')
	f.write("description:")
	f.write('\n')
	f.write("tags: sketchbook, moleskine")
	f.write('\n')
	f.write(index_meta)
	f.write('\n')
	f.write(next_page_meta)
	f.write('\n')
	f.write(prev_page_meta)
	f.write('\n')
	f.write("---")
	f.write('\n')
	f.write('<p class="sketchbook_container">')
	f.write('\n')
	f.write('<a href="' + next_page_url + '">' + img_url + '</a>')
	f.write('\n')
	f.write("</p>")
	f.write('\n')
	f.close()
	#print f

##create directory if not already exist
if not os.path.exists(directory):
    os.makedirs(directory)

while counter == 1:
	img_url = """<img """ + img_classes + 'src="' + output_directory_path + """/image/""" + sketchbook_name + """-front-cover.jpg" alt=" """ + sketchbook_name + """ sketchbook front cover" """ + img_width + " " + img_height + """>"""
	name_of = working_directory_path + sketchbook_name + "/" + sketchbook_name + "-front-cover" + ".html"
	next_page_meta = """next-page: """ + output_directory_path + "/" + sketchbook_name + """-pp-""" + str(left_page) + """-""" + str(right_page) +  """.html"""
	next_page_url = sketchbook_name + """-pp-""" + str(left_page) + """-""" + str(right_page) +  """.html"""
	prev_page_meta = """prev-page: """ + output_domain + "/sketchbooks.html"
	title_string = title_string_prepend + " " + "Front Cover"
	front_cover = write_to_file(name_of, title_string, next_page_url, next_page_meta, prev_page_meta, img_url)
	counter += 1
while counter == 2:
	img_url = """<img """ + img_classes + 'src="' + output_directory_path + """/image/""" + sketchbook_name + """-pp-""" + str(left_page) + "-" + str(right_page) + """.jpg" alt=" """ + sketchbook_name + """ sketchbook """ + str(left_page) + """-""" + str(right_page) + '" ' + img_width + " " + img_height + """>"""
	next_page_url = sketchbook_name + """-pp-""" + str((left_page + 2)) + """-""" + str((right_page + 2)) +  """.html"""
	next_page_meta = """next-page: """ + output_directory_path + "/" + sketchbook_name + """-pp-""" + str((left_page + 2)) + """-""" + str((right_page + 2)) +  """.html"""
	prev_page_meta = """prev-page: """ + output_directory_path + "/" + sketchbook_name + "-front-cover" + ".html"
	name_of = working_directory_path + sketchbook_name + "/" + sketchbook_name + "-pp-" + str(left_page) + "-" + str(right_page) + ".html"
	title_string = title_string_prepend + " " + "pp " + str(left_page) + """-""" + str(right_page)
	body_pages = write_to_file(name_of, title_string, next_page_url, next_page_meta, prev_page_meta, img_url)
	left_page += 2
	right_page += 2
	counter += 1
while counter > 2 and counter <= (spreads):
	img_url = """<img """ + img_classes + 'src="' + output_directory_path + """/image/""" + sketchbook_name + """-pp-""" + str(left_page) + "-" + str(right_page) + """.jpg" alt=" """ + sketchbook_name + """ sketchbook """ + str(left_page) + """-""" + str(right_page) + '" ' + img_width + " " + img_height + """>"""
	next_page_url = sketchbook_name + """-pp-""" + str((left_page + 2)) + """-""" + str((right_page + 2)) +  """.html"""
	next_page_meta = """next-page: """ + output_directory_path + "/" + sketchbook_name + """-pp-""" + str((left_page + 2)) + """-""" + str((right_page + 2)) +  """.html"""
	prev_page_meta = """prev-page: """ + output_directory_path + "/" + sketchbook_name + """-pp-""" + str((left_page - 2)) + """-""" + str((right_page - 2)) +  """.html"""
	name_of = working_directory_path + sketchbook_name + "/" + sketchbook_name + "-pp-" + str(left_page) + "-" + str(right_page) + ".html"
	title_string = title_string_prepend + " " + "pp " + str(left_page) + """-""" + str(right_page)
	body_pages = write_to_file(name_of, title_string, next_page_url, next_page_meta, prev_page_meta, img_url)
	left_page += 2
	right_page += 2
	counter += 1
while counter == (spreads + 1):
	img_url = """<img """ + img_classes + 'src="' + output_directory_path + """/image/""" + sketchbook_name + """-pp-""" + str(left_page) + "-" + str(right_page) + """.jpg" alt=" """ + sketchbook_name + """ sketchbook """ + str(left_page) + """-""" + str(right_page) + '" ' + img_width + " " + img_height + """>"""
	next_page_url = sketchbook_name + "-back-cover" + ".html"
	next_page_meta = """next-page: """ + output_directory_path + "/" + sketchbook_name + "-back-cover" + ".html"
	prev_page_meta = """prev-page: """ + output_directory_path + "/" + sketchbook_name + """-pp-""" + str((left_page - 2)) + """-""" + str((right_page - 2)) +  """.html"""
	name_of = working_directory_path + sketchbook_name + "/" + sketchbook_name + "-pp-" + str(left_page) + "-" + str(right_page) + ".html"
	title_string = title_string_prepend + " " + "pp " + str(left_page) + """-""" + str(right_page)
	body_pages = write_to_file(name_of, title_string, next_page_url, next_page_meta, prev_page_meta, img_url)
	counter += 1
while counter == (spreads + 2):
	img_url = """<img """ + img_classes + 'src="' + output_directory_path + """/image/""" + sketchbook_name + """-back-cover.jpg" alt=" """ + sketchbook_name + """ sketchbook back cover" """ + img_width +" " + img_height + """>"""
	name_of = working_directory_path + sketchbook_name + "/" + sketchbook_name + "-back-cover" + ".html"
	next_page_url = sketchbook_name + "-front-cover" + ".html"
	next_page_meta = """next-page: """ + output_directory_path + "/" + sketchbook_name + "-front-cover" + ".html"
	prev_page_meta = """prev-page: """ + output_directory_path + "/" + sketchbook_name + """-pp-""" + str(left_page) + """-""" + str(right_page) +  """.html"""
	title_string = title_string_prepend + " " + "Back Cover"
	back_cover = write_to_file(name_of, title_string, next_page_url, next_page_meta, prev_page_meta, img_url)
	counter +=1
else:
	print "all done with " + sketchbook_name
	print "Created " + str(counter) + " pages."
