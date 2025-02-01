#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
repo-collector
--------------
GitHubの指定リポジトリからコードを取得して、1つのテキストファイルにまとめるツール。

[Usage Example]
    python main.py --url https://github.com/psf/requests --dir .
"""

from controller import run_controller

if __name__ == "__main__":
    run_controller()
