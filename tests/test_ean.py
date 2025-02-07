from pybarcodes import EAN8, EAN13, EAN14, JAN
from tests.conftest import EANBarcodeTest


class TestEAN8(EANBarcodeTest):
    barcode_class = EAN8
    code = "0123456"
    checksum = 5
    invalid_code = "1"
    has_structure = False
    guard_positions = (None, 3), (33, 38), (-3, None)
    expected_guards = ("101", "01010", "101")


class TestEAN13(EANBarcodeTest):
    barcode_class = EAN13
    code = "400638133393"
    checksum = 1
    invalid_code = "1"
    has_structure = True
    guard_positions = (None, 3), (45, 50), (-3, None)
    expected_guards = ("101", "01010", "101")


class TestEAN14(EANBarcodeTest):
    barcode_class = EAN14
    code = "4070071967072"
    checksum = 0
    invalid_code = "1"
    has_structure = True
    guard_positions = (None, 3), (45, 50), (-3, None)
    expected_guards = ("101", "01010", "101")


class TestJAN(EANBarcodeTest):
    barcode_class = JAN
    code = "450638133393"
    checksum = 6
    invalid_code = "1"
    has_structure = True
    guard_positions = (None, 3), (45, 50), (-3, None)
    expected_guards = ("101", "01010", "101")
