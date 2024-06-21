import psycopg2

class Execute:
    def __init__(self):
        self.keepalive_kwargs = {
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 5,
            "keepalives_count": 5,
        }
        self.conn = self.connect()

    def connect(self):
        conn = psycopg2.connect(
            database="knitting",
            user="postgres",
            password="55555",
            host="127.0.0.1",
            port="5432",
            **self.keepalive_kwargs,
        )
        conn.autocommit = True
        return conn

    def insert(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            cur.close()
            return True
        except Exception as e:
            print(str(e))
            return False

    def insert_return_id(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            id = cur.fetchone()[0]
            cur.close()
            return id
        except Exception as e:
            print(str(e))
            return False

    def select(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            rows = [
                dict((cur.description[i][0], value) for i, value in enumerate(row))
                for row in cur.fetchall()
            ]
            cur.close()
            return rows

        except Exception as e:
            print(str(e))
            return False

    def update(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            cur.close()
            return True
        except Exception as e:
            print(str(e))
            return False

    def delete(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            cur.close()
            return True
        except Exception as e:
            print(str(e))
            return False