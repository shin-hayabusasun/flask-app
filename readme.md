# Flask プログラムの説明

このプロジェクトは、Flask を使用して構築された簡単な API サーバーと、それを利用するクライアントプログラムを含んでいます。

## ファイル構成

- **app.py**  
  クライアントプログラム。Flask サーバーに対して POST リクエストを送信し、レスポンスを受け取ります。

- **test.py**  
  シンプルな Flask サーバー。`/api/test` エンドポイントを提供し、JSON データを受け取り、レスポンスとしてメッセージを返します。

- **webapp.py(メイン)**  
  CORS 対応の Flask サーバー。以下のエンドポイントを提供します:
  - `/api/blog`: 投稿データを受け取り、データベースに保存します。また、保存された投稿データを取得できます。
  - `/api/blogtest`: フォームから投稿データを受け取り、データベースに保存します。
  - `/api/ir`: 外部APIにデータを転送します。

- **templates/form.html**  
  投稿フォームのHTMLテンプレート。

- **readme.md**  
  このプロジェクトの説明を記載したファイルです。

## 使用方法

### サーバーの起動

1. `webapp.py` を実行してサーバーを起動します。
   ```bash
   python webapp.py
   ```

2. サーバーが起動すると、以下のURLが利用可能になります:
   - `http://127.0.0.1:5000/api/blog`
   - `http://127.0.0.1:5000/api/blogtest`
   - `http://127.0.0.1:5000/api/ir`

### データベースの初期化

1. データベースを初期化するには、`create.py`を実行します。
   ```bash
   python create.py
   ```
   実行後、`blog.db`というSQLiteデータベースファイルが作成されます。

### 投稿フォームの使用

1. ブラウザで以下のURLを開きます:
   ```
   http://127.0.0.1:5000/api/blogtest
   ```
2. フォームにタイトルと本文を入力して送信すると、データがデータベースに保存されます。

### APIの使用例

#### `/api/blog` (POST)
投稿データをJSON形式で送信します。
```bash
curl -X POST -H "Content-Type: application/json" -d '{"title": "タイトル", "body": "本文"}' http://127.0.0.1:5000/api/blog
```

#### `/api/blog` (GET)
保存された投稿データを取得します。
```bash
curl http://127.0.0.1:5000/api/blog
```

#### `/api/ir` (POST)
外部APIにデータを転送します。
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com"}' http://127.0.0.1:5000/api/ir
```

---

これで、Flaskアプリケーションの使用方法がわかります。必要に応じて、エンドポイントや機能を拡張してください。