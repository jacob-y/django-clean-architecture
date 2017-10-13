from modules.Domain.Plugins.AbstractResponse import AbstractResponse


class GetAccessTokenResponse(AbstractResponse):

    def get_access_token(self):
        return self._data.get('access_token')
