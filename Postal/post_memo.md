* 日本郵便の郵便番号CSVはいろいろとヒドイ（郵便番号データの落とし穴）
 * 加工済みデータが配布されているらしいのでそれを使うことにする
 * [郵便番号データのダウンロード - zipcloud](http://zipcloud.ibsnet.co.jp/)
 * 更新にも対応してくれるらしいので、ときたま更新すべきかも（半年とか年一とか）

* 郵便データの落とし穴
 *[郵便番号データの落とし穴 – YU-TANG's MS-Access Discovery](http://www.f3.dion.ne.jp/~element/msaccess/AcTipsKenAllCsv.html)
 *[郵便番号データについて思ったこと|Studio Jampack](http://jamfunk.jp/wp/?p=390)
 *[郵便番号から住所を検索するサービスにまともなものがない – ぐるぐる～](http://d.hatena.ne.jp/bleis-tift/20080531/1212217681)

 * エラー処理
  *　郵便番号
   * 7桁かどうか
   * 数値のみで構成されているか
   * ハイフンは入っているか？（入っていれば削除）