# 読書記録アプリ
読んだ書籍の感想や要約を記録し, それをいつでも簡単に見返すことができる.

## 環境
- Python 3.9.12
- SQLite 3.44.2
- Flask 3.0.1
- Node.js 20.11.0
- Tailwind CSS 3.4.1

## 実行手順

### 環境構築
事前に Python, SQLite をインストールして, 配布ファイル（`/dist` にあるファイルのどちらか一方）をダウンロードしておく. 

プロジェクトフォルダを作成して, ターミナルで開く. 

Python 仮想環境を作成し, 起動する.
```
py -m venv venv
.\venv\Scripts\activate
```

pip で配布ファイルを仮想環境にインストールする.
```
pip install <配布ファイルのパス>
```

### 起動・停止
以下のコマンドでアプリが起動する. 
```
flask --app readingapp run
```
Web ブラウザで `http://127.0.0.1:5000/` を開いて使用する. アプリの停止は `Ctrl+C` .

### 初期設定
セキュリティを高めるため, 管理者はアプリの初期設定を行う必要がある.

1. 画面右下の「管理者ページへ」をクリックして, 管理者ページに移動する.

2. 初期パスワード `admin` を入力して, 管理者としてログインする.

3. 画面右上の「設定」をクリックして, アプリ設定画面を開く.

4. 現在のパスワード `admin` と新しいパスワード（任意）を入力して, 「変更」をクリック, 確認ダイアログの「OK」をクリックする.

5. ターミナル上で `Ctrl+C` を入力してアプリを終了した後, アプリを再び起動する.

6. 新しいパスワードで管理者ページにログインできれば初期設定は完了. ユーザーページにアクセスすると, 画面右下の「管理者ページへ」がなくなっていることが確認できる.

### ユーザーページ
- 本棚管理
  - 本棚 `/`
    - 保存した書籍が表示される.
    - 書籍を様々な条件で検索できる.
  - 新しい本 `/create`
    - 書籍を ISBN コードで検索できる.
    - 書籍を保存できる.
  - 読書記録 `/<投稿id>/update`
    - 書籍にコメントできる.
    - 読了したことを記録できる.
- 認証
  - 新規登録 `/auth/register`
  - ログイン `/auth/login`
- アカウント管理
  - アカウント情報 `/account/settings`
  - ユーザー名変更 `/account/username`
  - メールアドレス変更 `/account/email`
  - パスワード変更 `/account/password`
  - 退会 `/account/delete`

### 管理者ページ
- ユーザー管理
  - ユーザー一覧 `/admin`
  - ユーザー情報 `/admin/<ユーザーid>/update`
  - ユーザー名変更 `/admin/<ユーザーid>/username`
  - メールアドレス変更 `/admin/<ユーザーid>/email`
  - パスワード変更 `/admin/<ユーザーid>/password`
- ログイン `/admin/login`
- アプリ設定 `/admin/settings`
  - 管理者パスワードを変更できる.
  - その際, SECRET_KEY が自動で変更される.
  - 変更はアプリの再起動時に反映される.

### コマンド

- アプリの起動
```
flask --app readingapp run
```
- データベースの初期化, ダウンロードした書影の削除
```
flask --app readingapp init-data
```
- 管理者パスワードの初期化
```
flask --app readingapp init-pass
```

## 開発環境

### 環境構築
事前に Python, SQLite, Node.js をインストールする. 

プロジェクトフォルダを作成して, ターミナルで開く. 

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
pip install flask requests pytest coverage build
```

Tailwind CSS をインストールする.
```
cd tailwindcss
npm install
```

### デバッグモード
アプリをデバッグモードで起動する. 
```
flask --app readingapp run --debug
```
デバッグモードではファイルの更新が反映される. また, ユーザーページ下部に管理者ページへのリンクが現れる.

### Tailwind CSS の使用
`/readingapp/templates` 以下を編集するときは, `tailwindcss` で以下のコマンドを実行し, CSS ファイルが自動で更新されるようにしておく.
```
npx tailwindcss -i input.css -o ../readingapp/static/style.css --watch
```

### テスト
'''
coverage run -m pytest
'''
'''
coverage report
'''

### 配布ファイルの作成
'''
py -m build
'''
