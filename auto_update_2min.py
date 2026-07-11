import requests
import json
import os
import time
from datetime import datetime

# 自动获取桌面路径
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
if not os.path.exists(desktop):
    desktop = os.path.join(os.path.expanduser("~"), "桌面")

# 完整文件路径
filepath = os.path.join(desktop, "keno_data.json")

print("=" * 60)
print("🔄 凯诺数据自动更新程序")
print(f"📁 文件保存位置: {filepath}")
print("⏰ 更新间隔: 每2分钟")
print("=" * 60)
print("按 Ctrl+C 可停止程序\n")

def fetch_and_save():
    """获取数据并保存到桌面"""
    try:
        # 获取当前时间
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 发送请求
        url = "https://pc28.help/api/keno.json?nbr=1"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # 保存到文件
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # 获取文件大小
            file_size = os.path.getsize(filepath)
            
            print(f"[{now}] ✅ 更新成功 | 文件大小: {file_size} 字节")
            
            # 可选：显示数据摘要（只显示前100个字符）
            data_preview = json.dumps(data, ensure_ascii=False)[:100]
            print(f"   数据预览: {data_preview}...")
            
            return True
        else:
            print(f"[{now}] ❌ 请求失败 | 状态码: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 网络错误: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 数据格式错误: {e}")
        return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 未知错误: {e}")
        return False

# 立即执行第一次
print("首次运行，立即获取数据...")
fetch_and_save()

# 然后每2分钟循环执行
count = 1
while True:
    # 等待120秒（2分钟）
    for remaining in range(207, 0, -1):
        # 显示倒计时（每10秒更新一次，避免刷屏）
        if remaining % 10 == 0 or remaining <= 5:
            print(f"⏳ 下次更新倒计时: {remaining} 秒", end="\r")
        time.sleep(1)
    
    print(" " * 40, end="\r")  # 清除倒计时行
    count += 1
    print(f"\n--- 第 {count} 次更新 ---")
    fetch_and_save()