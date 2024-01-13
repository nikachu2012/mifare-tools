from smartcard.util import toHexString, toBytes
from sendAPDU import sendAPDU

def dumpdata(key: list[str], isAllAuth: bool):
    targetKey = list(map(toBytes, key))
    print(targetKey)
