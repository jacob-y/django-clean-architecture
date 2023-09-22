from ..AbstractPayPalResponse import AbstractPayPalResponse


class GetAccessTokenResponse(AbstractPayPalResponse):

    def is_successful(self) -> bool:
        return False

    def is_refunded(self) -> bool:
        return False

    def is_pending(self) -> bool:
        return False

    def redirect_url(self) -> str | None:
        return None

    def get_access_token(self):
        return self._data.get('access_token')
