from pypdf import PdfReader

def get_page_numbers(pdf_path, search_terms):
    reader = PdfReader(pdf_path)
    results = {}
    pages_text = [page.extract_text() for page in reader.pages]
    
    for term in search_terms:
        found_page = -1
        for i, text in enumerate(pages_text):
            clean_text = text.replace('\n', '')
            term_clean = term.replace(' ', '')
            if term_clean in clean_text or term in text:
                found_page = i + 1
                break
        results[term] = found_page
    return results

guide_terms = [
    "はじめに",
    "準備：演習環境のセットアップ",
    "1. プロジェクトのインポート（Eclipse）",
    "2. データベースのセットアップ",
    "演習2： Spring Web アプリケーション",
    "課題2.1：「ログイン（トップ画面）」の作成と画面遷移",
    "課題2.2：「書籍管理メニュー画面」の作成",
    "課題2.3：「書籍登録」のモック作成",
    "演習3：Spring Data JPA（データベースとの連携）",
    "データベースのテーブル定義",
    "課題3.1：エンティティクラスの作成",
    "課題3.2：リポジトリインターフェースの作成",
    "課題3.3：Service層の作成",
    "課題3.4：全件一覧と検索モックのDB連動化",
    "課題3.5：書籍詳細画面の実装",
    "課題3.6：新規登録機能の実装",
    "課題3.7：更新機能と削除機能の実装",
    "第4章：入力チェックとログイン認証",
    "課題4.1：入力チェック（Validation）の実装",
    "課題4.2：ユーザー管理用のEntityとRepository作成",
    "課題4.3：ログイン・ログアウト機能の追加",
    "演習5：共通レイアウトの適用とデザインの統一",
    "課題5.1：ライブラリの導入",
    "課題5.2：共通レイアウトの配置確認",
    "課題5.3：全画面へのレイアウト適用",
    "課題5.4：動作確認",
    "課題5.5：ログイン・ログアウトボタンの切り替え",
    "演習6：高度なデータ連携とユーザー体験の向上",
    "課題6.1：検索結果0件時の表示制御",
    "課題6.2：登録画面での動的なジャンル選択",
    "課題6.3：【発展】JPQLを用いた複合検索の実装",
    "課題6.4：【オプション】更新画面への動的リスト適用",
    "第7章： デザインの洗練（Bootstrapの導入）",
    "第7章でよく使う Bootstrap クラス早見表",
    "課題7.1： Bootstrap の導入",
    "課題7.2： ボタンのデザイン統一",
    "課題7.3： フォーム部品の整形",
    "課題7.4： テーブル（書籍一覧）の整形",
    "課題7.5： 全体のレイアウト刷新"
]

spec_terms = [
    "第2章：Spring Web アプリケーション",
    "第3章：Spring Data JPA (DB連携)",
    "第4章：バリデーションと認証",
    "第5章：共通レイアウトの適用",
    "第6章：高度なデータ連携とユーザー体験の向上",
    "第7章：Bootstrapによるスタイリング",
    "データベース構造"
]

print("--- GUIDE ---")
try:
    guide_res = get_page_numbers("docs/Exercise_Guide.pdf", guide_terms)
    for t, p in guide_res.items():
        print(f"{t}|{p}")
except Exception as e:
    print("Error reading guide:", e)

print("--- SPEC ---")
try:
    spec_res = get_page_numbers("docs/Comprehensive_Design_Specification.pdf", spec_terms)
    for t, p in spec_res.items():
        print(f"{t}|{p}")
except Exception as e:
    print("Error reading spec:", e)
