import argparse
import sys
from pathlib import Path

# pyscard
import smartcard.System
import smartcard.CardMonitoring
from smartcard.CardRequest import CardRequest
from smartcard.CardType import CardType
from smartcard.util import toHexString, toBytes


class isMifareClassic1K(CardType):
    def matches(self, atr, reader=None):
        # Mifare Classic 1K ATR: 3B 8F 80 01 80 4F 0C A0 00 00 03 06 .. 00 01 00 00 00 00 ..
        isMifare = [
            0x3B,
            0x8F,
            0x80,
            0x01,
            0x80,
            0x4F,
            0x0C,
            0xA0,
            0x00,
            0x00,
            0x03,
            0x06,
            None,
            0x00,
            0x01,
            0x00,
            0x00,
            0x00,
            0x00,
            None,
        ]
        flg = False
        for i, e in enumerate(atr):
            flg |= (isMifare[i] if isMifare[i] != None else e) != e

        return not flg


if __name__ == "__main__":
    title = "Mifare-Tools READ TAG"
    desc = "Created by nikachu2012"

    parser = argparse.ArgumentParser(prog="dumpdata.py", description=f"{title}\n{desc}")
    parser.add_argument(
        "-l", "--list", help="Print usable reader(s) list.", action="store_true"
    )

    parser.add_argument("-v", "--version", action="version", version="version 1.0")

    parser.add_argument(
        "--audio",
        help="Play wav audio while waiting for card read. (Windows only)",
        type=Path,
    )

    parser.add_argument(
        "--reader",
        type=int,
        default=0,
        help="Select reader index number. (You can get the number from the --list)",
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

            

        else:
            print(f"Selected reader({args.reader}) can't connect.")
