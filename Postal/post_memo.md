## 郵便番号による住所検索、参加者DBの更新

### 郵便番号のDBを取得
#### メモ
* 日本郵便HPからCSVで郵便番号リストをダウンロードできる
  * [郵便番号データダウンロード](http://www.post.japanpost.jp/zipcode/dl/kogaki-zip.html)
  * 12万行もあるのでとてもじゃないけどCSVでは扱えない
  * 1ヶ月に一度くらい更新されてるっぽい？
* CSVをsqlのデータベースに移す、DBの更新ができると良い（その都度作りなおしてもいいけど）  

＜参考になりそうなサイト＞
* 郵便番号csv → sqlite  
 * [PythonでSQLiteを使ってみる](http://bty.sakura.ne.jp/wp/archives/333)
 * [MySQLへ郵便番号データをインポートする](http://plaza.rakuten.co.jp/pgmemo/diary/200512110000/)
 * [プログラミング講座：SQLite を使って郵便番号から住所を検索するプログラム](http://www.mysticwall.com/course/postal01.html)
 * [郵便番号データについて思ったこと | Studio JamPack](http://jamfunk.jp/wp/?p=390)

* pyhonでsqlite
 * [Pythonのsqlite3ライブラリでデータベースを操作しよう](http://msrx9.bitbucket.org/blog/html/2013/07/04/db_study.html)
 * [SQLite](http://www.python-izm.com/contents/external/sqlite.shtml)
 * [データベース（sqlite）](https://www.quark.kj.yamagata-u.ac.jp/~hiroki/python/?id=16)  


* 日本郵便の郵便番号CSVはいろいろとヒドイ（郵便番号データの落とし穴）
  * 加工済みデータが配布されているらしいのでそれを使うことにする
  * [郵便番号データのダウンロード - zipcloud](http://zipcloud.ibsnet.co.jp/)
  * 更新にも対応してくれるらしいので、ときたま更新すべきかも（半年とか年一とか)  


* 郵便データの落とし穴
  * [郵便番号データの落とし穴 – YU-TANG's MS-Access Discovery](http://www.f3.dion.ne.jp/~element/msaccess/AcTipsKenAllCsv.html)
  * [郵便番号データについて思ったこと|Studio Jampack](http://jamfunk.jp/wp/?p=390)
  * [郵便番号から住所を検索するサービスにまともなものがない – ぐるぐる～](http://d.hatena.ne.jp/bleis-tift/20080531/1212217681)

 * エラー処理
   * 郵便番号
     * 7桁かどうか
     * 数値のみで構成されているか
     * ハイフンは入っているか？（入っていれば削除）
