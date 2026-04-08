# TrainoBook：Spring Boot 総合演習 - 書籍管理システム -

## 🚀 はじめに
本プロジェクトは、Thymeleaf、Spring Data JPA、Spring Security、そして Bootstrap 5 を用いた本格的な Web アプリケーション開発を学ぶための総合演習教材です。
「書籍管理システム」の構築を通じて、Spring Boot の基本から実践的なスタイリングまでを段階的に習得できます。

---

## 📚 学習リソース（まずはこちらを確認してください）

演習を進めるにあたっての「地図」と「羅針盤」となるドキュメントです。

1.  **[演習ガイド](docs/Exercise_Guide.md)**
    各章の課題内容、実装のヒント、テキストとの対応関係がまとめられています。
2.  **[書籍管理システム 全体設計書](docs/Comprehensive_Design_Specification.md)**
    各チャプター終了後の完成イメージ（スクリーンショット）や画面遷移図、技術的な構成が網羅されています。

---

## 📂 プロジェクト構成

受講生用のスターターキットと、学習のベンチマークとなる各章の回答コードが含まれています。

### 1. メイン演習（TrainoBook シリーズ）
-   **`TrainoBook`**：[受講生用] ここから実装を開始します（スターターキット）。
-   **`TrainoBook_Answer_2 ～ 7`**：[回答コード] 各チャプターの実装完了済みコードです。

### 2. データベースセットアップ
-   **`Spring_Enshu_DBSET`**：本演習で使用するデータベース（`spring_exercise`）の構築スクリプトが含まれています。

### 3. その他（参考用）
-   `enshu_answer_*` / `spring_answer_*`：各章の機能を単体で確認するための参考用コードです。

---

## 🛠 技術スタック
-   **Java**: 17
-   **Spring Boot**: 4.0.3
-   **テンプレートエンジン**: Thymeleaf / Thymeleaf Layout Dialect
-   **ORM**: Spring Data JPA
-   **データベース**: MySQL
-   **CSSフレームワーク**: Bootstrap 5
-   **ビルドツール**: Maven

---

## 🏁 クイックアクセス
実装を始める前に MySQL を起動し、**`dbsetup/dbset.bat`** を実行してデータベースをセットアップしてください。

各章の回答を確認する場合は、該当フォルダに移動して以下のコマンドを実行します。
```powershell
./mvnw spring-boot:run
```
