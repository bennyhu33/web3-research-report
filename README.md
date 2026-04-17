# 🌾 Web3 Research Report Skill

> 华尔街分析师框架驱动的 Web3 项目/代币投研报告生成器。支持 Quick / Standard / Deep 三种深度，Deep 版输出 8 张真实 PNG 图表 + 完整 Word 文档。

---

## 功能特性

| 深度 | 图表 | 字数 | 耗时 |
|------|------|------|------|
| Quick Scan | ❌ | ~500字 | ~1分钟 |
| Standard | ❌ | ~3000字 | ~5分钟 |
| **Deep** | ✅ **8张PNG** | ~5000字 | ~8分钟 |

---

## 目录结构

```
web3-research-report/
├── SKILL.md           # OpenClaw Skill 定义
├── templates.md       # 报告模板库（Quick/Standard/Deep 三种）
├── README.md          # 本文件
├── .gitignore
├── .env.example       # 环境变量模板
└── scripts/
    └── chart_generator.py   # 独立图表生成器（可单独使用）
```

---

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/bennyhu33/web3-research-report.git
cd web3-research-report
```

### 2. 安装依赖

```bash
pip install matplotlib Pillow numpy python-docx requests
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入你的 API Key
```

### 4. 生成图表（独立使用）

```python
import sys
sys.path.insert(0, 'scripts')
from chart_generator import generate_charts

data = {
    'symbol': 'NEAR',
    'current_price': 1.43,
    'ath_price': 20.42,
    'ath_date': 'Jan 2022',
    'supply': {
        'circulating': 1.22, 'staked': 0.55,
        'team_locked': 0.22, 'treasury': 0.20, 'total': 1.27
    },
    'price_history': {
        'dates': ["Q1'21","Q2'21","Q3'21","Q4'21"],
        'prices': [3.0, 8.5, 12.0, 20.42]
    },
    'revenue': {
        'labels': ['Ref Finance', 'Burrow', 'Octopus'],
        'values': [35, 18, 15]
    },
    'growth': {
        'quarters': ["Q3'23","Q4'23","Q1'24"],
        'subnets': [120, 180, 250],
        'miners': [15, 22, 30]
    },
    'valuation': {
        'scenarios': ['Bear $0.8', 'Current $1.43', 'Base $4.0', 'Bull $8.0'],
        'prices': [0.8, 1.43, 4.0, 8.0]
    },
    'risks': {
        'labels': ['Competition', 'Regulation', 'Tech Risk'],
        'scores': [7, 4, 5],
        'colors': ['#e74c3c','#f39c12','#27ae60']
    },
    'comparable': {
        'names': ['NEAR','SOL','AVAX','DOT'],
        'mcaps': [1.5, 95, 14, 12],
        'fees_ratio': [3.0, 2.5, 1.2, 0.8]
    },
    'holders': {
        'labels': ['Circulating','Staked','Team','Treasury'],
        'values': [45, 44, 17, 12],
        'colors': ['#95a5a6','#3498db','#1a1a2e','#9b59b6']
    }
}

generate_charts('NEAR', data, output_dir='./charts')
```

### 5. OpenClaw Skill 调用

在 OpenClaw 中直接使用自然语言：

```
出一份 NEAR 的深度投研报告（Deep版）
出一份 TAO 的标准投研报告
```

---

## 依赖说明

| 依赖 | 版本 | 用途 |
|------|------|------|
| `matplotlib` | ≥3.5 | 图表生成 |
| `Pillow` | ≥9.0 | 图片处理 |
| `numpy` | ≥1.21 | 数据计算 |
| `python-docx` | ≥0.8 | Word 文档生成 |
| `requests` | ≥2.28 | API 调用 |

---

## ⚠️ 安全声明

- **不要将 `.env` 文件提交到 GitHub！**
- 所有 API Key 通过环境变量注入，代码中不包含任何密钥
- `.env.example` 是模板，仅包含格式示例

---

## 许可证

MIT License

---

## 贡献

欢迎提交 Issue 和 Pull Request！
