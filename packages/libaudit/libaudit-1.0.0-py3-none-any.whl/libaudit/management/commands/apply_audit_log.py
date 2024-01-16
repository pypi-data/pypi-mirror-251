from django.core.management.base import BaseCommand
from django.db import ProgrammingError
from django.db import connections

from ...constants import SQL_FILES_DIR


class Command(BaseCommand):

    help = (
        'Настройка БД для логирования изменений объектов.'
    )

    @staticmethod
    def _read_sql(filename):
        """Чтение sql из файла."""
        sql_file_path = SQL_FILES_DIR.joinpath(filename)
        with sql_file_path.open(mode='r', encoding='utf-8') as sql_file:
            sql = sql_file.read()
        return sql

    def handle(self, *args, **options):
        sql = self._read_sql('apply_triggers.sql')
        with connections['default'].cursor() as cursor:
            try:
                cursor.execute(sql)
            except ProgrammingError as exc:
                raise exc
            else:
                self.stdout.write(
                    'Настройка логирования изменений прошла успешно.'
                )
