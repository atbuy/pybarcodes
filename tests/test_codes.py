import os
import sys
from pathlib import Path

root = Path(__file__).parent.parent
root = os.path.join(root)
sys.path.append(root)

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

    try:
        code = "^"
        barcode = CODE39(code)
    except IncorrectFormat:
        pass

    binary_string = barcode.get_binary_string
    start_char = binary_string[:6]
    stop_char = binary_string[-6:]
    assert start_char == "0 0110"
    assert stop_char == "0 0110"
