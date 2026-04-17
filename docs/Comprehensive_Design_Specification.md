<style>
  @media print {
    * {
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    @page {
      margin-top: 15mm;
      margin-bottom: 15mm;
      @bottom-center {
        content: "- " counter(page) " -";
        font-family: sans-serif;
        font-size: 10pt;
        color: #666;
      }
    }
  }
</style>
<div align="center" style="margin-top: 100px; margin-bottom: 200px;">
  <img src="images/trainocate_logo.png" width="350">
  <br><br><br>
  <h1 style="border: none; font-size: 2.5em; color: #1a365d;">書籍管理システム 補足資料</h1>
  <h2 style="color: #666; font-weight: 300;">画面遷移・イメージ図・ER図</h2>
  <br><br><br><br><br><br>
</div>
<div style="page-break-before: always;"></div>

<div style="page-break-before: always;"></div>

## 目次

- 第2章：Spring Web アプリケーション（画面遷移とデータ通信） ...... p.2
  - 画面遷移図 ...... p.2
  - 主要画面 ...... p.3
- 第3章：Spring Data JPA (DB連携) ...... p.5
  - 画面遷移図 ...... p.5
  - 主要画面 ...... p.6
- 第4章：バリデーションと認証 ...... p.8
  - 画面遷移図 ...... p.8
  - 主要画面 ...... p.9
- 第5章：共通レイアウトの適用 (Thymeleaf Layout Dialect) ...... p.11
  - 画面遷移図 ...... p.11
  - 主要画面 ...... p.12
- 第6章：高度なデータ連携とユーザー体験の向上 ...... p.14
  - 画面遷移図 ...... p.14
  - 主要画面 ...... p.15
- 第7章：Bootstrapによるスタイリング（完成形態） ...... p.17
  - 画面遷移図 ...... p.17
  - 主要画面 ...... p.18
- データベース構造 (ER図) ...... p.20

<div style="page-break-before: always;"></div>

# 書籍管理システム 補足資料<br><span style="font-size: 0.7em; font-weight: normal;">（画面遷移・イメージ図・ER図）</span>

本ドキュメントは、個人演習の補足資料です。演習を進めるにあたり、各章ごとの最終的な完成形（画面遷移や各画面のイメージ図）とデータベースの構造（ER図）を確認するためのリファレンスとして活用してください。

---

<div style="page-break-before: always;"></div>

## 第2章：Spring Web アプリケーション（画面遷移とデータ通信）

<div style="background-color: #e9f5ff; border-left: 5px solid #007bff; padding: 15px; margin-bottom: 20px; border-radius: 5px;">
  <strong>【テーマ】モックデータによる画面遷移の確立</strong><br><br>
  この段階ではデータベースを使用せず、Controller内で作成した固定データ（モック）を使用して画面表示と遷移を確認します。
</div>

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

<div style="page-break-before: always;"></div>

### 主要画面

| ログイン画面（モック：DB認証なしでの遷移テスト） | メニュー画面（モック：主要機能への導線確認） |
| :---: | :---: |
| ![Login](images/ch2_login_page_zoom1_5_1775531127831.png) | ![Menu](images/ch2_menu_page_zoom1_5_1775531151398.png) |

| 登録フォーム（入力値の受け渡しテスト用） | 登録内容の確認画面（入力値と遷移の妥当性確認） |
| :---: | :---: |
| ![Registration Form](images/ch2_registration_form_1775532568369.png) | ![Confirm](images/ch2_confirmation_page_zoom1_5_1775531182266.png) |

| 書籍一覧（モックデータによる一覧表示の確認） | 検索結果画面（固定データによる表示レイアウトの確認） |
| :---: | :---: |
| ![List](images/ch2_list_page_zoom1_5_1775531152394.png) | ![Search Result Mock](images/ch2_search_result_mock_zoom1_5_1775531187711.png) |

---

<div style="page-break-before: always;"></div>

## 第3章：Spring Data JPA (DB連携) 

<div style="background-color: #e9f5ff; border-left: 5px solid #007bff; padding: 15px; margin-bottom: 20px; border-radius: 5px;">
  <strong>【テーマ】データの永続化（DBとの接続）</strong><br><br>
  モックデータを卒業し、MySQLデータベースと連携します。第2章で作成した検索機能も、実際にDBからデータを取得するように実装します。
</div>

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

<div style="page-break-before: always;"></div>

### 主要画面

| メニュー画面（DBからデータを取得する検索機能の実装） | 書籍一覧（MySQLから取得したデータの表示確認） |
| :---: | :---: |
| ![Menu Fixed](images/ch3_menu_screen_fixed_1775532678571.png) | ![List](images/ch3_book_list_plain_1775540092670.png) |

| 個別情報の詳細表示（DBからの特定ID取得の検証） | 登録・更新完了画面（DB書き換えの成功報告） |
| :---: | :---: |
| ![Detail](images/ch3_detail_png_1775531308770.png) | ![Confirm](images/ch3_confirm_png_1775531334365.png) |

| 編集フォーム（DB情報の初期表示・変更確認） | タイトル検索結果（DBの部分一致検索の確認） |
| :---: | :---: |
| ![Update](images/ch3_update_png_1775531339324.png) | ![Search Results](images/ch3_search_result_plain_1775540104659.png) |

---

<div style="page-break-before: always;"></div>

## 第4章：バリデーションと認証

<div style="background-color: #e9f5ff; border-left: 5px solid #007bff; padding: 15px; margin-bottom: 20px; border-radius: 5px;">
  <strong>【テーマ】入力チェックとセキュリティの基本</strong><br><br>
  不正な入力を防ぐバリデーション機能と、セッションを利用した認証機能を実装します。
</div>

### 画面遷移図
```mermaid
graph TD
    Login[ログイン画面] -- 認証成功 --> Menu[メニュー画面]
    Login -- 認証失敗 --> LoginErr[ログイン画面（エラー表示）]
    Menu --> Form[書籍登録フォーム]
    Form -- 入力不備あり --> FormErr[登録フォーム（バリデーションエラー）]
    Form -- 正常入力 --> Confirm[登録・更新完了]
```

<div style="page-break-before: always;"></div>

### 主要画面

| ログイン認証失敗（意図したエラーメッセージの表出） | 入力チェックエラー（アノテーションによる不備検知） | メニュー画面（セッションから取得したユーザー情報の表示） |
| :---: | :---: | :---: |
| ![Login Error](images/ch4_login_error_zoom1_5.png) | ![Validation Error](images/ch4_validation_errors_zoom1_5.png) | ![Ch4 Menu With Session](images/ch4_book_index_zoom1_5.png) |

---

<div style="page-break-before: always;"></div>

## 第5章：共通レイアウトの適用 (Thymeleaf Layout Dialect)

<div style="background-color: #e9f5ff; border-left: 5px solid #007bff; padding: 15px; margin-bottom: 20px; border-radius: 5px;">
  <strong>【テーマ】保守性の向上とデザインの統一</strong><br><br>
  ヘッダーやフッターを共通パーツ化し、すべての画面で統一された外観を実現します。
</div>

### 画面遷移図
```mermaid
graph TD
    Component[共通レイアウト定義] --> PageA[書籍一覧]
    Component --> PageB[登録フォーム]
    subgraph 共通レイアウト
        Header[ヘッダーパーツ]
        Footer[フッターパーツ]
    end
```

<div style="page-break-before: always;"></div>

### 主要画面

| ログイン画面（共通レイアウト適用：未ログイン状態） | 書籍一覧（共通レイアウト適用：ログイン中ヘッダー表示） |
| :---: | :---: |
| ![Ch5 Login](images/ch5_login_page_design_check.png) | ![Ch5 List](images/ch5_book_list_design_check.png) |

| 登録・更新画面（共通レイアウトによる画面デザインの統一） |
| :---: |
| ![Ch5 Form](images/ch5_book_form_design_check.png) |

---

<div style="page-break-before: always;"></div>

## 第6章：高度なデータ連携とユーザー体験の向上

<div style="background-color: #e9f5ff; border-left: 5px solid #007bff; padding: 15px; margin-bottom: 20px; border-radius: 5px;">
  <strong>【テーマ】動的な項目取得（ジャンル連携）と0件制御・JPQL検索</strong><br><br>
  検索結果が0件の場合のメッセージ表示（0件制御）や、DBから取得したジャンル一覧をセレクトボックスとしてフォームに動的に反映させる機能を実装します。また、Repository層でJPQLを活用し、ジャンル名と価格による高度な複合検索を可能にします。
</div>

### 画面遷移図
```mermaid
graph LR
    Menu --> SearchTitle[タイトル検索]
    Menu --> SearchPrice[価格帯検索]
    Menu --> SearchComplex["複合検索<br/>(ジャンル × 上限価格)"]
    SearchTitle --> Results[検索結果一覧]
    SearchPrice --> Results
    SearchComplex --> Results
```

<div style="page-break-before: always;"></div>

### 主要画面

| 登録フォーム（DBから動的に抽出したジャンル選択） | 検索結果（該当データなし：UX向上のための0件案内） |
| :---: | :---: |
| ![Genre Select](images/ch6_book_form_genre_zoom1_5.png) | ![Search No Results](images/ch6_search_no_hits_zoom1_5.png) |

| 複合検索フォーム（ジャンル名：プログラミング、上限価格：5000を指定） | JPQLによる複合検索結果（ジャンル：プログラミング、上限価格：5000） |
| :---: | :---: |
| ![JPQL Search Form](images/ch6_jpql_search_form_zoom1_5.png) | ![JPQL Search Result](images/ch6_jpql_search_result_zoom1_5.png) |

---

<div style="page-break-before: always;"></div>

## 第7章：Bootstrapによるスタイリング（完成形態）

<div style="background-color: #e9f5ff; border-left: 5px solid #007bff; padding: 15px; margin-bottom: 20px; border-radius: 5px;">
  <strong>【テーマ】モダンなUIデザインの導入とUXの完成</strong><br><br>
  人気フレームワーク「Bootstrap 5」を導入し、デザインをプロフェッショナルな外観へ刷新しました。共通レイアウト（NavbarやContainer）の適用により、一貫性のあるレスポンシブなユーザー体験を提供します。
</div>

### 画面遷移図
```mermaid
graph LR
    Login[Bootstrapログイン] -- 認証成功 --> Menu[カード型メニュー]
    Menu -- 全書籍リストの確認 --> List[ストライプテーブル]
    Menu -- 検索 --> Search[検索結果]
    Menu -- 新規登録 --> Form[入力カード]
    List -- 選択 --> Detail[書籍詳細画面]
    Detail -- 編集 --> Update[編集カード]
    Form -- 完了 --> Confirm[成功アラート表示]
    Update -- 完了 --> Confirm
    Confirm -- 戻る --> Menu
```

<div style="page-break-before: always;"></div>

### 主要画面

| ログイン画面（グリッドシステムによる中央配置とalert表示の統合） | メニュー画面（cardクラスとg-4による機能のカード型レイアウト） |
| :---: | :---: |
| ![Final Login](images/ch7_login_standard.png) | ![Final Menu](images/ch7_menu_standard.png) |

| 書籍一覧画面（table-striped、table-hover、table-darkの適用による視認性向上） | 書籍詳細画面（container内での整理されたデータ表示とアクションボタン） |
| :---: | :---: |
| ![Final List](images/ch7_list_standard.png) | ![Final Detail](images/ch7_detail_standard.png) |

| 書籍登録フォーム（form-controlとform-selectによるモダンな入力体験） | 書籍更新フォーム（既存データの編集とレイアウトの完全な統一） |
| :---: | :---: |
| ![Final Form](images/ch7_form_standard.png) | ![Final Update](images/ch7_update_standard.png) |

| 登録・更新完了画面（操作の成功を知らせる明示的な通知レイアウト） | 検索結果画面（該当なし：alert-infoクラスによる親切な0件案内） |
| :---: | :---: |
| ![Final Confirm](images/ch7_confirm_standard.png) | ![Final No Results](images/ch7_search_no_hits_standard.png) |

---

<div style="page-break-before: always;"></div>

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
        int user_id PK
        string password
        string user_name
    }
```
