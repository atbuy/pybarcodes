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
from collections import namedtuple

from pybarcodes.barcode import Barcode
from pybarcodes.exceptions import IncorrectFormat
from pybarcodes.codings import ean as EANCoding


Size = namedtuple("Size", "width height")
Weights = namedtuple("Weights", "ODD EVEN")


class EAN(Barcode):
    """Base class for EAN type barcodes

    Shouldn't be used directly and it's subclasses are preferred
    """

    def __init__(self, barcode: Union[str, int]):
        super().__init__(barcode)

        # Do some error checking
        if isinstance(self.code, str):
            if len(self.code) < self.BARCODE_LENGTH:
                error = f"{self.__class__.__name__} should be at least {self.BARCODE_LENGTH} digits long, not {len(self.code)}."
                raise IncorrectFormat(error)
            else:
                self.code = self._clean_code()  

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
        
        # Find the structure of the first section
        # This is determined by the first digit
        if self.HAS_STRUCTURE:
            # We find the structure of the first section using the first digit
            structure = EANCoding.STRUCTURE[self.code[0]]

            # The first digit is removed
            code = self.code[1:]
        else:
            # If there is no structure then all digits should be in `L` coding
            structure = "L" * (self.FIRST_SECTION[1])

            # In EAN8 barcodes the first digit is accounted for
            code = self.code

        

        # Convert the barcode to a binary string with the CodeNumbers class
        # Add the left guard
        binary_string = EANCoding.LEFT_GUARD

        # Add the 6 digits after the left guard
        for i in range(*self.FIRST_SECTION):
            digit = int(code[i])
            coding = structure[i]
            binary_string += EANCoding.CODES[coding][digit]

        # Add the center guard
        binary_string += EANCoding.CENTER_GUARD

        # Add the 6 digits after the center guard
        for i in range(*self.SECOND_SECTION):
            digit = int(code[i])
            binary_string += EANCoding.CODES["R"][digit]

        binary_string += EANCoding.RIGHT_GUARD

        return binary_string

    @classmethod
    def calculate_checksum(cls, barcode: Union[str, "EAN13", "EAN8", "EAN14"]) -> int:
        """
        Calculate the checksum from the barcode given

        This is a class method because it can only be used just to calculate any barcode
        of the same type, not only the instance's checksum

        Parameters
        ----------
        barcode: Union[str, "EAN13"]
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

        if isinstance(barcode, cls):
            barcode = barcode.code
        elif isinstance(barcode, str):
            pass
        else:
            raise TypeError(f"Can't accept type {type(barcode)}")

        if len(barcode) >= cls.BARCODE_LENGTH:
            barcode = barcode[:cls.BARCODE_LENGTH]
            # Here there is no check digit so it's calculated
            digits = list(map(int, list(barcode)))

            # Get even and odd indeces of the digits
            weighted_odd = digits[1::2]
            weighted_even = digits[::2]

            # Calculate the checksum
            checksum = sum(weighted_odd) * cls.WEIGHTS.ODD + sum(weighted_even) * cls.WEIGHTS.EVEN
            if checksum % 10 == 0:
                return 0

            # Find the closest multiple of 10, that is equal to
            # or higher than the checksum and return the difference
            closest10 = ((checksum // 10) * 10) + 10
            return closest10 % checksum

        raise IncorrectFormat(f"Barcode should be at least {cls.BARCODE_LENGTH} digits long.")


class EAN14(EAN):
    """The class to represent an EAN14 barcode

    Attributes
    ----------
    BARCODE_LENGTH: int
        The number of digits in an EAN14 barcode
    BARCODE_SIZE: Tuple[int, int]
        The barcode's size and not the output image's size
    BARCODE_FONT_SIZE: int
        The size of the font under the barcode  
    BARCODE_COLUMN_NUMBER: int
        How many binary columns the barcode consists of
    BARCODE_PADDING: Tuple[int, int]
        The padding around the actual barcode
    """

    BARCODE_LENGTH = 13
    BARCODE_SIZE = 720, 360
    BARCODE_FONT_SIZE = 46
    BARCODE_COLUMN_NUMBER = 108
    BARCODE_PADDING = Size(100, 200)
    FIRST_SECTION = (0, 6)
    SECOND_SECTION = (6, BARCODE_LENGTH)
    WEIGHTS = Weights(1, 3)
    HAS_STRUCTURE = True

    def __init__(self, barcode: Union[str, int]):
        super().__init__(barcode)


class EAN13(EAN):
    """The class to represent an EAN13 barcode

    Attributes
    ----------
    BARCODE_LENGTH: int
        The number of digits in an EAN13 barcode
    BARCODE_SIZE: Tuple[int, int]
        The barcode's size and not the output image's size
    BARCODE_FONT_SIZE: int
        The size of the font under the barcode  
    BARCODE_COLUMN_NUMBER: int
        How many binary columns the barcode consists of
    BARCODE_PADDING: Tuple[int, int]
        The padding around the actual barcode
    """

    BARCODE_LENGTH = 12
    BARCODE_SIZE = 720, 360
    BARCODE_FONT_SIZE = 46
    BARCODE_COLUMN_NUMBER = 110
    BARCODE_PADDING = Size(100, 200)
    FIRST_SECTION = (0, 6)
    SECOND_SECTION = (6, BARCODE_LENGTH)
    WEIGHTS = Weights(3, 1)
    HAS_STRUCTURE = True

    def __init__(self, barcode: Union[str, int]):
        super().__init__(barcode)


class EAN8(EAN):
    """The class to represent an EAN8 barcode

    Attributes
    ----------
    BARCODE_LENGTH: int
        The number of digits of the barcode
    BARCODE_SIZE: Tuple[int, int]
        The barcode's size and not the output image's size
    BARCODE_FONT_SIZE: int
        The size of the font under the barcode  
    BARCODE_COLUMN_NUMBER: int
        How many binary columns the barcode consists of
    BARCODE_PADDING: Tuple[int, int]
        The padding around the actual barcode
    """

    BARCODE_LENGTH = 7
    BARCODE_SIZE = 480, 240
    BARCODE_FONT_SIZE = 40
    BARCODE_COLUMN_NUMBER = 75
    BARCODE_PADDING = Size(0, 200)
    FIRST_SECTION = (0, 4)
    SECOND_SECTION = (4, BARCODE_LENGTH+1)
    WEIGHTS = Weights(1, 3)
    HAS_STRUCTURE = False

    def __init__(self, barcode: Union[str, int]):
        super().__init__(barcode)


class JAN(EAN13, EAN):
    """The class to represent an EAN13 barcode

    Attributes
    ----------
    BARCODE_LENGTH: int
        The number of digits in an EAN13 barcode
    BARCODE_SIZE: Tuple[int, int]
        The barcode's size and not the output image's size
    BARCODE_FONT_SIZE: int
        The size of the font under the barcode  
    BARCODE_COLUMN_NUMBER: int
        How many binary columns the barcode consists of
    BARCODE_PADDING: Tuple[int, int]
        The padding around the actual barcode
    """

    def __init__(self, barcode: Union[str, int]):
        super().__init__(barcode)

        if not (self.code[:2] in ("45", "49")):
            raise IncorrectFormat("JAN type barcodes need to start with country code 45 or 49")
