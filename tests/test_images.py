from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image

from pybarcodes import CODE39, EAN13


def assert_barcode_image(image: Image.Image) -> None:
    assert image.mode == "RGB"
    assert image.width > 0
    assert image.height > 0
    assert image.getbbox() == (0, 0, image.width, image.height)


def test_ean_image_generation_and_save(tmp_path: Path):
    barcode = EAN13("400638133393")

    image = barcode.render()
    assert_barcode_image(image)
    assert_barcode_image(barcode.image)

    output_path = tmp_path / "ean13.png"
    saved_image = barcode.save(
        str(output_path), module_width=3, bar_height=80, quiet_zone=20, draw_text=False
    )

    assert output_path.exists()
    assert saved_image.size == (len(barcode.get_binary_string) * 3 + 40, 80)
    with Image.open(output_path) as image_file:
        assert image_file.size == saved_image.size
        assert image_file.mode == "RGB"


def test_code39_image_generation():
    barcode = CODE39("ABC123")

    image = barcode.image

    assert_barcode_image(image)


def test_renderer_controls():
    barcode = EAN13("400638133393")

    image = barcode.render(
        module_width=4,
        bar_height=120,
        quiet_zone=12,
        font_size=16,
        draw_text=False,
    )

    assert image.size == (len(barcode.get_binary_string) * 4 + 24, 120)


def test_renderer_rejects_invalid_controls():
    barcode = EAN13("400638133393")

    with pytest.raises(ValueError):
        barcode.render(module_width=0)
    with pytest.raises(ValueError):
        barcode.render(bar_height=0)
    with pytest.raises(ValueError):
        barcode.render(quiet_zone=0)
    with pytest.raises(ValueError):
        barcode.render(font_size=0)


def test_text_outputs(tmp_path: Path):
    barcode = EAN13("400638133393")

    output_path = tmp_path / "ean13.txt"
    barcode.write(str(output_path))

    assert output_path.read_text() == "4006381333931"
    assert barcode.to_text_bytes() == b"4006381333931"
    assert isinstance(barcode.to_text_bytesio(), BytesIO)
    assert barcode.to_text_bytesio().read() == b"4006381333931"
    assert isinstance(barcode.to_bytesio(), BytesIO)
    assert barcode.to_bytesio().read() == b"4006381333931"
    assert str(barcode) == "<EAN13(code=4006381333931)>"
    assert repr(barcode) == "<EAN13(code=4006381333931)>"


def test_image_bytes_outputs():
    barcode = EAN13("400638133393")

    image_bytes = barcode.to_image_bytes(
        module_width=3, bar_height=80, quiet_zone=20, draw_text=False
    )
    assert image_bytes.startswith(b"\x89PNG")

    image_buffer = barcode.to_image_bytesio(
        module_width=3, bar_height=80, quiet_zone=20, draw_text=False
    )
    assert isinstance(image_buffer, BytesIO)
    with Image.open(image_buffer) as image_file:
        assert image_file.size == (len(barcode.get_binary_string) * 3 + 40, 80)
        assert image_file.mode == "RGB"
