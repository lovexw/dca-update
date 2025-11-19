#!/usr/bin/env python3
"""
每日比特币价格更新脚本
从 CoinGecko API 获取当前比特币价格并更新到 btc-price all.csv 文件
"""

import requests
import csv
from datetime import datetime, timezone, timedelta
import sys
import os

# API 配置
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
CSV_FILE = "btc-price all.csv"

def get_btc_price():
    """从 CoinGecko API 获取当前比特币价格"""
    try:
        response = requests.get(COINGECKO_API, timeout=10)
        response.raise_for_status()
        data = response.json()
        price = data['bitcoin']['usd']
        return int(price)
    except Exception as e:
        print(f"获取价格失败: {e}", file=sys.stderr)
        sys.exit(1)

def get_beijing_date():
    """获取北京时间的日期（UTC+8）"""
    utc_now = datetime.now(timezone.utc)
    beijing_time = utc_now + timedelta(hours=8)
    return beijing_time.strftime('%Y-%m-%d')

def update_csv(date_str, price):
    """更新CSV文件，添加新的价格记录"""
    # 读取现有数据
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if not lines:
        print("CSV文件为空", file=sys.stderr)
        sys.exit(1)
    
    header = lines[0].strip()
    
    # 检查日期是否已存在
    existing_dates = set()
    for line in lines[1:]:
        if line.strip():
            parts = line.strip().split(',')
            if parts:
                existing_dates.add(parts[0])
    
    if date_str in existing_dates:
        print(f"日期 {date_str} 已存在，跳过更新")
        return False
    
    # 插入新记录（在表头后面）
    new_line = f"{date_str},{price}\n"
    lines.insert(1, new_line)
    
    # 写回文件
    with open(CSV_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"成功添加记录: {date_str},{price}")
    return True

def main():
    """主函数"""
    print("开始更新比特币价格...")
    
    # 获取北京时间日期
    date_str = get_beijing_date()
    print(f"北京时间日期: {date_str}")
    
    # 获取当前价格
    price = get_btc_price()
    print(f"当前比特币价格: ${price:,}")
    
    # 更新CSV
    updated = update_csv(date_str, price)
    
    if updated:
        print("✓ 价格数据已成功更新到 btc-price all.csv")
    else:
        print("ℹ 今日价格已存在，无需更新")

if __name__ == "__main__":
    main()
