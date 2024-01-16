from django.db import migrations

from ..migration import InstallAuditLog


class Migration(migrations.Migration):

    """Инициализация системы журналирования изменений."""

    dependencies = []

    operations = [
        InstallAuditLog(),
    ]
