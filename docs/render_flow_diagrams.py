"""補足資料用の画面遷移図を Mermaid CLI で PNG にレンダリングする。"""

from pathlib import Path
import json
import shutil
import subprocess
import tempfile

from PIL import Image, ImageChops


DIAGRAMS = {
    "flow_ch2.png": """
graph LR
    Login[ログイン画面] -- ログイン --> Menu[メニュー画面]
    Menu -- 全書籍リストの確認 --> List[書籍一覧]
    Menu -- 検索 --> Search[検索結果]
    Menu -- 書籍情報の登録 --> Form[書籍登録フォーム]
    Form -- 登録 --> Confirm[登録確認画面]
    Confirm -- メニューに戻る --> Menu
""",
    "flow_ch3.png": """
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
""",
    "flow_ch4.png": """
graph TD
    Login[ログイン画面] -- 認証成功 --> Menu[メニュー画面]
    Login -- 認証失敗 --> LoginErr[ログイン画面<br>（エラー表示）]
    Menu --> Form[書籍登録フォーム]
    Form -- 入力不備あり --> FormErr[登録フォーム<br>（エラー表示）]
    Form -- 正常入力 --> Confirm[登録・更新完了]
""",
    "flow_ch5.png": """
graph TD
    Component[共通レイアウト定義] --> PageA[書籍一覧]
    Component --> PageB[登録フォーム]
    subgraph 共通レイアウト
        Header[ヘッダーパーツ]
        Footer[フッターパーツ]
    end
""",
    "flow_ch6.png": """
graph LR
    Menu[メニュー画面] --> SearchTitle[タイトル検索]
    Menu --> SearchPrice[価格帯検索]
    Menu --> SearchComplex[複合検索<br>ジャンル × 上限価格]
    SearchTitle --> Results[検索結果一覧]
    SearchPrice --> Results
    SearchComplex --> Results
""",
    "flow_ch7.png": """
graph TD
    Login[Bootstrapログイン] -- 認証成功 --> Menu[カード型メニュー]
    Menu -- 全書籍リストの確認 --> List[ストライプテーブル]
    Menu -- 検索 --> Search[検索結果]
    Menu -- 新規登録 --> Form[入力カード]
    List -- 選択 --> Detail[書籍詳細画面]
    Detail -- 編集 --> Update[編集カード]
    Form -- 完了 --> Confirm[成功アラート表示]
    Update -- 完了 --> Confirm
    Confirm -- 戻る --> Menu
""",
}


MERMAID_CONFIG = {
    "theme": "base",
    "securityLevel": "loose",
    "flowchart": {
        "htmlLabels": True,
        "curve": "basis",
        "nodeSpacing": 46,
        "rankSpacing": 58,
    },
    "themeVariables": {
        "fontFamily": "BIZ UDGothic, Meiryo, sans-serif",
        "primaryColor": "#ffffff",
        "primaryTextColor": "#123a5f",
        "primaryBorderColor": "#b8cad9",
        "lineColor": "#2f6f9f",
        "secondaryColor": "#e9f5ff",
        "tertiaryColor": "#f7fafc",
        "edgeLabelBackground": "#f4f7fb",
        "clusterBkg": "#f4f7fb",
        "clusterBorder": "#c8d5e3",
    },
}


def trim_white_margin(image_path: Path, padding: int = 36) -> None:
    image = Image.open(image_path).convert("RGB")
    background = Image.new("RGB", image.size, "white")
    diff = ImageChops.difference(image, background)
    bbox = diff.getbbox()
    if not bbox:
        return

    left, top, right, bottom = bbox
    cropped = image.crop((left, top, right, bottom))
    framed = Image.new(
        "RGB",
        (cropped.width + padding * 2, cropped.height + padding * 2),
        "white",
    )
    framed.paste(cropped, (padding, padding))
    framed.save(image_path)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    out_dir = base_dir / "images" / "flows"
    out_dir.mkdir(parents=True, exist_ok=True)
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not npx:
        raise RuntimeError("npx が見つかりません。Node.js / npm のインストールを確認してください。")

    with tempfile.TemporaryDirectory() as tmp_name:
        tmp_dir = Path(tmp_name)
        config_path = tmp_dir / "mermaid_config.json"
        config_path.write_text(json.dumps(MERMAID_CONFIG, ensure_ascii=False), encoding="utf-8")

        for filename, source in DIAGRAMS.items():
            input_path = tmp_dir / f"{Path(filename).stem}.mmd"
            output_path = out_dir / filename
            input_path.write_text(source.strip() + "\n", encoding="utf-8")

            subprocess.run(
                [
                    npx,
                    "-y",
                    "@mermaid-js/mermaid-cli",
                    "-i",
                    str(input_path),
                    "-o",
                    str(output_path),
                    "-c",
                    str(config_path),
                    "-b",
                    "white",
                    "-s",
                    "2",
                ],
                check=True,
            )
            trim_white_margin(output_path)
            print(output_path)


if __name__ == "__main__":
    main()
