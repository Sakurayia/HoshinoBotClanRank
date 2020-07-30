import sqlite3
import os

DB_PATH = os.path.expanduser('~/.hoshino/clan_fav_new.db')


class ClanFav:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self._create_table()

    def _connect(self):
        return sqlite3.connect(DB_PATH)

    def _create_table(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS CLANFAVTABLE
                          (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                           GROUPID       INT     NOT NULL,
                           CLANNAME      TEXT    NOT NULL,
                           RANK          INT     NOT NULL,
                           SCORE         INT     NOT NULL);''')
        except:
            raise Exception('创建关注表发生错误')

    def _insert(self, gid, name, rank, score):
        try:
            conn = self._connect()
            conn.execute("INSERT INTO CLANFAVTABLE (ID,GROUPID,CLANNAME,RANK,SCORE) \
                                VALUES (NULL, ?, ?, ?, ?)", (gid, name, rank, score))
            conn.commit()
            return True
        except:
            raise Exception('添加关注发生错误')

    def _delete(self, gid, name):
        try:
            conn = self._connect()
            conn.execute("DELETE FROM CLANFAVTABLE WHERE GROUPID=? AND CLANNAME=?", (gid, name))
            conn.commit()
            return True
        except:
            raise Exception('删除关注发生错误')

    def _update(self, gid, name, prename, rank, score):
        try:
            conn = self._connect()
            conn.execute("UPDATE CLANFAVTABLE SET CLANNAME=?, RANK=?, SCORE=? WHERE GROUPID=? AND CLANNAME=?", (name, rank, score, gid, prename))
            conn.commit()
            return True
        except:
            raise Exception('更新关注发生错误')

    def _find(self, gid):
        try:
            r = self._connect().execute("SELECT CLANNAME, RANK, SCORE FROM CLANFAVTABLE WHERE GROUPID=?",(gid,)).fetchall()
            return r
        except:
            raise Exception('查询关注发生错误')

    def _find_by_name(self, gid, name):
        try:
            r = self._connect().execute("SELECT ID FROM CLANFAVTABLE WHERE GROUPID=? AND CLANNAME=?", (gid, name)).fetchone()
            return r
        except:
            raise Exception('查询关注发生错误')
