from flask import Flask, request, jsonify
import requests
 
app = Flask(__name__)
 
@app.route('/api/ir', methods=['POST'])
def handle_request():
    data = request.get_json()  # JSON形式のリクエストを取得 #urlを取得
    print("受け取ったデータ:", data)
    
    #url
    url = data.get('url', 'urlなし')

    #n8n
    api=''

    #受けとったurl
    data = {
        'url': url
    }

    try:
        # 外部APIへPOST（JSON形式で）
        response = requests.post(api, json=data)

        return jsonify({
            'status': 'success',
            'result': response.result
            })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)