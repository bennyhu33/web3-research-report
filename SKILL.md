---
name: web3-research-report
description: |
  Web3 项目代币投研报告生成器。使用华尔街分析师框架，支持三种深度模板：
  - Quick Scan（快速扫描）：执行摘要 + 风险/催化剂，约500字
  - Standard（标准投研）：完整12章节，无图表
  - Deep（深度分析）：12章节 + 全表格 + 真实 PNG 图表

  模板定义详见 templates.md，图表生成器详见 scripts/chart_generator.py
argument-hint: <代币名称或地址> --chain <链> --depth <quick|standard|deep> --include-tables <A,B,C,D,E> --include-charts <matplotlib|none>
---

# Web3 投研报告生成器

## 功能说明

生成标准化 Web3 项目/代币投研报告，采用华尔街分析师框架。

**模板定义：** 详见 `./templates.md`  
**图表生成器：** 详见 `./scripts/chart_generator.py`

## 快速开始

```
/research [项目名] --chain [链] --depth [深度]
```

**示例：**
```
/research Hyperliquid --chain eth --depth deep
/research BONK --chain sol --depth standard
/research WIF --chain sol --depth quick
```

## 可配置参数

| 参数 | 必须 | 默认值 | 说明 |
|------|------|--------|------|
| 代币名称/地址 | ✅ | — | 项目名称或合约地址 |
| `--chain` | ✅ | — | 链：`sol` / `bsc` / `eth` / `base` |
| `--depth` | ❌ | `standard` | 报告深度 |
| `--include-tables` | ❌ | `all` | 输出哪些表格：`A,B,C,D,E` 或 `all` |
| `--include-charts` | ❌ | 视 depth 而定 | 图表类型：`matplotlib` / `none`（Deep 默认 matplotlib） |

### 深度说明

| 深度 | 章节数 | 表格 | 图表 | 适用场景 | 耗时 |
|------|--------|------|------|----------|------|
| `quick` | 精简 | 无 | 无 | 初步筛选 | ~1-3分钟 |
| `standard` | 12章节 | A/B/C/D | 无 | 常规报告 | ~5-8分钟 |
| `deep` | 12章节 | A/B/C/D/E | **8张真实 PNG** | 重点标的 | ~10-15分钟 |

### 图表说明（Deep 版）

**注意：Deep 版使用 `matplotlib` 生成真实 PNG 图片，通过 `python-docx` 插入 Word 文档，不再使用 Mermaid 代码。**

| 图表 | 内容 |
|------|------|
| chart1_price_timeline | 代币历史价格走势图，含 ATH 和当前价格标注 |
| chart2_supply_pie | 代币供应分布饼图（流通/质押/团队/国库） |
| chart3_revenue_bar | 各子网/项目日均发射量柱状图 |
| chart4_growth | 双轴增长图（子网数柱状 + 矿工/用户数曲线） |
| chart5_valuation | 估值情景对比柱状图（悲观/基准/乐观） |
| chart6_risk | 风险评估矩阵（风险评分 + 质押收益 vs 通胀） |
| chart7_comparable | 可比项目市值 vs Fees/MCap 双轴图 |
| chart8_holders | 持仓地址分布水平柱状图 |

### 表格说明

| 表格 | 内容 | quick | standard | deep |
|------|------|:-----:|:--------:|:----:|
| A. 可比项目对比 | TVL/FDV/Fees/回流/风险 | — | ✅ | ✅+ |
| B. 代币分配与解锁 | 占比/解锁/释放 | — | ✅ | ✅+ |
| C. 主要持仓地址 | 标签/数量/净变动 | — | — | ✅ |
| D. 估值情景假设 | 假设/方法/价格 | — | ✅ | ✅ |
| E. 交易策略触发 | 入场/止损/止盈/对冲 | — | ✅ | ✅+ |

**+ 表示深度版有额外字段**

## 图表生成（Deep 版必须步骤）

### Step 1：安装依赖

```bash
pip install matplotlib Pillow numpy python-docx
```

### Step 2：在报告中调用

```python
from scripts.chart_generator import generate_charts

# 准备数据
data = {
    'symbol': 'TAO',
    'current_price': 245,
    'ath_price': 759,
    'supply': {'circulating': 10.1, 'staked': 6.5, 'team_locked': 0.5, 'treasury': 1.0, 'total': 21.0},
    'price_history': {'dates': [...], 'prices': [...]},
    'revenue': {'labels': [...], 'values': [...]},
    'valuation': {'scenarios': [...], 'prices': [...]},
    'risks': {'labels': [...], 'scores': [...]},
    ...
}

# 生成图表到指定目录
output_dir = '/root/.openclaw/workspace/tmp_files/charts/'
generate_charts('TAO', data, output_dir=output_dir)
```

### Step 3：插入 Word 文档

```python
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run()
run.add_picture(output_dir + 'chart1_price_timeline.png', width=Inches(6.2))

cap = doc.add_paragraph('图：代币价格走势与关键事件')
cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap.runs[0].font.size = Pt(9)
cap.runs[0].italic = True
```

## 数据获取优先级

1. 项目官网、Docs、白皮书、官方公告
2. CoinGecko / CoinMarketCap（价格/市值/供应量）
3. GMGN CLI（`gmgn-cli token info/security/holders`）— BSC/SOL/Base
4. DeFiLlama / Dune / Glassnode（TVL/协议数据）
5. taostats.io / taorevenue.com（Bittensor 专用）
6. 审计报告（OpenZeppelin / Trail of Bits）
7. 主流媒体（The Block / Cointelegraph / The Defiant）

## 核心约束

- **关键结论必须量化**
- 无法获取的数据标注「未得：原因 + 替代获取方式」
- 所有事实陈述必须带来源
- 超出12个月的数据仅用于背景并注明日期
- **风险必须包含下行情景**，不止唱多
- **Deep 版图表必须为真实 PNG，插入 Word 时附图注**

## 注意事项

- 本工具输出仅供教育研究目的，**不构成投资建议**
- 报告质量依赖于可获取的数据量，部分项目可能数据有限
- 涉及财务决策前请自行核实数据并咨询专业人士
- 图表生成依赖 `matplotlib` + `Pillow` + `numpy`，首次使用需 `pip install`

## 相关工具

- **gmgn-cli** — 链上数据查询（持仓、K线、交易数据）
- **CoinGecko API** — 价格、市场数据
- **DeFiLlama** — TVL、协议数据
- **chart_generator.py** — 标准8张投研图表生成器

## 完整使用示例

```bash
# 标准版（无图表）
/research Hyperliquid --chain eth --depth standard

# Deep 版（8张 PNG 图表 + 5个完整表格）
/research Bittensor --chain eth --depth deep

# 标准版但只要 A+B 表格
/research BONK --chain sol --depth standard --include-tables A,B
```
