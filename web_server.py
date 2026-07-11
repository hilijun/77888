from flask import Flask, send_from_directory, jsonify
import requests
import json
import os

# 获取当前文件所在的目录（这是最关键的一行）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

@app.route('/')
def index():
    """返回 index.html"""
    # 使用相对路径，在任何环境都有效
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/api/live')
def get_live_data():
    """从远程API获取实时数据"""
    try:
        url = "https://pc28.help/api/keno.json?nbr=1"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return jsonify(response.json())
        return jsonify({"error": f"状态码: {response.status_code}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/local')
def get_local_data():
    """读取本地JSON文件（如果存在）"""
    try:
        filepath = os.path.join(BASE_DIR, 'keno_data.json')
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data)
        return jsonify({"error": "数据文件不存在"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test')
def test():
    return "✅ Flask 运行正常！"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
