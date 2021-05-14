from typing import Union


class Barcode:
    def __init__(self, barcode: Union[str, int], size: str = "mid"):
        self.code = str(barcode)
        self.size = size or "mid"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: code={self.code}>"

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    barcode = Barcode(123454)
    print(barcode)
