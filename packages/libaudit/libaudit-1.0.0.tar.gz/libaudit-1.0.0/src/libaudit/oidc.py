from typing import Tuple
from typing import Union

from oidc_auth.authentication import JSONWebTokenAuthentication as BaseAuth

from . import constants
from . import db
from . import requests


class JSONWebTokenAuthentication(BaseAuth):

    """Авторизация с установкой параметров в БД в случае успеха."""

    def authenticate(self, request):
        auth: Union[Tuple, None] = super().authenticate(request)

        if auth is None:
            return auth

        # Пользователь определен через OIDC_RESOLVE_USER_FUNCTION
        self._set_db_params(request, *auth)

        return auth

    def _set_db_params(self, request, user, userinfo):
        # Начальный контекст.
        # Не передаем request[rest_framework.request.Request], т.к. это приводит к
        # рекурсии через св-во request.user
        context = requests.get_audit_log_context()

        context.update({constants.USER_ID_KEY: str(user.pk)})

        db.set_db_params(**context)
