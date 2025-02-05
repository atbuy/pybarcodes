import pytest
from PIL import Image

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

    # Check image
    image = barcode.image

    assert isinstance(image, Image.Image)
    assert image.size == tuple(
        map(sum, zip(barcode.BARCODE_SIZE, barcode.BARCODE_PADDING))
    )
    assert image.mode == "RGB"

    with pytest.raises(IncorrectFormat):
        code = "^"
        barcode = CODE39(code)

    binary_string = barcode.get_binary_string
    start_char = binary_string[:6]
    stop_char = binary_string[-6:]
    assert start_char == "0 0110"
    assert stop_char == "0 0110"
