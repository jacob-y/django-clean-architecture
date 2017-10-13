from modules.Application.PluginAdaptors.PayPal.PayPalResponseMixin import PayPalResponseMixin


class CreateOrderResponse(PayPalResponseMixin):

    def payment_id(self):
        return self._data.get('id')

    def redirect_url(self):
        if self._data.get('links'):
            for l in self._data.get('links'):
                if l.get('rel') == 'approve':
                    return l.get('href')
        return None

    def is_successful(self):
        return self._data.get('status') == self.ORDER_COMPLETED

    def is_pending(self):
        return self._data.get('status') in [
            self.ORDER_CREATED, self.ORDER_SAVED, self.ORDER_APPROVED, self.ORDER_PAYER_ACTION_REQUIRED,
            self.ORDER_PARTIALLY_COMPLETED]

    def is_failed(self) -> bool:
        return self._data.get('status') == self.ORDER_VOIDED
