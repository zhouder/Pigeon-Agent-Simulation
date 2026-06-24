"""
Pigeon-Agent-Simulation-Framework — 数据可视化脚本
生成3种图表供 LaTeX 调用
"""

import os
import sys
import json
import csv
import math
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import pandas as pd

# 项目路径
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, "results")
FIGURES = os.path.join(BASE, "figures")
os.makedirs(FIGURES, exist_ok=True)

sns.set_theme(style="whitegrid", font_scale=1.0)
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False


def load_weekly_csv(filepath: str) -> pd.DataFrame:
    """加载每周快照"""
    return pd.read_csv(filepath)


def fig1_debt_kline():
    """图1: 社交债务K线图 — 对比两组债务总额演化"""
    control = load_weekly_csv(os.path.join(RESULTS, "control_weekly.csv"))
    ablation = load_weekly_csv(os.path.join(RESULTS, "ablation_weekly.csv"))

    fig, ax1 = plt.subplots(figsize=(10, 5.5))

    # 主坐标轴: 债务总额
    ax1.plot(control["week"], control["total_debt"],
             "o-", color="#E74C3C", linewidth=2.0, markersize=3,
             label="对照组(含记账狂) 债务总额", alpha=0.85)
    ax1.plot(ablation["week"], ablation["total_debt"],
             "s-", color="#3498DB", linewidth=2.0, markersize=3,
             label="实验组(无记账狂→阿鱼) 债务总额", alpha=0.85)

    # 次坐标轴: 泡沫指数
    ax2 = ax1.twinx()
    ax2.plot(control["week"], control["bubble_index"],
             ":", color="#C0392B", linewidth=1.5, alpha=0.5,
             label="对照组 泡沫指数(SBBI)")
    ax2.plot(ablation["week"], ablation["bubble_index"],
             ":", color="#2980B9", linewidth=1.5, alpha=0.5,
             label="实验组 泡沫指数(SBBI)")

    # 外部冲击标注
    shock_weeks = [11, 23, 30, 37, 45]
    shock_names = ["双十一", "述职季", "水星逆行", "春节催婚", "流感潮"]
    for sw, sn in zip(shock_weeks, shock_names):
        ax1.axvline(x=sw, color="#2C3E50", linestyle="--", alpha=0.3, linewidth=0.8)
        ax1.text(sw, ax1.get_ylim()[1] * 0.95, sn,
                 rotation=45, fontsize=7, alpha=0.6, ha="left")

    # 临界阈值线
    ax2.axhline(y=85, color="#8E44AD", linestyle="-.", alpha=0.4,
                linewidth=1.0, label="坍缩阈值(SBBI=85)")

    ax1.set_xlabel("时间 (周)", fontsize=11)
    ax1.set_ylabel("社交债务总额 (元)", fontsize=11, color="#2C3E50")
    ax2.set_ylabel("社交泡沫破裂指数 (SBBI)", fontsize=11, color="#8E44AD")

    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left",
               fontsize=8, framealpha=0.8)

    ax1.set_xlim(0, 53)
    ax1.set_title("图1: 社交债务总额与泡沫破裂指数对比 (含外部冲击)",
                  fontsize=12, fontweight="bold", pad=12)
    ax1.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES, "fig1_debt_kline.pdf"),
                dpi=300, bbox_inches="tight")
    plt.close()
    print("✅ 图1: Debt K-line 已生成")


def fig2_excuse_heatmap():
    """图2: 借口热力图 — 52周借口类型分布"""
    # 加载两组数据
    control_excuses = json.load(
        open(os.path.join(RESULTS, "control_excuses.json"), "r", encoding="utf-8")
    )
    ablation_excuses = json.load(
        open(os.path.join(RESULTS, "ablation_excuses.json"), "r", encoding="utf-8")
    )

    categories = [
        "medical", "work", "family", "mystical",
        "animal", "selfcare", "weather", "commitment",
    ]
    cat_labels = {
        "medical": "医疗", "work": "工作", "family": "家庭",
        "mystical": "玄学", "animal": "动物", "selfcare": "自我关怀",
        "weather": "天气", "commitment": "承诺变体",
    }
    agent_labels = {
        "pigeon": "小鸽", "pleaser": "阿讨好",
        "bookkeeper": "记账狂", "slacker": "摆烂仔",
        "workaholic": "卷王", "fish": "阿鱼",
    }

    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    for idx, (data, title) in enumerate([
        (control_excuses, "对照组 (含记账狂)"),
        (ablation_excuses, "实验组 (阿鱼替代记账狂)")
    ]):
        ax = axes[idx]

        # 构建矩阵: weeks x categories (按4周聚合)
        matrix = np.zeros((52 // 1, len(categories)))

        for week_str, agents in data.items():
            week = int(week_str.split("_")[1])
            if week > 52:
                continue
            for agent_id, cats in agents.items():
                for cat, count in cats.items():
                    if cat in categories:
                        col = categories.index(cat)
                        matrix[week - 1, col] += count

        # 按4周聚合降噪
        agg_matrix = np.zeros((13, len(categories)))
        for i in range(13):
            start = i * 4
            end = min(start + 4, 52)
            agg_matrix[i, :] = matrix[start:end, :].sum(axis=0)

        # 归一化
        row_sums = agg_matrix.sum(axis=1, keepdims=True)
        row_sums = np.where(row_sums == 0, 1, row_sums)
        norm = agg_matrix / row_sums

        im = ax.imshow(norm.T, aspect="auto", cmap="YlOrRd",
                       interpolation="nearest")

        # 标注
        ax.set_yticks(range(len(categories)))
        ax.set_yticklabels([cat_labels[c] for c in categories], fontsize=9)
        ax.set_xticks(range(13))
        ax.set_xticklabels([f"{i*4+1}-{min((i+1)*4, 52)}周" for i in range(13)],
                           fontsize=7, rotation=45)
        ax.set_title(title, fontsize=11, fontweight="bold")

        # 添加数值标签
        for i in range(len(categories)):
            for j in range(13):
                val = norm[j, i]
                if val > 0.05:
                    ax.text(j, i, f"{val:.2f}",
                            ha="center", va="center",
                            fontsize=5, color="white" if val > 0.5 else "black")

    fig.suptitle("图2: 借口类型分布热力图 (4周聚合)", fontsize=13,
                 fontweight="bold", y=1.01)
    fig.colorbar(im, ax=axes, orientation="vertical",
                 fraction=0.02, pad=0.04, label="比例")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES, "fig2_excuse_heatmap.pdf"),
                dpi=300, bbox_inches="tight")
    plt.close()
    print("✅ 图2: Excuse Heatmap 已生成")


def fig3_phase_diagram():
    """图3: 泡沫破裂相图 — 承诺数 vs 兑现数"""
    control = load_weekly_csv(os.path.join(RESULTS, "control_weekly.csv"))
    ablation = load_weekly_csv(os.path.join(RESULTS, "ablation_weekly.csv"))

    # 累积承诺和兑现
    control["cum_promises"] = control["promises_made"].cumsum()
    control["cum_kept"] = control["promises_kept"].cumsum()
    ablation["cum_promises"] = ablation["promises_made"].cumsum()
    ablation["cum_kept"] = ablation["promises_kept"].cumsum()

    fig, ax = plt.subplots(figsize=(9, 8))

    # 对角线(完美兑现线)
    max_val = max(control["cum_promises"].max(), ablation["cum_promises"].max()) + 5
    ax.plot([0, max_val], [0, max_val], "--", color="#2C3E50",
            alpha=0.4, linewidth=1.5, label="完美兑现线 (100%)")

    # 80%兑现线
    ax.plot([0, max_val], [0, max_val * 0.8], ":", color="#7F8C8D",
            alpha=0.3, linewidth=1.0, label="80%兑现线")

    # 临界兑现线(预测坍缩边界)
    ax.plot([0, max_val], [0, max_val * 0.3], "-.", color="#E74C3C",
            alpha=0.4, linewidth=1.2, label="坍缩边界(30%兑现率)")

    # 对照组: 时间序列散点(带路径)
    ax.plot(control["cum_promises"], control["cum_kept"],
            "o-", color="#E74C3C", linewidth=1.5, markersize=4,
            alpha=0.7, label="对照组(含记账狂) 演化路径",
            zorder=5)
    # 起点和终点标注
    ax.scatter(control["cum_promises"].iloc[0],
               control["cum_kept"].iloc[0],
               c="#E74C3C", s=100, marker="o", zorder=6)
    ax.annotate("起点 (第1周)",
                (control["cum_promises"].iloc[0], control["cum_kept"].iloc[0]),
                fontsize=8, xytext=(5, 5), textcoords="offset points")
    ax.scatter(control["cum_promises"].iloc[-1],
               control["cum_kept"].iloc[-1],
               c="#C0392B", s=120, marker="D", zorder=6)
    ax.annotate(f"终点 (第52周)\n兑现率={control['cum_kept'].iloc[-1]/max(control['cum_promises'].iloc[-1],1)*100:.0f}%",
                (control["cum_promises"].iloc[-1], control["cum_kept"].iloc[-1]),
                fontsize=8, xytext=(-60, -20), textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color="#C0392B", alpha=0.6))

    # 实验组
    ax.plot(ablation["cum_promises"], ablation["cum_kept"],
            "s-", color="#3498DB", linewidth=1.5, markersize=4,
            alpha=0.7, label="实验组(阿鱼替代记账狂) 演化路径",
            zorder=5)
    ax.scatter(ablation["cum_promises"].iloc[-1],
               ablation["cum_kept"].iloc[-1],
               c="#2980B9", s=120, marker="D", zorder=6)
    ax.annotate(f"终点 (第52周)\n兑现率={ablation['cum_kept'].iloc[-1]/max(ablation['cum_promises'].iloc[-1],1)*100:.0f}%",
                (ablation["cum_promises"].iloc[-1], ablation["cum_kept"].iloc[-1]),
                fontsize=8, xytext=(10, -25), textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color="#2980B9", alpha=0.6))

    # 标注坍缩临界区
    ax.fill_between([0, max_val], [0, 0], [0, max_val * 0.3],
                    alpha=0.08, color="#E74C3C", label="系统坍缩区")

    ax.set_xlabel('累计"下次一定"承诺数', fontsize=11)
    ax.set_ylabel("累计实际兑现数", fontsize=11)
    ax.set_title("图3: 社交信用系统相图 — 承诺 vs 兑现",
                 fontsize=12, fontweight="bold")
    ax.legend(loc="upper left", fontsize=8, framealpha=0.8)
    ax.set_xlim(0, max_val)
    ax.set_ylim(0, max_val)
    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES, "fig3_phase_diagram.pdf"),
                dpi=300, bbox_inches="tight")
    plt.close()
    print("✅ 图3: Phase Diagram 已生成")


def fig4_credit_decay():
    """补充图4: 信用分衰减对比 (含外部冲击标注)"""
    control = load_weekly_csv(os.path.join(RESULTS, "control_weekly.csv"))
    ablation = load_weekly_csv(os.path.join(RESULTS, "ablation_weekly.csv"))

    # 加载summary获取信用均值
    control_sum = json.load(open(os.path.join(RESULTS, "control_summary.json"), "r", encoding="utf-8"))
    ablation_sum = json.load(open(os.path.join(RESULTS, "ablation_summary.json"), "r", encoding="utf-8"))

    fig, ax = plt.subplots(figsize=(10, 4.5))

    # 从export无法直接获取每周信用分，用债务变化作为代理变量
    # 实际应该跟踪信用分，这里用债务反向指标
    ax.fill_between(control["week"], 0, control["total_debt"],
                    alpha=0.15, color="#E74C3C", label="_nolegend_")

    # 右侧y轴: 信用均值
    # 我们从承诺/兑现比估算
    cum_prom_c = control["promises_made"].cumsum()
    cum_kept_c = control["promises_kept"].cumsum()
    cum_prom_a = ablation["promises_made"].cumsum()
    cum_kept_a = ablation["promises_kept"].cumsum()

    ax.plot(control["week"], cum_kept_c / cum_prom_c.replace(0, 1) * 100,
            "-", color="#C0392B", linewidth=2, alpha=0.8,
            label="对照组 累积兑现率(%)")
    ax.plot(ablation["week"], cum_kept_a / cum_prom_a.replace(0, 1) * 100,
            "-", color="#2980B9", linewidth=2, alpha=0.8,
            label="实验组 累积兑现率(%)")

    # 外部冲击
    shock_weeks = [11, 23, 30, 37, 45]
    for sw in shock_weeks:
        ax.axvline(x=sw, color="#2C3E50", linestyle="--", alpha=0.3, linewidth=0.8)
        # 添加冲击区域
        ax.axvspan(sw - 1, sw + 2, alpha=0.06, color="#F39C12")

    ax.set_xlabel("时间 (周)", fontsize=11)
    ax.set_ylabel("累积兑现率 (%)", fontsize=11)
    ax.set_title("图4: 累积兑现率演化与外部冲击效应",
                 fontsize=12, fontweight="bold")
    ax.legend(loc="lower left", fontsize=9)
    ax.set_xlim(0, 53)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES, "fig4_credit_decay.pdf"),
                dpi=300, bbox_inches="tight")
    plt.close()
    print("✅ 图4: Credit Decay 已生成")


if __name__ == "__main__":
    print("=" * 50)
    print("  📊 开始生成可视化图表...")
    print("=" * 50)

    fig1_debt_kline()
    fig2_excuse_heatmap()
    fig3_phase_diagram()
    fig4_credit_decay()

    print(f"\n✅ 所有图表已保存至: {FIGURES}/")
    print(f"   📄 fig1_debt_kline.pdf")
    print(f"   📄 fig2_excuse_heatmap.pdf")
    print(f"   📄 fig3_phase_diagram.pdf")
    print(f"   📄 fig4_credit_decay.pdf")
