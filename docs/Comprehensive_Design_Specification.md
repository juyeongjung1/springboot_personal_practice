# 書籍管理システム 全体設計書

本ドキュメントは、演習を通してシステムをどのように構築していくかをまとめた正式な設計書です。各章のマイルストーンごとに、画面遷移と最終的な画面イメージを確認できます。

---

## 第2章：Spring Web アプリケーション（画面遷移とデータ通信）
**テーマ：モックデータによる画面遷移の確立**

この段階ではデータベースを使用せず、Controller内で作成した固定データ（モック）を使用して画面表示と遷移を確認します。

### 画面遷移図
```mermaid
graph LR
    Login[ログイン画面] -- ログイン --> Menu[メニュー画面]
    Menu -- 全書籍リストの確認 --> List[書籍一覧]
    Menu -- 検索 --> Search[検索結果]
    Menu -- 書籍情報の登録 --> Form[書籍登録フォーム]
    Form -- 登録 --> Confirm[登録確認画面]
    Confirm -- メニューに戻る --> Menu
```

### 主要画面
| ログイン画面 | メニュー画面（検索フォームあり） |
| :---: | :---: |
| ![Login](images/ch2_login_page_zoom1_5_1775531127831.png) | ![Menu](images/ch2_menu_page_zoom1_5_1775531151398.png) |

| 書籍登録フォーム | 登録確認画面 |
| :---: | :---: |
| ![Registration Form](images/ch2_registration_form_1775532568369.png) | ![Confirm](images/ch2_confirmation_page_zoom1_5_1775531182266.png) |

| 書籍一覧画面 | 検索結果（表示例） |
| :---: | :---: |
| ![List](images/ch2_list_page_zoom1_5_1775531152394.png) | ![Search Result Mock](images/ch2_search_result_mock_zoom1_5_1775531187711.png) |

---

## 第3章：Spring Data JPA (DB連携) 
**テーマ：データの永続化（DBとの接続）**

モックデータを卒業し、MySQLデータベースと連携します。第2章で作成した検索機能も、実際にDBからデータを取得するように実装します。

### 画面遷移図
```mermaid
graph LR
    Menu[メニュー画面] --> List[書籍一覧]
    Menu --> Form[書籍登録フォーム]
    Menu --> Search[検索結果一覧]
    List -- 選択 --> Detail[書籍詳細画面]
    Detail -- 編集 --> Update[書籍更新フォーム]
    Detail -- 削除 --> List
    Form -- 登録 --> Confirm[登録・更新完了]
    Update -- 更新 --> Confirm
    Confirm -- メニューに戻る --> Menu
```

### 主要画面
| メニュー画面（検索フォームあり） | 書籍一覧画面 |
| :---: | :---: |
| ![Menu Fixed](images/ch3_menu_screen_fixed_1775532678571.png) | ![List](images/ch3_book_list_plain_1775540092670.png) |

| 書籍詳細画面 | 登録・更新完了画面 |
| :---: | :---: |
| ![Detail](images/ch3_detail_png_1775531308770.png) | ![Confirm](images/ch3_confirm_png_1775531334365.png) |

| 更新フォーム | 検索結果画面 |
| :---: | :---: |
| ![Update](images/ch3_update_png_1775531339324.png) | ![Search Results](images/ch3_search_result_plain_1775540104659.png) |

---

## 第4章：バリデーションと認証
**テーマ：入力チェックとセキュリティの基本**

不正な入力を防ぐバリデーション機能と、セッションを利用した認証機能を実装します。

### 画面遷移図
```mermaid
graph TD
    Login[ログイン画面] -- 認証成功 --> Menu[メニュー画面]
    Login -- 認証失敗 --> LoginErr[ログイン画面（エラー表示）]
    Menu --> Form[書籍登録フォーム]
    Form -- 入力不備あり --> FormErr[登録フォーム（バリデーションエラー）]
    Form -- 正常入力 --> Confirm[登録・更新完了]
```

### 主要画面
| ログインエラー表示 | バリデーションエラー（赤字表示） |
| :---: | :---: |
| ![Login Error](images/ch4_login_error_1775531487990.png) | ![Validation Error](images/ch4_validation_errors_1775531544781.png) |

---

## 第5章：共通レイアウトの適用 (Thymeleaf Layout Dialect)
**テーマ：保守性の向上とデザインの統一**

ヘッダーやフッターを共通パーツ化し、すべての画面で統一された外観を実現します。

### 画面遷移図
```mermaid
graph TD
    Component[共通レイアウト定義] --> PageA[書籍一覧]
    Component --> PageB[登録フォーム]
    subgraph Shared Layout
        Header[ヘッダーパーツ]
        Footer[フッターパーツ]
    end
```

### 主要画面
| 共通レイアウト適用後の書籍一覧 |
| :---: |
| ![Common Layout](images/ch5_layout_header_content_1775530050363.png) |

---

## 第6章：リレーション（1対多）と検索機能
**テーマ：テーブル結合と動的クエリ**

「ジャンル」テーブルとの結合により、書籍にジャンル名を付与します。また、キーワード検索機能を実装します。

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
| ![Genre Select](images/ch6_genre_select_box_1775530168540.png) | ![Search Results](images/ch6_search_result_no_criteria_1775540253533.png) |

---

## 第7章：Bootstrapによるスタイリング（完成形態）
**テーマ：モダンなUIデザインの導入**

人気フレームワーク「Bootstrap 5」を導入し、デザインを刷新します。

### 画面遷移図
```mermaid
graph LR
    Login[Bootstrapログイン] --> Menu[カード型メニュー]
    Menu --> List[ストライプテーブル]
    Menu --> Form[入力カード]
```

### 主要画面
| メニュー（カードデザイン） | 検索結果画面 |
| :---: | :---: |
| ![Final Menu](images/ch7_index_menu_1775530275046.png) | ![Final Search Results](images/ch7_search_result_bootstrap_1775540370341.png) |

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
