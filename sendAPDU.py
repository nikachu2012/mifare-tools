from smartcard.util import toHexString, toBytes
from logger import log

# f = open("mifare_tools.log", mode="a")


def sendAPDU(data:list[int], connection=None) -> tuple:
    if not connection:
        return None
    else:
        try:
            return connection.transmit(
                data
            )
        except Exception as e:
            print("\033[31mERROR - Couldn't send APDU\033[0m")
            raise e

def sendAPDUwithLOG(data:list[int], logObj, connection=None, ) -> tuple:
    log(logObj, f"sendAPDU-status: Card sending... (APDU: {toHexString(data)})")
    try:
        result = connection.transmit(
            data
        )

        if result[1] == 0x90 and result[2] == 0x00:
            log(logObj, f"sendAPDU-status: Card send success! (SW1: {hex(result[1])}, SW2: {hex(result[2])}, Response: {toHexString(result[0])})")
            return result
        else:
            log(logObj, f"sendAPDU-WARNING: Card result error (SW1: {hex(result[1])}, SW2: {hex(result[2])}, Response: {toHexString(result[0])})")
            return None

    except Exception as e:
        print("\033[31mERROR - Couldn't send APDU\033[0m")
        log(logObj, f"!sendAPDU-Error: Couldn't send APDU.")

        raise e
