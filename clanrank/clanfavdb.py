import sqlite3
import os

DB_PATH = os.path.expanduser('~/.hoshino/clan_fav.db')


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
                           CLANNAME      TEXT    NOT NULL);''')
        except:
            raise Exception('创建收藏表发生错误')

    def _insert(self, gid, name):
        try:
            conn = self._connect()
            conn.execute("INSERT INTO CLANFAVTABLE (ID,GROUPID,CLANNAME) \
                                VALUES (NULL, ?, ?)", (gid, name))
            conn.commit()
            return True
        except:
            raise Exception('添加收藏发生错误')

    def _delete(self, gid, name):
        try:
            conn = self._connect()
            conn.execute("DELETE FROM CLANFAVTABLE WHERE GROUPID=? AND CLANNAME=?", (gid, name))
            conn.commit()
            return True
        except:
            raise Exception('删除收藏发生错误')

    def _update(self, gid, name, prename):
        try:
            conn = self._connect()
            conn.execute("UPDATE CLANFAVTABLE SET CLANNAME=? WHERE GROUPID=? AND CLANNAME=?", (name, gid, prename))
            conn.commit()
            return True
        except:
            raise Exception('更新收藏发生错误')

    def _find(self, gid):
        try:
            r = self._connect().execute("SELECT CLANNAME FROM CLANFAVTABLE WHERE GROUPID=?",(gid,)).fetchall()
            return r
        except:
            raise Exception('查询收藏发生错误')

    def _find_by_name(self, gid, name):
        try:
            r = self._connect().execute("SELECT ID FROM CLANFAVTABLE WHERE GROUPID=? AND CLANNAME=?", (gid, name)).fetchone()
            return r
        except:
            raise Exception('查询收藏发生错误')
