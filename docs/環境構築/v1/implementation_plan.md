# Spring Boot 実行環境の構築計画

以下の手順で、Spring Boot アプリケーションを実行し、画面で検証できる環境を構築します。

## ユーザー承認が必要な点
- JDK 17 (Microsoft Build of OpenJDK 17) を `winget` を使用してシステムにインストールします。
- 実行のために `8080` ポートを使用します（デフォルト）。

## 提案する変更内容

### 環境構築

#### JDK 17 のインストール
- `winget install Microsoft.OpenJDK.17 --accept-package-agreements --accept-source-agreements` を実行して、JDK 17 をインストールします。
- インストール後、PATH の反映を確認するために `java -version` で確認します。

#### データベースの確認
- MySQL がポート 3306 で動作していることは確認済みです。
- `TrainoBook_Answer_7/src/main/resources/application.properties` に記載されている `traino_book` データベース、`book_user` ユーザーが存在し、適切に設定されているかを確認します。
- 必要であれば、初期データ投入用の SQL を実行します。

### アプリケーションの実行
- `TrainoBook_Answer_7` ディレクトリに移動し、`./mvnw spring-boot:run` を実行してアプリケーションを起動します。

## オープンな質問
- [IMPORTANT] データベース `traino_book` やユーザー `book_user` は既にセットアップ済みでしょうか？未設定の場合は、初期化用の SQL スクリプトをこちらで実行する必要があります。
- winget による JDK のインストールを自動で行ってよろしいでしょうか？

## 検証計画

### 自動テスト
- `java -version` で JDK 17 が正しく認識されていることを確認。
- アプリケーションが起動し、コンソールにエラーが出ないことを確認。

### 手動検証
- ブラウザを使用して、`http://localhost:8080/` にアクセスし、画面が表示されることを確認。
