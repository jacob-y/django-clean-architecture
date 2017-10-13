import re
from typing import Optional


class Card:
    AMEX = 'AmericanExpress'
    BANCONTACT = 'Bancontact'
    CB = 'CB'
    DINERS_CLUB = 'DinersClub'
    DISCOVER = 'Discover'
    JCB = 'JCB'
    MASTERCARD = 'MasterCard'
    MAESTRO = 'Maestro'
    SOLO = 'Solo'
    VISA = 'Visa'
    VISA_ELECTRON = 'VisaElectron'

    BRANDS = [AMEX, BANCONTACT, CB, DINERS_CLUB, DISCOVER, JCB, MASTERCARD, MAESTRO, SOLO, VISA, VISA_ELECTRON]

    token: str  # the real card number is not stored, we use a pre-saved token
    last_4_numbers: str  # we are allowed by PCI DSS to store the last 4 numbers (and the 6 first if we wanted to)
    expiry_month: str
    expiry_year: str
    brand: str

    def __init__(self, token: str, last_4_numbers: str, expiry_month: str, expiry_year: str, brand: str):
        self.token = token
        self.last_4_numbers = last_4_numbers
        self.expiry_month = expiry_month
        self.expiry_year = expiry_year
        self.brand = brand

    def get_expiry_date(self) -> Optional[str]:
        if self.expiry_month and self.expiry_year:
            return f'{self.expiry_month.zfill(2)}/20{self.expiry_year}'
        return None

    def is_valid(self) -> bool:
        return (
                self.token and
                self.brand and self.brand in self.BRANDS and
                self.last_4_numbers and re.match(r'^\d{4}$', self.last_4_numbers) and
                self.expiry_month and re.match(r'^\d{1,2}$', self.expiry_month) is not None and
                self.expiry_year and re.match(r'^\d{2}$', self.expiry_year) is not None
        )
