#複数のPythonファイルを順に起動する方法

以下のようなbatファイルを作成することで、Pythonファイルを連続で起動できます。</br>
置く場所は、"複数起動したいプログラムの入ったフォルダ"をまとめるフォルダです。  


方法としては多分ゴリ押しだと思うので参考程度に。  
該当フォルダに移動→Pythonpathを追加→プログラム起動→まとめフォルダに戻る→次のフォルダに移動を延々と繰り返すような挙動です。  
cd hogehoge　〜 cd ../までで1セットですね。

以下コードのサンプルです。

	cd hogehoge
	set PYTHONPATH=%cd%
	python hoge.py
	cd ../
	cd hogehoge2
	set PYTHONPATH=%cd%
	python hoge2.py

※このファイルはGithubの練習も兼ねております

