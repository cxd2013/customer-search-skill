# Customer Search Skill

使用必应地图搜索本地商户（眼镜店、视光中心等）的联系信息，并整理成 Excel 文件。

## 功能

- 🔍 搜索本地商户联系信息
- 📋 提取商户名称、地址、电话
- 📊 整理并导出为 Excel
- 🧹 数据清洗（去空格、过滤无效记录）

## 安装

### 方式 1: 通过 URL 安装

```bash
npx skills add https://github.com/cxd2013/customer-search-skill
```

### 方式 2: 手动安装

```bash
# 解压到 skills 目录
unzip customer-search.zip -d ~/.workbuddy/skills/
```

## 使用方法

在 WorkBuddy 中说：

```
帮我搜索"眼镜店"的客户信息
```

## 搜索流程

1. 使用 Bing 地图搜索关键词
2. 提取商户信息（名称、地址、电话）
3. 切换到地图标签获取详细数据
4. 整理数据并导出 Excel
5. 数据清洗（去空格、过滤无效记录）

## 文件结构

```
customer-search/
├── SKILL.md                    # 核心技能说明
├── README.md                   # 说明文档
├── scripts/
│   └── export_excel.py         # Excel 导出脚本
└── references/
    └── search_templates.md      # 搜索关键词模板
```

## 搜索示例

- `眼镜店 视光中心 联系方式`
- `眼科医院 电话`
- `配镜中心 联系电话`

## 注意事项

- 搜狗搜索可能触发反爬虫验证，建议使用 Bing 搜索
- 部分商户可能没有联系电话，这些记录会被自动过滤

## License

MIT
