#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
repo-collector
--------------
GitHubの指定リポジトリからコードを取得して、1つのテキストファイルにまとめるツール。

[Usage Example]
    python repo_collector.py --url https://github.com/psf/requests --dir .
"""

import argparse
import os
import requests


def get_repo_owner_and_name(repo_url: str):
    """
    GitHubリポジトリのURLからオーナー名とリポジトリ名を抽出する関数。
    例: "https://github.com/username/repo" -> ("username", "repo")
    """
    repo_url = repo_url.rstrip('/')
    parts = repo_url.split('/')
    if len(parts) < 5:
        raise ValueError("無効なGitHubリポジトリURLです。例: https://github.com/username/repo")
    owner = parts[-2]
    repo = parts[-1]
    return owner, repo


def fetch_repo_files(owner: str, repo: str, path: str = ""):
    """
    指定されたowner/repoの指定パス内のコンテンツ情報を取得し、
    再帰的にすべてのファイル（typeが'file'の項目）のリストを返す関数。

    GitHub API:
      https://api.github.com/repos/{owner}/{repo}/contents/{path}
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(api_url)
    response.raise_for_status()
    items = response.json()

    files = []
    for item in items:
        if item['type'] == 'file':
            files.append(item)
        elif item['type'] == 'dir':
            files.extend(fetch_repo_files(owner, repo, item['path']))
    return files


def fetch_file_content(file_info: dict) -> str:
    """
    GitHub APIから取得したファイル情報（file_info）に含まれるdownload_urlを使って
    ファイル内容を取得し返す関数。
    """
    download_url = file_info.get('download_url')
    if not download_url:
        return ""
    resp = requests.get(download_url)
    resp.raise_for_status()
    return resp.text


def merge_repo_code(repo_url: str) -> (str, str):
    """
    指定されたGitHubリポジトリURLからすべてのファイルを取得し、
    ファイルごとにコメント行を挿入してまとめた文字列を作成して返す関数。

    Returns:
        (repo_name, merged_text)
         repo_name: リポジトリ名(例: "requests")
         merged_text: すべてのファイル内容をまとめたテキスト
    """
    owner, repo_name = get_repo_owner_and_name(repo_url)
    files = fetch_repo_files(owner, repo_name)

    merged_text = []
    for file_info in files:
        path = file_info.get('path', 'unknown')
        try:
            content = fetch_file_content(file_info)
        except Exception as e:
            print(f"[Warning] {path} の取得に失敗: {e}")
            continue

        merged_text.append(f"\n\n# ===== File: {path} =====\n\n{content}")

    return repo_name, "".join(merged_text)


def main():
    parser = argparse.ArgumentParser(
        description="GitHubリポジトリから全ファイルをまとめて1つのテキストファイルに出力するツール"
    )
    parser.add_argument(
        "--url",
        required=True,
        help="対象のGitHubリポジトリURL (例: https://github.com/psf/requests)"
    )
    parser.add_argument(
        "--dir",
        default=".",
        help="出力ファイルの作成先ディレクトリ (default: カレントディレクトリ)"
    )

    args = parser.parse_args()
    repo_url = args.url
    output_dir = args.dir

    # リポジトリの全ファイルをまとめて取得
    print(f"Target Repo: {repo_url}")
    repo_name, merged_text = merge_repo_code(repo_url)

    # 出力ファイル名: "summary-<repo_name>.txt"
    #  例: "summary-requests.txt"
    output_filename = f"summary-{repo_name}.txt"
    output_path = os.path.join(output_dir, output_filename)

    # テキストを書き出し
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(merged_text)

    print(f"Created: {output_path}")


if __name__ == "__main__":
    main()
