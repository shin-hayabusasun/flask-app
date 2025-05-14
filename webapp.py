from flask import Flask, request, jsonify
import requests
import logging
from flask_sqlalchemy import SQLAlchemy
from datetime  import datetime
import pytz
from flask_cors import CORS
from flask import render_template

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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