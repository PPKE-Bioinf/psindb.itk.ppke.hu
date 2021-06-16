import time
import mariadb
from contextlib import closing


class DB:
    conn = None
    db_args = None
    retries = None
    retry_wait = 8
    sql_client = None

    # do not instantiate this class
    def __new__(cls):
        raise NotImplementedError

    @classmethod
    def connect(cls, sql_client=mariadb):
        cls.sql_client = sql_client
        cls.conn = sql_client.connect(**cls.db_args)
        cls.conn.ping()

    @classmethod
    def execute_sql(cls, sql_string, data=None):
        try:
            cls.conn.ping()
        except mariadb.InterfaceError:
            cls.conn.reconnect()

        with closing(cls.conn.cursor()) as cur:
            for i in range(cls.retries):
                try:
                    if data:
                        query = cur.execute(sql_string, data)
                    else:
                        query = cur.execute(sql_string)

                    # store the cursors content in a list
                    results = list(cur.fetchall())

                    # commit all transactions, better safe than sorry :)
                    cls.conn.commit()

                    return query, results

                except (
                        AttributeError, cls.sql_client.OperationalError
                ) as e:
                    print(
                        f"DB connection lost. Reconnecting ({i})...")

                    print("ERROR")
                    print(e)

                    time.sleep(cls.retry_wait)

                    try:
                        db = cls.sql_client.connect()
                        db.ping(True)
                    except (
                        AttributeError, cls.sql_client.OperationalError
                    ) as e:
                        print(
                            "Can't establish DB connection, waiting for retry"
                        )

                        print("ERROR")
                        print(e)

                        time.sleep(30)

            raise Exception("Failed to establish DB connection")
