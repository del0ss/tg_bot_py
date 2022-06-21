import psycopg2 as psycopg

from .base_repository import AbstractRepository


class PgRepository(AbstractRepository):
    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self.conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()
        self.createTables()

    def createTables(self):
        self.cur.execute('''CREATE TABLE if not EXISTS users
                                              (id SERIAL PRIMARY KEY,
                                              phone         VARCHAR,
                                              tgId         BIGINT,
                                              roleId INT); ''')
        self.cur.execute('''CREATE TABLE if not EXISTS attempts
                                              (id SERIAL PRIMARY KEY,
                                              tgId         BIGINT,
                                              attempt       int DEFAULT 5); ''')
        self.cur.execute('''CREATE TABLE if not EXISTS spamlist
                                              (id SERIAL PRIMARY KEY,
                                              tgId         BIGINT,
                                              timespam       VARCHAR); ''')
        self.conn.commit()

    def getUser(self, tg_id):
        self.cur.execute(f"SELECT tgId FROM users WHERE tgId=%s", (tg_id,))
        data = self.cur.fetchone()
        self.conn.commit()
        return data

    def getPhone(self, phone: int) -> bool:
        self.cur.execute("SELECT phone FROM users WHERE phone=%s", (phone,))
        data = self.cur.fetchone()
        self.conn.commit()
        return data

    def updateTgId(self, phone, tg_id):
        self.cur.execute("UPDATE users SET tgId=%s  WHERE phone=%s", (tg_id, phone))
        self.conn.commit()

    def insertAttempt(self, tg_id):
        if self.cur.execute("SELECT tgid FROM attempts WHERE tgId=%s", (tg_id,)) is None:
            self.cur.execute("INSERT INTO  attempts (id, tgId) VALUES (DEFAULT, %s)", (tg_id,))
            self.conn.commit()

    def attempt(self, tg_id):
        self.cur.execute("UPDATE attempts SET attempt = attempt - 1 WHERE tgid=%s", (tg_id,))
        self.cur.execute("SELECT attempt FROM attempts WHERE tgid=%s", (tg_id,))
        data = self.cur.fetchone()
        self.conn.commit()
        return data

    def deleteAttempt(self, tg_id):
        self.cur.execute("DELETE FROM attempts WHERE tgid=%s", (tg_id,))
        self.conn.commit()

    def insertSpamList(self, tg_id, time):
        self.cur.execute("INSERT INTO  spamlist (id, tgid, timespam) VALUES (DEFAULT, %s, %s)", (tg_id, time))
        self.conn.commit()

    def getSpamList(self, tg_id):
        self.cur.execute("SELECT timespam FROM spamlist WHERE tgid=%s", (tg_id,))
        data = self.cur.fetchone()
        self.conn.commit()
        return data

    def deleteUserFromSpamList(self, tg_id):
        self.cur.execute("DELETE FROM spamlist WHERE tgid=%s", (tg_id,))
        self.conn.commit()
