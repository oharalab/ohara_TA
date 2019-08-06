===== USAGE =====
author: H
./C_Program_Compiler_develop.py -z <提出された zip ファイルを含むフォルダへのパス> -e <採点する課題（ex4 なら 4）>

===== INSTALLATION ====
author: Y
１．student.txt の作成
一応，先生から許可を得た後，course power の履修者〜〜から一括ダウンロード
（ファイル名はstudent.csvが良い）
その後，make_student_list.py を動かせば良い
２．デバッグ時は場合によって，nkf のインストールが必要
sudo apt install nkf
３．注意事項：
・make_input.py によって作成される answer は稀に修正が必要となるので注意
（bs4 の対応が面倒だったのでO棟やN棟では動作しない）
・make_csv.py のスコア計算の割合は勘なので，3,4,5の点数は真面目につけること
・いくつか明らかでないバグがあるかも

===== STRUCTURE =====
bin - cygwin 用の nkf
exercise - ex{0} - inputs 	 - ex{0}_{1} - trial{2}.txt
				 - sentences - ex4th.zip
		         - answers	 - ex{0}_{1} - ex{0}_{1}.c
html - 表示用のファイル
thirdparty - html 表示用のライブラリ
students.txt - 学生リスト

===== RELEASE NOTE =====
author: Y
2018/12/05
> How to use
・ (unavailable in cygwin, because it uses bs4 (BeautifulSoup4)) 
    make_input.py -z zipfile

> Update
・ html からの入力と回答の生成（answer 作るのがめんどくさい人用）

author: I
2018/10/08
> Update
・ 複数回提出されたときに最新のファイルを選択
・ 学生番号と氏名の表示
・ 問題文のモーダル表示
・ 解答例の表示（要模範解答プログラム）
・ debug.txt の廃止

>　Bug
・ ファイルパスに日本語が含まれている場合への対応

2018/10/01
> Update
・ UI を html に変更
・ practice と exercise が両方提出されたときに，命名規則 > タイムスタンプ となるように変更

> Bug
・ 命名規則に従っていないファイルへの対応
