# repo-collector

GitHub の指定リポジトリからすべてのファイルを取得し、1つのテキストファイルにまとめるツールです。  
学習目的で作成したものであり、**本ツールを使用したことによるいかなる結果についても一切の責任を負いません**。  
ご利用の際は、プログラムや取得するリポジトリのライセンスを含め、各種規約を十分にご確認ください。

---

## 注意事項

- **APIレートリミット**: GitHub の API を多数コールするため、レートリミットに達する場合があります。現状はその対策を行っていないので、レートリミットにかかった場合は時間をおいて再度実行してください（TODO: レートリミット対策の検討）。
- **利用範囲**: 学習目的を想定しています。取得するコードのライセンスや、他人の権利を侵害しないようご注意ください。
- **免責**: 本ソフトウェアを使用したことによって発生した損害・不具合・トラブルなど、いかなる事象についても作成者は責任を負いかねます。自己責任のもとでご利用ください。

---

## セットアップ & 使い方

1. **リポジトリのクローンまたはダウンロード**

   ```bash
   git clone https://github.com/Yulikepython/repo-collector.git
   cd repo-collector
   ```

2. **必要ライブラリのインストール**

   ```bash
   pip install -r requirements.txt
   ```
   > ※ 仮想環境（`venv/`）などを用意して利用することをおすすめします。

3. **.collectignore.sample について（任意）**  
   特定の拡張子やパスを取得したくない場合は、同梱の `.collectignore.sample` を参考にして  
   ```bash
   cp .collectignore.sample .collectignore
   ```
   などで `.collectignore` を作成し、無視したいパターンを追記してください。

4. **実行方法**  
   - **`--dir` オプションは省略可能** です。指定しない場合、カレントディレクトリを出力先とします。
   - 例: リポジトリ [psf/requests](https://github.com/psf/requests) を取得し、カレントディレクトリに `summary-requests.txt` を出力する場合:
     
     ```bash
     python main.py --url https://github.com/psf/requests
     ```
     
     カレントディレクトリ以外を指定したい場合:
     ```bash
     python main.py --url https://github.com/psf/requests --dir /path/to/output
     ```
     
     `repo_collector.py` は単体でも動作しますが、`.collectignore` 等を利用した無視パターン機能は含まれない点にご注意ください。

5. **出力ファイル**  
   - 実行後、指定ディレクトリ（省略時はカレントディレクトリ）に `summary-リポジトリ名.txt` の形式でファイルが作成されます。  
   - 取得した各ファイルの内容を、`# ===== File: ファイルパス =====` の見出しコメント付きで連結したテキストが出力されます。

---

## ディレクトリ構成

```
repo-collector/
├─ repo_collector.py   # 単体でも動作するメインスクリプト
├─ services.py         # APIコールなどのサービス層
├─ controller.py       # 引数パースと全体の制御
├─ main.py             # controllerを利用した実行入口
├─ ignore_manager.py   # .collectignoreを読み込み、無視すべきパスを判定
├─ venv/               # (任意) 仮想環境用フォルダ
├─ .collectignore.sample  # ignoreしたいパターンのサンプル
├─ requirements.txt    # インストールが必要なライブラリ一覧
└─ README.md           # 本ファイル
```

---

## TODO

- [ ] **レートリミット回避策**: GitHub のトークン認証（Personal Access Token の使用）やリクエスト間隔の調整などの対応を検討。
- [ ] **フィルタリング強化**: 取得したいファイルの種類を指定したり、取得しないディレクトリをまとめて除外したりする機能。
- [ ] **出力形式の拡張**: テキストファイル以外のフォーマットへの出力（Markdown、HTML など）も検討。

---

## ライセンス / License

本リポジトリは [MIT License](./LICENSE) のもとで公開されています。  
ご利用の際は、[MIT ライセンス](./LICENSE)をご確認ください。

---

**Disclaimer**: This software is provided "as is", without warranty of any kind, express or implied.  
Use it at your own risk.  