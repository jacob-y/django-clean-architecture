from abc import ABC
from modules.Domain.Plugins.AbstractResponse import AbstractResponse


class AbstractPayPalResponse(AbstractResponse, ABC):

    def error_message(self) -> str | None:
        return self._data.get('details')[0].get('description') \
            or self._data.get('error', {}).get('message') \
            or self._data.get('message')

    def error_code(self) -> str | None:
        return self._data.get('details') and self._data.get('details')[0].get('issue') \
            or self._data.get('details') \
            or self._data.get('error', {}).get('name') \
            or self._data.get('name')

    def id(self) -> str:
        return self._data.get('id')

    def status(self) -> str | None:
        return self._data.get('status') or None
