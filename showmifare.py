import smartcard.System
import smartcard.CardMonitoring
from smartcard.Exceptions import NoCardException
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes


# made lib
from isMifareClassic1K import isMifareClassic1K
from sendAPDU import sendAPDU

import dearpygui.dearpygui as dpg



def showmifare():
    readers = smartcard.System.readers()

    selected = ""

    def getIndex(target):
        for i, e in enumerate(readers):
            if str(e) == target:
                return i
        return None

    def getData(sender):
        if dpg.get_value(selectedReader):
            reader_connection = readers[getIndex(dpg.get_value(selectedReader))].createConnection()
        else:
            return
        dpg.configure_item(sender, show=False)
        dpg.configure_item(cardStatusText, show=False)
        dpg.configure_item(atrText, show=False)
        dpg.configure_item(uidText, show=False)
        dpg.set_value(status, "Status: Card waiting...")
        while True:
            try:
                reader_connection.connect()
                break
            except NoCardException as e:
                continue

        uiddata, sw1, sw2 = sendAPDU(
            [0xFF, 0xCA, 0x00, 0x00, 0x00], reader_connection
        )

        if sw1 != 0x90 and sw2 != 0x00:
            uiddata == None
        
        dpg.set_value(status, "Status: Card read.")
        
        atr = reader_connection.getATR()
        if isMifareClassic1K().matches(atr):
            dpg.configure_item(cardStatusText, color=[0,255,0,255])
            dpg.set_value(cardStatusText, "Mifare Classic 1K Detected")
            dpg.configure_item(cardStatusText, show=True)

            dpg.set_value(atrText, toHexString(atr))
            dpg.configure_item(atrText, show=True)

            if uiddata:
                dpg.set_value(uidText, toHexString(uiddata))
                dpg.configure_item(uidText, show=True)

        else:
            dpg.configure_item(cardStatusText, color=[255,0,0,255])
            dpg.set_value(cardStatusText, "Detected card is not Mifare Classic 1K")
            dpg.configure_item(cardStatusText, show=True)

        dpg.configure_item(sender, show=True)

        pass

    with dpg.window(label="Display Mifare Info", width=600, height=300, pos=(100,100)):
        selectedReader = dpg.add_combo(readers, label="Select reader")
        dpg.add_button(label="Get Info", callback=getData)
        status = dpg.add_text("Status: None")

        cardStatusText = dpg.add_text(show=False)
        atrText = dpg.add_input_text(show=False, label="ATR", width=500, readonly=True, hexadecimal=True)
        uidText = dpg.add_input_text(show=False, label="UID", width=500, readonly=True, hexadecimal=True)


