#!/usr/bin/env
# -*- coding: utf-8 -*-

#######################################################
# pythonからデータベースにアクセス
#######################################################

import datetime as dt
import pandas as pd
import re
import sqlite3 as sq
import unicodedata as ud

#######################################################
# いろいろと準備
#######################################################

# エラーリスト
Error_post = []
Error_address = []
today = "{0:%y%m%d}".format(dt.date.today())
fp = open("output/Error_" + today + ".txt", "w")

# 郵便番号DBの読み込み
post_db = sq.connect("postal.db")
cur = post_db.cursor()

# 参加者DBの読み込み
df = pd.read_csv("参加者リスト.csv", index_col="研究者番号", encoding="utf-8")
postcodes = df[["郵便番号", "住所"]]   # DataFrame型
print("#旧_参加者DB")
print(postcodes)

# 書き込み用データフレーム, CSVの準備
df_write = pd.DataFrame()
output_path = "参加者リスト_" + today + ".csv"

# ハイフン変換
# 半角ハイフン(-),全角ハイフン マイナス（−）, 長音（ー）, 全角ダッシュ（―）、全角ハイフン（‐）
hyphens = ["-", "−", "ー", "―", "‐"]

# 全角数字, 半角数字検索用
zenkaku_n = re.compile(r"^[０-９]+$")

#######################################################
# 関数
#######################################################


# 郵便番号の形式を揃える
def arrange_postcode(code):
    # ハイフン変換(全角、半角対応)
    for e in hyphens:
        if e in code:
            # 文字列置換の（準備）関数：maketransの第3引数に渡すと部分削除になる
            # ハイフンとダッシュが存在するので注意
            code = code.translate(str.maketrans("", "", "-−ー―‐"))
            break
        else:
            pass

    # 全角数字を半角数字に変換(NFKCは上手くいくためのオプション？)
    if zenkaku_n.search(code) is not None:
        code = ud.normalize('NFKC', code)

    else:
        pass  # もしこれ以外が含まれていた場合は一端スルー

    return code


# 郵便番号から住所を特定
def post_address(pcode):
    # DBから一致する住所を検索（リスト + タプルで返ってくる）
    cur.execute("""SELECT prefecture,city,address \
                   FROM japan_post WHERE postcode='%s'""" % pcode)

    # DBから抽出したリストからタプルを取り出す（今回は一致するのは1つだけのはず）
    results = cur.fetchall()[0]

    # DB抽出で指定した順番で入っているので取り出し（都道府県、市町村、町域）
    prefecture, city, address = results[0], results[1], results[2]

    return prefecture, city, address


# 元の住所から、郵便番号から取得した住所を使った置き換えで番地等を抽出
def number_address(ID, right, pref, city, addr):
    if "NaN" not in [pref, city, addr]:  # 郵便番号による住所取得に失敗してないもののみ

        # 都道府県を置き換え（もし住所内で省略されていた場合はスルー）
        if pref in right:
            right = right.replace(pref, "")
        else:
            pass

        # 市町村、町域を置き換え（もし住所内で省略されていた場合はエラー）
        for i in [city, addr]:
            if i in right:
                right = right.replace(i, "")
            else:  # 市町村以下を省略することはめったにないのでなければエラーとする
                right = "NaN"
                Error_address.append(ID)
                break
    else:   # 郵便番号による住所取得に失敗しているもの（こちらでも再度エラーリスト行き）
        right = "NaN"
        Error_address.append(ID)

    return right

#######################################################
# メイン処理
#######################################################

if __name__ == '__main__':
    print("#Run process")
    # 参加者DBから一行づつ住所列を作成
    for ID, info in postcodes.iterrows():  # 第二の返り値はSereis型で返ってくるので下で分割
        code = info["郵便番号"]
        right = info["住所"]

        pcode = arrange_postcode(code)  # 郵便番号の形式を整える
        print("Postcode:  " + pcode)

        if len(pcode) == 7 and pcode.isdigit():  # 7桁の数字であるもののみ処理
            try:
                pref, city, addr = post_address(pcode)  # 郵便番号DBから住所を取得
            except:
                Error_post.append(ID)  # よく分かんないエラーをエラーリストに放り込む
                pref, city, addr = "NaN", "NaN", "NaN"  # とりあえず0で埋める
        else:
            Error_post.append(ID)  # 郵便番号でないものをエラーリストに放り込む
            pref, city, addr = "NaN", "NaN", "NaN"  # とりあえず0で埋める

        # 元の住所から、郵便番号から取得した住所を使った置き換えで番地等を抽出
        try:
            number = number_address(ID, right, pref, city, addr)
        except:
            number = "NaN"

        # データから１行作成
        df_addr = pd.DataFrame({"研究者番号": [ID],
                                "郵便番号": [pcode],
                                "都道府県": [pref],
                                "市町村": [city],
                                "町域": [addr],
                                "番地等": [number]},
                               columns=["研究者番号", "郵便番号", "都道府県",
                                        "市町村", "町域", "番地等"])

        # 住所列に１行づつ追加していく
        df_write = pd.concat([df_write, df_addr])

    # 住所列のindexを再設定
    df_write = df_write.set_index(["研究者番号"])

    # 元のデータベースを使って、新しく住所列を追加
    df = df.drop(["郵便番号"], axis=1)  # 整えた後の郵便番号に統一するために、いちど郵便番号列を削除
    df = pd.concat([df, df_write], axis=1)  # 元のデータフレーム + 住所列
    df.to_csv(output_path)  # 新規でCSV出力
    print("#新_参加者DB")
    print(df)

    # エラーが出たものを別フォルダにアウトプット
    print("#Error_ID")
    print("##Error_post")
    print(Error_post)
    print("##Error_address")
    print(Error_address)

    # 郵便番号→住所でエラーがでたもの
    if len(Error_post) > 0:
        fp.write("##Error_post" + "\n")
        for m in Error_post:
            fp.write(str(m) + "\n")

    # 住所→番地等でエラーがでたもの
    if len(Error_address) > 0:
        fp.write("##Error_address" + "\n")
        for n in Error_address:
            fp.write(str(n) + "\n")

    print("#End process")

# いろいろ終了
fp.close()  # エラーリストを閉じる
post_db.close()  # データベースを閉じる
