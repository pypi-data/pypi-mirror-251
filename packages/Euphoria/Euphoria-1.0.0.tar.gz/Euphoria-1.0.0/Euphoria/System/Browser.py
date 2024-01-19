# Euphoria (System) - Browser

''' This is the "Browser" module. '''

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
import validators
import webbrowser

# Function 1 - Open
def open(url, operation=1, auto_raise=True, on_start=None, on_end=None):
    # Nested Function 1 - Function
    def function():
        pass

    # Variables
    parameters = ["url", "operation", "auto_raise", "on_start", "on_end"]

    # Parameters & Data Types
    paramaters_data = {
        "url": [str, "a string"],
        "operation": [int, "an integer"],
        "auto_raise": [bool, "a boolean"],
        "on_start": [(type(function), type(None)), "a function or None"],
        "on_end": [(type(function), type(None)), "a function or None"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            # Raising a TypeError Exception
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Checking if "url" is Valid
    if (validators.url(url)):
        pass
    else:
        # Raising an Exception
        raise Exception("The 'url' argument doesn't seem to be a valid URL.")

    # Checking if "operation" is Valid
    if (operation in [1, 2, 3]):
        pass
    else:
        # Raising an Exception
        raise Exception("The 'operation' argument must be either 1, 2, or 3.")

    # Calling the "on_start" Function
    on_start()

    # Opening the URL in the Browser
    webbrowser.open(url, new=operation-1, autoraise=auto_raise)

    # Calling the "on_end" Function
    on_end()