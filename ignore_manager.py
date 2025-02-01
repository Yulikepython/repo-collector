import os
import fnmatch

# ここで「デフォルトで無視したい拡張子」を定義しておく
DEFAULT_IGNORE_EXTENSIONS = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".pdf",
    ".zip",
    ".exe",
    # 必要に応じて追加
]

def load_ignore_patterns(ignore_file: str = ".collectignore") -> list:
    """
    .collectignore に記載された無視パターンをリストとして返す。
    ファイルが存在しない場合は空リストを返す。
    加えて、DEFAULT_IGNORE_EXTENSIONS も無視パターンとして自動的に追加する。
    """
    patterns = []

    # ユーザ定義の .collectignore があれば読み込む
    if os.path.exists(ignore_file):
        with open(ignore_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 空行やコメント(#)行は無視
                if not line or line.startswith('#'):
                    continue
                patterns.append(line)

    # デフォルト拡張子を ignore パターンとして追加 (例: *.png, *.jpg, ...)
    for ext in DEFAULT_IGNORE_EXTENSIONS:
        pattern = f"*{ext}"  # 例: "*.png"
        if pattern not in patterns:  # 重複登録を防ぐ
            patterns.append(pattern)

    return patterns


def is_ignored(path: str, patterns: list) -> bool:
    """
    渡されたパスが、ignoreパターンのいずれかにマッチしたらTrueを返す。
    fnmatchを使用してワイルドカードマッチングを行う。
    例:
        patterns = ["dist/", "*.pyc", ".DS_Store", "*.png", ...]
        path = "dist/setup.py" -> True
        path = "setup.pyc" -> True
        path = "images/logo.png" -> True
        path = "src/main.py" -> False
    """
    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False
