from modules.Application.PluginAdaptors.PayPal.PayPalResponseMixin import PayPalResponseMixin


class ShowOrderDetailsResponse(PayPalResponseMixin):

    def _get_capture_status(self) -> bool:
        if len(self._data.get('purchase_units')) > 0:
            return self._data.get('purchase_units')[0].get('payments').get('captures')[0].get('status')
        return False

    def capture_id(self) -> bool:
        if (
                self._data.get('purchase_units')
                and len(self._data.get('purchase_units')) > 0
                and self._data.get('purchase_units')[0].get('payments')
                and self._data.get('purchase_units')[0].get('payments').get('captures')
                and len(self._data.get('purchase_units')[0].get('payments').get('captures')) > 0
        ):
            return self._data.get('purchase_units')[0].get('payments').get('captures')[0].get('id')
        return False

    def is_successful(self) -> bool:
        return self.gateway_status() == self.ORDER_COMPLETED and self._get_capture_status() == self.CAPTURE_COMPLETED

    def is_refunded(self) -> bool:
        return self.gateway_status() == self.ORDER_COMPLETED and self._get_capture_status() == self.CAPTURE_REFUNDED

    def is_pending(self) -> bool:
        return self._data.get('status') in [
            self.ORDER_CREATED, self.ORDER_SAVED, self.ORDER_APPROVED, self.ORDER_PAYER_ACTION_REQUIRED] \
            or self._get_capture_status() in [self.CAPTURE_PENDING, self.CAPTURE_PARTIALLY_REFUNDED]

    def is_failed(self) -> bool:
        return self._data.get('status') == self.ORDER_VOIDED or self._get_capture_status() in [
            self.CAPTURE_DECLINED, self.CAPTURE_FAILED]
