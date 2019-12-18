rem @echo off

rem 作成日 : 2014年7月10日
rem 作成者 : 宮本夏規
rem 目的   : TEXファイルからPDFファイルを作成するバッチファイル
rem ※このファイルの拡張子を".txt"から".bat"に書き換えるとバッチファイルになります。

rem 設定事項
set FILENAME="gra_thes"

rem このバッチが存在するフォルダをカレントに
rem pushd %0\..

cls

platex %FILENAME%.tex
platex %FILENAME%.tex

dvipdfmx %FILENAME%.dvi
rem dvipdfmx -f msembed.map %FILENAME%.dvi

%FILENAME%.pdf

rem pause

exit

