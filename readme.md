# Flask プログラムの説明

このプロジェクトは、Flask を使用して構築された簡単な API サーバーと、それを利用するクライアントプログラムを含んでいます。

## ファイル構成

- **app.py**  
  クライアントプログラム。Flask サーバーに対して POST リクエストを送信し、レスポンスを受け取ります。

- **test.py**  
  シンプルな Flask サーバー。`/api/test` エンドポイントを提供し、JSON データを受け取り、レスポンスとしてメッセージを返します。

- **webapp.py(メイン)**  
  CORS 対応の Flask サーバー。ユーザー認証（サインアップ・ログイン・ログアウト）と投稿APIを提供します。
  - `/api/signup`: ユーザー登録（パスワードはハッシュ化して保存）
  - `/api/login`: ログイン（Flask-Loginでセッション管理。ログイン成功時はセッションクッキーが自動で返されます）
  - `/api/logout`: ログアウト（@login_required付き。セッションが有効な場合のみアクセス可能）
  - `/api/blog`: 投稿データの登録・取得（POST/GET）
  - `/api/blog/<int:post_id>`: 投稿データの個別取得
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
   - `http://127.0.0.1:5000/api/signup`
   - `http://127.0.0.1:5000/api/login`
   - `http://127.0.0.1:5000/api/logout`
   - `http://127.0.0.1:5000/api/blog`
   - `http://127.0.0.1:5000/api/blog/<post_id>`
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

#### `/api/signup` (POST)
ユーザー登録（JSON形式で送信）
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "ユーザー名", "password": "パスワード"}' http://127.0.0.1:5000/api/signup
```

#### `/api/login` (POST)
ログイン（JSON形式で送信。以降のリクエストはCookieを利用するため、フロントエンドは`credentials: 'include'`を指定してください）
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "ユーザー名", "password": "パスワード"}' http://127.0.0.1:5000/api/login
```

#### `/api/logout` (POST)
ログアウト（ログイン済みセッションでのみ有効）
```bash
curl -X POST http://127.0.0.1:5000/api/logout
```

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

#### `/api/blog/<post_id>` (GET)
指定したIDの投稿データを取得します。
```bash
curl http://127.0.0.1:5000/api/blog/1
```

#### `/api/ir` (POST)
外部APIにデータを転送します。
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com"}' http://127.0.0.1:5000/api/ir
```

---

## フロントエンド（Next.jsなど）から利用する場合の注意

- 認証付きAPI（ログイン・ログアウト・@login_required付きAPI）を利用する場合は、fetchやaxiosで`credentials: 'include'`を必ず指定してください。
- Flask側は`CORS(app, supports_credentials=True)`でCORS対応済みです。

---

これで、Flaskアプリケーションの使用方法がわかります。必要に応じて、エンドポイントや機能を拡張してください。