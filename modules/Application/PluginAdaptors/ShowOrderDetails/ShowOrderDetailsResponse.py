from ..AbstractPayPalResponse import AbstractPayPalResponse


class ShowOrderDetailsResponse(AbstractPayPalResponse):

    def _get_capture_status(self) -> bool:
        if len(self._data.get('purchase_units')) > 0:
            return self._data.get('purchase_units')[0].get('payments').get('captures')[0].get('status')
        return False

    def is_successful(self) -> bool:
        return self.status() == 'COMPLETED' and self._get_capture_status() == 'COMPLETED'

    def is_pending(self) -> bool:
        return self._data.get('status') in ['CREATED', 'SAVED', 'APPROVED', 'ACTION_REQUIRED'] \
            or self._get_capture_status() != 'COMPLETED'

    def redirect_url(self) -> str | None:
        return None
