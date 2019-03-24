import psycopg2
from config.settings import DNS

def get_connection():
    return psycopg2.connect(DNS)
