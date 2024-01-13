import smartcard.System
import smartcard.CardMonitoring
from smartcard.Exceptions import NoCardException
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes

from datetime import datetime


# made lib
from isMifareClassic1K import isMifareClassic1K
from sendAPDU import sendAPDU, sendAPDUwithLOG
from logger import log
from convertBinaryArray import convertBinaryArrayToStr

import dearpygui.dearpygui as dpg

sector_count = 16

def dumpdata_classic1K():
    readers = smartcard.System.readers()

    def getIndex(target):
        for i, e in enumerate(readers):
            if str(e) == target:
                return i
        raise
    
    def fillKeyA():
        fillv = dpg.get_value(keyAarray[0])

        for i in range(sector_count):
            dpg.set_value(keyAarray[i], fillv)

    def fillKeyB():
        fillv = dpg.get_value(keyBarray[0])

        for i in range(sector_count):
            dpg.set_value(keyBarray[i], fillv)

    def getData(sender):
        starttime = datetime.now().isoformat()
        with dpg.window(label=f"Process Status ({starttime})", width=600, height=400, pos=(300,0)):
            savebtn = dpg.add_button(label="Save to file")
            logText = dpg.add_text()

        log(logText, "started: Dump data (Mifare Classic 1K)")

        if dpg.get_value(selectedReader):
            reader_connection = readers[getIndex(dpg.get_value(selectedReader))].createConnection()
            log(logText, f"Reader({dpg.get_value(selectedReader)}) connected.")

        else:
            log(logText, f"!ERROR: Reader({dpg.get_value(selectedReader)}) can't connect.")
            log(logText, f"Exit...")
            return
        
        dpg.configure_item(sender, show=False)

        log(logText, "status: Card waiting...")
        dpg.set_value(status, "Status: Card waiting...")

        while True:
            try:
                reader_connection.connect()
                log(logText, "status: Card connected")
                break
            except NoCardException as e:
                continue
        
        log(logText, "status: Card dumping...")
        dpg.set_value(status, "Status: Card Dumping...")

        # uiddata, sw1, sw2 = sendAPDU(
        #     [0xFF, 0xCA, 0x00, 0x00, 0x00], reader_connection
        # )

        # if sw1 != 0x90 and sw2 != 0x00:
        #     uiddata == None
            
        atr = reader_connection.getATR()
        if isMifareClassic1K().matches(atr):
            log(logText, f"status: Mifare Classic 1K detected. (ATR: {toHexString(atr)})")

            # LoadAuthenticationKeys = [0xFF, 0x82, 0x00, 0x00, 0x06]
            # Authentication = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, 0x0c, 0x60, 0x00]
            # ReadBinaryBlocks = [0xFF, 0xB0, 0x00, 0x00, 0x10]

            sector_data = [[] for _ in range(sector_count*4)]

            for i in range(sector_count):
                log(logText, f"status: === Dump sector {i} ===")

                key = None
                if dpg.get_value(keyAarray[i]) != "" and dpg.get_value(keyBarray[i]) != "":
                    isB = False
                    key = dpg.get_value(keyAarray[i])
                elif dpg.get_value(keyAarray[i]) != "":
                    isB = False
                    key = dpg.get_value(keyAarray[i])
                elif dpg.get_value(keyBarray[i]) != "":
                    isB = True
                    key = dpg.get_value(keyBarray[i])
                else:
                    log(logText, f"!ERROR: Both KeyA/B are None(sector {i})")
                    log(logText, f"Exit...")

                    dpg.set_value(status, "Status: Error detected. (Next Ready)")
                    break

                apdu = [0xFF, 0x82, 0x00, 0x00, 0x06] + toBytes(key)
                response = sendAPDUwithLOG(apdu + toBytes(key), logText, reader_connection)
                if not response:
                    continue
                
                apdu = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, i*4, 0x61 if isB else 0x60, 0x00]
                response = sendAPDUwithLOG(apdu, logText, reader_connection)

                if not response:
                    continue
                
                apdu = [0xFF, 0xB0, 0x00, i*4+0, 0x10]
                response = sendAPDUwithLOG(apdu, logText, reader_connection)
                if not response:
                    continue
                sector_data[i*4+0] = response[0]

                apdu = [0xFF, 0xB0, 0x00, i*4+1, 0x10]
                response = sendAPDUwithLOG(apdu, logText, reader_connection)
                if not response:
                    continue
                sector_data[i*4+1] = response[0]

                apdu = [0xFF, 0xB0, 0x00, i*4+2, 0x10]
                response = sendAPDUwithLOG(apdu, logText, reader_connection)
                if not response:
                    continue
                sector_data[i*4+2] = response[0]

                apdu = [0xFF, 0xB0, 0x00, i*4+3, 0x10]
                response = sendAPDUwithLOG(apdu, logText, reader_connection)
                if not response:
                    continue
                sector_data[i*4+3] = response[0]

            else:
                log(logText, f"status: All dump success!")

                with dpg.window(label=f"Dumped Data ({starttime})", width=600, height=400, pos=(300,0)):
                    resultView = dpg.add_input_text(multiline=True, readonly=True, width=-1, height=-1)

                    print(convertBinaryArrayToStr(sector_data, True))

                    dpg.set_value(resultView, convertBinaryArrayToStr(sector_data, True))
                
                dpg.set_value(status, "Status: Success! (Next Ready)")

        else:
            log(logText, f"status: This card is not Mifare Classic 1K (ATR: {atr})")

        
        dpg.configure_item(sender, show=True)

    with dpg.window(label="Dump Data (Mifare Classic 1K)", width=400, height=600, pos=(150,150)):
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Save", callback=lambda: False)
                dpg.add_menu_item(label="Save As", callback=lambda: False)

            with dpg.menu(label="Tool"):
                dpg.add_menu_item(label="Fill KeyA with sector 0", callback=fillKeyA)
                dpg.add_menu_item(label="Fill KeyB with sector 0", callback=fillKeyB)

        selectedReader = dpg.add_combo(readers, label="Select reader")
        dpg.add_button(label="Dump Data", callback=getData)
        status = dpg.add_text("Status: Ready")

        dpg.add_text("== KeyA/B (Tips: You can fill key from \"Tool\")")

        keyAarray = []
        keyBarray = []
        with dpg.table():
            dpg.add_table_column(label="Sector", width_fixed=True)
            dpg.add_table_column(label="KeyA")
            dpg.add_table_column(label="KeyB")

            for i in range(sector_count):
                with dpg.table_row():
                    dpg.add_text(f"{i}")
                    keyAarray.append(dpg.add_input_text(hexadecimal=True, hint="KeyA", width=-1, no_spaces=True))
                    keyBarray.append(dpg.add_input_text(hexadecimal=True, hint="KeyB", width=-1, no_spaces=True))

