# 読書記録アプリ
読んだ書籍の感想や要約を記録し, それをいつでも簡単に見返すことができる.
## 使用技術
python3, sqlite3, flask, tailwindcss

## 環境構築
### 事前準備
事前に python3, sqlite3 をインストールし, プロジェクトフォルダに python 仮想環境を作成し、起動する.
```
py -m venv venv
.\venv\Scripts\activate
```

### 実行環境の構築
配布ファイルを pip でインストールする.
```
pip install <dist-file-path>
```

### 開発環境の構築
python3, sqlite3 に加え、node.js, tailwindcss をインストールしておく.

github よりリポジトリをクローンする.
```
git clone https://github.com/ttsugiyc/readingapp
```
tailwindcss の準備をする.
```
cd tailwindcss
npm install
```