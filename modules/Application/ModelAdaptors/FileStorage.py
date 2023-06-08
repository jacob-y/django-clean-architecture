import json

from modules.Domain.Models.Configuration import Configuration


class FileStorage(Configuration):

    data = None

    def __init__(self):
        with open('fileStorage/credentials.json') as f:
            self.data = json.loads(f.read())

    def get_paypal_client_id(self) -> str:
        if self.data.get('client_id') is None:
            raise Exception('The client ID is not set')
        return self.data['client_id']

    def get_paypal_client_secret(self) -> str:
        if self.data.get('client_secret') is None:
            raise Exception('The client secret is not set')
        return self.data['client_secret']
