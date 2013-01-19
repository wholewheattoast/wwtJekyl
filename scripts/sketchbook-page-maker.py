#output sketchbook page
 
pages = 198
spreads = pages // 2
totalFiles = spreads + 2
left_page = 1
right_page = 2


working_directory_path = "/Users/shawn/Dropbox/Sites/wwtJekyl/_posts/sketchbook/"
output_directory_path = "."
sketchbook_name = "stork-bites"
title_string_prepend = """title: """ + str(sketchbook_name)
img_classes = """class="img-rounded" """
img_width = 'width="900"'
img_height = 'height="713"'

counter = 0

def write_to_file(name_of, title_string, next_page_url, prev_page_url, img_url):
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
	f.write(next_page_url)
	f.write('\n')
	f.write(prev_page_url)
	f.write('\n')
	f.write("---")
	f.write('\n')
	f.write("<p>")
	f.write('\n')
	f.write(str(img_url))
	f.write('\n')
	f.write("</p>")
	f.write('\n')
	f.close()
	#print f

#Front Cover
img_url = """<img """ + img_classes + """src="http://www.wholewheattoast.com/image/sketchbooks/""" + sketchbook_name + """/""" + sketchbook_name + """-front-cover.jpg" alt=" """ + sketchbook_name + """ sketchbook front cover" """ + img_width + " " + img_height + """>"""
name_of = working_directory_path + sketchbook_name + "/" + sketchbook_name + "-front-cover" + ".html"
next_page_url = """next-page: """ + output_directory_path + "/" + sketchbook_name + "/" + sketchbook_name + """-pp-""" + str(left_page) + """-""" + str(right_page) +  """.html"""
prev_page_url = """prev-page: """ + output_directory_path + "/" + sketchbook_name + "/index" + """.html"""
title_string = title_string_prepend + " " + "Front Cover"

front_cover = write_to_file(name_of, title_string, next_page_url, prev_page_url, img_url)

#body pages
while counter < spreads:
	img_url = """<img """ + img_classes + 'src="' + output_directory_path + """/image/""" + sketchbook_name + """-pp-""" + str(left_page) + "-" + str(right_page) + """.jpg" alt=" """ + sketchbook_name + """ sketchbook """ + str(left_page) + """-""" + str(right_page) + '" ' + img_width + " " + img_height + """>"""
	next_page_url = """next-page: """ + output_directory_path + "/" + sketchbook_name + """-pp-""" + str((left_page + 2)) + """-""" + str((right_page + 2)) +  """.html"""
	prev_page_url = """prev-page: """ + output_directory_path + "/" + sketchbook_name + """-pp-""" + str((left_page - 2)) + """-""" + str((right_page - 2)) +  """.html"""
	name_of = working_directory_path + sketchbook_name + "/" + sketchbook_name + "-pp-" + str(left_page) + "-" + str(right_page) + ".html"
	title_string = title_string_prepend + " " + "pp " + str(left_page) + """-""" + str(right_page)

	body_pages = write_to_file(name_of, title_string, next_page_url, prev_page_url, img_url)

	left_page += 2
	right_page += 2
	counter += 1

	#print "counter", counter

#Envelope Page ???

#Back Cover
img_url = """<img """ + img_classes + """src="http://www.wholewheattoast.com/image/sketchbooks/""" + sketchbook_name + """/""" + sketchbook_name + """-back-cover.jpg" alt=" """ + sketchbook_name + """ sketchbook back cover" """ + img_width +" " + img_height + """>"""
name_of = working_directory_path + sketchbook_name + "/" + sketchbook_name + "-back-cover" + ".html"
next_page_url = """next-page: """ + output_directory_path + "/" + sketchbook_name + "/index" + """.html"""
prev_page_url = """prev-page: """ + output_directory_path + "/" + sketchbook_name + """-pp-""" + str(left_page) + """-""" + str(right_page) +  """.html"""
title_string = title_string_prepend + " " + "Back Cover"

back_cover = write_to_file(name_of, title_string, next_page_url, prev_page_url, img_url)




