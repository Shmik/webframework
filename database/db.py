from config.settings import DATABASE_SETTINGS
import psycopg2


class Connection():
    def __enter__(self):
        self.conn = psycopg2.connect(
            database=DATABASE_SETTINGS['database_name'],
            user=DATABASE_SETTINGS['user'],
            password=DATABASE_SETTINGS['password']
        )
        return self.conn

    def __exit__(self, *args):
        self.conn.close()
