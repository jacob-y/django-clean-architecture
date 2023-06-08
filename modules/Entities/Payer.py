class Payer:

    first_name: str
    last_name: str
    email: str
    address1: str
    address2: str | None
    city: str
    country_code: str
    post_code: str
    lang: str

    def __init__(self, first_name: str, last_name: str, email: str, address1: str, address2: str | None, city: str,
                 country_code: str, post_code: str, lang: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.country_code = country_code
        self.post_code = post_code
        self.lang = lang
