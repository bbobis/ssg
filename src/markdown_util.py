import os
import re

from htmlnode import markdown_to_html_node


def extract_title(markdown: str) -> str:
    matches = re.findall(r"^\#{1}\s{1}.+", markdown)
    if not matches:
        raise Exception("No title found")
    return matches[0].replace("# ", "", 1).strip().strip("\n")


def generate_page(from_path: str, template_path: str, dest_path: str):
    markdown_content = ""
    with open(from_path) as markdown_file:
        markdown_content = markdown_file.read()

    template_content = ""
    with open(template_path) as template_file:
        template_content = template_file.read()

    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    page = template_content.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_content)

    dirname = os.path.dirname(dest_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(dest_path, "w") as new_page:
        new_page.write(page)
