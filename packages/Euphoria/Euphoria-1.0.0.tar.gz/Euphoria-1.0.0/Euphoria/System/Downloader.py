# Euphoria (System) - Downloader

''' This is the "Downloader" module. '''

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

# Function 1 - Download
def download(url, path):
    # Variables
    parameters = ["url", "path"]

    # Parameters & Data Types
    paramaters_data = {
        "url": [str, "a string"],
        "path": [str, "a string"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            # Raising a TypeError Exception
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Try/Except - Fetching the File's Data
    try:
        # Variables
        data = requests.get(url).content
    except requests.ConnectionError:
        # Raising a ConnectionError Exception
        raise ConnectionError("A connection error occurred. Please try again.")
    except:
        # Raising an Exception
        raise Exception("An error occurred while fetching the file. Please try again.")

    # Writing to the File
    with open(path, "wb") as file:
        file.write(data)