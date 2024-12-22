"""
Author: Jake Burch
Rev: 1.0
Takes a system hive file, finds the current selected control set, and pulls data pertaining to USB Devices
including serial numbers, friendly names, and last connect/disconnect times.
"""

import regipy.exceptions
from regipy import RegistryHive
import tkinter as tk
from tkinter import filedialog

print("Please Select a valid SYSTEM hive file:")    # Prompt user to select a SYSTEM HIVE
root = tk.Tk()
root.withdraw()  # Hide the main window
while True:
    try:
        file_path = filedialog.askopenfilename()  # Opens the file explorer

        reg = RegistryHive(file_path)
        key = reg.get_key("Select").get_value("Current")
        controlSet = (reg.get_control_sets(file_path))  # Get Control Set from path
        controlSet = str(controlSet)  # Set controlSet to string
        controlSet = controlSet[4:17]  # Trim excess characters
        break

    except regipy.exceptions.RegistryKeyNotFoundException as e:
        print("Cannot read System hive or not selecting a valid hive type", e)

    except Exception as e:
        print("An unknown error has occurred...")

key = str(key)

completePath = 'Select\\' + controlSet + '\\Enum\\USBSTOR'

try:
    for x in reg.get_key(completePath).iter_subkeys(): # Iterate over USBSTOR key for Subkeys
        print("\nUSB Device: ", x.name)

        for y in x.iter_subkeys(): # Iterate over subkeys inside USB
            print("Friendly Name:", y.get_value("FriendlyName"))
            if "&" in y.name[1]:
                print("Serial Number:", y.name, "(Windows Generated)")
            else:
                print("Serial Number:", y.name, "(Vendor Generated)")
            path = completePath + "\\" + y.name
            print("First Install Time: " + str(reg.get_key("Select\\ControlSet001\\Enum\\USBSTOR\\" + x.name +
                                                           "\\" + y.name + "\\Properties"
                                                           "\\{83da6326-97a6-4088-9453-a1923f573b29}\\0064").get_value(
                                                           '(default)')))

            print("Install Time: " + str(reg.get_key("Select\\ControlSet001\\Enum\\USBSTOR\\" + x.name +
                                                           "\\" + y.name + "\\Properties"
                                                           "\\{83da6326-97a6-4088-9453-a1923f573b29}\\0065").get_value(
                                                           '(default)')))
            print("Last Connection Time: " + str(reg.get_key("Select\\ControlSet001\\Enum\\USBSTOR\\" + x.name +
                                                           "\\" +  y.name + "\\Properties"
                                                           "\\{83da6326-97a6-4088-9453-a1923f573b29}\\0066").get_value(
                                                           '(default)')))

            print("Last Disconnect Time: " + str(reg.get_key("Select\\ControlSet001\\Enum\\USBSTOR\\" + x.name +
                                                           "\\" + y.name + "\\Properties"
                                                           "\\{83da6326-97a6-4088-9453-a1923f573b29}\\0067").get_value(
                                                           '(default)')))

        print("\n")
except regipy.exceptions.RegistryKeyNotFoundException as e:
    print("Key not found:", e)
