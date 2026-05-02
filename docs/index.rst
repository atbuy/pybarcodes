.. pybarcodes documentation master file, created by
   sphinx-quickstart on Fri May 14 10:03:22 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pybarcodes
==========

pybarcodes generates EAN-13, EAN-8, EAN-14, JAN, and CODE39 barcodes as Pillow
images, image bytes, or normalized text.

Quick start
-----------

Create a barcode from the payload without the check digit. The instance stores
the normalized value, including the calculated check digit.

.. code-block:: python

   from pybarcodes import EAN13

   barcode = EAN13("590123412345")

   assert barcode.code == "5901234123457"
   barcode.save("ean13.png")

Validation and normalization
----------------------------

Use the class methods when you want to validate user input before creating an
instance, or when you only need the normalized text.

.. code-block:: python

   from pybarcodes import CODE39, EAN13

   EAN13.validate("590123412345")
   ean13_value = EAN13.normalize("590123412345")

   code39_value = CODE39.normalize("HELLO-123")

Rendering controls
------------------

Prefer barcode-aware rendering options over resizing the final bitmap. They keep
bar widths, quiet zones, and text placement predictable.

.. code-block:: python

   from pybarcodes import EAN13

   barcode = EAN13("590123412345")
   image = barcode.render(
       module_width=3,
       bar_height=180,
       quiet_zone=24,
       font_size=28,
   )
   image.save("ean13-large.png")

   barcode.save("ean13-bars-only.png", draw_text=False)

Bytes output
------------

Use text bytes when you need the normalized barcode value, or image bytes when
you need an encoded image for storage, APIs, or web responses.

.. code-block:: python

   from pybarcodes import EAN13

   barcode = EAN13("590123412345")

   text_bytes = barcode.to_text_bytes()
   png_bytes = barcode.to_image_bytes(format="PNG")

Type hints
----------

pybarcodes includes inline type annotations and ships a ``py.typed`` marker so
type checkers can use the public API types from installed packages.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
