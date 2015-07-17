#!/usr/bin/env
# -*- coding: utf-8 -*-

#######################################################
# 加工済みの郵便番号データをSQLiteのデータベースへ変換する
#######################################################

import csv
import datetime as dt
import sqlite3 as sq

print("Run process")

# SQLiteデータベースの新規作成
today = "{0:%y%m%d}".format(dt.date.today())
dbname = "postal_" + today + ".db"
db = sq.connect(dbname)
cur = db.cursor()

# テーブルの作成（なければ作る）
check = cur.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='japan_post'")
check = check.fetchone()

if check is None:
    # japan_postというテーブルを作成
    print("Create table")

    cur.execute("""create table japan_post(
                postcode integer,
                prefecture text,
                city text,
                address text,
                rubi_pref text,
                rubi_city text,
                rubi_addr text)""")
else:
    cur.execute("""DELETE FROM japan_post""")  # テーブル内のデータ削除
    pass


print("Prepare Database")

# 日本郵便からダウンロードした郵便番号リストを読み込み
fp = open("x-ken-all.csv", encoding="cp932")
post = csv.reader(fp)
print("Road CSV")

# CSVから各情報を読み込み、キープする
print("Start insert")

for row in post:
    t = (row[2],  # 郵便番号
         row[6],  # 都道府県
         row[7],  # 市町村
         row[8],  # 町域
         row[3],  # よみ-都道府県
         row[4],  # よみ-市町村
         row[5])  # よみ-町域

    cur.execute("insert into japan_post values(?,?,?,?,?,?,?)", t)

print("Finish insert")

# データベースに書き込み（確定させる）
db.commit()
print("Commit!")

# データベースを閉じる
db.close()
print("End process")
