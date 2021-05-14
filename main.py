from pybarcodes.ean import EAN13

code = "012345678905"
barcode = EAN13(code)
barcode.save("C:/Users/filip/Desktop/output.png")
