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

if __name__ == "__main__":
    title = "Mifare-Tools READ TAG"
    desc = "Created by nikachu2012"

    parser = argparse.ArgumentParser(prog="dumpdata.py", description=f"{title}\n{desc}")
    parser.add_argument("-l", "--list", help="Print usable reader(s) list.", action="store_true")
    parser.add_argument("-v", "--version", action="version", version="version 1.0")
    parser.add_argument("--audio", help="Play wav audio while waiting for card read. (Windows only)", type=Path)
    parser.add_argument("-r", "--reader", type=int, default=0, help="Select reader index number. (You can get the number from the --list)")
    parser.add_argument(
        "-a", "--action",type=str, help="Select action.", choices=["display", "dump", "write"]
    )
    parser.add_argument(
        "-kA", "--keyA",type=str, default="FFFFFF", help="Input keyA.", nargs="*"
    )
    parser.add_argument(
        "-kB", "--keyB",type=str, default="FFFFFF", help="Input keyB.", nargs="*"
    )
    args = parser.parse_args()

    print(title)
    print(desc)
    print("")

    if args.audio:
        try:
            import simpleaudio

            cardAudio = simpleaudio.WaveObject.from_wave_file(str(args.audio))
        except Exception as e:
            print("--audio loading error")
            print(e)

            sys.exit(-1)

    if args.list:
        readersList = smartcard.System.readers()

        if len(readersList) == 0:
            print("Not found any usable reader.")
        else:
            print("=== card list ===")
            for index, elements in enumerate(readersList):
                print(f"[{index}]: {elements}")

        sys.exit(0)

    elif args.reader != None:
        print("Card reading...  ")
        print("TIPS: Timeout in 30 seconds.")
        readersList = smartcard.System.readers()

        if len(readersList) > args.reader:
            cardtype = isMifareClassic1K()
            cardreq = CardRequest(cardType=cardtype, timeout=30)

            if args.audio:
                player = cardAudio.play()
                player.wait_done()

            cardservice = cardreq.waitforcard()
            cardservice.connection.connect()

            print(f"\033[32mMifare Classic 1K Detected\033[0m")
            print(f"ATR: {toHexString(cardservice.connection.getATR())}")

            data, sw1, sw2 = cardservice.connection.transmit(
                [0xFF, 0xCA, 0x00, 0x00, 0x00]
            )
            print(f"UID: {toHexString(data)}")

            if args.action == None:
                print("Not found action.")
                sys.exit(0)

            elif args.action == "dump":
                if args.keyA:
                    target = args.keyA
                elif args.keyB:
                    target = args.keyB
                else:
                    print("Not found keyA/B")
                    sys.exit(0)
                
                
                pass
        else:
            print(f"Selected reader({args.reader}) can't connect.")
