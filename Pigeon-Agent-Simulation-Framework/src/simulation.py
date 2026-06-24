"""
Pigeon-Agent-Simulation-Framework — 仿真引擎
处理52周模拟的主循环、债务演进、外部冲击
"""

import random
import math
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from src.agents import SimulationAgent


@dataclass
class DebtRecord:
    """单笔债务记录"""
    creditor_id: str
    debtor_id: str
    reason: str
    amount: float
    week_created: int
    last_updated: int
    is_next_time_status: bool = True
    paid: bool = False


@dataclass
class WeeklySnapshot:
    """每周快照"""
    week: int
    total_debt: float
    new_debt: float
    promises_made: int
    promises_kept: int
    bubble_index: float
    excuse_count: int
    shock_active: bool
    shock_name: str = ""
    agent_debts: Dict[str, float] = field(default_factory=dict)


class SimulationEngine:
    """仿真引擎"""

    # 借口分类
    EXCUSE_CATEGORIES = [
        "medical",    # 医疗类(牙医、生病)
        "work",       # 工作类(加班、DDL)
        "family",     # 家庭类(陪父母、相亲)
        "mystical",   # 玄学类(水逆、星座)
        "animal",     # 动物类(猫狗接生)
        "selfcare",   # 自我关怀(躺平、发呆)
        "weather",    # 天气类(下雨、太热)
        "commitment", # 承诺类(下次一定变体)
    ]

    def __init__(self, agents: List[SimulationAgent], group_name: str,
                 seed: int = 42):
        self.agents = agents
        self.group_name = group_name
        self.agents_map = {a.id: a for a in agents}
        random.seed(seed)

        # 债务记录
        self.debt_records: List[DebtRecord] = []
        self.weekly_snapshots: List[WeeklySnapshot] = []

        # 借口统计: {(week, agent_id, category): count}
        self.excuse_stats: Dict[Tuple[int, str, str], int] = {}

        # 每周状态
        self.current_week = 0

    def get_shock(self, week: int) -> Tuple[bool, str, str]:
        """检查本周是否有外部冲击"""
        from src.config import SHOCKS
        if week in SHOCKS:
            s = SHOCKS[week]
            return True, s["name"], s["description"]
        return False, "", ""

    def run_week(self, week: int):
        """运行一周模拟"""
        self.current_week = week
        shock_active, shock_name, shock_desc = self.get_shock(week)

        # === Phase 1: 群内交互(产生新债务) ===
        new_debt_this_week = 0.0
        promises_made = 0
        excuse_count = 0

        # 随机排序agent以模拟随机发言
        shuffled = self.agents.copy()
        random.shuffle(shuffled)

        for i, debtor in enumerate(shuffled):
            for j, creditor in enumerate(shuffled):
                if debtor.id == creditor.id:
                    continue

                # 决定是否产生新债务
                if random.random() < 0.15 + (0.05 if shock_active else 0):
                    amount = random.uniform(20, 150) * (
                        1.5 if shock_active and "双十一" in shock_name else 1.0
                    )
                    if debtor.make_promise(amount):
                        promises_made += 1
                        new_debt_this_week += amount

                        # 生成借口并分类
                        excuse = debtor.generate_excuse(
                            week, shock_active, shock_desc
                        )
                        excuse_cat = self._classify_excuse(excuse, debtor.id)
                        debtor.excuses_used.append((week, excuse, excuse_cat))
                        excuse_count += 1

                        # 记录借口统计
                        key = (week, debtor.id, excuse_cat)
                        self.excuse_stats[key] = self.excuse_stats.get(key, 0) + 1

                        # 创建债务记录
                        record = DebtRecord(
                            creditor_id=creditor.id,
                            debtor_id=debtor.id,
                            reason=excuse[:80],
                            amount=amount,
                            week_created=week,
                            last_updated=week,
                        )
                        self.debt_records.append(record)
                        debtor.debt_owed += amount
                        debtor.debt_owed_to[creditor.id] = \
                            debtor.debt_owed_to.get(creditor.id, 0) + amount

        # === Phase 2: 债务兑现阶段 ===
        promises_kept = 0
        for record in self.debt_records:
            if record.paid:
                continue

            debtor = self.agents_map[record.debtor_id]
            creditor = self.agents_map[record.creditor_id]

            # 鱼系记忆检查
            if debtor.forget_debt():
                # 忘记债务 = 债务实际消失
                record.paid = True
                debtor.debt_owed -= record.amount
                if creditor.id in debtor.debt_owed_to:
                    debtor.debt_owed_to[creditor.id] -= record.amount
                continue

            # 尝试兑现
            if debtor.keep_promise():
                promises_kept += 1
                record.paid = True
                debtor.debt_owed -= record.amount
                debtor.total_promises_kept += 1
                if creditor.id in debtor.debt_owed_to:
                    debtor.debt_owed_to[creditor.id] -= record.amount
            else:
                # 违约 → 信用分下降, 债务膨胀
                debtor.credit_score = max(200, debtor.credit_score - random.randint(5, 20))
                record.is_next_time_status = True
                record.last_updated = week
                # 债务膨胀(复利)
                inflation = record.amount * random.uniform(0.02, 0.08)
                record.amount += inflation

        # === Phase 3: 债权追索 ===
        total_collected = 0.0
        for collector in self.agents:
            collected = collector.collect_debt(week)
            if collected > 0:
                total_collected += collected
                # 从对应债务人扣减
                for record in self.debt_records:
                    if record.creditor_id == collector.id and not record.paid:
                        reduction = min(collected, record.amount)
                        record.amount -= reduction
                        collected -= reduction
                        if record.amount <= 0:
                            record.paid = True
                        if collected <= 0:
                            break

        # === Phase 4: 计算指数 ===
        active_debts = [r for r in self.debt_records if not r.paid]
        total_debt = sum(r.amount for r in active_debts)
        avg_duration = (
            sum(week - r.week_created for r in active_debts) / max(len(active_debts), 1)
        )
        avg_credit = sum(a.credit_score for a in self.agents) / len(self.agents)

        # 泡沫指数计算
        bubble = self._calc_bubble_index(
            total_debt, len(active_debts),
            avg_duration, avg_credit,
            promises_made, promises_kept,
            shock_active
        )

        # 保存快照
        snapshot = WeeklySnapshot(
            week=week,
            total_debt=round(total_debt, 2),
            new_debt=round(new_debt_this_week, 2),
            promises_made=promises_made,
            promises_kept=promises_kept,
            bubble_index=round(bubble, 2),
            excuse_count=excuse_count,
            shock_active=shock_active,
            shock_name=shock_name,
            agent_debts={a.id: round(a.debt_owed, 2) for a in self.agents},
        )
        self.weekly_snapshots.append(snapshot)

        # === Phase 5: 每周输出摘要 ===
        risk = self._risk_level(bubble)
        shock_tag = f" [冲击: {shock_name}]" if shock_active else ""
        line = (
            f"第{week:2d}周{shock_tag}: "
            f"债务={total_debt:>8.1f}元 | "
            f"泡沫指数={bubble:>5.1f} | "
            f"承诺={promises_made}次 → 兑现={promises_kept}次 | "
            f"借口={excuse_count}次 | "
            f"信用均值={avg_credit:.0f} | "
            f"风险={risk}"
        )
        return line

    def _classify_excuse(self, excuse: str, agent_id: str) -> str:
        """将借口分类"""
        keywords = {
            "medical": ["牙医", "生病", "发烧", "医院", "医生", "根管", "智齿",
                        "不舒服", "身体", "流感", "病", "痛"],
            "work": ["加班", "DDL", "项目", "会议", "季报", "汇报", "出差",
                     "述职", "KPI", "老板", "客户", "工作"],
            "family": ["妈妈", "爸爸", "父母", "相亲", "催婚", "亲戚", "回家",
                       "过年", "七大姑", "八大姨", "家里", "家人"],
            "mystical": ["水逆", "星座", "塔罗", "占卜", "量子", "运势", "玄学",
                         "bad omen", "血光", "叠加态", "内在对话"],
            "animal": ["猫", "狗", "接生", "宠物", "蚂蚁", "动物"],
            "selfcare": ["社恐", "躺平", "独处", "放松", "发呆", "心情",
                         "自我", "休息"],
            "weather": ["下雨", "天气", "太热", "太冷", "台风", "暴雨", "太阳"],
        }
        for cat, words in keywords.items():
            for w in words:
                if w in excuse:
                    return cat
        # 检查 agent 特殊
        if agent_id == "pigeon" and ("下周" in excuse or "下个月" in excuse):
            return "commitment"
        return "commitment"

    def _calc_bubble_index(self, total_debt, num_active, avg_duration,
                           avg_credit, promises_made, promises_kept,
                           shock_active) -> float:
        """计算社交泡沫破裂指数 (SBBI)"""
        # 债务规模因子 (0-40)
        debt_factor = min(40, total_debt / 30)

        # 拖欠时长因子 (0-20)
        duration_factor = min(20, avg_duration * 0.3)

        # 信用损耗因子 (0-25)
        credit_factor = max(0, (800 - avg_credit)) * 0.1

        # 承诺-兑现缺口因子 (0-15)
        total_promises = promises_made + promises_kept
        if total_promises > 0:
            gap_factor = (1 - promises_kept / max(total_promises, 1)) * 15
        else:
            gap_factor = 0

        # 冲击加成
        shock_bonus = 8 if shock_active else 0

        # 累计通胀(历史复利效应)
        total_active = sum(r.amount for r in self.debt_records if not r.paid)
        total_original = sum(r.amount for r in self.debt_records if not r.paid)

        bubble = min(99.9, debt_factor + duration_factor + credit_factor
                     + gap_factor + shock_bonus + 5)
        return max(0, bubble)

    def _risk_level(self, bubble: float) -> str:
        if bubble < 20:
            return "绿色"
        elif bubble < 40:
            return "黄色"
        elif bubble < 60:
            return "橙色"
        elif bubble < 85:
            return "红色"
        else:
            return "深红"


def run_simulation(agents: List[SimulationAgent], group_name: str,
                   weeks: int = 52, seed: int = 42) -> SimulationEngine:
    """运行完整模拟并返回引擎"""
    engine = SimulationEngine(agents, group_name, seed)

    print(f"\n{'='*60}")
    print(f"  {group_name} [{len(agents)} 个 Agent]")
    print(f"  {', '.join(a.name for a in agents)}")
    print(f"{'='*60}")

    results = []
    for week in range(1, weeks + 1):
        line = engine.run_week(week)
        results.append(line)

        # 每4周打印一次(保持输出可读)
        if week % 4 == 0 or week == 1 or week == weeks:
            print(line)

    # 最终总结
    last = engine.weekly_snapshots[-1]
    total_promises = sum(s.promises_made for s in engine.weekly_snapshots)
    total_kept = sum(s.promises_kept for s in engine.weekly_snapshots)

    summary = (
        f"\n{'='*60}\n"
        f"  {group_name} — 52周模拟总结\n"
        f"{'='*60}\n"
        f"  期末债务总额: {last.total_debt:.0f} 元\n"
        f"  最终泡沫指数: {last.bubble_index:.1f}\n"
        f"  最终风险预警: {engine._risk_level(last.bubble_index)}\n"
        f"  累计承诺次数: {total_promises}\n"
        f"  累计兑现次数: {total_kept}\n"
        f"  整体兑现率: {total_kept/max(total_promises, 1)*100:.1f}%\n"
        f"  信用均值: {sum(a.credit_score for a in engine.agents)/len(engine.agents):.0f}\n"
        f"{'='*60}\n"
    )
    print(summary)
    return engine
