from pybarcodes.ean import EAN13

code = "012345678905"
barcode = EAN13(code)
barcode.show()
