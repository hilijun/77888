from flask import Flask, send_from_directory, jsonify
import requests
import json
import os
from datetime import datetime

# 获取当前文件所在目录（Railway 上的工作目录）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# 历史记录文件路径（在 Railway 文件系统中）
HISTORY_FILE = os.path.join(BASE_DIR, 'history.json')
LATEST_FILE = os.path.join(BASE_DIR, 'keno_data.json')

# ==================== 页面路由 ====================

@app.route('/')
def index():
    """返回主页面 index.html"""
    try:
        return send_from_directory(BASE_DIR, 'index.html')
    except Exception as e:
        return f"加载页面失败: {e}", 500

# ==================== API 路由 ====================

@app.route('/api/live')
def get_live_data():
    """从远程 API 实时获取最新数据"""
    try:
        url = "https://pc28.help/api/keno.json?nbr=1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"网络请求失败: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/local')
def get_local_data():
    """读取本地 kenro_data.json 文件（最新数据）"""
    try:
        if os.path.exists(LATEST_FILE):
            with open(LATEST_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data)
        return jsonify({"error": "本地数据文件不存在，请先运行更新脚本"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history')
def get_history():
    """获取历史记录（最近 30 期）"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify({
                "count": len(data),
                "data": data,
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        # 如果文件不存在，返回空历史
        return jsonify({
            "count": 0,
            "data": [],
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test')
def test():
    """测试路由，检查 Flask 是否运行正常"""
    return "✅ Flask 运行正常！"

# ==================== 启动服务 ====================

if __name__ == '__main__':
    # Railway 会通过环境变量 PORT 指定端口
    port = int(os.environ.get('PORT', 5000))
    # 监听所有网络接口
    app.run(host='0.0.0.0', port=port)
