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


from typing import Union

from pybarcodes.barcode import Barcode
from pybarcodes.exceptions import IncorrectFormat
from pybarcodes.codings import ean as EANCoding


class EAN13(Barcode):
    def __init__(self, barcode):
        super().__init__(barcode)

        # The number of digits in an EAN13 barcode
        self.BARCODE_LENGTH = 12

        # The barcode's size and not the output image's size
        self.BARCODE_SIZE = 720, 360
        self.BARCODE_FONT_SIZE = 46

        # This declares how many columns this type of barcode has
        self.BARCODE_COLUMN_NUMBER = 95

        # Do some error checking
        if isinstance(self.code, str):
            if len(self.code) < self.BARCODE_LENGTH:
                error = f"{self.__class__.__name__} should be at least {self.BARCODE_LENGTH} digits long, not {len(self.code)}."
                raise IncorrectFormat(error)
            else:
                self.code = self._clean_code()

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
            weighted_odd = digits[1::2]
            weighted_even = digits[::2]

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

        binary_string += EANCoding.RIGHT_GUARD

        return binary_string


class EAN8(Barcode):
    def __init__(self, barcode: Union[str, int]):
        super().__init__(barcode)

        # The number of digits in an EAN8 barcode
        self.BARCODE_LENGTH = 7

        # The barcode's size and not the output image's size
        self.BARCODE_SIZE = 480, 380
        self.BARCODE_FONT_SIZE = 46

        # This declares how many columns this type of barcode has
        self.BARCODE_COLUMN_NUMBER = 53

        # Do some error checking
        if isinstance(self.code, str):
            if len(self.code) < self.BARCODE_LENGTH:
                error = f"{self.__class__.__name__} should be at least {self.BARCODE_LENGTH} digits long, not {len(self.code)}."
                raise IncorrectFormat(error)
            else:
                self.code = self._clean_code()
    
    @classmethod
    def calculate_checksum(cls, barcode: Union[str, "EAN8"]) -> int:
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

        if len(barcode) >= 7:
            barcode = barcode[:7]

            # Here there is no check digit so it's calculated
            digits = list(map(int, list(barcode)))

            # Get even and odd indeces of the digits
            odd_weight, even_weight = (1, 3)
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

        # Convert the barcode to a binary string with the CodeNumbers class
        # Add the left guard
        binary_string = EANCoding.LEFT_GUARD

        # Add the 6 digits after the left guard
        for i in range(0, 4):
            digit = int(self.code[i])
            binary_string += EANCoding.CODES["L"][digit]

        # Add the center guard
        binary_string += EANCoding.CENTER_GUARD

        # Add the 6 digits after the center guard
        for i in range(4, 8):
            digit = int(self.code[i])
            binary_string += EANCoding.CODES["R"][digit]

        binary_string += EANCoding.RIGHT_GUARD

        return binary_string
