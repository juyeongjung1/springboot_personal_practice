@echo off

mysql -uroot -pPa$$w0rd  < dropUser.sql
mysql -uroot -pPa$$w0rd  < dropDB.sql
echo =========================================================
echo データベースの削除が完了しました。
echo ※エラーが出る場合は再度、やり直してください。
echo =========================================================
pause
