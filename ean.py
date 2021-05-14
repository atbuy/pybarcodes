import os
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from collections import namedtuple

from barcode import Barcode
from exceptions import IncorrectFormat, IncorrectSizeSelection


class CodeNumbers:
    left_0 = "0001101"
    left_1 = "0011001"
    left_2 = "0010011"
    left_3 = "0111101"
    left_4 = "0100011"
    left_5 = "0110001"
    left_6 = "0101111"
    left_7 = "0111011"
    left_8 = "0110111"
    left_9 = "0001011"

    right_0 = "1110010"
    right_1 = "1100110"
    right_2 = "1101100"
    right_3 = "1001110"
    right_4 = "1011100"
    right_5 = "1001110"
    right_6 = "1010000"
    right_7 = "1000100"
    right_8 = "1001000"
    right_9 = "1110100"

    lefts = [left_0, left_1, left_2, left_3, left_4, left_5, left_6, left_7, left_8, left_9]
    rights = [right_0, right_1, right_2, right_3, right_4, right_5, right_6, right_7, right_8, right_9]

    left_guard = "101"
    center_guard = "01010"
    right_guard = "101"


class EAN13(Barcode):
    def __init__(self, barcode, size: str = "mid"):
        super().__init__(barcode, size)

        # The digit length of the EAN13 barcode
        self.barcode_length = 12

        # This is the minimum size of the barcode allowed,
        # rounded up to the nearest integer.
        # The maximum allowed size of the barcode, is 200% it's size.
        # To avoid scanning errors, the max size is defined by 180% the size of the minimum value
        self.BARCODE_SIZE_MIN_PX = 375, 200
        self.BARCODE_SIZE_MID_PX = tuple(map(lambda x: int(x * 1.4), self.BARCODE_SIZE_MIN_PX))
        self.BARCODE_SIZE_MAX_PX = tuple(map(lambda x: int(x * 1.8), self.BARCODE_SIZE_MIN_PX))

        self.BARCODE_FONT_SIZE_MIN = 22
        self.BARCODE_FONT_SIZE_MID = 26
        self.BARCODE_FONT_SIZE_MAX = 30
        self.size_options = {
            "min": (self.BARCODE_SIZE_MIN_PX, self.BARCODE_FONT_SIZE_MIN),
            "mid": (self.BARCODE_SIZE_MID_PX, self.BARCODE_FONT_SIZE_MID),
            "max": (self.BARCODE_SIZE_MAX_PX, self.BARCODE_FONT_SIZE_MAX)}

        # Do some error checking
        if isinstance(self.code, str):
            if len(self.code) != self.barcode_length:
                error = f"{self.__class__.__name__} should be {self.barcode_length} digits long, not {len(self.code)}."
                raise IncorrectFormat(error)

            if not self.code.isdigit():
                raise IncorrectFormat("Barcode can't contain non-digit characters.")
    
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

        Arguments
        ---------
        path: str
            The path of the file
        """
        with open(path, "w") as file:
            file.write(self.code)

    def write_image(self, path: str, size: str = "mid") -> Image.Image:
        """
        Create a PIL Image object and save it to the path given.
        It also return that image object to the caller.
        If no size is passed, then the method looks for the instansiated size.
        If there is no instansiated size, then an error is raised.

        Arguments
        ---------
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
        binary_string = self.get_binary_string()

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
        font_path = os.path.join(os.getcwd(), "fonts", "arial.ttf")

        draw = ImageDraw.Draw(base)
        font = ImageFont.truetype(font_path, font_size)

        text_width, _ = draw.textsize(self.code, font)
        x = base_center.x - text_width // 2
        y = base.height - (base.height - img.height) // 2
        draw.text((x, y), self.code, (0, 0, 0), font=font)
        base.save(path)
    
    def get_binary_string(self) -> str:
        """
        """

        # Convert the barcode to a binary string with the CodeNumbers class
        # Add the left guard
        binary_string = CodeNumbers.left_guard

        # Add the 6 digits after the left guard
        for i in range(0, 6):
            binary_string += CodeNumbers.lefts[int(self.code[i])]
        
        # Add the center guard
        binary_string += CodeNumbers.center_guard

        # Add the 6 digits after the center guard
        for i in range(6, len(self.code)):
            binary_string += CodeNumbers.rights[int(self.code[i])]
        
        binary_string += CodeNumbers.right_guard
        
        return binary_string

    
    def _get_column_size(self, size: str) -> int:
        """
        Finds and returns what the width of each column should be

        Arguments
        ---------
        size: str
            One of the 3 size options
        
        Returns
        -------
        Returns an integer with the width of the bar
        """
        size, _ = self.size_options[size]

        return size[0] // 95


    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: code={self.code}>"

    def __repr__(self):
        return self.__str__()



if __name__ == "__main__":
    code = "051000012517"
    barcode = EAN13(code)
    print(barcode)

    img_path = "C:/Users/filip/Desktop/image.png"
    barcode.write_image(img_path, "max")

    
