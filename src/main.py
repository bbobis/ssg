import os
import shutil
from typing import List

from markdown_util import generate_pages_recursive


def main():
    static_dir_path = os.path.join("static")
    public_dir_path = os.path.join("public")

    if os.path.exists(public_dir_path):
        print("Deleting public dir")
        shutil.rmtree(public_dir_path)

    os.mkdir(public_dir_path)
    print("Created public dir")

    copy_files(static_dir_path, public_dir_path, os.listdir(static_dir_path))

    template_path = os.path.join("template.html")
    content_path = os.path.join("content")
    generate_pages_recursive(content_path, template_path, public_dir_path)


def copy_files(curr_src_path: str, curr_dest_path: str, items: List["str"]) -> None:
    for item in items:
        new_src_path = os.path.join(curr_src_path, item)
        new_dest_path = os.path.join(curr_dest_path, item)
        if os.path.isfile(new_src_path):
            shutil.copy(new_src_path, new_dest_path)
            print("Copied", item, "to", new_dest_path)
            continue
        os.mkdir(new_dest_path)
        print("Created directory", new_dest_path)
        copy_files(new_src_path, new_dest_path, os.listdir(new_src_path))


if __name__ == "__main__":
    main()
