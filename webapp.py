from flask import Flask, request, jsonify
import requests
import logging

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

 
@app.route('/api/ir', methods=['POST'])
def handle_request():
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