from django.apps import AppConfig
from psindb.util.db import DB


class PsindbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'psindb'
    db_args = {
        "host": "psindb-db",
        "user": "daniel",
        "passwd": "password",
        "database": "PSDInteractome_v1_01",
    }

    def ready(self):
        print("READY")
        DB.db_args = self.db_args
        DB.retries = 5
        DB.connect()
