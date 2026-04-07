# 書籍管理システム 全体設計書（進化のプロセス）

本ドキュメントは、演習を通してシステムがどのように進化していくかを可視化したものです。各章のマイルストーンごとに、画面遷移とデザインの変化を確認できます。

---

## 第2章：Spring Web アプリケーション（画面遷移とデータ通信）
**テーマ：モックデータによる画面遷移の確立**

最初のステップでは、データベースを使用せず、コントローラー内で作成した固定データ（モック）を使用して画面表示と遷移を確認します。

### 画面遷移図
```mermaid
graph LR
    Login[ログイン画面] --> Menu[メニュー画面]
    Menu --> List[書籍一覧]
    Menu --> Form[書籍登録フォーム]
    Form --> Confirm[登録確認画面]
    Confirm --> List
```

### 主要画面（拡大表示）
| ログイン画面 | 書籍登録フォーム |
| :---: | :---: |
| ![Login](images/ch2_login_page_1775529705270.png) | ![Registration](images/ch2_book_registration_form_1775529713030.png) |

---

## 第3章：Spring Data JPA (DB連携) 
**テーマ：データの永続化（DBとの接続）**

第2章のモックデータを卒業し、MySQLデータベースと連携します。登録したデータが実際にDBに保存され、一覧画面で表示される「アプリケーションの骨格」が完成する重要な段階です。

### 画面遷移図
```mermaid
graph LR
    Menu[メニュー画面] -- 引継ぎ --> List[書籍一覧]
    Form[登録フォーム] -- 保存 --> DB[(MySQL)]
    DB -- 取得 --> List
```

### 主要画面
| 書籍一覧（DBデータ表示） |
| :---: |
| ![Book List DB](images/ch3_book_list_db_1775529833918.png) |

---

## 第4章：バリデーションと認証
**テーマ：入力チェックとセキュリティの基本**

不正なデータ入力を防ぐバリデーション機能と、セッションを利用した簡易的なログイン認証機能を実装します。

### 画面遷移図
```mermaid
graph TD
    Start((開始)) --> Login{ログイン}
    Login -- 失敗 --> LoginErr[ログイン画面: エラー表示]
    Login -- 成功 --> Menu[メニュー]
    Menu --> Form[登録フォーム]
    Form -- 不備あり --> FormErr[登録フォーム: 赤字メッセージ]
```

### 主要画面
| バリデーションエラー（赤字表示） |
| :---: |
| ![Validation Errors](images/ch4_validation_errors_1775529946941.png) |

---

## 第5章：共通レイアウトの適用 (Thymeleaf Layout Dialect)
**テーマ：保守性の向上とデザインの統一**

ヘッダーやフッターを共通パーツ化し、すべての画面で統一された「Webアプリらしい」外観を実現します。

### 画面遷移図
```mermaid
graph TD
    Component[共通レイアウト定義] --> PageA[書籍一覧]
    Component --> PageB[登録フォーム]
    subgraph Shared Layout
        Header[ヘッダー]
        Footer[フッター]
    end
```

### 主要画面
| 共通レイアウト適用後の書籍一覧 |
| :---: |
| ![Common Layout](images/ch5_layout_header_content_1775530050363.png) |

---

## 第6章：リレーション（1対多）と検索機能
**テーマ：テーブル結合と動的クエリ**

「ジャンル」テーブルとの結合（Join）により、書籍にジャンル名を付与します。また、JPQLを用いた検索機能を実装します。

### 画面遷移図
```mermaid
graph LR
    Menu --> SearchTitle[タイトル検索]
    Menu --> SearchPrice[価格帯検索]
    SearchTitle --> Results[検索結果一覧]
    SearchPrice --> Results
```

### 主要画面
| ジャンル選択（結合表示） | 検索結果（シンプル表示） |
| :---: | :---: |
| ![Genre Select](images/ch6_genre_select_box_1775530168540.png) | ![Search Results](images/ch6_search_results_no_criteria_1775530169992.png) |

---

## 第7章：Bootstrapによるスタイリング（完成形）
**テーマ：モダンなUIデザインの体験**

CSSを自前で書くのではなく、世界的に普及しているフレームワーク「Bootstrap 5」を導入し、プレミアムな外観へと一新します。

### 画面遷移図
```mermaid
graph LR
    Login[Bootstrapログイン] --> Menu[カード型メニュー]
    Menu --> List[ストライプテーブル]
    Menu --> Form[入力カード]
```

### 主要画面（最終形態）
| メニュー（カードデザイン） | 登録フォーム（Bootstrap適用） |
| :---: | :---: |
| ![Final Menu](images/ch7_index_menu_1775530275046.png) | ![Final Form](images/ch7_registration_form_final_1775530316545.png) |

---

## データベース構造 (ER図)
システム全体で管理するデータの構造です。

```mermaid
erDiagram
    BOOKS ||--o{ GENRES : "belongs to"
    BOOKS {
        int id PK
        string title
        string author
        int price
        int genre_id FK
    }
    GENRES {
        int id PK
        string name
    }
    USERS {
        string user_id PK
        string password
        string user_name
    }
```
