
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
            print("\033[31mERROR - Can't send APDU\033[0m")
            raise e
