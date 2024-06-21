#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File    ：sitecustomize.py
# @Author  ：Jay
# @Date    ：2024/6/21 15:14 
# @Remark  ：Automatically create sitecustomize.py in the Python environment
import os
import sys
import inspect


def find_project_root(directory):
    current_dir = os.path.abspath(directory)

    if os.path.isdir(current_dir):
        if "README.md" in os.listdir(current_dir):
            if current_dir not in sys.path:
                sys.path.append(current_dir)
            return directory

        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            raise Exception("Please create a README.md file in the project root directory before use!")

        return find_project_root(parent_dir)

    return directory


def sitecustomize():
    site_customize_code_headers = ""

    def addHeaders(existing_code):
        nonlocal site_customize_code_headers, site_customize_code
        if "import os" not in existing_code:
            site_customize_code_headers += "import os\n"
        if "import sys" not in existing_code:
            site_customize_code_headers += "import sys\n"
        site_customize_code = site_customize_code_headers + site_customize_code

    def write_file(existing_code, site_customize_path):
        nonlocal site_customize_code

        addHeaders(existing_code)
        with open(site_customize_path, "a") as f:
            print(site_customize_code)
            f.write(site_customize_code)

    def create_site_customize():
        """
        Function to create or update sitecustomize.py in the Python environment's site-packages directory.

        Returns:
            str: Success message if creation/update is successful.
            Raises Exception if sitecustomize.py already exists.
        """
        find_project_root(os.getcwd())

        existing_code = ""
        site_customize_path = os.path.join(sys.prefix, "lib", "site-packages", "sitecustomize.py")

        if os.path.exists(site_customize_path):
            with open(site_customize_path, "r") as f:
                existing_code = f.read()

            if site_customize_code.strip() not in existing_code.strip():
                write_file(existing_code=existing_code, site_customize_path=site_customize_path)
                return "Additional code appended to sitecustomize.py in the Python environment!"

            return "sitecustomize.py already contains the necessary code."

        write_file(existing_code=existing_code, site_customize_path=site_customize_path)
        return "sitecustomize.py created successfully in the Python environment!"

    site_customize_code = f"""\
{inspect.getsource(find_project_root)}

find_project_root(os.getcwd())
"""

    return create_site_customize()


# If this script is executed directly, call the create_site_customize function
if __name__ == "__main__":
    sitecustomize()