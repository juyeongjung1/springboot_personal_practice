@echo off
rem ===dbset.bat===
rem 使用の前提
rem 　１）データベース作成はローカルコンピュータです
rem 　２）rootユーザのパスワードはpasswordです
rem 

mysql -uroot -ppassword  < dropUser.sql
mysql -uroot -ppassword  < dropDB.sql
mysql -uroot -ppassword  < createUser.sql
mysql -uroot -ppassword  < createDB.sql
echo =========================================================
echo データベースの作成が完了しました。
echo ※エラーが出る場合は再度、やり直してください。
echo =========================================================
pause
