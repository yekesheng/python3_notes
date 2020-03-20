# -*- coding: utf-8 -*-

import MySQLdb

g_db_host = "localhost"
g_db_user = "testuser"
g_db_pass = "test1234"
g_db_name = "test"
g_db_sock = "/data/mysql8/data/mysql.sock"

class LogParser:

    def __init__(self):
        pass

    def __del__(self):
        pass

    def dumptoMysqldb(self, datalist):
        if len(datalist) <= 0:
            return
        conn=MySQLdb.connect(unix_socket=g_db_sock,host=g_db_host,user=g_db_user,passwd=g_db_pass,db=g_db_name,charset="utf8mb4")
        cursor = conn.cursor()
        try:
            sql = "insert into t_log(logTime,clientId,postData) values (%s,%s,%s)"
            cursor.executemany(sql, datalist)
        except:
            pass
        finally:
            conn.commit()
            cursor.close()
        conn.close()

    def parseAccess(self):
		    # [2020-03-19 10:26:01][28390] 62 16.204.18.7 -[[[logType],[35186],[tag],[postData],[1],[145]]]-
        logfile = "test.log"
        with open(logfile, 'r') as v_file:
            datalist = []
            while True:
                line = v_file.readline()
                if not line:
                    break
                if 'apiTime' not in line:
                    continue
                logtime = line[1:20]
                pos1 = line.index('-[[')
                pos2 = line.index(']]-')
                if pos1 <= 0 or pos2 <=0:
                    continue
                pos1 += 3
                logdata = line[pos1:pos2]
                logitem = logdata.split(',')
                if len(logitem) < 6:
                    continue
                if logitem[2] != '[tag]':
                    continue
                clientId = logitem[1][1:-1]
                postData = logitem[3][1:-1]
                datalist.append((logtime,clientId,postData))
                if len(datalist) >= 50:
                    self.dumptoMysqldb(datalist)
                    datalist = []
            self.dumptoMysqldb(datalist)

    def run(self):
        self.parseAccess()

def main():
    lparser = LogParser()
    lparser.run()

if __name__ == '__main__':
  main()
