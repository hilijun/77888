import requests
import json
import os
from datetime import datetime

def fetch_and_save():
    try:
        url = "https://pc28.help/api/keno.json?nbr=1"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # 提取数据
        extracted = data.get('data', {}).get('data', [])
        if not extracted:
            print("未获取到有效数据")
            return
        
        # 读取历史记录
        history_file = 'history.json'
        history = []
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        # 去重并追加
        new_item = {
            "nbr": extracted[0].get("nbr"),
            "nbrs": extracted[0].get("nbrs")
        }
        
        if not any(item.get('nbr') == new_item['nbr'] for item in history):
            history.append(new_item)
            # 只保留最近30期
            history = history[-30:]
            
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            print(f"[{datetime.now()}] ✅ 数据已更新")
        else:
            print(f"[{datetime.now()}] ℹ️ 数据已是最新")
            
    except Exception as e:
        print(f"[{datetime.now()}] ❌ 更新失败: {e}")

if __name__ == "__main__":
    fetch_and_save()
