import argparse
import json
import os
import os.path
import pystache
import time
import uuid


def write_out_template(dictionary, path, file_name, template):
    """
        Read in json
        Render the dictionary using the given template
        Save the file with file_name
        to the location specified by the path
    """

    html_path = "{}/{}".format(path, file_name)
    html_file = open(html_path,"w")

    results_template = open("../_templates/{}".format(template)).read()

    html_results = pystache.render(results_template, dictionary)
    html_file.write(html_results)

    html_file.close()
    

# From http://nedbatchelder.com/blog/200712.html#e20071211T054956
import re
def sort_nicely( l ):
    """ Sort the given list in the way that humans expect.
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    l.sort( key=alphanum_key )
    
    return l
