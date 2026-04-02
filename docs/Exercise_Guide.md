# Spring Boot 個人演習ガイド：書籍管理システム

## はじめに
本演習は、Spring Boot入門の研修終了翌日に、1日かけて取り組む総合演習です。
テキストで学習した順序に沿って「書籍管理システム」の機能を少しずつ作成・拡張していきます。最終的には、CRUD操作からログイン機能までを備えたWebアプリケーションが完成します。

---

## 演習2： Spring Web アプリケーション（画面遷移とデータ通信）

**【学習のねらい】**
第2章の知識（Controller、GET/POST、Formクラス、Model）を使って、書籍管理システムの「UI（画面）」と「Java側へのデータ送信」のモック（仮動作）を作成します。データベースへの保存・検索は次章で行うため、本章では**「入力したデータが画面遷移後に正しく表示されるか」**を確認します。

### 課題2.1：「ログイン（トップ画面）」の作成と画面遷移
プロジェクト実行時にシステム入り口となる「ログイン画面」を作り、特定の画面へ遷移する処理を作成しましょう。

1. `jp.co.trainocate.book.controller` パッケージを作成し、`LoginController` クラスを作成してください。これに `@Controller` アノテーションを付与します。
2. URL `http://localhost:8080/` にアクセスした際、`index.html` を返すように GET マッピングのメソッドを作成してください。
3. `src/main/resources/templates` の中に `index.html` （ログイン画面のHTMLファイル）を作成し、ページタイトルを「ログイン（書籍管理システム）」としてください。
4. `index.html` 内に、以下の構成でログイン用の `<form>` を作成してください。
   - 送信先（action）：`/login`
   - 送信方法（method）：`POST`
   - 入力項目：ユーザID（`name`属性を `userId` にする）、パスワード（`name`属性を `password` にする）
   - 送信ボタン：「ログイン」
5. `LoginController` に `/login` を受け取る POST マッピングのメソッドを作成し、引数で `userId` と `password` を受け取るようにしてください（第2章では認証処理のモックとして、受け取るだけで次に進みます）。
6. このメソッドの遷移先として、リダイレクトはさせずに、直接 `book_index.html` へ画面遷移するようにし、この後作成する「書籍管理メニュー画面」へそのまま移動させます。

### 課題2.2：「書籍管理メニュー画面」の作成 (リンクと検索モック)
ログイン成功後に表示される「書籍管理メニュー画面（`book_index.html`）」を作成し、他機能へのリンクや検索フォームを配置します。

1. `BookController` クラスを作成（`@Controller`付与）し、`/book/index` に対するGETマッピングを用意して、画面 `book_index.html` を返すようにします。
2. `src/main/resources/templates` の中に `book_index.html` （メニュー画面のHTMLファイル）を作成し、まず以下の2つのリンクを配置してください。
   - ①「全書籍リストの確認」への遷移リンク
   - ②「書籍情報の登録」への遷移リンク
   - **【ヒント】** Thymeleafを用いたリンクの作成方法は、5章を参照してください。書き方は以下のようになります。
     `<a th:href="@{/book/list}">全書籍リストの確認</a>`

3. ①のリンク先として動作させるため、`BookController` に `/book/list` のGETマッピングを追加し、遷移先の `book_list.html` （書籍リスト画面のHTMLファイル）を作成してください。この画面はモックとして「書籍一覧画面（※本来はここに本の一覧が出ます。第3章で作成します）」といった文言のみ表示しておいてください。

4. 再び `book_index.html` の中に戻り、以下の2つの検索用の `<form>` を作成してください。すべて `GET` メソッドで送信します。
   - **① 書籍名検索フォーム**：
     - 入力項目：テキストボックス（`name`属性を `keyword` にする）
     - 送信先（action）：`/book/search/title`
     - 送信ボタン：「タイトルで検索」
   - **② 価格検索フォーム**：
     - 入力項目：最低価格の数値（`name`属性を `minPrice` にする）、最高価格の数値（`name`属性を `maxPrice` にする）
     - 送信先（action）：`/book/search/price`
     - 送信ボタン：「価格帯で検索」

5. `BookController` に上記の検索用送信先（`/book/search/title`、`/book/search/price`）に対応するメソッドを作成してください。
6. Controllerの引数でそれぞれ送信されたパラメータを受け取り、`Model` に格納してください。
7. 遷移先の画面として、`src/main/resources/templates` の中に `book_search_result.html` （検索結果表示のHTMLファイル）を作成し、以下のように受信データを表示してください（Thymeleafの `${}` を使用）。
   - **出力する内容①のとき**：「検索条件：タイトルに『〇〇』が含まれる書籍」
   - **出力する内容②のとき**：「検索条件：価格が『〇〇』円〜『〇〇』円の書籍」
   ※実際の検索結果一覧を表示するのは第3章で実装します。

### 課題2.3：「書籍登録」のモック作成 (POST通信とFormクラス)
画面のリンクから登録画面へ遷移し、Formクラスを使って一括でデータを受け取る練習をします。

1. `jp.co.trainocate.book.form` パッケージを作成し、`BookForm` クラスを作成してください。
2. フィールドとして `title` (String)、`author` (String)、`price` (Integer) を用意し、Lombokの `@Data` を付けてください。
3. `BookController` に `/book/form` 用の GET マッピングを作成し、遷移先の `book_form.html` （書籍登録用HTMLファイル）を作成して入力画面を作ってください。
   - （※この画面は、課題2.2で作成した「書籍情報の登録」リンクから遷移してきます）
   - フォームの 送信先(action): `/book/register`、 method: `POST` 
   - 入力項目は、Formクラスのプロパティに合わせて `name`属性を `title`、`author`、`price` に設定してください。
4. `BookController` に `/book/register` 向けの POST マッピングメソッドを作成してください。
5. 引数に `BookForm` を指定してデータを受け取り、受け取ったFormオブジェクトをそのまま `Model` に格納してください。
6. 遷移先画面として `book_confirm.html` （登録完了画面のHTMLファイル）を作成し、「以下の内容で登録を受け付けました（※実際のDB保存は次章で実装します）」というメッセージと共に、入力されたタイトル・著者名・価格を表示してください。

---

## 演習3：Spring Data JPA（データベースとの連携）

**【学習のねらい】**
第3章の知識（Entity、Repository、Service、CRUD）と、一部の5・6章知識を使って、DBと連動する完全な書籍管理機能を作成します。

### データベースのテーブル定義

本システムでは、以下の3つのテーブルを使用します。エンティティを定義する際の参考にしてください。

**■ genre テーブル（ジャンル）**

| 列名 | データ型 | 制約 | 備考 |
|---|---|---|---|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | ジャンルID |
| name | VARCHAR(50) | NOT NULL | ジャンル名 |

**■ book テーブル（書籍）**

| 列名 | データ型 | 制約 | 備考 |
|---|---|---|---|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 書籍ID |
| title | VARCHAR(255) | NOT NULL | 書籍名 |
| author | VARCHAR(100) | NOT NULL | 著者名 |
| price | INT | NOT NULL | 価格 |
| genre_id | INT | FOREIGN KEY → genre(id) | ジャンルID（外部参照） |

**■ user テーブル（ユーザ）** ※第4章で使用

| 列名 | データ型 | 制約 | 備考 |
|---|---|---|---|
| user_id | INT(6) | PRIMARY KEY | ユーザID |
| password | VARCHAR(255) | NOT NULL | パスワード |
| user_name | VARCHAR(50) | NOT NULL | ユーザ名 |

> **【注意】** book テーブルの `genre_id` は、genre テーブルの `id` を参照する**外部キー**です。
> エンティティ定義時にJPAのリレーションアノテーション（`@ManyToOne` / `@OneToMany`）を使って関連付ける必要があります（テキスト **第6章** 参照）。

### 課題3.1：エンティティクラスの作成
データベースのテーブルに対応するEntityクラスを作成しましょう。

1. `jp.co.trainocate.book.entity` パッケージを作成してください。
2. 上記の **genre テーブル** に対応する `Genre` エンティティクラスを作成してください。
   - `@Entity`、`@Data`（Lombok）、`@Table(name = "genre")` を付与します。
   - 各フィールドに `@Id`、`@GeneratedValue`、`@Column` 等の適切なアノテーションを付けてください。
   - **【6章の内容】** 1つのジャンルに対して複数の書籍が紐づきます。`@OneToMany(mappedBy = "genre")` を使い、`List<Book>` 型のフィールドを追加してください。
3. 上記の **book テーブル** に対応する `Book` エンティティクラスを作成してください。
   - `@Entity`、`@Data`（Lombok）、`@Table(name = "book")` を付与します。
   - 各フィールドに適切なアノテーションを付けてください。
   - **【6章の内容】** 複数の書籍は1つのジャンルに属します。以下の2つのフィールドを定義してください。
     - `@ManyToOne` と `@JoinColumn` を使って `Genre` 型のフィールド（ジャンルオブジェクト）を定義
     - `@Column(name = "genre_id")` を使って `Integer` 型のフィールド（ジャンルIDの値そのもの）を定義

### 課題3.2：リポジトリインターフェースの作成
エンティティに対するデータベース操作を行うRepositoryを定義しましょう。
これから実装する機能（全件取得、キーワード検索、価格帯検索、IDでの1件検索、登録・更新・削除）を踏まえ、リポジトリを作成します。

1. `jp.co.trainocate.book.repository` パッケージを作成してください。
2. `BookRepository` インターフェース（`JpaRepository<Book, Integer>`を継承）を作成してください。
3. 以下の検索に必要なメソッドを、**メソッド命名規則**（テキスト第3章）に従って定義してください。
   - タイトルに特定の文字列を含む書籍を検索するメソッド（`findByTitleContaining`）
   - 価格が指定範囲内の書籍を検索するメソッド（`findByPriceBetween`）
   ※全件取得(findAll)、IDでの1件取得(findById)、保存(save)、削除(deleteById)はJpaRepositoryに標準で存在するため自作不要です。
4. `GenreRepository` インターフェース（`JpaRepository<Genre, Integer>`を継承）を作成してください。

### 課題3.3：Service層の作成
RepositoryをControllerから直接呼ばず、Service層を介してアクセスするようにします。
本構成は、テキスト第3章の末尾にも登場する実践的な設計パターンです。

1. `jp.co.trainocate.book.service` パッケージを作成してください。
2. 以下のメソッドを定義したインターフェース `BookService` を作成してください。
   - `List<Book> findAllProducts()`
   - `Book findProductById(Integer id)`
   - `List<Book> findProductsByTitle(String title)`
   - `List<Book> findProductsByPrice(Integer minPrice, Integer maxPrice)`
   - `Book saveProduct(BookForm bookForm)`
   - `void deleteProduct(Integer id)`
3. `BookService` を実装した `BookServiceImpl` クラスを作成してください。
   - クラスに `@Service` と `@RequiredArgsConstructor` (または `@Autowired`) を付けます。
   - `BookRepository` をDIし、各メソッドの中でリポジトリの該当処理を呼び出すようにオーバーライド（実装）してください。

### 課題3.4：全件一覧と検索モックのDB連動化
第2章で作ったモック画面を、Serviceを経由してDBから取得するように修正します。

1. `BookController` に `BookService` を `@Autowired` でDIしてください。
2. `/book/list` メソッドを修正し、`BookService.findAllProducts()` を呼び出して全件リストを取得し、`Model` に渡します。
3. `/book/search/title` および `/book/search/price` メソッドを修正し、それぞれServiceから検索結果リストを取得して `Model` に渡します。
4. `book_list.html` と `book_search_result.html` を改修し、Thymeleaf の `th:each` を用いて、書籍を一覧表（ID、書籍名、著者名、価格、ジャンル名）で表示するようにしてください。
   - **【重要（動的URL）】** 一覧の「書籍名」部分をリンクにし、クリックすると「詳細画面」へ飛ぶようにします。テキスト第5章を参考に、以下のような**動的URL**にしてください。
     `<a th:href="@{/book/detail/{id}(id=${book.id})}" th:text="${book.title}"></a>`

### 課題3.5：書籍詳細画面の実装（更新・削除の起点）
書籍名をクリックしたときに表示される詳細画面を作成します。この画面から「更新」と「削除」を行えるようにします。

1. `BookController` に、動的URL `/book/detail/{id}` を受け取る GET マッピングメソッドを作成してください。（`@PathVariable` を使います）
2. Serviceの `findProductById(id)` を使って対象の書籍を1件取得し、`Model` に格納してください。
3. 詳細画面 `book_detail.html` を作成し、ID、書籍名、著者名、価格、ジャンル名を表示してください。
4. この画面内に以下の2つのリンク（ボタン）を配置してください。
   - `更新` （遷移先: `/book/update/{id}` へ GET メソッドで遷移）
   - `削除` （遷移先: `/book/delete/{id}` へ GET または POST で遷移）

### 課題3.6：更新機能と削除機能の実装
詳細画面から呼び出される更新と削除の実装を行います。

1. **更新画面の表示**
   - `BookController` に `/book/update/{id}` を受け取る GET マッピングを追加してください。
   - DBから `id` で書籍を取得し、その値を保持した状態で入力・更新ができるフォーム画面 `book_update.html` へ遷移させます。
   ※第3章の段階では、ジャンルの変更は考慮せず、タイトル・著者・価格の更新のみで構いません。
2. **更新と登録の統合（saveメソッドの活用）**
   - JPAの `save()` メソッドは、「オブジェクトにIDがセットされている場合はUPDATE、Nullの場合はINSERT」という動きをします。
   - `/book/register`（または統合した `/book/save`）の POST マッピングで、フォームから `id` が送られてきたらそれを Entity にセットしてから `save()` を実行することで、登録・更新の両方を1つのメソッドで処理できます。
3. **削除の実行**
   - `BookController` に `/book/delete/{id}` を受け取るメソッドを追加し、Serviceの `deleteProduct(id)` を呼び出します。
   - 削除完了後は、全件リスト（`/book/list`）へ**リダイレクト**するようにしてください。
