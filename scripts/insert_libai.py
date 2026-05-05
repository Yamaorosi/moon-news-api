# scripts/insert_libai.py
from db.libai_db import get_libai_conn

poems = [
    {
        "title": "静夜思",
        "text": """床前明月光
疑是地上霜
举头望明月
低头思故乡""",
        "dynasty": "唐",
        "theme": "望郷"
    }
]

conn = get_libai_conn()
cur = conn.cursor()

for p in poems:
    cur.execute("""
    INSERT INTO poems (title, text, dynasty, theme)
    VALUES (?, ?, ?, ?)
    """, (p["title"], p["text"], p["dynasty"], p["theme"]))

conn.commit()
conn.close()
