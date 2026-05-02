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

    def render(
        self,
        size: tuple = None,
        module_width: int = None,
        bar_height: int = None,
        quiet_zone: int = None,
        font_size: int = None,
        draw_text: bool = True,
    ) -> Image.Image:
        """Create a PIL Image object for the barcode."""

        img = self._get_barcode_image(
            module_width=module_width,
            bar_height=bar_height,
            quiet_zone=quiet_zone,
            font_size=font_size,
            draw_text=draw_text,
        )
        if size is not None:
            resampling = getattr(Image, "Resampling", Image)
            img = img.resize(size, resampling.NEAREST)
        return img

    def save(
        self,
        path: str,
        size: tuple = None,
        module_width: int = None,
        bar_height: int = None,
        quiet_zone: int = None,
        font_size: int = None,
        draw_text: bool = True,
        **save_kwargs,
    ) -> Image.Image:
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

        img = self.render(
            size=size,
            module_width=module_width,
            bar_height=bar_height,
            quiet_zone=quiet_zone,
            font_size=font_size,
            draw_text=draw_text,
        )
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
        self,
        format: str = "PNG",
        size: tuple = None,
        module_width: int = None,
        bar_height: int = None,
        quiet_zone: int = None,
        font_size: int = None,
        draw_text: bool = True,
        **save_kwargs,
    ) -> BytesIO:
        """Return the rendered barcode image in a BytesIO object."""

        obj = BytesIO()
        self.render(
            size=size,
            module_width=module_width,
            bar_height=bar_height,
            quiet_zone=quiet_zone,
            font_size=font_size,
            draw_text=draw_text,
        ).save(obj, format=format, **save_kwargs)
        obj.seek(0)
        return obj

    def to_image_bytes(
        self,
        format: str = "PNG",
        size: tuple = None,
        module_width: int = None,
        bar_height: int = None,
        quiet_zone: int = None,
        font_size: int = None,
        draw_text: bool = True,
        **save_kwargs,
    ) -> bytes:
        """Return the rendered barcode image as bytes."""

        return self.to_image_bytesio(
            format=format,
            size=size,
            module_width=module_width,
            bar_height=bar_height,
            quiet_zone=quiet_zone,
            font_size=font_size,
            draw_text=draw_text,
            **save_kwargs,
        ).getvalue()

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

    @staticmethod
    def _positive_int(value: int, name: str) -> int:
        value = int(value)
        if value <= 0:
            raise ValueError(f"{name} must be greater than 0.")
        return value

    def _get_render_options(
        self,
        module_width: int = None,
        bar_height: int = None,
        quiet_zone: int = None,
        font_size: int = None,
        draw_text: bool = True,
    ):
        padding = self.BARCODE_PADDING
        selected_size, default_font_size = self.BARCODE_SIZE, self.BARCODE_FONT_SIZE

        module_width = (
            self._get_column_size()
            if module_width is None
            else self._positive_int(module_width, "module_width")
        )
        bar_height = (
            selected_size[1]
            if bar_height is None
            else self._positive_int(bar_height, "bar_height")
        )
        quiet_zone = (
            padding.width // 2
            if quiet_zone is None
            else self._positive_int(quiet_zone, "quiet_zone")
        )
        font_size = (
            default_font_size
            if font_size is None
            else self._positive_int(font_size, "font_size")
        )
        text_padding = padding.height if draw_text else 0

        return module_width, bar_height, quiet_zone, font_size, text_padding

    def _get_default_font(self, font_size: int) -> ImageFont.ImageFont:
        try:
            return ImageFont.load_default(size=font_size)
        except TypeError:
            return ImageFont.load_default()

    def _get_barcode_image(
        self,
        module_width: int = None,
        bar_height: int = None,
        quiet_zone: int = None,
        font_size: int = None,
        draw_text: bool = True,
    ) -> Image.Image:
        """Creates a PIL Image from the binary string of the barcode

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

        binary_string = self.get_binary_string

        # Create the image for the barcode
        img = Image.new(
            "RGB",
            (module_width * len(binary_string), bar_height),
            (255, 255, 255),
        )

        index = 0
        for digit in binary_string:
            color = (0, 0, 0) if digit == "1" else (255, 255, 255)
            column = Image.new("RGB", (module_width, img.height), color)
            img.paste(column, (index, 0))
            index += module_width

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
