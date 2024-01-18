import wpilib

I2C_DEV_ADDR = 0x70
BUTTON_A_PORT = 19
BUTTON_B_PORT = 20
POT_PORT = 7

#   Display Segment Mapping
#
#   Each segment is mapped to a one of 64 bits transmitted over the I2C bus where each
#   digit uses 16 bits. The bits are transmitted one digit at a time, starting with the
#   right most digit. For each digit, the most significant bit (bit 15) is transmitted
#   first and bit 0 is transmitted last. The mapping of each bit position to the various
#   segments is shown below.
#
#   Bit Position Map
#
#     ---- 8 ----
#   |  \   |   /  |
#   13  0  1  2   9
#   |    \ | /    |
#    -14-     -15-
#   |    / | \    |
#   12  5  4  3   10
#   |  /   |   \  |
#     ---  11 ---    .6
#
#   Notes:
#       1) The decimal point is bit position 6.
#       2) Bit position 7 is not used.


# Mapping between characters and display segments
CHAR_MAP = {
    "0": b"\x3F\x00",
    "1": b"\x06\x00",
    "2": b"\xDB\x00",
    "3": b"\xCF\x00",
    "4": b"\xE6\x00",
    "5": b"\xED\x00",
    "6": b"\xFD\x00",
    "7": b"\x07\x00",
    "8": b"\xFF\x00",
    "9": b"\xEF\x00",
    "0.": b"\x3F\x40",
    "1.": b"\x06\x40",
    "2.": b"\xDB\x40",
    "3.": b"\xCF\x40",
    "4.": b"\xE6\x40",
    "5.": b"\xED\x40",
    "6.": b"\xFD\x40",
    "7.": b"\x07\x40",
    "8.": b"\xFF\x40",
    "9.": b"\xEF\x40",
    "A": b"\xF7\x00",
    "B": b"\x8F\x12",
    "C": b"\x39\x00",
    "D": b"\x0F\x12",
    "E": b"\xF9\x00",
    "F": b"\xF1\x00",
    "G": b"\xBD\x00",
    "H": b"\xF6\x00",
    "I": b"\x09\x12",
    "J": b"\x1E\x00",
    "K": b"\x70\x0C",
    "L": b"\x38\x00",
    "M": b"\x36\x05",
    "N": b"\x36\x09",
    "O": b"\x3F\x00",
    "P": b"\xF3\x00",
    "Q": b"\x3F\x08",
    "R": b"\xF3\x08",
    "S": b"\x8D\x01",
    "T": b"\x01\x12",
    "U": b"\x3E\x00",
    "V": b"\x30\x24",
    "W": b"\x36\x28",
    "X": b"\x00\x2D",
    "Y": b"\x00\x15",
    "Z": b"\x09\x24",
    "*": b"\xC0\x3F",
    "?": b"\x83\x10",
    "@": b"\x36\x2D",  # Mapped to special non-ascii "butterfly" character
    "#": b"\x09\x2D",  # Mapped to special non-ascii "hourglass" character
    " ": b"\x00\x00",
}


def format_float(number: float) -> str:
    """Convert a float into a string with four digits max and one decimal digit"""
    rounded = round(number, 1)  # round the number to one decimal digit
    if (rounded > 999.9) or (rounded < -99.9):
        result = "####"  # Cannot display such an extreme number
    else:
        result = f"{number:5.1f}"[:5]
    return result


def format_string(message: str) -> str:
    """Align and pad the message to the given length."""
    return f"{str(message)[:4].upper():>4}"


class RevDigitBoard:
    def __init__(self):
        self._i2c = wpilib.I2C(wpilib.I2C.Port.kMXP, I2C_DEV_ADDR)
        self._button_a = wpilib.DigitalInput(BUTTON_A_PORT)
        self._button_b = wpilib.DigitalInput(BUTTON_B_PORT)
        self._potentiometer = wpilib.AnalogInput(POT_PORT)
        self._init_display()

    @property
    def button_a(self) -> bool:
        return self._button_a.get()

    @property
    def button_b(self) -> bool:
        return self._button_b.get()

    @property
    def potentiometer(self) -> float:
        return self._potentiometer.getVoltage()

    def display_message(self, message: str | float) -> None:
        """Display the provided value on the digit board"""
        if isinstance(message, float):
            self._display_float(message)
        else:
            self._display_string(message)

    def clear_display(self) -> None:
        """Clear the display"""
        self._write_display(b"\x00\x00\x00\x00\x00\x00\x00\x00")

    def _write_display(self, data: bytes) -> None:
        """Write a display update command using the specified segment data"""
        buffer = b"\x0F\x0F" + data
        self._i2c.writeBulk(buffer)

    def _init_display(self):
        """Initialize the display"""
        # Write commands to setup the display
        self._i2c.writeBulk(b"\x21")  # Enable display oscillator
        self._i2c.writeBulk(b"\xEF")  # Set to full brightness
        self._i2c.writeBulk(b"\x81")  # Turn on display, no blinking
        self.clear_display()

    def _display_float(self, message: float) -> None:
        """Display a floating point value to the display as a fixed point number"""
        buf = b""
        for i, c in enumerate(format_float(message)):
            # lookup the decimal point version of the third digit
            if i == 2:
                c += "."
            # ignore the decimal point character
            elif i == 3:
                continue
            # translate the character into the byte code
            try:
                buf = CHAR_MAP[c] + buf
            except KeyError:
                buf = b"\xFF\xFF" + buf  # Unsupported characters are left blank
        self._write_display(buf)

    def _display_string(self, message: str) -> None:
        """Display a string value to the display"""
        buf = b""
        for c in format_string(message):
            try:
                buf = CHAR_MAP[c] + buf
            except KeyError:
                buf = b"\xFF\xFF" + buf  # Unsupported characters are left blank
        self._write_display(buf)
