# 読書記録アプリ
読んだ書籍の感想や要約を記録し, それをいつでも簡単に見返すことができる.

## 環境
- Python 3.9.12
- SQLite 3.44.2
- Flask 3.0.1
- Tailwind CSS 3.4.1

## 実行手順
Windows 11 での実行手順について解説する.

### 環境構築
事前に Python, SQLite のインストール, 配布ファイル（拡張子が .tar.gz または .whl であるようなファイル）のダウンロード, プロジェクトフォルダの作成をしておく. 

ターミナルでプロジェクトフォルダを開く. 

プロジェクトフォルダに Python 仮想環境を作成し, 起動する.
```
py -m venv <仮想環境名>
.\<仮想環境名>\Scripts\activate
```

pip により配布ファイルをインストールする.
```
pip install <配布ファイルのパス>
```

### アプリの使用法
以下のコマンドでアプリが起動する. Web ブラウザで `http://127.0.0.1:5000/` にアクセスして使用する.
```
flask --app readingapp run
```
アプリの停止は `Ctrl+C` キー.

#### 初期設定
はじめに, セキュリティのため, 管理者は以下の手順でアプリの初期設定を行う必要がある.

1. 画面右下の「管理者ページへ」をクリックして, 管理者ページに移動する.

2. 初期パスワード `admin` を入力して, 管理者としてログインする.

3. 画面右上の「設定」をクリックして, アプリ設定画面を開く.

4. 現在のパスワード `admin` と新しいパスワード（任意）を入力して, 「変更」をクリック, 確認ダイアログの「OK」をクリックする.

5. ターミナル上で `Ctrl+C` を入力してアプリを終了したのち, アプリを再び起動する.

6. 新しいパスワードで管理者ページにログインできる. `http://127.0.0.1:5000/` にアクセスすると, 画面右下の「管理者ページへ」がなくなっている.

#### ユーザーページ

#### 管理者ページ

#### コマンド一覧

- アプリの起動
```
flask --app readingapp run
```
- データベースの初期化・ダウンロードした書影の削除
```
flask --app readingapp init-data
```
- 管理者パスワードの初期化
```
flask --app readingapp init-pass
```

## 開発環境の構築
事前に Python, SQLite, Node.js をインストールする. 

GitHub からリポジトリをクローンする.
```
git clone https://github.com/ttsugiyc/readingapp
```

Python 仮想環境を作成し, 起動する.
```
py -m venv venv
.\venv\Scripts\activate
```

仮想環境に依存ライブラリをインストールする.
```
pip install flask requests
```

Tailwind CSS をインストールする.
```
cd tailwindcss
npm install
```
templates フォルダを編集するときは, tailwindcss フォルダにて以下のコマンドを実行し, CSS ファイルが自動で変更されるようにしておく.
```
npx tailwindcss -i input.css -o ../readingapp/static/style.css --watch
```