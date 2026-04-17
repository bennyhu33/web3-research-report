#!/usr/bin/env python3
"""
Web3 投研报告图表生成器
==============================
使用 matplotlib 生成标准 7 张投研图表，输出真实 PNG 文件。

依赖：matplotlib, Pillow, numpy
安装：pip install matplotlib Pillow numpy

用法：
    from chart_generator import generate_charts

    data = {
        'symbol': 'TAO',
        'current_price': 245,
        'ath_price': 759,
        'ath_date': '2024-04',
        'supply': {
            'circulating': 10.1,   # M tokens
            'staked': 6.5,
            'team_locked': 0.5,
            'treasury': 1.0,
            'total': 21.0
        },
        'price_history': {
            'dates': ['2023-Q1','2023-Q2','2023-Q3','2023-Q4',
                      '2024-Q1','2024-Q2','2024-Q3','2024-Q4',
                      '2025-Q1','2025-Q2','2025-Q3','2025-Q4','2026-Q1'],
            'prices': [3, 5, 8, 12, 45, 759, 320, 240, 210, 165, 280, 320, 245]
        },
        'revenue': {
            'labels': ['Subnet 1\n(LLM)', 'Subnet 8\n(Image)', 'Subnet 3\n(Data)',
                       'Subnet 12\n(Code)', 'Subnet 22\n(Bio)', 'Subnet 32\n(Audio)'],
            'values': [800, 400, 200, 150, 100, 80]
        },
        'growth': {
            'quarters': ["Q1'24","Q2'24","Q3'24","Q4'24",
                         "Q1'25","Q2'25","Q3'25","Q4'25","Q1'26"],
            'subnets': [32, 48, 64, 80, 96, 112, 128, 128, 128],
            'miners': [2000, 3500, 5500, 7000, 8500, 9500, 10500, 11000, 11500]
        },
        'valuation': {
            'scenarios': ['Bear\n$120', 'Current\n$245', 'Base\n$280', 'Target\n$380', 'Bull\n$520'],
            'prices': [120, 245, 280, 380, 520],
            'colors': ['#e74c3c', '#16213e', '#1a1a2e', '#27ae60', '#e94560']
        },
        'risks': {
            'labels': ['Inflation\n(Hold, No Stake)', 'GPU\nCentralization',
                       'Regulatory\nUncertainty', 'Competition\n(Gensyn)',
                       'Macro\nLiquidity', 'Team\nUnlock'],
            'scores': [9, 7, 6, 6, 5, 6],
            'colors': ['#e74c3c', '#e67e22', '#f39c12', '#f39c12', '#27ae60', '#f39c12']
        },
        'comparable': {
            'names': ['TAO', 'Fetch.ai\n(FET)', 'Render\n(RENDER)',
                      'Akash\n(AKT)', 'Ocean\n(OCEAN)', 'Theta\n(TFUEL)'],
            'mcaps': [25, 15, 25, 6, 4, 12],
            'fees_ratio': [0.8, 1.0, 0.3, 2.0, 0.5, 0.2]
        },
        'holders': {
            'labels': ['Exchanges', 'Institutions', 'Staked\nValidators',
                       'Delegators', 'Team\nLocked', 'Treasury'],
            'values': [12, 22, 50, 14, 5, 10],
            'colors': ['#95a5a6', '#3498db', '#1a1a2e', '#9b59b6', '#e67e22', '#4ecdc4']
        }
    }

    generate_charts('TAO', data, output_dir='/tmp/charts/')
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    from matplotlib.patches import FancyBboxPatch
    from datetime import datetime
except ImportError as e:
    print(f"ERROR: Missing dependency '{e.name}'. Run: pip install matplotlib Pillow numpy")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# Color Palette
# ─────────────────────────────────────────────────────────────────────────────
C_MAIN    = '#1a1a2e'      # Deep navy - primary
C_ACCENT  = '#e94560'      # Coral red - highlight
C_SECOND  = '#16213e'      # Darker navy
C_LIGHT   = '#f8f9fa'      # Near-white background
C_TEXT    = '#2d2d2d'      # Dark text
C_GRID    = '#e8e8e8'      # Light grid
C_ALT1    = '#27ae60'      # Green
C_ALT2    = '#f5a623'      # Amber
C_ALT3    = '#9b59b6'     # Purple
C_WARN    = '#e74c3c'      # Red for warnings

# ─────────────────────────────────────────────────────────────────────────────
# Helper utilities
# ─────────────────────────────────────────────────────────────────────────────
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))

def style_axis(ax, ylabel='', xlabel='', title='', grid=True):
    ax.set_facecolor(C_LIGHT)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=9, color=C_TEXT)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=9, color=C_TEXT)
    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', color=C_MAIN, pad=10)
    if grid:
        ax.grid(axis='y', color=C_GRID, linewidth=0.8, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors=C_TEXT, labelsize=8.5)

def fmt_ytick(ax, fmt='${x:,.0f}'):
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: fmt.format(x=x)))

# ─────────────────────────────────────────────────────────────────────────────
# Chart 1: Price Timeline
# ─────────────────────────────────────────────────────────────────────────────
def chart_price_timeline(symbol, prices, dates, ath_price, ath_date,
                          current_price, output_path):
    """价格走势图，含 ATH 和当前价格标注"""
    fig, ax = plt.subplots(figsize=(12, 4.5))
    fig.patch.set_facecolor('white')
    style_axis(ax, ylabel='Price (USD)', title=f'{symbol} Price History & Key Events')

    # Filter out zeros
    filtered_prices = [p if p > 0 else np.nan for p in prices]
    x = np.arange(len(dates))

    ax.plot(x, filtered_prices, color=C_MAIN, linewidth=2.2, zorder=3, solid_capstyle='round')

    # Color dots: ATH in accent, others in main
    dot_colors = [C_ACCENT if p == ath_price else C_MAIN for p in filtered_prices]
    nan_mask = ~np.isnan(filtered_prices)
    ax.scatter(x[nan_mask], np.array(filtered_prices)[nan_mask],
               color=[dot_colors[i] for i in range(len(dot_colors)) if not nan_mask[i] == False],
               s=55, zorder=4)

    # ATH annotation
    ath_idx = None
    for i, (d, p) in enumerate(zip(dates, prices)):
        if p == ath_price:
            ath_idx = i
            break
    if ath_idx is not None:
        ax.annotate(f'ATH ${ath_price:,}\n({ath_date})',
                    xy=(ath_idx, ath_price),
                    xytext=(ath_idx + 1.5, ath_price * 1.08),
                    arrowprops=dict(arrowstyle='->', color=C_ACCENT, lw=1.5),
                    fontsize=9, color=C_ACCENT, fontweight='bold')

    # Current annotation
    ax.annotate(f'Current\n${current_price:,}',
                xy=(len(dates)-1, current_price),
                xytext=(len(dates)-3, current_price * 1.3),
                arrowprops=dict(arrowstyle='->', color=C_MAIN, lw=1.2),
                fontsize=9, color=C_MAIN, fontweight='bold')

    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels(dates, rotation=45, ha='right', fontsize=8)
    fmt_ytick(ax)
    ax.set_ylim(0, max(prices) * 1.25)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✓ Price timeline → {output_path}")

# ─────────────────────────────────────────────────────────────────────────────
# Chart 2: Supply Distribution Pie
# ─────────────────────────────────────────────────────────────────────────────
def chart_supply_pie(symbol, supply, output_path):
    """代币供应分布饼图"""
    fig, ax = plt.subplots(figsize=(8, 5.5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    labels = [
        f"Staked\n{supply['staked']:.1f}M ({supply['staked']/supply['total']*100:.0f}%)",
        f"Circulating\n{supply['circulating']:.1f}M ({supply['circulating']/supply['total']*100:.0f}%)",
        f"Team Locked\n{supply['team_locked']:.1f}M ({supply['team_locked']/supply['total']*100:.0f}%)",
        f"Treasury\n{supply['treasury']:.1f}M ({supply['treasury']/supply['total']*100:.0f}%)",
    ]
    sizes = [supply['staked'], supply['circulating'],
             supply['team_locked'], supply['treasury']]
    colors = [C_MAIN, C_ACCENT, C_ALT2, C_ALT1]
    explode = (0.03, 0.03, 0, 0)

    wedges, texts, = ax.pie(sizes, labels=labels, colors=colors,
                              explode=explode, startangle=90,
                              wedgeprops=dict(edgecolor='white', linewidth=2))
    for t in texts:
        t.set_fontsize(9.5)
        t.set_color(C_TEXT)

    ax.set_title(f'{symbol} Token Supply Distribution\n(April 2026)',
                 fontsize=13, fontweight='bold', color=C_MAIN, pad=15)

    # Center donut
    centre = plt.Circle((0, 0), 0.5, fc='white')
    ax.add_patch(centre)
    ax.text(0, 0.06, f"{supply['total']:.0f}M", fontsize=20, fontweight='bold',
            ha='center', va='center', color=C_MAIN)
    ax.text(0, -0.06, 'Max Supply', fontsize=10, ha='center', va='center', color=C_TEXT)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✓ Supply pie → {output_path}")

# ─────────────────────────────────────────────────────────────────────────────
# Chart 3: Revenue / Emission Bar
# ─────────────────────────────────────────────────────────────────────────────
def chart_revenue_bar(symbol, labels, values, output_path, title_override=None):
    """日均发射/收入柱状图"""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('white')
    style_axis(ax, ylabel='Daily Emission (Tokens)',
               title=title_override or f'{symbol} Daily Emission by Source')

    n = len(labels)
    colors = [C_MAIN, C_ACCENT, C_SECOND, C_ALT1, C_ALT2, C_ALT3, '#95a5a6'][:n]
    bars = ax.bar(labels, values, color=colors, edgecolor='white', linewidth=1.5, zorder=3)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.015,
                f'~{val:,}', ha='center', va='bottom', fontsize=10,
                fontweight='bold', color=C_TEXT)

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.set_ylim(0, max(values) * 1.18)
    plt.xticks(fontsize=9)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✓ Revenue bar → {output_path}")

# ─────────────────────────────────────────────────────────────────────────────
# Chart 4: Growth Dual-Axis
# ─────────────────────────────────────────────────────────────────────────────
def chart_growth_dual(symbol, quarters, primary_vals, secondary_vals,
                       primary_label, secondary_label, output_path,
                       title_override=None):
    """双轴增长图：柱状+折线"""
    fig, ax1 = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor('white')

    x = np.arange(len(quarters))
    width = 0.38

    bars = ax1.bar(x - width/2, primary_vals, width, label=primary_label,
                   color=C_MAIN, edgecolor='white', zorder=3)
    ax2 = ax1.twinx()
    line = ax2.plot(x, secondary_vals, color=C_ACCENT, linewidth=2.5,
                     marker='o', markersize=7, label=secondary_label, zorder=4)

    for bar, val in zip(bars, primary_vals):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                 f'{val:,}', ha='center', va='bottom', fontsize=8.5,
                 fontweight='bold', color=C_MAIN)

    ax1.set_xticks(x)
    ax1.set_xticklabels(quarters, fontsize=8.5)
    ax1.set_ylabel(primary_label, fontsize=9, color=C_MAIN)
    ax2.set_ylabel(secondary_label, fontsize=9, color=C_ACCENT)
    ax1.set_title(title_override or f'{symbol} Ecosystem Growth',
                  fontsize=12, fontweight='bold', color=C_MAIN, pad=12)
    ax1.grid(axis='y', color=C_GRID, linewidth=0.8)
    ax1.set_ylim(0, max(primary_vals) * 1.2)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1+lines2, labels1+labels2, loc='upper left', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✓ Growth dual-axis → {output_path}")

# ─────────────────────────────────────────────────────────────────────────────
# Chart 5: Valuation Scenarios
# ─────────────────────────────────────────────────────────────────────────────
def chart_valuation(symbol, scenarios, prices, current_price, output_path):
    """估值情景对比柱状图"""
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('white')
    style_axis(ax, ylabel='Price (USD)',
               title=f'{symbol} Price Target Scenarios')

    # Color: red for bear, navy for current, green for base/bull
    colors = []
    for s, p in zip(scenarios, prices):
        if 'Bear' in s or '悲观' in s or p < current_price * 0.7:
            colors.append(C_WARN)
        elif p == current_price:
            colors.append(C_SECOND)
        else:
            colors.append(C_ALT1)

    bars = ax.bar(scenarios, prices, color=colors, edgecolor='white',
                  linewidth=1.5, zorder=3, width=0.55)

    for bar, val in zip(bars, prices):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(prices)*0.015,
                f'${val}', ha='center', va='bottom', fontsize=11,
                fontweight='bold', color=C_TEXT)

    ax.axhline(y=current_price, color=C_SECOND, linestyle='--', linewidth=1.2, alpha=0.7)
    ax.text(len(scenarios)-1.2, current_price * 1.02, f'Current: ${current_price:,}',
            fontsize=9, color=C_SECOND)

    fmt_ytick(ax)
    ax.set_ylim(0, max(prices) * 1.2)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✓ Valuation scenarios → {output_path}")

# ─────────────────────────────────────────────────────────────────────────────
# Chart 6: Risk Matrix (dual panel)
# ─────────────────────────────────────────────────────────────────────────────
def chart_risk_matrix(symbol, risk_labels, risk_scores, risk_colors,
                        staking_yield, inflation, output_path):
    """风险评估矩阵（双图：条形+质押对比）"""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    fig.patch.set_facecolor('white')

    # Left: Horizontal risk bars
    ax = axes[0]
    ax.set_facecolor('white')
    y_pos = np.arange(len(risk_labels))
    bars = ax.barh(y_pos, risk_scores, color=risk_colors,
                   edgecolor='white', linewidth=1, zorder=3)
    ax.set_xlim(0, 11)
    ax.set_xlabel('Risk Score (1-10)', fontsize=9)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(risk_labels, fontsize=8.5)
    ax.set_title('Risk Assessment Matrix', fontsize=11, fontweight='bold',
                 color=C_MAIN, pad=10)
    ax.grid(axis='x', color=C_GRID, linewidth=0.8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for bar, val in zip(bars, risk_scores):
        ax.text(bar.get_width() + 0.12, bar.get_y() + bar.get_height()/2,
                str(val), va='center', fontsize=10, fontweight='bold', color=C_TEXT)

    # Right: Staking yield vs inflation
    ax2 = axes[1]
    ax2.set_facecolor('white')

    categories = [f'Staking Yield\n({staking_yield:.0f}%/yr)', f'Annual\nInflation\n({inflation:.1f}%)']
    y_pos2 = np.arange(len(categories))
    vals2 = [staking_yield, inflation]
    colors2 = [C_ALT1, C_WARN]

    bars2 = ax2.barh(y_pos2, vals2, color=colors2, edgecolor='white',
                      linewidth=1.5, zorder=3)
    ax2.set_xlim(0, max(inflation * 1.3, staking_yield * 1.3))
    ax2.set_xlabel('Annual Rate (%)', fontsize=9)
    ax2.set_yticks(y_pos2)
    ax2.set_yticklabels(categories, fontsize=9)
    ax2.set_title('Staking Yield vs Inflation\n(Critical)', fontsize=11,
                  fontweight='bold', color=C_MAIN, pad=10)
    ax2.grid(axis='x', color=C_GRID, linewidth=0.8)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    for bar, val in zip(bars2, vals2):
        ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                 f'{val:.1f}%', va='center', fontsize=10,
                 fontweight='bold', color=C_TEXT)

    net = staking_yield - inflation
    note = f"Net: {net:+.1f}%/yr"
    color_note = C_ALT1 if net > 0 else C_WARN
    ax2.text(0.02, 0.98, f"{'✅ Staking covers inflation' if net >= 0 else '⚠️ Inflation exceeds staking'}\n{note}",
             transform=ax2.transAxes, fontsize=9, color=color_note,
             fontweight='bold', va='top', ha='left',
             bbox=dict(boxstyle='round', facecolor='#fdecea' if net < 0 else '#eafaf1',
                      edgecolor=color_note, alpha=0.85))

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✓ Risk matrix → {output_path}")

# ─────────────────────────────────────────────────────────────────────────────
# Chart 7: Comparable Projects
# ─────────────────────────────────────────────────────────────────────────────
def chart_comparable(symbol, names, mcaps, fees_ratio, output_path):
    """可比项目对比：市值柱状+ Fees/MCap 柱状"""
    fig, ax1 = plt.subplots(figsize=(11, 5.5))
    fig.patch.set_facecolor('white')

    x = np.arange(len(names))
    width = 0.38

    # Highlight current symbol (first)
    colors_mcap = [C_ACCENT] + [C_MAIN] * (len(names) - 1)
    colors_fee = [C_ACCENT] + [C_SECOND] * (len(names) - 1)

    bars1 = ax1.bar(x - width/2, mcaps, width, label='Market Cap ($B)',
                     color=colors_mcap, edgecolor='white', alpha=0.85, zorder=3)
    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width/2, fees_ratio, width, label='Fees/MCap (%)',
                     color=colors_fee, edgecolor='white', alpha=0.85, zorder=3)

    for bar, val in zip(bars1, mcaps):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                 f'${val}B', ha='center', va='bottom', fontsize=8.5,
                 fontweight='bold', color=C_MAIN)

    for bar, val in zip(bars2, fees_ratio):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.04,
                 f'{val}%', ha='center', va='bottom', fontsize=8.5,
                 fontweight='bold', color=C_ACCENT)

    ax1.set_xticks(x)
    ax1.set_xticklabels(names, fontsize=9)
    ax1.set_ylabel('Market Cap ($B)', fontsize=9, color=C_MAIN)
    ax2.set_ylabel('Fees/MCap (%)', fontsize=9, color=C_ACCENT)
    ax1.set_title(f'Comparable Projects: Market Cap vs Fees/MCap\n({symbol} highlighted)',
                  fontsize=11, fontweight='bold', color=C_MAIN, pad=12)
    ax1.set_ylim(0, max(mcaps) * 1.25)
    ax2.set_ylim(0, max(fees_ratio) * 1.4)
    ax1.grid(axis='y', color=C_GRID, linewidth=0.8)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1+lines2, labels1+labels2, loc='upper right', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✓ Comparable projects → {output_path}")

# ─────────────────────────────────────────────────────────────────────────────
# Chart 8: Holders Distribution
# ─────────────────────────────────────────────────────────────────────────────
def chart_holders(symbol, labels, values, colors, output_path):
    """持仓地址分布水平柱状图"""
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('white')
    style_axis(ax, xlabel='Percentage (%)',
               title=f'{symbol} Token Holder Distribution')

    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, values, color=colors, edgecolor='white',
                   linewidth=1.5, zorder=3, height=0.55)

    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f'{val:.0f}%', va='center', fontsize=10,
                fontweight='bold', color=C_TEXT)

    ax.set_xlim(0, max(values) * 1.2)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✓ Holders distribution → {output_path}")

# ─────────────────────────────────────────────────────────────────────────────
# Master Generator
# ─────────────────────────────────────────────────────────────────────────────
CHART_CONFIGS = {
    'price_timeline': {
        'fn': chart_price_timeline,
        'requires': ['price_history', 'ath_price', 'current_price'],
    },
    'supply_pie': {
        'fn': chart_supply_pie,
        'requires': ['supply'],
    },
    'revenue_bar': {
        'fn': chart_revenue_bar,
        'requires': ['revenue'],
    },
    'growth': {
        'fn': chart_growth_dual,
        'requires': ['growth'],
    },
    'valuation': {
        'fn': chart_valuation,
        'requires': ['valuation'],
    },
    'risk_matrix': {
        'fn': chart_risk_matrix,
        'requires': ['risks'],
    },
    'comparable': {
        'fn': chart_comparable,
        'requires': ['comparable'],
    },
    'holders': {
        'fn': chart_holders,
        'requires': ['holders'],
    },
}

def generate_charts(symbol, data, output_dir='/tmp/charts/',
                    chart_types=None, figsize_mult=1.0):
    """
    主入口：生成全套图表。

    Args:
        symbol: 代币符号（如 'TAO'）
        data: 包含所有数据的字典（结构见文件顶部 docstring）
        output_dir: 图表输出目录
        chart_types: 要生成的图表类型列表，None=全部
        figsize_mult: 全局图表大小倍数（默认 1.0）
    """
    ensure_dir(output_dir)
    print(f"\n📊 Generating charts for {symbol}...")

    if chart_types is None:
        chart_types = list(CHART_CONFIGS.keys())

    # ── Chart 1: Price Timeline ──────────────────────────────────────────────
    if 'price_timeline' in chart_types and 'price_history' in data:
        ph = data['price_history']
        chart_price_timeline(
            symbol,
            ph['prices'], ph['dates'],
            data.get('ath_price', max(ph['prices'])),
            data.get('ath_date', ''),
            data.get('current_price', ph['prices'][-1]),
            os.path.join(output_dir, 'chart1_price_timeline.png')
        )

    # ── Chart 2: Supply Pie ───────────────────────────────────────────────────
    if 'supply_pie' in chart_types and 'supply' in data:
        chart_supply_pie(
            symbol, data['supply'],
            os.path.join(output_dir, 'chart2_supply_pie.png')
        )

    # ── Chart 3: Revenue Bar ────────────────────────────────────────────────
    if 'revenue_bar' in chart_types and 'revenue' in data:
        rev = data['revenue']
        chart_revenue_bar(
            symbol, rev['labels'], rev['values'],
            os.path.join(output_dir, 'chart3_revenue_bar.png')
        )

    # ── Chart 4: Growth Dual-Axis ───────────────────────────────────────────
    if 'growth' in chart_types and 'growth' in data:
        g = data['growth']
        chart_growth_dual(
            symbol,
            g['quarters'], g['subnets'], g['miners'],
            'Active Subnets', 'Registered Miners',
            os.path.join(output_dir, 'chart4_growth.png')
        )

    # ── Chart 5: Valuation Scenarios ────────────────────────────────────────
    if 'valuation' in chart_types and 'valuation' in data:
        v = data['valuation']
        chart_valuation(
            symbol,
            v['scenarios'], v['prices'],
            data.get('current_price', 0),
            os.path.join(output_dir, 'chart5_valuation.png')
        )

    # ── Chart 6: Risk Matrix ─────────────────────────────────────────────────
    if 'risk_matrix' in chart_types and 'risks' in data:
        r = data['risks']
        chart_risk_matrix(
            symbol,
            r['labels'], r['scores'], r['colors'],
            data.get('staking_yield', 10),
            data.get('inflation', 25.6),
            os.path.join(output_dir, 'chart6_risk.png')
        )

    # ── Chart 7: Comparable Projects ─────────────────────────────────────────
    if 'comparable' in chart_types and 'comparable' in data:
        c = data['comparable']
        chart_comparable(
            symbol,
            c['names'], c['mcaps'], c['fees_ratio'],
            os.path.join(output_dir, 'chart7_comparable.png')
        )

    # ── Chart 8: Holders Distribution ────────────────────────────────────────
    if 'holders' in chart_types and 'holders' in data:
        h = data['holders']
        chart_holders(
            symbol,
            h['labels'], h['values'], h.get('colors', [C_MAIN]*len(h['labels'])),
            os.path.join(output_dir, 'chart8_holders.png')
        )

    print(f"\n✅ All charts saved to: {output_dir}/")
    print(f"   Files: {sorted(os.listdir(output_dir))}")
    return output_dir


# ─────────────────────────────────────────────────────────────────────────────
# CLI entrypoint
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import json

    # Demo with hardcoded TAO data (same as used in TAO deep report)
    TAO_DATA = {
        'symbol': 'TAO',
        'current_price': 245,
        'ath_price': 759,
        'ath_date': 'Apr 2024',
        'staking_yield': 10,
        'inflation': 25.6,
        'supply': {
            'circulating': 10.1, 'staked': 6.5, 'team_locked': 0.5,
            'treasury': 1.0, 'total': 21.0
        },
        'price_history': {
            'dates': ["Q1'23","Q2'23","Q3'23","Q4'23",
                       "Q1'24","Q2'24","Q3'24","Q4'24",
                       "Q1'25","Q2'25","Q3'25","Q4'25","Q1'26"],
            'prices': [3, 5, 8, 12, 45, 759, 320, 240, 210, 165, 280, 320, 245]
        },
        'revenue': {
            'labels': ['S1-LLM','S8-Image','S3-Data','S12-Code','S22-Bio','S32-Audio'],
            'values': [800, 400, 200, 150, 100, 80]
        },
        'growth': {
            'quarters': ["Q1'24","Q2'24","Q3'24","Q4'24",
                         "Q1'25","Q2'25","Q3'25","Q4'25","Q1'26"],
            'subnets': [32, 48, 64, 80, 96, 112, 128, 128, 128],
            'miners': [2000, 3500, 5500, 7000, 8500, 9500, 10500, 11000, 11500]
        },
        'valuation': {
            'scenarios': ['Bear\n$120','Current\n$245','Base\n$280','Target\n$380','Bull\n$520'],
            'prices': [120, 245, 280, 380, 520]
        },
        'risks': {
            'labels': ['Inflation\n(No Stake)', 'GPU\nCentralization',
                       'Regulatory\nUncertainty', 'Competition\n(Gensyn)',
                       'Macro\nLiquidity', 'Team\nUnlock'],
            'scores': [9, 7, 6, 6, 5, 6],
            'colors': ['#e74c3c','#e67e22','#f39c12','#f39c12','#27ae60','#f39c12']
        },
        'comparable': {
            'names': ['TAO','FET','RENDER','AKT','OCEAN','TFUEL'],
            'mcaps': [25, 15, 25, 6, 4, 12],
            'fees_ratio': [0.8, 1.0, 0.3, 2.0, 0.5, 0.2]
        },
        'holders': {
            'labels': ['Exchanges','Institutions','Staked\nValidators',
                       'Delegators','Team\nLocked','Treasury'],
            'values': [12, 22, 50, 14, 5, 10],
            'colors': ['#95a5a6','#3498db','#1a1a2e','#9b59b6','#e67e22','#4ecdc4']
        }
    }

    out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/charts'
    generate_charts('TAO', TAO_DATA, output_dir=out)
