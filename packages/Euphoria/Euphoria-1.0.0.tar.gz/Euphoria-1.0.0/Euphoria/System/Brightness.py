# Euphoria (System) - Brightness

''' This is the "Brightness" module. '''

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
import platform
from .__init__ import UnsupportedOSError

# Checking the OS
if (platform.system() not in ["Windows", "Linux"]):
    # Raising an UnsupportedOSError Exception
    raise UnsupportedOSError("This module only works on Windows and Linux.")
else:
    # Try/Except - Importing "screen-brightness-control"
    try:
        # Importing
        import screen_brightness_control as sbc
    except:
        # Raising a ModuleNotFoundError Exception
        raise ModuleNotFoundError("The 'screen-brightness-control' package must be installed for this module to work.")

# Function 1 - Max
def max():
    # Setting the Brightness
    sbc.set_brightness(100)

# Function 2 - Min
def min():
    # Setting the Brightness
    sbc.set_brightness(0)

# Function 3 - Set
def set(value, display=0):
    # Variables
    parameters = ["value", "display"]

    # Parameters & Data Types
    paramaters_data = {
        "value": [(int, float), "an integer or a float"],
        "display": [(int, str), "an integer or a string"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            # Raising a TypeError Exception
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Setting the Brightness
    sbc.set_brightness(value, display=display)

# Function 4 - Fade
def fade(final, start=None, interval=0.01, increment=1, blocking=True):
    # Variables
    parameters = ["final", "start", "interval", "increment", "blocking"]

    # Parameters & Data Types
    paramaters_data = {
        "final": [(int, float), "an integer or a float"],
        "start": [(int, float, type(None)), "an integer or a float"],
        "interval": [(int, float), "an integer or a float"],
        "increment": [(int, float), "an integer or a float"],
        "blocking": [bool, "a boolean"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            # Raising a TypeError Exception
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Setting the Brightness
    sbc.fade_brightness(final, start=start, interval=interval, increment=increment, blocking=blocking)

# Function 5 - Get
def get():
    # Returning the Data
    return {"Brightness": sbc.get_brightness(), "Monitors": sbc.list_monitors_info()}