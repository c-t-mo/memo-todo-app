# メモ・ToDoアプリ

シンプルなメモ・ToDo管理Webアプリです。Dockerコンテナ上で動作し、ブラウザからアクセスできます。

## 概要・用途

- タスク（タイトル＋メモ内容）を追加・一覧表示・完了切り替え・削除できます
- データはコンテナ内のSQLiteデータベースに保存されます
- 「入力（フォーム）→処理（Flaskによる登録・更新・削除）→出力（一覧表示）」という構成になっています

## 使用技術

- Python 3.12 / Flask（バックエンドAPI）
- SQLite（データ保存）
- HTML / CSS / JavaScript（フロントエンド、素のJSでAPIを呼び出し）
- Docker / Docker Compose

## ディレクトリ構成

```
memo-todo-app/
├── app.py              # Flaskアプリ本体（APIエンドポイント）
├── requirements.txt     # Python依存パッケージ
├── Dockerfile
├── docker-compose.yml
├── templates/
│   └── index.html       # メイン画面
├── static/
│   ├── style.css
│   └── script.js
└── data/                 # SQLiteデータベース（実行時に自動生成、gitには含めない）
```

## 実行方法（Docker Composeを使う場合）

1. このリポジトリをクローンする

   ```bash
   git clone <このリポジトリのURL>
   cd memo-todo-app
   ```

2. Docker Composeで起動する

   ```bash
   docker compose up --build
   ```

3. ブラウザで以下にアクセスする

   ```
   http://localhost:5000
   ```

4. 終了する場合は `Ctrl + C`、コンテナを削除する場合は以下を実行

   ```bash
   docker compose down
   ```

## 実行方法（Dockerのみを使う場合）

```bash
docker build -t memo-todo-app .
docker run -p 5000:5000 memo-todo-app
```

## 使い方

1. 画面上部のフォームに「タイトル」（必須）と「メモ内容」（任意）を入力し、「追加する」を押す
2. 一覧にタスクが追加される
3. タスクをクリックすると完了状態（取り消し線）を切り替えられる
4. ゴミ箱アイコン（🗑）でタスクを削除できる

## 主な機能

- タスクの追加（入力フォーム）
- タスク一覧の表示（一覧取得API）
- 完了・未完了の切り替え
- タスクの削除

## 動作画面

<img width="416" height="326" alt="スクリーンショット 2026-08-03 183447" src="https://github.com/user-attachments/assets/cd33f7a7-2ac5-448a-b059-fd136db8b29e" />


## ライセンス

このリポジトリは大学の授業課題として作成したものです。
