import os
import frontmatter
import pystache


# TODO take these as cli arguments
file_path_to_read = "../publications/"
template = "basic_html.mustache"
path_to_write_to = "test"

for root, dirs, files in os.walk("../publications/", topdown=False):
    for name in files:
        print(os.path.join(root, name))
        file_name = os.path.join(root, name)
        post = frontmatter.load(file_name)

        parsed_post = {}
        parsed_post["post_content"] = post.content
        parsed_post["title"] = post["title"]
        parsed_post["date"] = post["date"]
        # parsed_post["post_front_matter_keys"] = sorted(post.keys())

        # write out file to a template
        results_template = open("../_templates/{}".format(template)).read()
        html_results = pystache.render(results_template, parsed_post)
        html_results_encoded = html_results.encode(
            encoding='UTF-8', errors='strict'
        )

        html_path = "{}/{}/{}".format(
            path_to_write_to, "publications", os.path.basename(root)
        )

        # TODO i don't think this is the best way?
        html_file_path = "{}/{}".format(html_path, name)

        if not os.path.exists(html_path):
            os.makedirs(html_path)
            print("---------- Created  {}".format(html_path))

        with open(html_file_path, "w") as f:
            f.write(html_results_encoded.decode('utf-8'))
            print(".......... Wrote out  {}".format(html_file_path))
