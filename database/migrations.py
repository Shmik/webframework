import logging

from database.db import get_connection
from psycopg2 import sql
from apps.model_register import ModelRegister
import apps.migrations as app_migrations
import os

model_register = ModelRegister()
MIGRATIONS_PATH = os.path.dirname(app_migrations.__file__)

class MakeMigrations():
    def __init__(self):
        migrations_table_exists = self.check_table_exists('migration')
        if migrations_table_exists:
            print('Migrations table exists')
        else:
            self.create_migrations_table()

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

    def check_table_exists(self, table_name):
        with get_connection() as conn:
            with conn.cursor() as curs:
            # Check that the migrations table exists.
                curs.execute("""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.tables
                        WHERE table_schema = 'public'
                        AND table_name = %s
                    );
                """, (table_name,))
                table_exists = curs.fetchone()[0]
        return table_exists

    def get_column_data(self, table_name):
        with get_connection() as conn:
            with conn.cursor() as curs:
                curs.execute("""
                        SELECT column_name, udt_name, column_default, character_maximum_length
                        FROM information_schema.columns
                        WHERE table_schema = 'public'
                        AND table_name = %s;
                """, (table_name,))
                column_data = curs.fetchall()
        return column_data

    def make_all_apps(self):
        for model in model_register.get_apps():
            self.make_for_model(model)

    def make_for_model(self, model):
        table_name = model.get_table()
        if not self.check_table_exists(table_name):
            query = self.build_create_table_query_for_model(model)
            self.create_migration_file(query)

    def build_create_table_query_for_model(self, model):
        columns = []
        for field_name, field_class in model.get_fields().items():
            query = sql.SQL("{} ").format(sql.Identifier(field_name)) + field_class.create_sql
            if getattr(field_class, 'max_length', None):
                query += sql.SQL("({})").format(sql.Literal(field_class.max_length))
            columns.append(query)

        create_statement = sql.SQL("CREATE TABLE {} ({})" ).format(
            sql.Identifier(model.get_table()),
            sql.SQL(', ').join(columns)
        )
        with get_connection() as conn:
            return create_statement.as_string(conn)

    def get_next_migration_number(self):
        """
        Migrations will always start with a 4 digit number which increases.
        """
        migration_file_list = os.listdir(MIGRATIONS_PATH)
        migration_file_list.remove('__init__.py')
        if len(migration_file_list) > 0:
            migration_file_list.sort()
            return int(migration_file_list[-1][0:4]) + 1
        else:
            return 0

    def create_migration_file(self, query):
        next_number = self.get_next_migration_number()
        filename = f'{next_number:04}_migration.py'
        filepath = f'{MIGRATIONS_PATH}/{filename}'
        with open(filepath, 'x') as f:
            f.write(query)

class Migrate():
    def __init__(self):
        self.execute_pending_migrations()

    def get_migrations_file_list(self):
        migration_file_list = os.listdir(MIGRATIONS_PATH)
        migration_file_list.remove('__init__.py')
        migration_file_list.sort()
        return migration_file_list

    def get_completed_migrations_list(self):
        with get_connection() as conn:
            with conn.cursor() as curs:
                curs.execute("""
                    SELECT name
                    FROM migration
                    ORDER BY name
                    """
                )
                column_data = curs.fetchall()
        return [result[0] for result in column_data]

    def execute_pending_migrations(self):
        migration_files = self.get_migrations_file_list()
        completed_migrations = self.get_completed_migrations_list()
        pending = [filename for filename in migration_files if filename not in completed_migrations]
        for filename in pending:
            self.execute(filename)

    def execute(self, filename):
        filepath = f'{MIGRATIONS_PATH}/{filename}'
        print (f'Executing migration {filename}')
        with open(filepath, 'r') as file:
            query = file.read()
        with get_connection() as conn:
            with conn.cursor() as curs:
                # execute migration
                curs.execute(query)
                # and record completed
                print (f'inserting {filename}')
                curs.execute("INSERT INTO migration (name) VALUES (%s)", (filename,))
