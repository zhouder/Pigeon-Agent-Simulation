"""
Pigeon-Agent-Simulation-Framework — 主入口
运行两个平行宇宙的52周模拟
"""

import os
import sys
import random

# 添加项目根目录到 path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import CONTROL_AGENTS, ABLATION_AGENTS
from src.agents import get_agents_for_group
from src.simulation import run_simulation
from src.export import (export_weekly_csv, export_debt_csv,
                        export_excuse_stats_json, export_summary)


RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def main():
    # =========================================
    # 对照组: 含记账狂
    # =========================================
    control_agents = get_agents_for_group(CONTROL_AGENTS)
    control_engine = run_simulation(
        agents=control_agents,
        group_name="【对照组】含记账狂 — 理性监督者存在",
        weeks=52,
        seed=42,
    )

    # =========================================
    # 实验组: 记账狂 → 鱼系青年(消融实验)
    # =========================================
    ablation_agents = get_agents_for_group(ABLATION_AGENTS)
    ablation_engine = run_simulation(
        agents=ablation_agents,
        group_name="【实验组】记账狂→鱼系青年 — 无理性监督者",
        weeks=52,
        seed=42,
    )

    # =========================================
    # 导出数据
    # =========================================
    # 对照组
    export_weekly_csv(control_engine, os.path.join(RESULTS_DIR, "control_weekly.csv"))
    export_debt_csv(control_engine, os.path.join(RESULTS_DIR, "control_debts.csv"))
    export_excuse_stats_json(control_engine, os.path.join(RESULTS_DIR, "control_excuses.json"))
    export_summary(control_engine, os.path.join(RESULTS_DIR, "control_summary.json"))

    # 实验组
    export_weekly_csv(ablation_engine, os.path.join(RESULTS_DIR, "ablation_weekly.csv"))
    export_debt_csv(ablation_engine, os.path.join(RESULTS_DIR, "ablation_debts.csv"))
    export_excuse_stats_json(ablation_engine, os.path.join(RESULTS_DIR, "ablation_excuses.json"))
    export_summary(ablation_engine, os.path.join(RESULTS_DIR, "ablation_summary.json"))

    print(f"\n✅ 所有结果已保存至: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
