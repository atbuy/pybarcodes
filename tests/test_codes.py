from pybarcodes import CODE39
from tests.conftest import BaseBarcodeTest


class TestCODE39(BaseBarcodeTest):
    barcode_class = CODE39
    code = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.-$+/$ "
    checksum = "/"
    invalid_code = "^"
    has_structure = False
    guard_positions = (None, 6), (-6, None)
    expected_guards = ("0 0110", "0 0110")

    def test_checksum(self):
        assert self.barcode_class.calculate_checksum(self.code) == 40
