from modules.Domain.Plugins.AbstractResponse import AbstractResponse


class FakeResponse(AbstractResponse):
    """
    Mock a payment gateway response interpretation.
    """

    def error_message(self) -> str | None:
        return self._data.get('error_message')

    def error_code(self) -> str | None:
        return self._data.get('error_code')

    def is_successful(self) -> bool:
        return self._data.get('is_successful') or False

    def is_pending(self) -> bool:
        return self._data.get('is_pending') or False

    def is_refunded(self) -> bool:
        return self._data.get('is_refunded') or False

    def redirect_url(self) -> str | None:
        return self._data.get('redirect_url')

    def payment_id(self) -> str | None:
        return self._data.get('id')

    def capture_id(self) -> str | None:
        return self._data.get('capture_id')

    def gateway_status(self) -> str | None:
        return self._data.get('status')
