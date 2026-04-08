---
name: "customer-search"
description: "使用必应地图搜索查找本地商户（眼镜店、视光中心等）的联系信息，并整理成Excel文件。当用户需要搜索客户、查找商户电话、收集联系信息或整理潜在客户名单时使用此技能。"
---

# Customer Search Skill

搜索本地商户（眼镜店、视光中心等）的联系信息，并将结果整理成Excel文件。

## 使用场景

- 搜索特定行业的商户信息（眼镜店、视光中心、眼科医院等）
- 收集商户的联系方式（电话、地址）
- 整理潜在客户名单并导出为Excel

## 搜索流程

### 1. 启动浏览器

使用 playwright-cli 启动浏览器：

```bash
playwright-cli open
playwright-cli goto "https://cn.bing.com/search?q=关键词+联系方式+电话"
```

### 2. 获取搜索结果

使用快照获取页面内容：

```bash
playwright-cli snapshot --filename=search_results.yaml
```

### 3. 提取商户信息

从搜索结果中提取：
- 商户名称
- 地址
- 联系电话

### 4. 切换到地图标签获取更多数据

如有必要，切换到地图搜索结果标签页获取更详细的信息：

```bash
playwright-cli tab-select 1
playwright-cli snapshot --filename=maps_results.yaml
```

### 5. 关闭浏览器

```bash
playwright-cli close
```

### 6. 整理数据并导出Excel

使用 Python 脚本处理数据并生成 Excel 文件：

```python
import pandas as pd

# 商户数据
data = [
    ['商户名称', '地址', '城市', '联系电话'],
    # ... 从搜索结果中提取的数据
]

# 创建DataFrame并保存
df = pd.DataFrame(data[1:], columns=data[0])
df.to_excel('output.xlsx', index=False)
```

### 7. 数据清洗

导出后可进行数据清洗：
- 去除电话号码中的空格
- 删除没有联系电话的记录
- 统一电话号码格式

## 注意事项

- 搜狗搜索可能触发反爬虫验证，建议使用 Bing 搜索
- 部分商户可能没有联系电话，这些记录应被过滤
- 地图搜索结果通常包含更详细的商户信息
