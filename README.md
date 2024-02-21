# 読書記録アプリ
読書内容を記録しておくアプリ。
書籍の感想や要約・読み終えたかどうかを記録し、それをいつでも簡単に見返すことができる。

![Bookshelf Image](/img/bookshelf.png)
![Small Bookshelf Image](/img/bookshelf_sm.png)

## 環境
- Python 3.9.12
- SQLite 3.44.2
- Flask 3.0.1
- Node.js 20.11.0
- Tailwind CSS 3.4.1
- Google Books APIs

## 機能一覧

### ユーザーページ
- アカウント作成機能
- ログイン／ログアウト機能
- アカウント情報変更機能
- 書籍管理機能
  - 書籍追加／削除機能
  - コメント機能
  - 読了管理機能
  - 検索機能

### 管理者ページ
- ログイン／ログアウト機能
- 管理者パスワード変更機能
- ユーザー管理機能
  - アカウント情報変更機能
  - 検索機能

## 実行手順

### 環境構築
事前に Python、SQLite をインストールして、配布ファイル（`/dist` にあるファイルのどちらか一方）をダウンロードしておく。

作業フォルダを作成して、ターミナルで開く。

Python 仮想環境を作成して、起動する。
```
py -m venv venv
.\venv\Scripts\activate
```

配布ファイルを仮想環境にインストールする。
```
pip install <配布ファイルのパス>
```

### 起動・停止
アプリの起動は次のコマンドで行う。
```
flask --app readingapp run
```
Web ブラウザで `http://127.0.0.1:5000/` を開いて使用する。アプリの停止は `Ctrl+C`。

### 初期設定
セキュリティを高めるため、管理者はアプリの初期設定を行う必要がある。

1. 画面右下の「管理者ページへ」をクリックして、管理者ページに移動する。

2. 初期パスワード `admin` を入力して、管理者としてログインする。

3. 画面右上の「設定」をクリックして、アプリ設定画面を開く。

4. 現在のパスワード `admin` と新しいパスワード（任意）を入力して、「変更」をクリック、確認ダイアログの「OK」をクリックする。

5. ターミナル上で `Ctrl+C` を入力してアプリを終了した後、アプリを再び起動する。

6. 新しいパスワードで管理者ページにログインできれば初期設定は完了。ユーザーページにアクセスすると、画面右下の「管理者ページへ」がなくなっていることが確認できる。

### コマンド

- アプリの起動
```
flask --app readingapp run
```
- データベースの初期化、ダウンロードした書影の削除
```
flask --app readingapp init-data
```
- 管理者パスワードの初期化
```
flask --app readingapp init-pass
```

## 開発環境

### 環境構築
事前に Python、SQLite、Node.js をインストールする。

GitHub からリポジトリをクローンする。
```
git clone https://github.com/ttsugiyc/readingapp
cd readingapp
```

Python 仮想環境を作成して、起動する。
```
py -m venv venv
.\venv\Scripts\activate
```

仮想環境に依存ライブラリをインストールする。
```
pip install flask requests build
```

Tailwind CSS をインストールする。
```
cd tailwindcss
npm install
```

### デバッグモード
アプリをデバッグモードで起動するには、次のコマンド。
```
flask --app readingapp run --debug
```
デバッグモードではファイルの更新が反映される。また、ユーザーページ下部に管理者ページへのリンクが常に表示される。

### Tailwind CSS の使用
`/readingapp/templates` 以下を編集するときは、`/tailwindcss` で以下のコマンドを実行し、CSS ファイルが自動で更新されるようにしておく。
```
npx tailwindcss -i input.css -o ../readingapp/static/style.css --watch
```

### テスト

### 配布ファイルの作成
配布ファイルの更新は次のコマンド。
```
py -m build
```
