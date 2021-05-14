import os
import sys
from pathlib import Path

root = Path(__file__).parent.parent
root = os.path.join(root)
sys.path.append(root)

from pybarcodes.ean import EAN13
from pybarcodes.exceptions import IncorrectFormat


def test_ean13():
    code = "400638133393"
    barcode = EAN13(code)
    barcode2 = EAN13(code)

    assert barcode.size == "max"
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

    try:
        code = "1"
        barcode = EAN13(code)
    except IncorrectFormat:
        pass

    # Check if guards in correct positions
    binary_string = barcode.get_binary_string
    left_guard = binary_string[:3]
    right_guard = binary_string[-3:]
    center_guard = binary_string[45:50]
    assert left_guard == "101"
    assert right_guard == "101"
    assert center_guard == "01010"

test_ean13()