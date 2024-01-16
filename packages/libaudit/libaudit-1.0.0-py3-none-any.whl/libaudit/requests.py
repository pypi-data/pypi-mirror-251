from . import constants


def get_audit_log_context(request=None):
    """Возвращает контекст для логирования изменений.

    Если передан запрос, то контекст извлекается из запроса.
    """
    context = {constants.USER_ID_KEY: None}

    if request is None:
        return context

    context.update({constants.USER_ID_KEY: str(request.user.pk)})

    return context
