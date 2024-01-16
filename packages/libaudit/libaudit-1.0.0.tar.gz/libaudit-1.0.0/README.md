# Библиотека логирования изменений данных в БД
## Подключение

requirements:

    libaudit>=1.0.0,<2.0

settings:

    INSTALLED_APPS = [
        ...
        'libaudit',
        ...
    ]

    MIDDLEWARE = [
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'libaudit.middleware.AuditLogMiddleware',
        ...
    ]

    REST_FRAMEWORK = {
        ...
	    'DEFAULT_AUTHENTICATION_CLASSES': (
	        'libaudit.oidc.JSONWebTokenAuthentication',
	    )
	    ...
	}

## Запуск тестов
    $ tox
