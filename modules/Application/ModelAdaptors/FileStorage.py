import json
import os
from modules.Domain.Models.ConfigurationInterface import Configuration


class FileStorage(Configuration):

    data = None

    def __init__(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        with open(ROOT_DIR+'/../../../fileStorage/credentials.json') as f:
            self.data = json.loads(f.read())

    def get_paypal_client_id(self) -> str:
        if self.data.get('client_id') is None:
            raise Exception('The client ID is not set')
        return self.data['client_id']

    def get_paypal_client_secret(self) -> str:
        if self.data.get('client_secret') is None:
            raise Exception('The client secret is not set')
        return self.data['client_secret']
