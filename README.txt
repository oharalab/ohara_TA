===== USAGE =====
./C_Program_Compiler_develop.py -z <提出された zip ファイルを含むフォルダへのパス> -e <採点する課題（ex4 なら 4）>

===== STRUCTURE =====
bin - cygwin 用の nkf 
exercise - ex{0} - inputs 	 - ex{0}_{1} - trial{2}.txt
				 - sentences - ex4th.zip
		         - answers	 - ex{0}_{1} - ex{0}_{1}.c
html - 表示用のファイル
thirdparty - html 表示用のライブラリ
students.txt - 学生リスト

===== RELEASE NOTE =====
2018/10/08
> Update
・ 複数回提出されたときに最新のファイルを選択
・ 学生番号と氏名の表示
・　問題文のモーダル表示
・　解答例の表示（要模範解答プログラム）
・ debug.txt の廃止 

>　Bug
・ ファイルパスに日本語が含まれている場合への対応

2018/10/01
> Update
・ UI を html に変更
・ practice と exercise が両方提出されたときに，命名規則 > タイムスタンプ となるように変更

> Bug
・ 命名規則に従っていないファイルへの対応