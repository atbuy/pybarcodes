from collections import namedtuple
from typing import Union

from PIL import Image, ImageDraw

from .barcode import Barcode
from .codings import codex as CODEXCoding
from .exceptions import IncorrectFormat

Size = namedtuple("Size", "width height")


class Code(Barcode):
    def __init__(self, barcode: Union[str, int]):
        super().__init__(barcode)

        self.checksum = self.code[-1]

        # Calculate the variable width of the barcod
        # 6 pixels for each character
        if self.BARCODE_SIZE[0] == -1:
            self.BARCODE_SIZE = (
                (len(self.code) * 6 + len(CODEXCoding.GUARD) * 2) * 6,
                self.BARCODE_SIZE[1],
            )

        column_size = 0
        for char in self.get_binary_string:
            if char == "0":
                column_size += 1
            elif char in ("1", " "):
                column_size += 3
            column_size += 1

        # Calculate how many character will have to be written
        self.BARCODE_COLUMN_NUMBER = column_size

    @classmethod
    def validate(cls, barcode: Union[str, int]) -> None:
        code = str(barcode).upper()

        for char in code:
            if char not in CODEXCoding.CODES or char == "_":
                raise IncorrectFormat(
                    f"Character {char} is not supported by {cls.__name__}"
                )

    @classmethod
    def normalize(cls, barcode: Union[str, int]) -> str:
        cls.validate(barcode)
        code = str(barcode).upper()
        reference = cls._calculate_checksum(code)
        checkchar = CODEXCoding.REFERENCE_NUMBERS[reference]
        return code + checkchar

    @classmethod
    def _calculate_checksum(cls, barcode: str) -> int:
        code = barcode.upper()
        for char in code:
            if char not in CODEXCoding.REFERENCE_DIGITS:
                raise IncorrectFormat(
                    f"Character {char} is not supported by {cls.__name__}"
                )

        if len(code) == 1:
            return CODEXCoding.REFERENCE_DIGITS[code]

        numbers = [CODEXCoding.REFERENCE_DIGITS[char] for char in list(code)]
        return sum(numbers) % 43

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
        elif barcode is None:
            return CODEXCoding.REFERENCE_DIGITS[self.checksum]
        else:
            raise TypeError(f"Can't accept type {type(barcode)}")

        return self._calculate_checksum(barcode)

    def _get_barcode_image(
        self,
        module_width: int = None,
        bar_height: int = None,
        quiet_zone: int = None,
        font_size: int = None,
        draw_text: bool = True,
    ) -> Image.Image:
        """Creates a PIL Image from the binary string of the barcode.

        Returns
        -------
        A PIL Image with the barcode is returned to the caller.
        """

        module_width, bar_height, quiet_zone, font_size, text_padding = (
            self._get_render_options(
                module_width=module_width,
                bar_height=bar_height,
                quiet_zone=quiet_zone,
                font_size=font_size,
                draw_text=draw_text,
            )
        )

        # Create the image to write the columns
        img = Image.new(
            "RGB",
            (module_width * self.BARCODE_COLUMN_NUMBER, bar_height),
            (255, 255, 255),
        )

        # This is the spacing we are going to add after each digit
        space = Image.new("RGB", (module_width, img.height), (255, 255, 255))

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
                column_width = module_width * 3
            elif digit == " ":
                column_width = module_width * 3
                color = (255, 255, 255)
            else:
                column_width = module_width

            # First paste the column
            column = Image.new("RGB", (column_width, img.height), color)
            img.paste(column, (index, 0))
            index += column_width

            if not (color[0] == 255):
                # Then paste the spacing
                img.paste(space, (index, 0))
                index += space.width

        # Crop redundant whitespace after barcode
        img = img.crop((0, 0, index, img.height))

        base = Image.new(
            "RGB",
            (img.width + quiet_zone * 2, bar_height + text_padding),
            (255, 255, 255),
        )

        # Paste the barcode on the center of the padded base
        Point = namedtuple("Point", "x y")
        base_center = Point(base.width // 2, base.height // 2)

        base.paste(img, (quiet_zone, text_padding // 2))

        if not draw_text:
            return base

        draw = ImageDraw.Draw(base)
        font = self._get_default_font(font_size)

        text_width = draw.textlength(self.code, font)
        x = base_center.x - text_width // 2
        y = text_padding // 2 + img.height

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

        return self.normalize(self.code)

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
    BARCODE_PADDING = Size(50, 100)

    def __init__(self, barcode: Union[str, int]):
        super().__init__(barcode.upper())
