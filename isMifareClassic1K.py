from smartcard.CardType import CardType

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
