import pytest

from pybarcodes import CODE39
from pybarcodes.exceptions import IncorrectFormat


def test_code39():
    code = "0123456789abcdefghijklmnopqrstuvwxyz.-$+/$ "
    barcode = CODE39(code)

    assert barcode.BARCODE_FONT_SIZE
    assert barcode.BARCODE_PADDING
    assert barcode.BARCODE_SIZE
    assert barcode.BARCODE_COLUMN_NUMBER

    assert barcode == code.upper() + "/"

    assert barcode.calculate_checksum(code) == 40
    assert barcode.calculate_checksum() == 40
    assert CODE39.normalize("abc123") == CODE39("abc123").code
    assert CODE39.validate("abc123") is None

    with pytest.raises(IncorrectFormat):
        CODE39("^")

    with pytest.raises(IncorrectFormat):
        barcode.calculate_checksum("^")
    with pytest.raises(IncorrectFormat):
        CODE39.validate("^")

    binary_string = barcode.get_binary_string
    start_char = binary_string[:6]
    stop_char = binary_string[-6:]
    assert start_char == "0 0110"
    assert stop_char == "0 0110"
