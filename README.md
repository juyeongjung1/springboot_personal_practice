# Spring Boot 個人演習プロジェクト

## 概要
「Spring Boot入門」テキストを受講した後の理解度アップのための個人演習プロジェクトです。  
テキスト内で学習した内容を基に、ゼロから自力で作成するための演習問題と、その解答サンプルが含まれています。

## プロジェクト構成

### データベースセットアップ
| フォルダ | 説明 |
|---|---|
| `Spring_Sample_DBSET` | テキストサンプル用DB（`spring_sample`）のセットアップスクリプト |
| `Spring_Enshu_DBSET` | 演習用DB（`spring_exercise`）のセットアップスクリプト |

### テキストサンプル （`spring_answer_*`）
テキスト内の各章に対応するSpring Bootサンプルコードです。  
**DB**: `spring_sample`（product, category, userテーブル）

| フォルダ | 章 | 主な学習内容 |
|---|---|---|
| `spring_answer_2` | 第2章 | Controller基礎、リクエストマッピング（GET/POST）、フォーム送信 |
| `spring_answer_3` | 第3章 | Spring Data JPA（CRUD操作）、Repository、Entity、検索メソッド |
| `spring_answer_4` | 第4章 | ログイン認証、セッション管理、バリデーション |
| `spring_answer_5` | 第5章 | Serviceレイヤー（ビジネスロジック分離）、Thymeleaf Layout |
| `spring_answer_6` | 第6章 | テーブル結合（@ManyToOne / @OneToMany）、カテゴリ別検索 |
| `spring_answer_7` | 第7章 | Bootstrap統合、UI改善、総合演習 |

### 演習問題 解答 （`enshu_answer_*`）
テキストの各章に対応する演習問題の解答コードです。  
**DB**: `spring_exercise`（employee, locationテーブル）

| フォルダ | 章 | 主な学習内容 |
|---|---|---|
| `enshu_answer_2` | 第2章 | BMI計算アプリ（Controller基礎、フォーム処理） |
| `enshu_answer_3` | 第3章 | 社員CRUD操作（Spring Data JPA） |
| `enshu_answer_4` | 第4章 | ログイン認証、バリデーション |
| `enshu_answer_5` | 第5章 | Thymeleaf Layout、Service分離 |
| `enshu_answer_6` | 第6章 | 社員-勤務地テーブル結合（@ManyToOne / @OneToMany） |
| `enshu_answer_7` | 第7章 | Bootstrap統合、UI改善 |

## 技術スタック
- **Java**: 17
- **Spring Boot**: 3.1.5 ～ 3.3.7
- **テンプレートエンジン**: Thymeleaf
- **ORM**: Spring Data JPA
- **データベース**: MySQL
- **ビルドツール**: Maven
- **その他**: Lombok, ModelMapper, Bootstrap, Bean Validation

## データベースセットアップ方法
1. MySQLを起動
2. サンプル用DB: `Spring_Sample_DBSET/dbset.bat` を実行
3. 演習用DB: `Spring_Enshu_DBSET/dbset.bat` を実行
