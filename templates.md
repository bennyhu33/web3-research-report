# Web3 投研报告模板库

本文档定义了三种深度的投研报告模板。

---

## 图表生成说明（Deep 版核心更新）

**重要：Word/PDF 报告中的图表必须使用 `chart_generator.py` 生成真实 PNG 图片，再通过 python-docx 插入文档。**

### 图表生成脚本

**路径：** `scripts/chart_generator.py`

**依赖安装：**
```bash
pip install matplotlib Pillow numpy
```

**使用方式：**
```python
from chart_generator import generate_charts, chart_config

# 生成全部图表
generate_charts(token_symbol, data, output_dir='/tmp/charts/')

# 或按类型生成
generate_charts(token_symbol, data, chart_types=['price_timeline', 'supply_pie', 'valuation'])
```

**支持的图表类型：**

| 类型 | 函数 | 说明 |
|------|------|------|
| `price_timeline` | `price_line()` | 价格历史走势图，含 ATH/当前标注 |
| `supply_pie` | `supply_pie()` | 代币供应分布饼图 |
| `revenue_bar` | `revenue_bar()` | 收入/发射量柱状图 |
| `growth_line` | `growth_line()` | 双轴：子网数+用户数增长曲线 |
| `valuation_bars` | `valuation_bars()` | 估值情景对比柱状图 |
| `risk_matrix` | `risk_matrix()` | 风险评估矩阵（双图） |
| `holders_bar` | `holders_bar()` | 持仓地址分布柱状图 |
| `comparable_radar` | `comparable_radar()` | 可比项目多维度雷达图 |
| `fee_mcap_bar` | `fee_mcap_bar()` | Fees/MCap 可比公司柱状图 |

**在 Word 中插入图表：**
```python
from docx import Document
doc = Document()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run()
run.add_picture('/tmp/charts/price_timeline.png', width=Inches(6.2))
# 图注
cap = doc.add_paragraph('图：代币价格走势（202X-202X）')
cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
```

---

## 模板 A：快速扫描版 (Quick Scan)

**产出：** 执行摘要 + 风险/催化剂（约500字）
**适用：** 初步筛选、每日行情快速点评
**耗时：** ~1-3分钟

### 结构

```
1. 执行摘要
   - 评级（买入/持有/卖出）
   - 目标区间（可选）
   - 3个最大催化剂
   - 3个最大风险
   - 关键监控指标（1-3个）
2. 一句话结论（≤30字）
```

---

## 模板 B：标准投研版 (Standard)

**产出：** 完整12章节（无图表）
**适用：** 常规项目研究、日常投研报告
**耗时：** ~5-8分钟

### 结构

```
1. 免责声明与合规提示
2. 执行摘要
   - 评级（买入/持有/卖出）
   - 目标区间（3个月/6个月/12个月）
   - 3个最大催化剂
   - 3个最大风险
   - ≥5个关键监控指标
3. 方法与数据来源
4. 项目概述
   - 愿景与使命
   - 产品/协议功能（表格）
   - 技术架构简述
   - 路线图（含日期）
5. 代币经济与治理
   - 发行量、分配比例（表格）
   - 解锁日历（表格）
   - 质押/回购/销毁机制
6. 技术与安全
   - 审计摘要
   - 已知漏洞及修复
7. 链上数据与市场指标
   - TVL/OI/交易量/流动性深度
   - 活跃地址、持仓集中度
   - 交易所上市情况
8. 竞争格局与可比项目
   - ≥3个可比项目对比表（A表）
9. 估值分析
   - 三种情景（保守/基准/乐观）（D表）
10. 交易策略与执行（E表）
    - 入场/止损/止盈/对冲
11. 假设与数据缺口清单
12. 结论（≤3句话）
```

### 必需表格

| 表格 | 必须 | 内容 |
|------|------|------|
| A. 可比项目对比 | ✅ | TVL/FDV/年化Fees/回流机制/主要风险 |
| B. 代币分配与解锁 | ✅ | 占比/解锁规则/未来12月释放 |
| C. 主要持仓地址 | ❌ | —（深度版包含） |
| D. 估值情景假设 | ✅ | 假设/估值方法/隐含价格/概率 |
| E. 交易策略触发 | ✅ | 入场/止损/止盈/对冲 |

---

## 模板 C：深度分析版 (Deep)

**产出：** 完整12章节 + 5个全表格 + 真实 PNG 图表
**适用：** 重点标的、机构级报告、正式分享
**耗时：** ~10-15分钟

### 结构

在标准版基础上，全部章节完整输出，并增加：

### 完整表格（5个全含）

| 表格 | 必须 | 新增内容 |
|------|------|---------|
| A. 可比项目对比 | ✅ | + 30d Perp Volume / 质押收益率 |
| B. 代币分配与解锁 | ✅ | + 数据来源 / 可信度评级 |
| C. 主要持仓地址 | ✅ | + 标签/链/持仓数量/30天净变动/来源 |
| D. 估值情景假设 | ✅ | + 折现率/现金流口径 |
| E. 交易策略触发 | ✅ | + 加仓/减仓规则 |

### 图表输出（真实 PNG，Deep 版必须）

#### 标准 7 张图表

**1. 价格走势图（必须）**
```
图表标题：代币价格走势与关键事件
内容：历史价格线 + ATH 标注 + 当前价格 + 关键事件时间线
```

**2. 代币供应分布饼图（必须）**
```
图表标题：代币流通量分布
内容：流通/质押/团队/国库占比（带数值标签）
```

**3. 收入/发射量柱状图（必须）**
```
图表标题：日均收入/发射量对比
内容：各子网/各项目的日均发射或收入柱状图
```

**4. 生态增长双轴图（必须）**
```
图表标题：生态增长轨迹
内容：左轴-子网/矿工数柱状图 + 右轴-用户/OI增长曲线
```

**5. 估值情景对比柱状图（必须）**
```
图表标题：价格目标情景对比
内容：悲观/当前/基准/乐观/牛市价格柱状图（带数值标签）
```

**6. 风险评估矩阵（必须）**
```
图表标题：风险评估矩阵
内容：
  左图：各风险项评分（水平条形图，颜色区分高中低）
  右图：质押收益 vs 通胀对比柱状图
```

**7. 可比项目对比图（必须）**
```
图表标题：可比项目市值 vs Fees/MCap 对比
内容：左轴-市值柱状图 + 右轴-Fees/MCap 折线/柱状图
```

#### Word 插入示例

```python
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 插入图表（居中，宽 6.2 英寸保持清晰度）
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run()
run.add_picture('/tmp/charts/price_timeline.png', width=Inches(6.2))

# 图注（斜体灰色小字）
cap = doc.add_paragraph('图：代币价格走势与关键事件（2023-2026）')
cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap.runs[0].font.size = Pt(9)
cap.runs[0].italic = True
```

---

## 模板选择参数

| 参数 | 值 | 说明 |
|------|-----|------|
| `--depth` | `quick` / `standard` / `deep` | 报告深度 |
| `--include-tables` | `A,B,C,D,E` 或 `all` | 输出哪些表格 |
| `--include-charts` | `matplotlib` / `mermaid` / `none` | 输出哪些图表（Deep 默认 matplotlib） |
| `--max-length` | `500` / `2000` / `5000` | 最大字数限制 |

### 使用示例

```bash
# 快速扫描
/research Hyperliquid --chain eth --depth quick

# 标准版（无图表）
/research Hyperliquid --chain eth --depth standard

# 深度版（真实 PNG 图表 + 全表格）
/research Hyperliquid --chain eth --depth deep

# 自定义：标准版但只要 A+B 表格
/research Hyperliquid --chain eth --depth standard --include-tables A,B
```

---

## 约束与原则（所有模板通用）

- **关键结论必须量化**，无法获取的数据标注「未得：原因 + 替代获取方式」
- **所有事实陈述必须带来源**（官网/白皮书/链上浏览器/第三方平台）
- **超出12个月的数据仅用于背景**，并注明日期
- **风险必须包含下行情景**，不止唱多
- **「未得」项必须给出替代获取路径**
- **Deep 版图表必须为真实 PNG，插入 Word 时图注居中斜体**

---

## 结束前自检清单

□ 所有数据是否带来源引用？
□ 「未得」项是否标注原因 + 替代方式？
□ 关键结论是否量化？
□ 风险是否包含下行情景？
□ 表格数据是否完整无空值？（Deep 版）
□ **图表是否为真实 PNG 文件而非 Mermaid 代码？**（Deep 版）
□ **图表是否已通过 python-docx 插入 Word 文档？**（Deep 版）
□ 结论是否 ≤3句话？
