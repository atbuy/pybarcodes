from io import BytesIO
from pathlib import Path

from PIL import Image

from pybarcodes import CODE39, EAN13


def assert_barcode_image(image: Image.Image) -> None:
    assert image.mode == "RGB"
    assert image.width > 0
    assert image.height > 0
    assert image.getbbox() == (0, 0, image.width, image.height)


def test_ean_image_generation_and_save(tmp_path: Path):
    barcode = EAN13("400638133393")

    image = barcode.image
    assert_barcode_image(image)

    output_path = tmp_path / "ean13.png"
    saved_image = barcode.save(str(output_path), size=(120, 80))

    assert output_path.exists()
    assert saved_image.size == (120, 80)
    with Image.open(output_path) as image_file:
        assert image_file.size == (120, 80)
        assert image_file.mode == "RGB"


def test_code39_image_generation():
    barcode = CODE39("ABC123")

    image = barcode.image

    assert_barcode_image(image)


def test_text_outputs(tmp_path: Path):
    barcode = EAN13("400638133393")

    output_path = tmp_path / "ean13.txt"
    barcode.write(str(output_path))

    assert output_path.read_text() == "4006381333931"
    assert isinstance(barcode.to_bytesio(), BytesIO)
    assert barcode.to_bytesio().read() == b"4006381333931"
    assert str(barcode) == "<EAN13(code=4006381333931)>"
    assert repr(barcode) == "<EAN13(code=4006381333931)>"
