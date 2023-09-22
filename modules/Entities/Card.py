import re
from typing import Optional


class Card:
    AMEX = 'American Express'
    BANCONTACT = 'Bancontact'
    CB = 'CB'
    DINERS_CLUB = 'Diners club'
    DISCOVER = 'Discover'
    JCB = 'JCB'
    MASTERCARD = 'MasterCard'
    MAESTRO = 'Maestro'
    SOLO = 'Solo'
    VISA = 'Visa'
    VISA_ELECTRON = 'VisaElectron'

    BRANDS = [AMEX, BANCONTACT, CB, DINERS_CLUB, DISCOVER, JCB, MASTERCARD, MAESTRO, SOLO, VISA, VISA_ELECTRON]

    BRAND_ALIASES = {
        AMEX: ['amex', 'americanexpress', 'american express'],
        BANCONTACT: ['bancontact', 'bcmc', 'mistercash'],
        CB: ['cb', 'cartebleue'],
        DINERS_CLUB: ['diners club', 'dinersclub'],
        DISCOVER: ['discover'],
        JCB: ['jcb'],
        MASTERCARD: ['mastercard'],
        MAESTRO: ['maestro'],
        SOLO: ['solo'],
        VISA: ['visa'],
        VISA_ELECTRON: ['visa electron', 'visaelectron']
    }

    number: str
    expiry_month: str
    expiry_year: str
    cvv: str
    brand: str

    def __init__(self, number: str, expiry_month: str, expiry_year: str, cvv: str, brand: str):
        self.number = number
        self.expiry_month = expiry_month
        self.expiry_year = expiry_year
        self.cvv = cvv
        self.brand = brand

    def get_brand(self) -> Optional[str]:
        for brand, aliases in self.BRAND_ALIASES:
            if str.lower(self.brand) in aliases:
                return brand
        return None

    def get_expiry_date(self) -> Optional[str]:
        if self.expiry_month and self.expiry_year:
            return '20' + self.expiry_year + self.expiry_month.zfill(2)
        return None

    def mask(self) -> Optional[str]:
        if self.number:
            return self.number[-4:].rjust(len(self.number), "*")
        return None

    def is_valid(self) -> bool:
        return (self.number and re.match(r'^\d{13,19}$', self.number)
                and self.expiry_month and re.match(r'^\d{1,2}$', self.expiry_month) is not None
                and self.expiry_year and re.match(r'^\d{2}$', self.expiry_year) is not None
                and self.cvv and re.match(r'^\d{3,4}$', self.cvv) is not None
        )
