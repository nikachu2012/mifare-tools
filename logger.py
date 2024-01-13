import dearpygui.dearpygui as dpg
from datetime import datetime

def log(target: any, text: str):
    dpg.set_value(target, dpg.get_value(target)+f"[{datetime.now().isoformat()}] {text}\n")
    return
