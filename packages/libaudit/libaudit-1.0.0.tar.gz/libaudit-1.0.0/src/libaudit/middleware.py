from django.utils.deprecation import MiddlewareMixin

from . import db
from . import requests


class AuditLogMiddleware(MiddlewareMixin):

    """Извлекает из запроса информацию о пользователе и передает в БД.

    Информация о пользователе затем используется для логирования изменеий.
    """

    def process_request(self, request):
        db.set_db_params(**requests.get_audit_log_context(request))

    def process_response(self, request, response):
        db.set_db_params(**requests.get_audit_log_context(request))
        return response
