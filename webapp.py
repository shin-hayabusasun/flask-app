from flask import Flask, request, jsonify
import requests
import logging
from flask_sqlalchemy import SQLAlchemy
import os
from datetime  import datetime
import pytz
from flask_cors import CORS
from flask import render_template
from flask_login import LoginManager, UserMixin,login_user,logout_user,login_required #login用
from werkzeug.security import generate_password_hash, check_password_hash #login用ハッシュ

app = Flask(__name__)
CORS(app,supports_credentials=True) #CORSを有効にする.セッションを有効にするためにsupports_credentials=Trueを指定

#login用
login_manager = LoginManager()
login_manager.init_app(app)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24) #ランダムなシークレットキーを生成セッション
db = SQLAlchemy(app)
#設定

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    created_at= db.Column(db.DateTime, nullable=False,default=datetime.now(pytz.timezone('Asia/Tokyo')))
    def to_dict(self):
            return {
                'id': self.id,
                'title': self.title,
                'body': self.body,
                'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }

#login用
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) #有効なセッションがある場合にユーザーを取得

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # パスワードをハッシュ化
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password): #check_password_hash(db.password, password):
        # ログイン成功
        login_user(user)  # Flask-Loginを使用してユーザーをログインさせる
        return jsonify({'message': 'Login successful'}), 200 #セッションも送られる
    else:
        # ログイン失敗
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
@login_required #セッションが有効な場合のみアクセス可能
def logout():
    logout_user() # Flask-Loginを使用してユーザーをログアウトさせる


@app.route('/api/blog', methods=['GET','POST'])
def handle_request():
    if request.method == 'POST':
        data = request.get_json()  # JSON形式のリクエストを取得
        print("受け取ったデータ:", data)
        
        # たとえば 'name' パラメータがあると仮定
        name = data.get('title')
        body = data.get('body')
        # データベースに保存

        new_post = Post(title=name, body=body)

        db.session.add(new_post)
        db.session.commit()

        return jsonify({
            'message': f'完了しました'
        })
    else:
        posts=Post.query.all()
        return jsonify([post.to_dict() for post in posts])
@app.route('/api/blog/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    print("受け取ったデータ:", post.to_dict())
    return jsonify(post.to_dict())


        

@app.route('/api/blogtest', methods=['GET','POST'])
def handle_request_test():
    if request.method == 'POST':
        
        
        # たとえば 'name' パラメータがあると仮定
        name = request.form.get('title')
        body = request.form.get('body')
        # データベースに保存

        new_post = Post(title=name, body=body)

        db.session.add(new_post)
        db.session.commit()
        posts=Post.query.all()
        print("受け取ったデータ:")
        for post in posts:
            
            print(post.id)
            print(post.title)
            print(post.body)
            print(post.created_at)
        return render_template('form.html')

    else:
        posts=Post.query.all()
        for post in posts:
            logging.debug("受け取ったデータ:")
            logging.debug(post.id)
            logging.debug(post.title)
            logging.debug(post.body)
            logging.debug(post.created_at)
   

        return render_template('form.html')


@app.route('/api/ir', methods=['POST'])
def handle_request_ir():
    dataa = request.get_json()  # JSON形式のリクエストを取得 #urlを取得
    print("受け取ったデータ:", dataa)
    logging.debug("受け取ったデータ:", dataa.get('url'))
    
    #url
    url = dataa.get('url', 'urlなし')

    #n8n
    api=''

    #受けとったurl
    dataq = {
        'url': url
    }
    print("受け取ったデータ:", dataq.get('url'))
    

    try:
        # 外部APIへPOST（JSON形式で）
        response = requests.post(api, json=dataq)

        return jsonify({
            'status': 'success',
            'result': response.result
            })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)