#!/usr/bin/env python3
"""
客户信息导出脚本
用于将搜索到的商户数据整理成Excel文件，支持电话和邮箱收集
"""

import sys
import json
import re
import pandas as pd
from pathlib import Path

# 电话号码正则
PHONE_PATTERN = re.compile(r'1[3-9]\d{9}')  # 手机号
PHONE_PATTERN_2 = re.compile(r'0\d{2,3}[-\s]?\d{7,8}')  # 固话

# 电子邮箱正则
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

def clean_phone_number(phone):
    """清洗电话号码，去除空格和特殊字符"""
    if pd.isna(phone) or phone == '' or phone == 'nan':
        return None
    # 去除空格和连字符
    phone_str = str(phone).replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    return phone_str if phone_str else None

def extract_phones(text):
    """从文本中提取所有电话号码"""
    if not text:
        return []

    phones = set()

    # 提取手机号
    for match in PHONE_PATTERN.findall(text):
        phones.add(match)

    # 提取固话
    for match in PHONE_PATTERN_2.findall(text):
        cleaned = match.replace(' ', '').replace('-', '')
        phones.add(cleaned)

    return list(phones)

def extract_emails(text):
    """从文本中提取所有邮箱"""
    if not text:
        return []

    emails = set()

    for match in EMAIL_PATTERN.findall(text):
        # 过滤常见的无效邮箱
        if not any(x in match.lower() for x in ['example.com', 'test.com', 'domain.com']):
            emails.add(match.lower())

    return list(emails)

def clean_data(data):
    """清洗和过滤数据"""
    cleaned = []

    for item in data:
        # 确保有足够的数据
        if len(item) < 4:
            continue

        name = item[0] if item[0] else ''
        address = item[1] if len(item) > 1 and item[1] else ''
        city = item[2] if len(item) > 2 and item[2] else ''
        phone = clean_phone_number(item[3]) if len(item) > 3 and item[3] else None
        email = item[4].lower() if len(item) > 4 and item[4] else None

        # 至少要有名称或联系方式
        if name or phone or email:
            cleaned.append([name, address, city, phone, email])

    return cleaned

def export_to_excel(data, output_file, include_email=True):
    """
    将商户数据导出为Excel

    Args:
        data: 商户信息列表，每项为 [名称, 地址, 城市, 电话, 邮箱]
        output_file: 输出文件路径
        include_email: 是否包含邮箱列
    """
    # 清洗数据
    cleaned_data = clean_data(data)

    if not cleaned_data:
        print('没有有效数据可导出')
        return None

    # 选择列
    if include_email:
        columns = ['客户名称', '地址', '城市', '联系电话', '电子邮箱']
    else:
        columns = ['客户名称', '地址', '城市', '联系电话']
        cleaned_data = [[row[0], row[1], row[2], row[3]] for row in cleaned_data]

    # 创建DataFrame
    df = pd.DataFrame(cleaned_data, columns=columns)

    # 保存为Excel
    df.to_excel(output_file, index=False, sheet_name='客户信息')

    # 打印统计
    print(f'Excel文件已创建: {output_file}')
    print(f'共收录 {len(df)} 家商户信息')
    print(f'有电话记录: {df["联系电话"].notna().sum()}')
    if include_email:
        print(f'有邮箱记录: {df["电子邮箱"].notna().sum()}')

    return df

def interactive_export():
    """交互式导出"""
    print('=== 客户信息导出工具 ===')
    print()

    # 收集数据
    data = []
    print('请输入客户信息（输入空行结束）：')
    print('格式：客户名称, 地址, 城市, 联系电话, 电子邮箱（可选）')
    print()

    while True:
        try:
            line = input().strip()
            if not line:
                break

            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 4:
                # 提取电话和邮箱
                if len(parts) == 4:
                    parts.append(None)

                # 如果电话字段包含邮箱格式
                if EMAIL_PATTERN.match(str(parts[3])):
                    parts[4] = parts[3]
                    parts[3] = None

                data.append(parts)
            else:
                print('格式错误，请重试')

        except EOFError:
            break

    if not data:
        print('没有输入数据')
        return

    # 询问输出文件名
    output = input('\n输出文件名（默认：customers.xlsx）：').strip()
    if not output:
        output = 'customers.xlsx'
    if not output.endswith('.xlsx'):
        output += '.xlsx'

    # 询问是否包含邮箱
    include_email = input('是否包含邮箱列（y/N）：').strip().lower() == 'y'

    # 导出
    export_to_excel(data, output, include_email)

if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == '--interactive':
        interactive_export()
    elif len(sys.argv) >= 2:
        # 从文件读取
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'customers.xlsx'

        # 支持JSON格式
        if input_file.endswith('.json'):
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            # CSV格式
            df = pd.read_csv(input_file)
            data = df.values.tolist()

        include_email = '电子邮箱' in df.columns if isinstance(df, pd.DataFrame) else True
        export_to_excel(data, output_file, include_email)
    else:
        print('用法:')
        print('  python export_excel.py <数据文件.json> [输出文件.xlsx]')
        print('  python export_excel.py --interactive')
