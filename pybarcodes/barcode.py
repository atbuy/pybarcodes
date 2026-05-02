from collections import namedtuple
from io import BytesIO
from typing import Union

from PIL import Image, ImageDraw, ImageFont


class Barcode:
    """A base class for all barcode types"""

    def __init__(self, barcode: Union[str, int]):
        self.code = self.normalize(barcode)

    @classmethod
    def validate(cls, barcode: Union[str, int]) -> None:
        """Validate barcode input."""

    @classmethod
    def normalize(cls, barcode: Union[str, int]) -> str:
        """Return the normalized barcode value used by the instance."""

        cls.validate(barcode)
        return str(barcode)

    @property
    def image(self) -> Image.Image:
        """Retrieves and returns the PIL.Image object with the barcode

        Returns
        -------
        PIl.Image.Image:
            The barcode image
        """

        return self.render()

    def render(self, size: tuple = None) -> Image.Image:
        """Create a PIL Image object for the barcode."""

        img = self._get_barcode_image()
        if size is not None:
            img = img.resize(size)
        return img

    def save(self, path: str, size: tuple = None, **save_kwargs) -> Image.Image:
        """Create a PIL Image object and save it to the path given.

        It also returns that image object to the caller.

        Parameters
        ----------
        path: str
            The path to save the image to

        Returns
        -------
        Returns a PIL Image object to the caller
        """

        img = self.render(size=size)
        img.save(path, **save_kwargs)
        return img

    def show(self) -> None:
        """Shows the barcode image"""

        self.render().show()

    def to_text_bytes(self, encoding: str = "ascii") -> bytes:
        """Return the normalized barcode text as bytes."""

        return self.code.encode(encoding)

    def to_text_bytesio(self, encoding: str = "ascii") -> BytesIO:
        """
        Write the barcode to a BytesIO object

        Returns
        -------
        Returns the BytesIO object created
        """

        obj = BytesIO(self.to_text_bytes(encoding=encoding))
        obj.seek(0)
        return obj

    def to_bytesio(self, encoding: str = "ascii") -> BytesIO:
        """Return the normalized barcode text in a BytesIO object."""

        return self.to_text_bytesio(encoding=encoding)

    def to_image_bytesio(
        self, format: str = "PNG", size: tuple = None, **save_kwargs
    ) -> BytesIO:
        """Return the rendered barcode image in a BytesIO object."""

        obj = BytesIO()
        self.render(size=size).save(obj, format=format, **save_kwargs)
        obj.seek(0)
        return obj

    def to_image_bytes(
        self, format: str = "PNG", size: tuple = None, **save_kwargs
    ) -> bytes:
        """Return the rendered barcode image as bytes."""

        return self.to_image_bytesio(format=format, size=size, **save_kwargs).getvalue()

    def write(self, path: str, encoding: str = "ascii") -> None:
        """
        Tries to save the barcode to a text file

        Parameters
        ----------
        path: str
            The path of the file
        """
        with open(path, "w", encoding=encoding) as file:
            file.write(self.code)

    def _get_barcode_image(self) -> Image.Image:
        """Creates a PIL Image from the binary string of the barcode

        Returns
        -------
        A PIL Image with the barcode is returned to the caller.
        """

        # Get the padding around the barcode
        padding = self.BARCODE_PADDING

        # Get the final image's width and height
        selected_size, font_size = self.BARCODE_SIZE, self.BARCODE_FONT_SIZE

        # This is for the white space around the barcode
        padded_size = (
            selected_size[0] + padding.width,
            selected_size[1] + padding.height,
        )

        # Get each column's width and height
        column_size = self._get_column_size()

        # Create a white base image to write columns
        base = Image.new("RGB", padded_size, (255, 255, 255))

        # Create the image for the barcode
        img = Image.new(
            "RGB",
            (column_size * self.BARCODE_COLUMN_NUMBER, selected_size[1]),
            (255, 255, 255),
        )

        # Get the binary string representation of the barcode digits
        binary_string = self.get_binary_string

        index = 0
        for digit in binary_string:
            color = (0, 0, 0) if digit == "1" else (255, 255, 255)
            column = Image.new("RGB", (column_size, img.height), color)
            img.paste(column, (index, 0))
            index += column_size

        # Crop redundant whitespace after barcode
        img = img.crop((0, 0, index, img.height))

        # Paste the barcode on the center of the padded base
        Point = namedtuple("Point", "x y")
        base_center = Point(base.width // 2, base.height // 2)
        img_center = Point(img.width // 2, img.height // 2)

        base.paste(img, (base_center.x - img_center.x, base_center.y - img_center.y))

        draw = ImageDraw.Draw(base)
        try:
            font = ImageFont.load_default(size=font_size)
        except TypeError:
            font = ImageFont.load_default()

        text_width = draw.textlength(self.code, font)
        x = base_center.x - text_width // 2
        y = base.height - (base.height - img.height) // 2

        draw.text((x, y), self.code, (0, 0, 0), font=font)
        return base

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.code == other.code
        elif isinstance(other, str):
            return self.code == other

        return False

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}(code={self.code})>"

    def __repr__(self):
        return self.__str__()
