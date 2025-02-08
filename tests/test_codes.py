from unittest import TestCase

import pytest

from pybarcodes import CODE39
from pybarcodes.codes import Size
from pybarcodes.exceptions import IncorrectFormat


class Code39Test(TestCase):
    def setUp(self) -> None:
        self.code = "0123456789abcdefghijklmnopqrstuvwxyz.-$+/$ "
        self.barcode = CODE39(self.code)

        return super().setUp()

    def test_attributes(self):
        self.assertEqual(self.barcode.BARCODE_FONT_SIZE, 30)
        self.assertEqual(self.barcode.BARCODE_PADDING, Size(50, 100))
        self.assertEqual(self.barcode.BARCODE_SIZE, (1656, 240))
        self.assertEqual(self.barcode.BARCODE_COLUMN_NUMBER, 848)

    def test_value(self):
        expected_value = self.code.upper() + "/"

        self.assertEqual(self.barcode, expected_value)

    def test_checksum(self):
        checksum_code = self.barcode.calculate_checksum(self.code)
        checksum = self.barcode.calculate_checksum()

        self.assertEqual(checksum_code, 40)
        self.assertEqual(checksum, 40)

    def test_incorrect_format(self):
        code = "^"

        with pytest.raises(IncorrectFormat):
            CODE39(code)

    def test_start_stop(self):
        binary_string = self.barcode.get_binary_string

        expected_start_stop = "0 0110"
        start_char = binary_string[:6]
        stop_char = binary_string[-6:]

        self.assertEqual(start_char, expected_start_stop)
        self.assertEqual(stop_char, expected_start_stop)
