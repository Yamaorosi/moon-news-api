import json
import os
from db.libai_db import get_libai_conn, init_libai_db


# JSONファイルの場所
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
JSON_PATH = os.path.join(ROOT_DIR, "data", "libai.json")


def load_poems():
    """
    1. JSONファイルを読み込む関数
    """
    # 指定したパスにファイルがあるかチェック
    if not os.path.exists(JSON_PATH):
        raise FileNotFoundError(f"JSONが見つからないよ: {JSON_PATH}")

    # ファイルを開いて、中身をPythonで扱える「リスト/辞書形式」に変換して返す
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def insert_poems():
    """
    2. DBへのテーブル作成とデータ投入を行う関数
    """
    # DBのテーブルがなければ作成する（初期化）
    init_libai_db()

    # JSONからデータをロード
    poems = load_poems()
    
    # DBに接続してカーソルを取得
    conn = get_libai_conn()
    cur = conn.cursor()

    # リストを1つずつループで処理
    for p in poems:
        # DBに保存。IDが重複していたら無視（IGNORE）して次へ行く
        cur.execute("""
        INSERT OR IGNORE INTO poems (id, title, data)
        VALUES (?, ?, ?)
        """, (
            p["id"],
            p["title"],
            # 辞書データを文字列(JSON)に変換。日本語をそのまま保存。
            json.dumps(p, ensure_ascii=False)
        ))

    # 変更を保存して、接続を閉じる
    conn.commit()
    conn.close()

if __name__ == "__main__":
    try:
        insert_poems()
        print("✔ libai.json をDBに投入完了")
    except Exception as e:
        print(f"❌ 失敗: {e}")
