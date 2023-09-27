from ..AbstractPayPalResponse import AbstractPayPalResponse


class CreateOrderResponse(AbstractPayPalResponse):

    def id(self):
        return self._data.get('id')

    def redirect_url(self):
        if self._data.get('links'):
            for l in self._data.get('links'):
                if l.get('rel') == 'approve':
                    return l.get('href')
        return None

    def is_successful(self):
        return self._data.get('status') == 'COMPLETED'

    def is_refunded(self) -> bool:
        return False

    def is_pending(self):
        return self._data.get('status') in ['CREATED', 'SAVED', 'APPROVED', 'PAYER_ACTION_REQUIRED']
