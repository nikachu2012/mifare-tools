import argparse
import sys
from pathlib import Path

# pyscard
import smartcard.System
import smartcard.CardMonitoring
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes

# made lib
from isMifareClassic1K import isMifareClassic1K
from dumpdata_classic1K import dumpdata_classic1K
from sendAPDU import sendAPDU
from showmifare import showmifare

# dearpygui
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

def save_callback():
    print("Save Clicked")

def print_me(sender):
    print(f"Menu Item: {sender}")

dpg.create_context()
dpg.create_viewport(title="Mifare Tools  Created by nikachu2012", width=1280, height=720)
dpg.setup_dearpygui()

with dpg.viewport_menu_bar():
    with dpg.menu(label="File"):
        dpg.add_menu_item(label="Save", callback=print_me)
        dpg.add_menu_item(label="Save As", callback=print_me)

        with dpg.menu(label="Settings"):
            dpg.add_menu_item(label="Setting 1", callback=print_me, check=True)
            dpg.add_menu_item(label="Setting 2", callback=print_me)

    dpg.add_menu_item(label="Help", callback=print_me)

    with dpg.menu(label="Debug"):
        dpg.add_menu_item(label="Show Dear PyGui demo", callback=lambda: demo.show_demo())

    # with dpg.menu(label="Widget Items"):
    #     dpg.add_checkbox(label="Pick Me", callback=print_me)
    #     dpg.add_button(label="Press Me", callback=print_me)
    #     dpg.add_color_picker(label="Color Me", callback=print_me)

with dpg.window(label="Select action", width=300, height=400):
    dpg.add_text("Select action!")
    dpg.add_button(label="Display Mifare Info", callback=showmifare)
    dpg.add_button(label="Dump data (Mifare Classic 1K)", callback=dumpdata_classic1K)
    dpg.add_input_text(label="string")
    dpg.add_slider_float(label="float")

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
