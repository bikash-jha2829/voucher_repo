from contextlib import closing
from typing import List

import psycopg2
import psycopg2.extras


class PgHook:
    """
    :param database: database
    :param user: username
    :param password: password
    :param host: the endpoint
    :param port: port exposed by postgres  (default 5432)
    """

    def __init__(self, database: str, user: str, password: str, host: str, port: int):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def get_conn(self):
        """
        This method returns a connection object for postgres.
        """
        return psycopg2.connect(database=self.database,
                                user=self.user,
                                password=self.password,
                                host=self.host,
                                port=self.port)

    def execute_query(self, query: str) -> List[List[psycopg2.extras.DictRow]]:
        """
        This method executes a query and fetches all of the results in the query
        :return: lists[list -> DictRow Object]
        """
        with closing(self.get_conn().cursor(cursor_factory=psycopg2.extras.DictCursor)) as cur:
            cur.execute(query)
            return cur.fetchall()