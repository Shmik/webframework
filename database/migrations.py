import logging

from database.db import get_connection
from apps.model_register import ModelRegister

model_register = ModelRegister()

class MakeMigrations():
    def __init__(self):
        migrations_table_exists = self.migrations_table_exists()
        if migrations_table_exists:
            print('Migrations table exists')
        else:
            self.create_migrations_table()

    def migrations_table_exists(self):
        with get_connection() as conn:
            with conn.cursor() as curs:
            # Check that the migrations table exists.
                curs.execute("""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.tables
                        WHERE table_schema = 'public'
                        AND table_name = 'migration'
                    );
                """)
                migrations_table_exists = curs.fetchone()[0]
        return migrations_table_exists

    def create_migrations_table(self):
        print('Creating migrations table')
        with get_connection() as conn:
            with conn.cursor() as curs:
                curs.execute("""
                    CREATE TABLE migration (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100)
                    );
                """)

    def check_models_for_changes(self):
        for model in model_register.apps:


class Migrate():
    pass