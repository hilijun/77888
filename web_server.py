from flask import Flask, jsonify
import requests
import os
from datetime import datetime
import traceback

app = Flask(__name__)

URL_KJ = "https://pc28.help/api/kj.json?nbr=1"
URL_KENO = "https://pc28.help/api/keno.json?nbr=1"

@app.route('/')
def index():
    return """
    <h1>开奖数据合并服务 ✅</h1>
    <p>访问 <a href="/api/merge">/api/merge</a> 查看合并数据</p>
    <p>当前时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    """

@app.route('/api/live')
def get_live_data():
    """兼容旧接口：直接返回合并数据"""
    return get_merged_data()

@app.route('/api/merge')
def get_merged_data():
    """获取并合并两个API的数据"""
    try:
        timeout = 10
        
        kj_response = requests.get(URL_KJ, timeout=timeout)
        keno_response = requests.get(URL_KENO, timeout=timeout)
        
        if kj_response.status_code != 200:
            return jsonify({"error": f"kj.json 请求失败: {kj_response.status_code}"}), 500
        if keno_response.status_code != 200:
            return jsonify({"error": f"keno.json 请求失败: {keno_response.status_code}"}), 500
        
        kj_data = kj_response.json()
        keno_data = keno_response.json()
        
        # 构建 keno 映射表
        keno_map = {}
        keno_list = keno_data.get('data', [])
        if isinstance(keno_list, list):
            for item in keno_list:
                nbr = item.get('nbr')
                if nbr:
                    keno_map[str(nbr)] = {
                        'nbrs': item.get('nbrs', '').split(',') if item.get('nbrs') else [],
                        'bonus': item.get('bonus', '')
                    }
        
        # 处理 kj 数据
        merged = []
        kj_list = kj_data.get('data', [])
        if isinstance(kj_list, list):
            for item in kj_list:
                period = item.get('nbr')
                if not period:
                    continue
                
                keno_info = keno_map.get(str(period), {})
                merged.append({
                    "nbr": period,
                    "number": item.get('number', ''),
                    "num": item.get('num', ''),
                    "combination": item.get('combination', ''),
                    "time": item.get('time', ''),
                    "date": item.get('date', ''),
                    "nbrs": keno_info.get('nbrs', []),
                    "bonus": keno_info.get('bonus', '')
                })
        
        return jsonify({
            "source": "merged",
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": len(merged),
            "data": merged
        })
        
    except requests.exceptions.Timeout:
        return jsonify({"error": "请求超时"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "网络连接失败"}), 503
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route('/api/local')
def get_local_data():
    """兼容旧接口：返回合并数据"""
    return get_merged_data()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
