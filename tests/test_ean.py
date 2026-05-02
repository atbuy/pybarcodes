import pytest

from pybarcodes import EAN8, EAN13, EAN14, JAN
from pybarcodes.exceptions import IncorrectFormat


def test_ean13():
    code = "400638133393"
    barcode = EAN13(code)
    barcode2 = EAN13(code)

    # Check if the required attributes exist
    assert barcode.BARCODE_LENGTH
    assert barcode.BARCODE_SIZE
    assert barcode.BARCODE_FONT_SIZE
    assert barcode.BARCODE_COLUMN_NUMBER
    assert barcode.BARCODE_PADDING
    assert barcode.FIRST_SECTION
    assert barcode.SECOND_SECTION
    assert barcode.WEIGHTS
    assert barcode.HAS_STRUCTURE

    assert barcode == code + "1"
    assert barcode == barcode2

    # Check if the checksum digit is calculated correctly
    # The check digit should be `1`
    code = "400638133393"
    checkdigit = EAN13.calculate_checksum(code)
    assert checkdigit == 1

    code = "40063813339398736412039867123409586345"
    barcode = EAN13(code)
    # The check digit is calculated when instansiating
    assert barcode == "4006381333931"

    with pytest.raises(IncorrectFormat):
        EAN13("1")

    # Check if guards are in the correct positions
    binary_string = barcode.get_binary_string
    left_guard = binary_string[:3]
    right_guard = binary_string[-3:]
    center_guard = binary_string[45:50]
    assert left_guard == "101"
    assert right_guard == "101"
    assert center_guard == "01010"


def test_ean13_checksum_edge_cases():
    assert EAN13.calculate_checksum("000000000001") == 7
    assert EAN13("000000000001") == "0000000000017"


def test_ean8():
    code = "0123456"
    barcode = EAN8(code)

    # Check if the required attributes exist
    assert barcode.BARCODE_LENGTH
    assert barcode.BARCODE_SIZE
    assert barcode.BARCODE_FONT_SIZE
    assert barcode.BARCODE_COLUMN_NUMBER
    assert barcode.BARCODE_PADDING
    assert barcode.FIRST_SECTION
    assert barcode.SECOND_SECTION
    assert barcode.WEIGHTS
    assert not barcode.HAS_STRUCTURE

    # Check digit for this barcode should be `5`
    assert EAN8.calculate_checksum(code) == 5

    code = "012345628743652398476528347652987"
    barcode = EAN8(code)

    # The check digit is calculated when instansiating
    assert barcode == "01234565"

    with pytest.raises(IncorrectFormat):
        EAN8("1")

    # Check if guards in correct positions
    binary_string = barcode.get_binary_string
    left_guard = binary_string[:3]
    right_guard = binary_string[-3:]
    center_guard = binary_string[33:38]
    assert left_guard == "101"
    assert right_guard == "101"
    assert center_guard == "01010"


def test_ean8_checksum_edge_cases():
    assert EAN8.calculate_checksum("0000001") == 7
    assert EAN8("0000001") == "00000017"


def test_ean14():
    code = "4070071967072013242346"
    barcode = EAN14(code)

    # Check if the required attributes exist
    assert barcode.BARCODE_LENGTH
    assert barcode.BARCODE_SIZE
    assert barcode.BARCODE_FONT_SIZE
    assert barcode.BARCODE_COLUMN_NUMBER
    assert barcode.BARCODE_PADDING
    assert barcode.FIRST_SECTION
    assert barcode.SECOND_SECTION
    assert barcode.WEIGHTS
    assert barcode.HAS_STRUCTURE

    # Check digit for this barcode should be `0`
    assert EAN14.calculate_checksum(code) == 0

    # The check digit is calculated when instansiating
    assert barcode == "40700719670720"

    with pytest.raises(IncorrectFormat):
        EAN14("1")

    # Check if guards in correct positions
    binary_string = barcode.get_binary_string
    left_guard = binary_string[:3]
    right_guard = binary_string[-3:]
    center_guard = binary_string[45:50]
    assert left_guard == "101"
    assert right_guard == "101"
    assert center_guard == "01010"


def test_ean14_checksum_edge_cases():
    assert EAN14.calculate_checksum("0000000000001") == 7
    assert EAN14("0000000000001") == "00000000000017"


def test_jan():
    code = "450638133393"
    barcode = JAN(code)
    barcode2 = JAN(code)

    # Check if the required attributes exist
    assert barcode.BARCODE_LENGTH
    assert barcode.BARCODE_SIZE
    assert barcode.BARCODE_FONT_SIZE
    assert barcode.BARCODE_COLUMN_NUMBER
    assert barcode.BARCODE_PADDING
    assert barcode.FIRST_SECTION
    assert barcode.SECOND_SECTION
    assert barcode.WEIGHTS
    assert barcode.HAS_STRUCTURE

    assert barcode == code + "6"
    assert barcode == barcode2

    # Check if the checksum digit is calculated correctly
    # The check digit should be `1`
    code = "450638133393"
    checkdigit = JAN.calculate_checksum(code)
    assert checkdigit == 6

    code = "45063813339398736412039867123409586345"
    barcode = JAN(code)
    # The check digit is calculated when instansiating
    assert barcode == "4506381333936"
    with pytest.raises(IncorrectFormat):
        JAN("1")

    # Check if guards are in the correct positions
    binary_string = barcode.get_binary_string
    left_guard = binary_string[:3]
    right_guard = binary_string[-3:]
    center_guard = binary_string[45:50]
    assert left_guard == "101"
    assert right_guard == "101"
    assert center_guard == "01010"


@pytest.mark.parametrize("barcode_type", [EAN8, EAN13, EAN14])
def test_ean_calculate_checksum_rejects_non_digits(barcode_type):
    with pytest.raises(IncorrectFormat):
        barcode_type.calculate_checksum("x" * barcode_type.BARCODE_LENGTH)
