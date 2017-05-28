import os
import psycopg2

from faxbox.db import User


class Client(object):

    def __init__(self, url=None):
        self.url = url or os.environ.get('DATABASE_URL')

    def add_user(self, name, email, number):
        with psycopg2.connect(self.url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO users (name, email, number) VALUES (%s, %s, %s);',
                    (name, email, number)
                )

    def fetch_user_by_email(self, email):
        with psycopg2.connect(self.url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT name, email, number FROM users WHERE email = %s',
                    (email, )
                )
                data = cur.fetchone()

                if not data:
                    return None

                return User(*data)

    def fetch_user_by_number(self, number):
        with psycopg2.connect(self.url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT name, email, number FROM users WHERE number = %s',
                    (number, )
                )
                data = cur.fetchone()

                if not data:
                    return None

                return User(*data)
