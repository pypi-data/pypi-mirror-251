# Euphoria (System) - Keyboard

''' This is the "Keyboard" module. '''

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
import pyautogui

# Variables
KEYS = pyautogui.KEY_NAMES

# Function 1 - Write
def write(text, interval=0.0):
    # Variables
    parameters = ["text", "interval"]

    # Parameters & Data Types
    paramaters_data = {
        "text": [str, "a string"],
        "interval": [(int, float), "an integer or a float"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            # Raising a TypeError Exception
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Writing the Text
    pyautogui.write(text, interval=interval)

# Function 2 - Press
def press(keys, presses=1, interval=0.0):
    # Variables
    parameters = ["keys", "presses", "interval"]

    # Parameters & Data Types
    paramaters_data = {
        "keys": [(str, list), "a string or a list"],
        "presses": [int, "an integer"],
        "interval": [(int, float), "an integer or a float"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            # Raising a TypeError Exception
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Checking if "keys" is a String or List
    if (isinstance(keys, list)):
        # Creating Another Variable "keys" with LowerCase Keys
        keys = [key.lower() for key in keys]

        # Iterating through "keys"
        for key in keys:
            # Checking if "key" is Valid
            if (key in KEYS):
                pass
            else:
                # Raising an Exception
                raise Exception("The key '{0}' is not a valid key. The available keys are: \n\n".format(key) + str(KEYS))
    elif (isinstance(keys, str)):
        # Creating Another Variable "keys" with LowerCase Key
        keys = keys.lower()

        # Checking if "keys" is Valid
        if (keys in KEYS):
            pass
        else:
            # Raising an Exception
            raise Exception("The key '{0}' is not a valid key. The available keys are: \n\n".format(keys) + str(KEYS))

    # Pressing the Key(s)
    pyautogui.press(keys, presses=presses, interval=interval)

# Function 3 - Key Down
def key_down(key):
    # Checking the Data Type of "key"
    if (isinstance(key, str)):
        # Checking if "key" is Valid
        if (key.lower() in KEYS):
            # Operation on the Key
            pyautogui.keyDown(key.lower())
        else:
            # Raising an Exception
            raise Exception("The key '{0}' is not a valid key. The available keys are: \n\n".format(key) + str(KEYS))
    else:
        # Raising a TypeError Exception
        raise TypeError("The 'key' argument must be a string.")

# Function 4 - Key Up
def key_up(key):
    # Checking the Data Type of "key"
    if (isinstance(key, str)):
        # Checking if "key" is Valid
        if (key.lower() in KEYS):
            # Operation on the Key
            pyautogui.keyUp(key.lower())
        else:
            # Raising an Exception
            raise Exception("The key '{0}' is not a valid key. The available keys are: \n\n".format(key) + str(KEYS))
    else:
        # Raising a TypeError Exception
        raise TypeError("The 'key' argument must be a string.")

# Function 5 - Hot Key
def hot_key(*args):
    # Iterating through "args"
    for arg in args:
        # Checking the Data Type of "arg"
        if (isinstance(arg, str)):
            # Checking if "arg" is Valid
            if (arg in KEYS):
                pass
            else:
                # Raising an Exception
                raise Exception("The key '{0}' is not a valid key. The available keys are: \n\n".format(arg) + str(KEYS))
        else:
            # Raising an Exception
            raise TypeError("Each key must be a string.")

    # Operation on the Keys
    pyautogui.hotkey(args)