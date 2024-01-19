# Euphoria (System) - Packages

''' This is the "Packages" module. '''

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
import requests
import subprocess
from bs4 import BeautifulSoup

# Function 1 - List Packages
def list_packages(language):
    # Variables
    languages = ["python"]

    # Checking the Data Type of "language"
    if (isinstance(language, str)):
        # Checking if "language" is Valid
        if (language.lower() in languages):
            # Checking the Value of "language"
            if (language.lower() == "python"):
                # Try/Except - Fetching and Returning the Packages
                try:
                    # Returning the List of Packages
                    return [f"{package[0]}=={package[1]}" for package in [package.split() for package in subprocess.check_output(["pip", "list"], stderr=subprocess.DEVNULL).decode().split("\n")[2:-1]]]
                except:
                    # Raising an Exception
                    raise Exception("An occurred while retrieving the list of Python packages. Please try again.")
        else:
            # Raising an Exception
            raise Exception("The 'language' argument must be a valid programming language's name. The available languages are: " + str(languages))
    else:
        # Raising a TypeError Exception
        raise TypeError("The 'language' argument must be a string.")

# Function 2 - Package Versions
def package_versions(language, name):
    # Variables
    flag = False
    languages = ["python"]
    parameters = ["language", "name"]

    # Variables - Package Version
    package_version_latest = None
    package_version_installed = None

    # Parameters & Data Types
    paramaters_data = {
        "language": [str, "a string"],
        "name": [str, "a string"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            # Raising a TypeError Exception
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Checking if "language" is Valid
    if (language.lower() in languages):
        # Checking the Value of "language"
        if (language.lower() == "python"):
            # Looping through the "list_packages()" Function
            for package in list_packages("python"):
                # Checking if "name" in "package"
                if (name in package):
                    # Changing "flag" to True
                    flag = True

                    # Assigning the Variable "package_version_installed"
                    package_version_installed = package.split("==")[1]

            # Checking the "flag"
            if (not flag):
                # Raising an Exception
                raise Exception("No package data was found for {0}.".format(name))

            # Try/Except - Fetching the Package's Latest Version
            try:
                # Assigning the Variable "package_version_latest"
                package_version_latest = BeautifulSoup(requests.get("https://pypi.org/project/{0}".format(name)).text, "html.parser").body.main.find_all("div")[1].h1.text.strip().split()[1]
            except requests.ConnectionError:
                # Raising a ConnectionError Exception
                raise ConnectionError("A connection error occurred. Please try again.")
            except:
                # Raising an Exception
                raise Exception("An error occurred while fetching the package's latest version. Please try again.")

            # Returning the Dictionary
            return {
                "Latest": package_version_latest,
                "Installed": package_version_installed,
                "Upgrade Needed": package_version_installed < package_version_latest
            }
    else:
        # Raising an Exception
        raise Exception("The 'language' argument must be a valid programming language's name. The available languages are: " + str(languages))