from unittest import TestCase

import pytest

from pybarcodes import EAN8, EAN13, EAN14, JAN
from pybarcodes.ean import Size, Weights
from pybarcodes.exceptions import IncorrectFormat


class EAN13Test(TestCase):
    def setUp(self) -> None:
        self.code = "400638133393"
        self.long_code = "40063813339398736412039867123409586345"

        self.barcode1 = EAN13(self.code)
        self.barcode2 = EAN13(self.code)

        return super().setUp()

    def test_attributes(self):
        self.assertEqual(self.barcode1.BARCODE_LENGTH, 12)
        self.assertEqual(self.barcode1.BARCODE_SIZE, (720, 360))
        self.assertEqual(self.barcode1.BARCODE_FONT_SIZE, 46)
        self.assertEqual(self.barcode1.BARCODE_COLUMN_NUMBER, 110)
        self.assertEqual(self.barcode1.BARCODE_PADDING, Size(100, 200))
        self.assertEqual(self.barcode1.FIRST_SECTION, (0, 6))
        self.assertEqual(self.barcode1.SECOND_SECTION, (6, 12))
        self.assertEqual(self.barcode1.WEIGHTS, Weights(3, 1))
        self.assertTrue(self.barcode1.HAS_STRUCTURE)

    def test_value(self):
        expected_code = self.code + "1"

        self.assertEqual(self.barcode1, expected_code)
        self.assertEqual(self.barcode1, self.barcode2)

    def test_checksum(self):
        checkdigit = EAN13.calculate_checksum(self.code)
        barcode = EAN13(self.long_code)

        self.assertEqual(checkdigit, 1)
        self.assertEqual(barcode, "4006381333931")

    def test_incorrect_format(self):
        code = "1"

        with pytest.raises(IncorrectFormat):
            EAN13(code)

    def test_guards(self):
        binary_string = self.barcode1.get_binary_string

        expected_left_right_guard = "101"
        expected_center_guard = "01010"

        left_guard = binary_string[:3]
        right_guard = binary_string[-3:]
        center_guard = binary_string[45:50]

        self.assertEqual(left_guard, expected_left_right_guard)
        self.assertEqual(right_guard, expected_left_right_guard)
        self.assertEqual(center_guard, expected_center_guard)


class EAN8Test(TestCase):
    def setUp(self) -> None:
        self.code = "0123456"
        self.long_code = "012345628743652398476528347652987"

        self.barcode = EAN8(self.code)

        return super().setUp()

    def test_attributes(self):
        self.assertEqual(self.barcode.BARCODE_LENGTH, 7)
        self.assertEqual(self.barcode.BARCODE_SIZE, (480, 240))
        self.assertEqual(self.barcode.BARCODE_FONT_SIZE, 40)
        self.assertEqual(self.barcode.BARCODE_COLUMN_NUMBER, 75)
        self.assertEqual(self.barcode.BARCODE_PADDING, Size(0, 200))
        self.assertEqual(self.barcode.FIRST_SECTION, (0, 4))
        self.assertEqual(self.barcode.SECOND_SECTION, (4, 8))
        self.assertEqual(self.barcode.WEIGHTS, Weights(1, 3))
        self.assertEqual(self.barcode.HAS_STRUCTURE, False)

    def test_checksum(self):
        long_barcode = EAN8(self.long_code)
        check_digit = EAN8.calculate_checksum(self.code)

        self.assertEqual(long_barcode, "01234565")
        self.assertEqual(check_digit, 5)

    def test_incorrect_format(self):
        code = "1"

        with pytest.raises(IncorrectFormat):
            EAN8(code)

    def test_guards(self):
        binary_string = self.barcode.get_binary_string

        expected_left_right_guard = "101"
        expected_center_guard = "01010"

        left_guard = binary_string[:3]
        right_guard = binary_string[-3:]
        center_guard = binary_string[33:38]

        self.assertEqual(left_guard, expected_left_right_guard)
        self.assertEqual(right_guard, expected_left_right_guard)
        self.assertEqual(center_guard, expected_center_guard)


class EAN14Test(TestCase):
    def setUp(self) -> None:
        self.code = "4070071967072013242346"
        self.barcode = EAN14(self.code)

        return super().setUp()

    def test_attributes(self):
        self.assertEqual(self.barcode.BARCODE_LENGTH, 13)
        self.assertEqual(self.barcode.BARCODE_SIZE, (720, 360))
        self.assertEqual(self.barcode.BARCODE_FONT_SIZE, 46)
        self.assertEqual(self.barcode.BARCODE_COLUMN_NUMBER, 108)
        self.assertEqual(self.barcode.BARCODE_PADDING, Size(100, 200))
        self.assertEqual(self.barcode.FIRST_SECTION, (0, 6))
        self.assertEqual(self.barcode.SECOND_SECTION, (6, 13))
        self.assertEqual(self.barcode.WEIGHTS, Weights(1, 3))
        self.assertTrue(self.barcode.HAS_STRUCTURE)

    def test_checksum(self):
        barcode = "40700719670720"
        check_digit = EAN14.calculate_checksum(self.code)

        self.assertEqual(check_digit, 0)
        self.assertEqual(self.barcode, barcode)

    def test_incorrect_format(self):
        code = "1"

        with pytest.raises(IncorrectFormat):
            EAN14(code)

    def test_guards(self):
        binary_string = self.barcode.get_binary_string

        expected_left_right_guard = "101"
        expected_center_guard = "01010"

        left_guard = binary_string[:3]
        right_guard = binary_string[-3:]
        center_guard = binary_string[45:50]

        self.assertEqual(left_guard, expected_left_right_guard)
        self.assertEqual(right_guard, expected_left_right_guard)
        self.assertEqual(center_guard, expected_center_guard)


class JANTest(TestCase):
    def setUp(self) -> None:
        self.code = "450638133393"
        self.long_code = "45063813339398736412039867123409586345"

        self.barcode1 = JAN(self.code)
        self.barcode2 = JAN(self.code)

        return super().setUp()

    def test_attributes(self):
        self.assertEqual(self.barcode1.BARCODE_LENGTH, 12)
        self.assertEqual(self.barcode1.BARCODE_SIZE, (720, 360))
        self.assertEqual(self.barcode1.BARCODE_FONT_SIZE, 46)
        self.assertEqual(self.barcode1.BARCODE_COLUMN_NUMBER, 110)
        self.assertEqual(self.barcode1.BARCODE_PADDING, Size(100, 200))
        self.assertEqual(self.barcode1.FIRST_SECTION, (0, 6))
        self.assertEqual(self.barcode1.SECOND_SECTION, (6, 12))
        self.assertEqual(self.barcode1.WEIGHTS, Weights(3, 1))
        self.assertTrue(self.barcode1.HAS_STRUCTURE)

    def test_value(self):
        expected_code = self.code + "6"

        self.assertEqual(self.barcode1, expected_code)
        self.assertEqual(self.barcode1, self.barcode2)

    def test_checksum(self):
        check_digit = JAN.calculate_checksum(self.code)
        expected_barcode = "4506381333936"
        long_barcode = JAN(self.long_code)

        self.assertEqual(check_digit, 6)
        self.assertEqual(self.barcode1, expected_barcode)
        self.assertEqual(long_barcode, expected_barcode)

    def test_incorrect_format(self):
        code = "1"

        with pytest.raises(IncorrectFormat):
            JAN(code)

    def test_guards(self):
        binary_string = self.barcode1.get_binary_string

        expected_left_right_guard = "101"
        expected_center_guard = "01010"

        left_guard = binary_string[:3]
        right_guard = binary_string[-3:]
        center_guard = binary_string[45:50]

        self.assertEqual(left_guard, expected_left_right_guard)
        self.assertEqual(right_guard, expected_left_right_guard)
        self.assertEqual(center_guard, expected_center_guard)
