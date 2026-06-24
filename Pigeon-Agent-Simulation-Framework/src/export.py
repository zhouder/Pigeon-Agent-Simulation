"""
Pigeon-Agent-Simulation-Framework — 数据导出工具
将模拟结果保存为CSV/JSON
"""

import csv
import json
from typing import List
from src.simulation import SimulationEngine


def export_weekly_csv(engine: SimulationEngine, filepath: str):
    """导出每周快照为 CSV"""
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "week", "total_debt", "new_debt", "promises_made",
            "promises_kept", "bubble_index", "excuse_count",
            "shock_active", "shock_name"
        ])
        for snap in engine.weekly_snapshots:
            writer.writerow([
                snap.week, snap.total_debt, snap.new_debt,
                snap.promises_made, snap.promises_kept,
                snap.bubble_index, snap.excuse_count,
                snap.shock_active, snap.shock_name,
            ])


def export_debt_csv(engine: SimulationEngine, filepath: str):
    """导出债务记录为 CSV"""
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "creditor_id", "debtor_id", "reason", "amount",
            "week_created", "last_updated", "paid"
        ])
        for rec in engine.debt_records:
            writer.writerow([
                rec.creditor_id, rec.debtor_id, rec.reason,
                round(rec.amount, 2), rec.week_created,
                rec.last_updated, rec.paid,
            ])


def export_excuse_stats_json(engine: SimulationEngine, filepath: str):
    """导出借口统计为 JSON"""
    # 按周+agent聚合
    data = {}
    for (week, agent_id, cat), count in engine.excuse_stats.items():
        week_str = f"week_{week}"
        if week_str not in data:
            data[week_str] = {}
        if agent_id not in data[week_str]:
            data[week_str][agent_id] = {}
        data[week_str][agent_id][cat] = count

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def export_summary(engine: SimulationEngine, filepath: str):
    """导出最终摘要"""
    last = engine.weekly_snapshots[-1]
    total_promises = sum(s.promises_made for s in engine.weekly_snapshots)
    total_kept = sum(s.promises_kept for s in engine.weekly_snapshots)

    summary = {
        "group_name": engine.group_name,
        "num_agents": len(engine.agents),
        "total_debt": last.total_debt,
        "bubble_index": last.bubble_index,
        "total_promises": total_promises,
        "total_kept": total_kept,
        "fulfillment_rate": total_kept / max(total_promises, 1),
        "risk_level": engine._risk_level(last.bubble_index),
        "shocks_triggered": [
            {"week": s.week, "name": s.shock_name}
            for s in engine.weekly_snapshots if s.shock_active
        ],
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
