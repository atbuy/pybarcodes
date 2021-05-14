class IncorrectFormat(Exception):
    """Raised when the user didn't pass the correct format for the barcode they are using"""
    pass


class IncorrectSizeSelection(Exception):
    """Raised when the user didn't pass a correct barcode size option"""
    pass
