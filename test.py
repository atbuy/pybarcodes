from pybarcodes import EAN14


code = "4070071967072013242346"
barcode = EAN14(code)
barcode.save("test2.png")