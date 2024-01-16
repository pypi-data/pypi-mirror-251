import pathlib

from django.db.migrations.operations.base import Operation


class InstallAuditLog(Operation):

    """Настраивает основную БД."""

    reversible = True

    def state_forwards(self, app_label, state):
        pass

    @staticmethod
    def _read_sql(filename):
        """Чтение sql из файла."""
        sql_file_path = pathlib.Path(__file__).parent / 'sql' / filename
        with sql_file_path.open(mode='r', encoding='utf-8') as sql_file:
            sql = sql_file.read().replace('%', '%%')
        return sql

    def database_forwards(
        self, app_label, schema_editor, from_state, to_state
    ):
        if schema_editor.connection.alias != 'default':
            return

        schema_editor.execute('CREATE EXTENSION IF NOT EXISTS hstore;')

        sql = self._read_sql('apply_triggers.sql')
        schema_editor.execute(sql)

    def database_backwards(
        self, app_label, schema_editor, from_state, to_state
    ):
        if schema_editor.connection.alias != ['default']:
            return

        sql = self._read_sql('remove_triggers.sql')
        schema_editor.execute(sql)
