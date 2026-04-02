@echo off
rem ===dbset.bat===
rem 使用の前提
rem 　１）データベース作成はローカルコンピュータです
rem 　２）rootユーザのパスワードはPa$$w0rdです
rem 

mysql -uroot -pPa$$w0rd  < dropUser.sql
mysql -uroot -pPa$$w0rd  < dropDB.sql
mysql -uroot -pPa$$w0rd  < createUser.sql
mysql -uroot -pPa$$w0rd  < createDB.sql
echo =========================================================
echo データベースの作成が完了しました。
echo ※エラーが出る場合は再度、やり直してください。
echo =========================================================
pause
