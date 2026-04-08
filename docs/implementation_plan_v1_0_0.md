# pom.xml ビルドエラー修正計画 (v1.0.0)

## 概要
`TrainoBook/pom.xml` において、Spring Boot のバージョンが `3.4.1` に設定されている一方で、依存関係に標準外の `spring-boot-starter-webmvc` 等が指定されているため、バージョン未指定エラーが発生しています。
ワークスペース内の他の解答プロジェクト（`TrainoBook_Answer_7` 等）を確認したところ、Spring Boot `4.0.3` を使用しており、そちらではこれらのスターターが定義されているようです。
したがって、`TrainoBook` プロジェクトのビルド設定を `4.0.3` 環境に合わせることで、この問題を解決します。

## ユーザー確認事項
> [!IMPORTANT]
> この修正により、Spring Boot のバージョンが `3.4.1` から `4.0.3` に変更されます。これは本演習環境固有のバージョンアップとなります。また、Groovy のバージョン指定も追加されます。

## 提案される変更点

### TrainoBook プロジェクト

#### [MODIFY] [pom.xml](file:///c:/work/springboot_personal_practice/springboot_personal_practice/TrainoBook/pom.xml)
- `<parent>` の `<version>` を `3.4.1` から `4.0.3` に更新します。
- `<properties>` セクションに `<groovy.version>5.0.3</groovy.version>` を追加します。
  - これは以前の会話ログ（Conversation 7579eb3c）にて、Groovy 5.x の互換性問題を修正するために必要とされていた処置です。

## 検証計画

### 自動テスト / ビルド確認
- `mvn clean compile` を実行し、依存関係のエラーが解消されることを確認します。

### 手動確認
- アプリケーションを起動し、既存の機能（ブラウザでの表示等）に影響がないか確認します。

## Open Questions
- 特になし（解答プロジェクトの構成への準拠を優先します）。
