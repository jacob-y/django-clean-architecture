class Iban:
    iban: str
    bic: str

    def __init__(self, iban: str, bic: str):
        self.iban = iban
        self.bic = bic

    def mask(self):
        return self.iban[-8:].rjust(len(self.iban), "*")
