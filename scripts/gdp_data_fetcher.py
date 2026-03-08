#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
各国 GDP 数据自动抓取工具
数据来源：世界银行公开 API
功能：抓取指定国家的年度 GDP、人口、人均 GDP 数据，导出为 Excel
"""

import requests
import pandas as pd
from datetime import datetime

# ============ 配置区 ============
# 你想抓取哪些国家？这里用国家代码（ISO 3 位代码）
COUNTRIES = {
    'USA': '美国',
    'CHN': '中国',
    'JPN': '日本',
    'DEU': '德国',
    'GBR': '英国',
    'FRA': '法国',
    'IND': '印度',
    'BRA': '巴西',
}

# 抓取最近几年的数据
START_YEAR = 2018
END_YEAR = 2023
# ===============================


def fetch_world_bank_data(country_code, indicator, start_year, end_year):
    """
    从世界银行 API 抓取数据
    
    参数:
        country_code: 国家代码（如 'USA'）
        indicator: 指标代码
            - NY.GDP.MKTP.CD: GDP（美元，现价）
            - SP.POP.TOTL: 总人口
            - NY.GDP.PCAP.CD: 人均 GDP（美元，现价）
        start_year: 起始年份
        end_year: 结束年份
    
    返回: 字典 {年份：数值}
    """
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}"
    params = {
        'date': f'{start_year}:{end_year}',
        'format': 'json',
        'per_page': 50
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        # 世界银行 API 返回格式：[元数据，数据列表]
        if len(data) < 2 or not data[1]:
            return {}
        
        # 整理成 {年份：数值} 的格式
        result = {}
        for item in data[1]:
            year = int(item['date'])
            value = item['value']
            if value is not None:
                result[year] = value
        
        return result
    
    except Exception as e:
        print(f"⚠️  抓取 {country_code} 的 {indicator} 数据失败：{e}")
        return {}


def main():
    print("🌍 开始抓取世界各国经济数据...")
    print(f"📊 国家：{len(COUNTRIES)} 个")
    print(f"📅 年份：{START_YEAR} - {END_YEAR}")
    print("-" * 50)
    
    # 准备数据存储
    all_data = []
    
    # 逐个抓取国家数据
    for country_code, country_name in COUNTRIES.items():
        print(f"\n⏳ 正在抓取 {country_name} ({country_code}) 的数据...")
        
        # 抓取三项指标
        gdp_data = fetch_world_bank_data(country_code, 'NY.GDP.MKTP.CD', START_YEAR, END_YEAR)
        pop_data = fetch_world_bank_data(country_code, 'SP.POP.TOTL', START_YEAR, END_YEAR)
        gdp_per_capita_data = fetch_world_bank_data(country_code, 'NY.GDP.PCAP.CD', START_YEAR, END_YEAR)
        
        # 整理每年的数据
        for year in range(START_YEAR, END_YEAR + 1):
            gdp = gdp_data.get(year)
            pop = pop_data.get(year)
            gdp_per_capita = gdp_per_capita_data.get(year)
            
            # 只有当三项数据都有时才添加
            if gdp and pop and gdp_per_capita:
                all_data.append({
                    '国家': country_name,
                    '国家代码': country_code,
                    '年份': year,
                    'GDP(美元)': gdp,
                    '人口': pop,
                    '人均 GDP(美元)': gdp_per_capita,
                })
        
        print(f"✅ {country_name} 抓取完成")
    
    # 转换成 DataFrame（类似 Excel 表格的数据结构）
    if not all_data:
        print("\n❌ 抱歉，没有抓取到任何数据，请检查网络连接")
        return
    
    df = pd.DataFrame(all_data)
    
    # 添加计算列：人均 GDP（自己算的，验证一下）
    df['人均 GDP 计算值 (美元)'] = df['GDP(美元)'] / df['人口']
    
    # 格式化大数字，让它更易读
    def format_large_number(num):
        if num >= 1e12:
            return f"{num/1e12:.2f} 万亿"
        elif num >= 1e9:
            return f"{num/1e9:.2f} 亿"
        elif num >= 1e6:
            return f"{num/1e6:.2f} 百万"
        else:
            return f"{num:.0f}"
    
    # 创建展示用的表格（格式化后）
    df_display = df.copy()
    df_display['GDP(美元)'] = df_display['GDP(美元)'].apply(format_large_number)
    df_display['人口'] = df_display['人口'].apply(format_large_number)
    df_display['人均 GDP(美元)'] = df_display['人均 GDP(美元)'].apply(lambda x: f"${x:,.0f}")
    df_display['人均 GDP 计算值 (美元)'] = df_display['人均 GDP 计算值 (美元)'].apply(lambda x: f"${x:,.0f}")
    
    # 生成文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    excel_filename = f'各国 GDP 数据_{timestamp}.xlsx'
    csv_filename = f'各国 GDP 数据_{timestamp}.csv'
    
    # 导出为 Excel
    df_display.to_excel(excel_filename, index=False, sheet_name='各国 GDP 数据')
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    # 打印摘要
    print("\n" + "=" * 50)
    print("✅ 数据抓取完成！")
    print("=" * 50)
    print(f"📁 Excel 文件：{excel_filename}")
    print(f"📁 CSV 文件：{csv_filename}")
    print(f"📊 共 {len(df)} 条数据记录")
    print(f"🌍 国家数：{len(COUNTRIES)}")
    print(f"📅 年份范围：{START_YEAR} - {END_YEAR}")
    
    # 显示最新一年的数据摘要
    latest_year = END_YEAR
    latest_data = df[df['年份'] == latest_year]
    if not latest_data.empty:
        print(f"\n📈 {latest_year} 年数据摘要（按 GDP 排序）：")
        summary = latest_data[['国家', 'GDP(美元)', '人均 GDP(美元)']].copy()
        summary = summary.sort_values('GDP(美元)', ascending=False)
        summary['GDP(美元)'] = summary['GDP(美元)'].apply(format_large_number)
        summary['人均 GDP(美元)'] = summary['人均 GDP(美元)'].apply(lambda x: f"${x:,.0f}")
        print(summary.to_string(index=False))
    
    print("\n🎉 搞定！你可以用 Excel 打开文件查看完整数据")


if __name__ == '__main__':
    main()
