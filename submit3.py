# coding: utf-8

from shibboleth_login import ShibbolethClient
from bs4 import BeautifulSoup
import sqlite3
from contextlib import closing
import os

name = "username"
password = "password"
url = 'url'
dbname = 'html.db'


class htmlDB:
    dates = []
    charges = []
    categories = []
    notices_main = []
    notices_detail = []

    def __init__(self):
        with ShibbolethClient(name, password) as client:
            res = client.get(url)

        soup = BeautifulSoup(res.text, "lxml")

        htmlDB.dates = soup.select('dd.nl_notice_date')
        htmlDB.charges = soup.select('dd.nl_div_in_charge')
        htmlDB.categories = soup.select('dd.nl_category')
        htmlDB.notices_main = soup.select('dd > a')
        htmlDB.notices_detail = soup.select('p.notice_info')

    def CreateDB(self):
        path = "./html.db"
        if(os.path.exists(path)):
            print("Already created data base")
        else:
            with closing(sqlite3.connect(dbname)) as connect:
                cur = connect.cursor()

                table = '''create table information (dates VARCHAR, charges VARCHAR ,categories VARCHAR , notices_main VARCHAR, notices_detail VARCHAR )'''
                cur.execute(table)
                connect.commit()

                for html_date, html_charge, html_category, html_notice_main, html_notice_detail in zip(htmlDB.dates, htmlDB.charges, htmlDB.categories, htmlDB.notices_main, htmlDB.notices_detail):
                    first_insert_sql = 'insert into information (dates, charges, categories, notices_main, notices_detail) values (?,?,?,?,?)'
                    info = (self.EnocodeData(html_date.get_text()), self.EnocodeData(html_charge.get_text()), self.EnocodeData(html_category.get_text()), self.EnocodeData(html_notice_main.get_text()), self.EnocodeData(html_notice_detail.get_text()))
                    cur.execute(first_insert_sql, info)

                connect.commit()
                print("Created data base")

    def InsertRow(self,date,charge,category,notice_main,notice_detail):
        with closing(sqlite3.connect(dbname)) as connect:
            cur = connect.cursor()

            insert_sql = '''insert into information (dates, charges, categories, notices_main, notices_detail) values (?,?,?,?,?)'''
            insert_info = (date, charge, category, notice_main, notice_detail)
            cur.execute(insert_sql, insert_info)
            connect.commit()
            print("Inserted row")

    def DeleteRow(self,date,charge,category,notice_main,notice_detail):
        with closing(sqlite3.connect(dbname)) as connect:
            cur = connect.cursor()

            delete_sql = '''delete from information where dates=? and charges=? and categories=? and notices_main=? and notices_detail=?'''
            delete_info = (date, charge, category, notice_main, notice_detail)
            cur.execute(delete_sql, delete_info)
            connect.commit()
            print("Deleted row")

    def UpdateRow(self,tar_date,tar_charge,tar_category,tar_notice_main,tar_notice_detail,date,charge,category,notice_main,notice_detail):
        with closing(sqlite3.connect(dbname)) as connect:
            cur = connect.cursor()

            update_sql = '''update information set dates=?, charges=?, categories=?, notices_main=?, notices_detail=? where dates=? and charges=? and categories=? and notices_main=? and notices_detail=?'''
            update_info = (date, charge, category, notice_main, notice_detail, tar_date, tar_charge, tar_category, tar_notice_main, tar_notice_detail)
            cur.execute(update_sql, update_info)
            connect.commit()
            print("Updated row")

    def GetRow(self,date,charge,category,notice_main,notice_detail):
        with closing(sqlite3.connect(dbname)) as connect:
            connect.row_factory = sqlite3.Row
            cur = connect.cursor()

            get_sql = '''select * from information where dates=? or charges=? or categories=? or notices_main=? or notices_detail=?'''
            get_info = (date.encode('shift_jis'), charge.encode('shift_jis'), category.encode('shift_jis'), notice_main.encode('shift_jis'), notice_detail.encode('shift_jis'))
            cur.execute(get_sql, get_info)
            for row in cur:
                print(row['dates'].decode('shift_jis','ignore'))
                print(row['charges'].decode('shift_jis', 'ignore'))
                print(row['categories'].decode('shift_jis', 'ignore'))
                print(row['notices_main'].decode('shift_jis', 'ignore'))
                print(row['notices_detail'].decode('shift_jis', 'ignore'))

    def EnocodeData(self,target):
        return target.encode('shift_jis','ignore').decode('shift_jis','ignore').strip().encode('shift_jis','ignore')


if __name__ == "__main__":
    ctrldb = htmlDB()
    ctrldb.CreateDB()