# Euphoria - setup.py

''' This is the 'setup.py' file. '''

'''
Copyright 2023 Aniketh Chavare

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Imports
from setuptools import setup, find_packages

# README.md
with open("README.md") as readme_file:
    README = readme_file.read()

# Setup Arguments
setup_args = dict (
    name = "Euphoria",
    version = "1.0.0",
    description = "Euphoria is the only cross-platform, versatile, and advanced Python package you will ever need!",
    long_description = README,
    long_description_content_type = "text/markdown",
    license = "Apache License 2.0",
    packages = find_packages(),
    include_package_data = True,
    author = "Aniketh Chavare",
    author_email = "anikethchavare@outlook.com",
    project_urls = {
        "Homepage": "https://pypi.org/project/Euphoria",
        "Repository": "https://github.com/anikethchavare/Euphoria",
        "Documentation": "https://anikethchavare.gitbook.io/euphoria",
        "Download": "https://github.com/anikethchavare/Euphoria/releases",
        "Changelog": "https://github.com/anikethchavare/Euphoria/blob/main/CHANGELOG.md",
        "Issues": "https://github.com/anikethchavare/Euphoria/issues"
    },
    install_requires = [
        "requests",
        "beautifulsoup4",
        "colorama",
        "pyperclip",
        "PyAutoGUI"
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development"
    ]
)

# Running the Setup File
if __name__ == "__main__":
    setup(**setup_args)