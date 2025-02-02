import argparse
import os
from services import merge_repo_code
from ignore_manager import load_ignore_patterns


def run_controller():
    """
    コマンドライン引数をパースして、指定されたGitHubリポジトリのコードを1ファイルにまとめる。
    .collectignore (あれば) を読み込んで無視パターンとして適用する。
    """
    parser = argparse.ArgumentParser(
        description="GitHubリポジトリからファイルをまとめて1つのテキストファイルに出力するツール"
    )
    parser.add_argument(
        "--url",
        required=True,
        help="対象のGitHubリポジトリURL (例: https://github.com/psf/requests)"
    )
    parser.add_argument(
        "--dir",
        default=None,  # Noneの場合は後でデフォルト設定
        help="出力ファイルの作成先ディレクトリ。指定がない場合はカレントディレクトリ。"
    )

    args = parser.parse_args()
    repo_url = args.url

    # --dir が None ならカレントディレクトリを使用
    output_dir = args.dir if args.dir is not None else "."

    # .collectignore をロード
    ignore_patterns = load_ignore_patterns(".collectignore")

    print(f"Target Repo: {repo_url}")
    if ignore_patterns:
        print(f"Ignore patterns: {ignore_patterns}")
    else:
        print("No ignore patterns found.")

    # リポジトリの全ファイルを結合
    repo_name, merged_text = merge_repo_code(repo_url, ignore_patterns)

    # 出力ファイル名例: "summary-requests.txt"
    output_filename = f"summary-{repo_name}.txt"
    output_path = os.path.join(output_dir, output_filename)

    # テキストを書き出し
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(merged_text)

    print(f"Created: {output_path}")
