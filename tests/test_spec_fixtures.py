import pytest

from pybarcodes import CODE39, EAN8, EAN13, EAN14


# GS1 check digit algorithm reference:
# https://www.gs1.org/services/how-calculate-check-digit-manually
@pytest.mark.parametrize(
    ("barcode_type", "payload", "expected_code"),
    [
        (EAN8, "9638507", "96385074"),
        (EAN13, "629104150021", "6291041500213"),
        (EAN14, "1061414145678", "10614141456786"),
    ],
)
def test_gs1_check_digit_fixtures(barcode_type, payload, expected_code):
    assert barcode_type.normalize(payload) == expected_code
    assert barcode_type(payload).code == expected_code


def test_ean8_binary_pattern_fixture():
    barcode = EAN8("9638507")

    assert barcode.get_binary_string == (
        "1010001011010111101111010110111010101001110111001010001001011100101"
    )


def test_ean13_binary_pattern_fixture():
    barcode = EAN13("629104150021")

    assert barcode.get_binary_string == (
        "101"
        "0010011"
        "0010111"
        "0110011"
        "0100111"
        "0100011"
        "0011001"
        "01010"
        "1001110"
        "1110010"
        "1110010"
        "1101100"
        "1100110"
        "1000010"
        "101"
    )


# Code 39 MOD43 reference:
# https://docshield.tungstenautomation.com/ControlSuite/en_US/1.5.0-uh5vow9jo0/help/QCP/Dita/ACSCChecksum.html
def test_code39_mod43_check_digit_fixture():
    assert CODE39.normalize("+1110001111") == "+11100011115"
    assert CODE39("+1110001111").calculate_checksum("+1110001111") == 5
