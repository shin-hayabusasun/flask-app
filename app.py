from webapp import app, db

# アプリケーションコンテキストを設定してデータベースを初期化
with app.app_context():
    db.create_all()
    print("データベースが初期化されました。")
