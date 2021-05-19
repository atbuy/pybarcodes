from PIL import Image, ImageDraw, ImageFont
from typing import Union
from collections import namedtuple

from .barcode import Barcode
from .exceptions import IncorrectFormat
from .codings import codex as CODEXCoding


Size = namedtuple("Size", "width height")


class Code(Barcode):
    def __init__(self, barcode: Union[str, int]):
        super().__init__(barcode.upper())

        self.code = self._clean_code()

        # Calculate the variable width of the barcode
        # 10 pixels for each character
        if self.BARCODE_SIZE[0] == -1:
            self.BARCODE_SIZE = (len(self.code) * 6 + len(CODEXCoding.GUARD) * 2) * 7, self.BARCODE_SIZE[1]

        column_size = 0
        for char in self.get_binary_string:
            if char == "0":
                column_size += 1
            elif char in ("1", " "):
                column_size += 3
            column_size += 1

        # Calculate how many character will have to be written
        self.BARCODE_COLUMN_NUMBER = column_size

    @property
    def get_binary_string(self) -> str:
        """Converts the code to the binary string that it produces.

        The binary string contains the start and stop characters
        and the actual characters themselves, encoded in binary.

        Returns
        -------
        str:
            The return string contains 1's and 0's that represent the barcode.
            This string is used to iterate over, to create the barcode.
        """

        # Replace all characters with valid reference characters (N, W, S and _)
        code = "".join([CODEXCoding.CODES[char] for char in self.code])

        # Add the start character
        code = CODEXCoding.GUARD + code

        # Add the stop character
        code += CODEXCoding.GUARD

        return self._convert_to_binary(code)

    def calculate_checksum(self, barcode: Union[str, "CODE39"] = None) -> int:
        """Calculate the checksum of the barcode

        Parameters
        ----------
        barcode: Union[str, "CODE39"]
            The barcode to calculate the check digit of.

        Returns
        -------
        A single digit integer that helps determine if the barcode is correct

        Raises
        ------
        TypeError
            Raised when the barcode is not an acceptable type
        IncorrectFormat
            Raised when the barcode is not in the format expected
        """  

        if isinstance(barcode, self.__class__):
            barcode = barcode.code
        elif isinstance(barcode, str):
            pass
        elif barcode is None or self.code:
            return CODEXCoding.REFERENCE_DIGITS[self.checksum]
        else:
            raise TypeError(f"Can't accept type {type(barcode)}")

        barcode = barcode.upper()

        # If the barcode is only 1 character long
        # Then the check sum will be that same character
        if len(barcode) == 1:
            return CODEXCoding.REFERENCE_DIGITS[barcode]

        # Find the number value of each digit
        numbers = [CODEXCoding.REFERENCE_DIGITS[char] for char in list(barcode)]

        # Calculate the modulo 43 of the sum
        return sum(numbers) % 43

    def _get_barcode_image(self) -> Image.Image:
        """Creates a PIL Image from the binary string of the barcode.

        Returns
        -------
        A PIL Image with the barcode is returned to the caller.
        """

        # Get the padding around the barcode
        padding = self.BARCODE_PADDING

        # Get the image's width and height
        selected_size, font_size = self.BARCODE_SIZE, self.BARCODE_FONT_SIZE

        # This is for the whitespace around the barcode
        padded_size = selected_size[0] + padding.width, selected_size[1] + padding.height

        # Get each column's width and height
        column_size = self._get_column_size()

        # Create a white base image to paste the barcode on
        base = Image.new("RGB", padded_size, (255, 255, 255))

        # Create the image to write the columns
        img = Image.new("RGB", (column_size * self.BARCODE_COLUMN_NUMBER, selected_size[1]), (255, 255, 255))

        # This is the spacing we are going to add after each digit
        space = Image.new("RGB", (column_size, img.height), (255, 255, 255))

        # Create a binary string representation of the barcode digits
        binary_string = self.get_binary_string

        index = 0
        for digit in binary_string:
            color = (0, 0, 0)

            # If the character is a `1`, then we write a bar with ratio 3:1
            # So the bar needs to be 3 times the size of the bar we write in the `0` situation
            # If the character is a ` ` (space) then we write 3 times the size on the spacing
            # We also need to add a single width column of spacing after each digit
            if digit == "1":
                column_width = round(column_size * 3)
            elif digit == " ":
                column_width = round(column_size * 3)
                color = (255, 255, 255)
            else:
                column_width = column_size

            # First paste the column
            column = Image.new("RGB", (column_width, img.height), color)
            img.paste(column, (index, 0))
            index += column_width

            if not (color[0] == 255):
                # Then paste the spacing
                img.paste(space, (index, 0))
                index += column_size

        # Crop redundant whitespace after barcode
        img = img.crop((0, 0, index, img.height))

        # Paste the barcode on the center of the padded base
        Point = namedtuple("Point", "x y")
        base_center = Point(base.width // 2, base.height // 2)
        img_center = Point(img.width // 2, img.height // 2)

        base.paste(img, (base_center.x - img_center.x, base_center.y - img_center.y))

        # Write the digits at the bottom
        font_path = "./fonts/arial.ttf"

        draw = ImageDraw.Draw(base)
        font = ImageFont.truetype(font_path, font_size)

        text_width, _ = draw.textsize(self.code, font)
        x = base_center.x - text_width // 2
        y = base.height - (base.height - img.height) // 2

        draw.text((x, y), self.code, (0, 0, 0), font=font)
        return base

    def _convert_to_binary(self, string: str) -> str:
        """Renders the string from `get_binary_string` into binary

        The string given would be in some form of `NSWNWN` etc.
        The output of this example would be `0 1010`.

        Returns
        -------
        The binary string + spaces is returned to the caller.
        """

        references = {"N": "0", "W": "1", "S": " "}
        out = ""
        for char in string:
            out += references[char]

        return out

    def _clean_code(self) -> str:
        """Tries to correct the barcode given

        Returns
        -------
        A new barcode is returned that has the correct length
        and the check digit is calculated if not given
        """
        for char in self.code:
            if not (char in CODEXCoding.CODES) or char == "_":
                raise IncorrectFormat(f"Character {char} is not supported by {self.__class__.__name__}")

        reference = self.calculate_checksum(self.code)
        checkchar = CODEXCoding.REFERENCE_NUMBERS[reference]

        self.checksum = checkchar
        return self.code + str(checkchar)

    def _trim(self, code: str) -> str:
        """Removes the start and stop characters from the barcode

        Parameters
        ----------
        code: str
            The code of type `Code` to trim

        Returns
        -------

        str:
            The barcode is returned without the start and stop characters
        """

        return code[5:-6]

    def _get_column_size(self) -> int:
        """Finds and returns what the width of each column should be

        Returns
        -------
        Returns an integer with the width of the bar
        """

        return self.BARCODE_SIZE[0] // self.BARCODE_COLUMN_NUMBER


class CODE39(Code):
    """The class to represent Code39 barcodes

    Attributes
    ----------
    BARCODE_SIZE: Tuple[int, int]
        The barcode's size and not the output image's size
    BARCODE_FONT_SIZE: int
        The size of the font under the barcode
    BARCODE_PADDING: Tuple[int, int]
        The padding around the actual barcode
    """

    BARCODE_SIZE = -1, 240
    BARCODE_FONT_SIZE = 30
    BARCODE_PADDING = Size(100, 200)

    def __init__(self, barcode: Union[str, int]):
        super().__init__(barcode)
