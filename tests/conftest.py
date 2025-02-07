import abc

import pytest
from PIL import Image

from pybarcodes.barcode import Barcode
from pybarcodes.exceptions import IncorrectFormat

GuardPosition = tuple[int, int]
GuardPositions = tuple[GuardPosition, GuardPosition, GuardPosition]


class BaseBarcodeTest(abc.ABC):
    @property
    @abc.abstractmethod
    def barcode_class(self) -> [Barcode]:
        """
        The barcode class to test
        """
        pass

    @property
    @abc.abstractmethod
    def code(self) -> str:
        """
        The code to test
        """
        pass

    @property
    @abc.abstractmethod
    def checksum(self) -> int:
        """
        The checksum of the code
        """
        pass

    @property
    @abc.abstractmethod
    def invalid_code(self) -> str:
        """
        An invalid code to test
        """
        pass

    @property
    @abc.abstractmethod
    def has_structure(self) -> bool:
        """
        If the barcode has a structure
        """
        pass

    @property
    @abc.abstractmethod
    def guard_positions(self) -> GuardPositions:
        """
        The positions of the guards in the barcode
        """
        pass

    @property
    @abc.abstractmethod
    def expected_guards(self) -> tuple[str, str, str]:
        """
        The expected guards in the barcode
        """
        pass

    @property
    def barcode(self):
        """
        The barcode instance
        """
        return self.barcode_class(self.code)

    def test_attributes(self):
        """
        Test if the required attributes exist
        """
        assert self.barcode.BARCODE_SIZE
        assert self.barcode.BARCODE_FONT_SIZE
        assert self.barcode.BARCODE_PADDING

    def test_equality(self):
        """
        Test if the barcode is equal to the code and checksum
        """
        barcode2 = self.barcode_class(self.code)
        assert self.barcode == f"{self.code}{self.checksum}"
        assert self.barcode == barcode2

    def test_image(self):
        """
        Test if the barcode is an image
        """
        image = self.barcode.image

        assert isinstance(image, Image.Image)
        assert image.mode == "RGB"
        assert image.size == tuple(
            map(sum, zip(self.barcode.BARCODE_SIZE, self.barcode.BARCODE_PADDING))
        )

    def test_save(self, fs):
        """
        Test if the barcode is saved to a file
        """
        file = fs.create_file("barcode.png")
        self.barcode.save(file.path, size=(100, 100))
        assert file.byte_contents[:8] == b"\x89PNG\r\n\x1a\n"

    def test_show(self, mocker):
        """
        Test if the barcode is shown
        """
        mock_show = mocker.patch("PIL.Image.Image.show")
        self.barcode.show()
        mock_show.assert_called_once()

    def test_to_bytesio(self):
        """
        Test if the barcode is written to a BytesIO object
        """
        obj = self.barcode.to_bytesio()
        obj_bytes = obj.read()
        assert self.code.upper().encode("ascii") in obj_bytes

    def test_checksum(self):
        """
        Test if the checksum digit is calculated correctly
        """
        assert self.barcode_class.calculate_checksum(self.code) == self.checksum

    def test_invalid_code(self):
        """
        Test if the barcode raises an error for an invalid code
        """
        with pytest.raises(IncorrectFormat):
            self.barcode_class(self.invalid_code)

    def test_guards(self):
        """
        Test if the guards are in the correct positions
        """
        binary_string = self.barcode.get_binary_string
        for i, guard in enumerate(self.expected_guards):
            start, end = self.guard_positions[i]
            assert binary_string[start:end] == guard


class EANBarcodeTest(BaseBarcodeTest, abc.ABC):
    def test_attributes(self):
        """
        Test if the required attributes exist
        """
        super().test_attributes()
        assert self.barcode.BARCODE_LENGTH
        assert self.barcode.BARCODE_COLUMN_NUMBER
        assert self.barcode.FIRST_SECTION
        assert self.barcode.SECOND_SECTION
        assert self.barcode.WEIGHTS
        assert self.barcode.HAS_STRUCTURE == self.has_structure
