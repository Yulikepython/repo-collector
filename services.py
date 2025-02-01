import requests
from ignore_manager import is_ignored


def get_repo_owner_and_name(repo_url: str):
    """
    GitHubリポジトリURLから (オーナー名, リポジトリ名) を抽出。
    例: "https://github.com/username/repo" -> ("username", "repo")
    """
    repo_url = repo_url.rstrip('/')
    parts = repo_url.split('/')
    if len(parts) < 5:
        raise ValueError("無効なGitHubリポジトリURLです。例: https://github.com/username/repo")
    owner = parts[-2]
    repo = parts[-1]
    return owner, repo


def fetch_repo_files(owner: str, repo: str, path: str, ignore_patterns: list):
    """
    再帰的にリポジトリのファイル一覧を取得する。
    ignore_patternsにマッチするディレクトリやファイルは取得しない。

    GitHub API:
      https://api.github.com/repos/{owner}/{repo}/contents/{path}
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(api_url)
    response.raise_for_status()
    items = response.json()

    all_files = []
    for item in items:
        item_path = item['path']

        # ignoreパターンに一致する場合はスキップ
        if is_ignored(item_path, ignore_patterns):
            continue

        if item['type']=='file':
            all_files.append(item)
        elif item['type']=='dir':
            all_files.extend(fetch_repo_files(owner, repo, item_path, ignore_patterns))
    return all_files


def fetch_file_content(file_info: dict) -> str:
    """
    GitHub APIから取得したファイル情報からdownload_urlを使って内容をダウンロードし返す。
    """
    download_url = file_info.get('download_url')
    if not download_url:
        return ""
    resp = requests.get(download_url)
    resp.raise_for_status()
    return resp.text


def merge_repo_code(repo_url: str, ignore_patterns: list) -> (str, str):
    """
    指定されたGitHubリポジトリURLからすべてのファイルを取得し、
    ファイルごとにコメント行を挿入してまとめた文字列を返す。

    Returns:
        (repo_name, merged_text)
         - repo_name: リポジトリ名(例: "requests")
         - merged_text: すべてのファイル内容をまとめたテキスト
    """
    owner, repo_name = get_repo_owner_and_name(repo_url)
    files = fetch_repo_files(owner, repo_name, "", ignore_patterns)

    merged_chunks = []
    for file_info in files:
        path = file_info.get('path', 'unknown')
        try:
            content = fetch_file_content(file_info)
        except Exception as e:
            print(f"[Warning] {path} の取得に失敗: {e}")
            continue

        merged_chunks.append(f"\n\n# ===== File: {path} =====\n\n{content}")

    return repo_name, "".join(merged_chunks)
