#!/usr/bin/env python3
"""
客户信息导出脚本
用于将搜索到的商户数据整理成Excel文件
"""

import sys
import json
import pandas as pd
from pathlib import Path

def clean_phone_number(phone):
    """清洗电话号码，去除空格"""
    if pd.isna(phone) or phone == '' or phone == 'nan':
        return None
    # 去除空格
    phone_str = str(phone).replace(' ', '')
    return phone_str if phone_str else None

def export_to_excel(data, output_file):
    """
    将商户数据导出为Excel

    Args:
        data: 商户信息列表，每项为 [名称, 地址, 城市, 电话]
        output_file: 输出文件路径
    """
    # 创建DataFrame
    df = pd.DataFrame(data, columns=['客户名称', '地址', '城市', '联系电话'])

    # 清洗电话数据
    df['联系电话'] = df['联系电话'].apply(clean_phone_number)

    # 过滤掉没有电话的记录
    df = df[df['联系电话'].notna() & (df['联系电话'] != '')]

    # 保存为Excel
    df.to_excel(output_file, index=False, sheet_name='客户信息')
    print(f'Excel文件已创建: {output_file}')
    print(f'共收录 {len(df)} 家商户信息')

    return df

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python export_excel.py <数据文件.json> [输出文件.xlsx]')
        sys.exit(1)

    data_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'customers.xlsx'

    # 读取JSON数据
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 导出Excel
    export_to_excel(data, output_file)
