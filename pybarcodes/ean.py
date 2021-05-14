# MIT License

# Copyright (c) 2021 Vitaman02

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from typing import Union
from collections import namedtuple

from pybarcodes.barcode import Barcode
from pybarcodes.exceptions import IncorrectFormat, IncorrectSizeSelection
from pybarcodes.codings import ean as EANCoding


class EAN13(Barcode):
    def __init__(self, barcode, size: str = "max"):
        super().__init__(barcode, size)

        # The digit length of the EAN13 barcode
        # The length of the actual barcode is 12 digits,
        # but this library doesn't create the check digit,
        # unless the length of the barcode is 12 digits.
        self.barcode_length = 12

        # This is the minimum size of the barcode allowed,
        # rounded up to the nearest integer.
        # The maximum allowed size of the barcode, is 200% it's size.
        # To avoid scanning errors, the max size is defined by 180% the size of the minimum value
        self.BARCODE_SIZE_MIN_PX = 400, 200
        self.BARCODE_SIZE_MID_PX = tuple(map(lambda x: int(x * 1.4), self.BARCODE_SIZE_MIN_PX))
        self.BARCODE_SIZE_MAX_PX = tuple(map(lambda x: int(x * 1.8), self.BARCODE_SIZE_MIN_PX))

        self.BARCODE_FONT_SIZE_MIN = 26
        self.BARCODE_FONT_SIZE_MID = 30
        self.BARCODE_FONT_SIZE_MAX = 34
        self.size_options = {
            "min": (self.BARCODE_SIZE_MIN_PX, self.BARCODE_FONT_SIZE_MIN),
            "mid": (self.BARCODE_SIZE_MID_PX, self.BARCODE_FONT_SIZE_MID),
            "max": (self.BARCODE_SIZE_MAX_PX, self.BARCODE_FONT_SIZE_MAX)
        }

        # Do some error checking
        if isinstance(self.code, str):
            if not self.code.isdigit():
                raise IncorrectFormat("Barcode can't contain non-digit characters.")

            if len(self.code) < self.barcode_length:
                error = f"{self.__class__.__name__} should be at least {self.barcode_length} digits long, not {len(self.code)}."
                raise IncorrectFormat(error)
            else:
                self.code = self._clean_code()

            
    
    def write(self) -> BytesIO:
        """
        Write the barcode to a BytesIO object

        Returns
        -------
        Returns the BytesIO object created
        """

        obj = BytesIO()
        obj.write(self.code.encode("ascii"))
        obj.seek(0)
        return obj

    def write_file(self, path: str) -> None:
        """
        Tries to save the barcode to a text file

        Parameters
        ----------
        path: str
            The path of the file
        """
        with open(path, "w") as file:
            file.write(self.code)

    def save(self, path: str, size: str = "max") -> Image.Image:
        """
        Create a PIL Image object and save it to the path given.
        It also return that image object to the caller.
        If no size is passed, then the method looks for the instansiated size.
        If there is no instansiated size, then an error is raised.

        Parameters
        ----------
        path: str
            The path to save the image to
        size: str
            The selected size.
            A selection of the 3 available types: "min", "mid", "max".
            Preffered size is "mid"
        
        Returns
        -------
        Returns a PIL Image object to the caller
        """

        # Check if the size given is one of the options
        if not (size in self.size_options):
            raise IncorrectSizeSelection(f"Didn't find size option '{size}'. Available size options are '{self.size_options}'")
        
        img = self._get_barcode_image(size)
        img.save(path)
    
    def show(self, size: str = "max") -> None:
        """Shows the barcode image"""

        # Check if the size given is one of the options
        if not (size in self.size_options):
            raise IncorrectSizeSelection(f"Didn't find size option '{size}'. Available size options are '{self.size_options}'")

        img = self._get_barcode_image(size)
        img.show()

    def _get_barcode_image(self, size: str) -> Image.Image:
        # Get the final image's width and height
        selected_size, font_size = self.size_options[size]

        # This is for the white space around the barcode
        padded_size = selected_size[0] + 100, selected_size[1] + 200

        # Get each column's width and height
        column_size = self._get_column_size(size)

        # Create a white base image to write columns
        base = Image.new("RGB", padded_size, (255, 255, 255))

        # Create the image for the barcode
        img = Image.new("RGB", selected_size, (255, 255, 255))
        
        # Get the binary string representation of the barcode digits
        binary_string = self.get_binary_string

        index = 0
        for digit in binary_string:
            color = (0, 0, 0) if digit == "1" else (255, 255, 255)
            column = Image.new("RGB", (column_size, img.height), color)
            img.paste(column, (index, 0))
            index += column_size
        
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

    @classmethod
    def calculate_checksum(cls, barcode: Union[str, "EAN13"]) -> int:
        """
        Calculate the checksum from the barcode given

        Returns
        -------
        A single digit integer that helps determine if the barcode is correct
        """
        if isinstance(barcode, cls):
            barcode = barcode.code
        elif isinstance(barcode, str):
            pass
        else:
            raise TypeError(f"Can't accept type {type(barcode)}")

        if len(barcode) >= 12:
            barcode = barcode[:12]
            # Here there is no check digit so it's calculated
            digits = list(map(int, list(barcode)))

            # Get even and odd indeces of the digits
            odd_weight, even_weight = (3, 1)
            weighted_even = digits[::2]
            weighted_odd = digits[1::2]
            
            # Calculate the checksum
            checksum = sum(weighted_odd) * odd_weight + sum(weighted_even) * even_weight
            if checksum % 10 == 0:
                return 0
            
            # Find the closest multiple of 10, that is equal to
            # or higher than the checksum and return the difference
            closest10 = ((checksum // 10) * 10) + 10
            return closest10 % checksum

        raise IncorrectFormat("Barcode should be at least 12 digits long.")

    @property
    def get_binary_string(self) -> str:
        """
        Converts the code to the binary string that it produces
        The binary string contains the left, center and right guards,
        and also the binary values of each digit.

        Returns
        -------
        The return string contains 1's and 0's that represent the barcode.
        This string is used to iterate over, to create the barcode.
        """

        # First find the structure that the first group of 6 follows.
        # This is determined by the first digit of the barcode
        structure = EANCoding.STRUCTURE[self.code[0]]

        code = self.code[1:]

        # Convert the barcode to a binary string with the CodeNumbers class
        # Add the left guard
        binary_string = EANCoding.LEFT_GUARD

        # Add the 6 digits after the left guard
        for i in range(0, 6):
            digit = int(code[i])
            coding = structure[i]
            binary_string += EANCoding.CODES[coding][digit]
        
        # Add the center guard
        binary_string += EANCoding.CENTER_GUARD

        # Add the 6 digits after the center guard
        for i in range(6, 12):
            digit = int(code[i])
            binary_string += EANCoding.CODES["R"][digit]
        
        check_digit = self.calculate_checksum(self.code)
        binary_string += EANCoding.CODES["R"][check_digit]

        binary_string += EANCoding.RIGHT_GUARD
        
        return binary_string

    
    def _get_column_size(self, size: str) -> int:
        """
        Finds and returns what the width of each column should be

        Parameters
        ----------
        size: str
            One of the 3 size options
        
        Returns
        -------
        Returns an integer with the width of the bar
        """
        size, _ = self.size_options[size]

        return size[0] // 95

    def _clean_code(self) -> str:
        """
        Tries to correct the barcode given

        Returns
        -------
        A new barcode is returned that has the correct length
        and the check digit is calculated if not given
        """
        if len(self.code) == 12:
            # Calculate the checksum digit
            check_digit = self.calculate_checksum(self.code)
            return self.code + str(check_digit)
        elif len(self.code) >= 13:
            # If the length is longer than 13 digits strip them
            # and calculate the check digit
            code = self.code[:12]
            check_digit = EAN13.calculate_checksum(code)
            code += str(check_digit)
            return code
        
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.code == other.code
        elif isinstance(other, str):
            return self.code == other
        return False

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: code={self.code} size={self.size}>"

    def __repr__(self):
        return self.__str__()
