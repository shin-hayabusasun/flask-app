from flask import Flask, request, jsonify

 
app = Flask(__name__)
 
@app.route('/api/test', methods=['POST'])
def handle_request():
    data = request.get_json()  # JSON形式のリクエストを取得
    print("受け取ったデータ:", data)
    
    # たとえば 'name' パラメータがあると仮定
    name = data.get('name', '名前なし')

    return jsonify({
        'message': f'こんにちは、{name}さん！'
    })

if __name__ == '__main__':
    app.run(debug=True)