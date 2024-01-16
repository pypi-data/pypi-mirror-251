import os


# Папка с sql файлами
SQL_FILES_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'sql',
))


USER_ID_KEY = 'libaudit.user_id'
