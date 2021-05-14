import os
import sys
from pathlib import Path

root = Path(__file__).parent.parent
root = os.path.join(root)
sys.path.append(root)

from pybarcodes.ean import EAN13

def test_ean13():
    code = "012345678905"
    barcode = EAN13(code)
    barcode2 = EAN13(code)

    assert barcode.size == "mid"
    assert barcode == code
    assert barcode == barcode2 + "1"
    
