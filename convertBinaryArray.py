from smartcard.util import toHexString, toBytes

def convertBinaryArrayToStr(data: list[list[int]], hasASCII: bool) -> str:
    result = ""

    try:
        for i, e in enumerate(data):
            if e is []:
                message = "Couldn't dump this sector data."
                result += f"Sector {i // 4:<2} Block {i:<3}: {message:<47}"

                if hasASCII:
                    result += f" <                >"

                result += "\n"
                continue

            toConvertASCII = ""

            for j in e:
                if 0x00 <= j <= 0x20 or 0x7f <= j <= 0xA0:
                    toConvertASCII += " "
                else:
                    toConvertASCII += chr(j)

            if i % 4 == 0:
                sectorText = f"Sector {i // 4:<2}"
            else:
                sectorText = f"         "

            result += f"{sectorText} Block {i:<3}: {toHexString(e):<47}"
            
            if hasASCII:
                result += f" <{toConvertASCII:<16}>"

            result += "\n"

        return result
        
    except Exception as e:
        raise e
