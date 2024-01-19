# Euphoria (System) - Volume

''' This is the "Volume" module. '''

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
import os
import platform
from .__init__ import UnsupportedOSError

# Checking the OS
if (platform.system() not in ["Windows"]):
    # Raising an UnsupportedOSError Exception
    raise UnsupportedOSError("This module only works on Windows.")

# Function 1 - Max
def max():
    # Setting the Volume
    os.chdir(os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets")
    os.system("setvol 100")

# Function 2 - Min
def min():
    # Setting the Volume
    os.chdir(os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets")
    os.system("setvol 0")

# Function 3 - Increase
def increase(value):
    # Checking the Data Type of "value"
    if (isinstance(value, int)):
        # Setting the Volume
        os.chdir(os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets")
        os.system("setvol +" + str(value))
    else:
        # Raising a TypeError Exception
        raise TypeError("The 'value' argument must be an integer.")

# Function 4 - Decrease
def decrease(value):
    # Checking the Data Type of "value"
    if (isinstance(value, int)):
        # Setting the Volume
        os.chdir(os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets")
        os.system("setvol -" + str(value))
    else:
        # Raising a TypeError Exception
        raise TypeError("The 'value' argument must be an integer.")

# Function 5 - Mute
def mute():
    # Setting the Volume
    os.chdir(os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets")
    os.system("setvol mute")

# Function 6 - Unmute
def unmute():
    # Setting the Volume
    os.chdir(os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets")
    os.system("setvol unmute")

# Function 7 - Set
def set(value):
    # Checking the Data Type of "value"
    if (isinstance(value, int)):
        # Setting the Volume
        os.chdir(os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets")
        os.system("setvol " + str(value))
    else:
        # Raising a TypeError Exception
        raise TypeError("The 'value' argument must be an integer.")