"""
Pigeon-Agent-Simulation-Framework — 智能体定义模块
每个Agent的行为由参数驱动的随机过程模拟。
"""

import random
import math
from typing import List, Dict, Optional


class SimulationAgent:
    """模拟智能体基类"""

    def __init__(self, config: dict):
        self.id = config["id"]
        self.name = config["name"]
        self.nickname = config["nickname"]
        self.personality = config["personality"]
        self.debt_style = config["debt_style"]

        # 行为参数: [违约概率基础, 过度承诺倾向, 债权追索强度, 借口创造力]
        self.params = self._init_params()

        # 运行时状态
        self.total_promises_made = 0      # 累计承诺次数
        self.total_promises_kept = 0      # 累计兑现次数
        self.excuses_used = []            # 借口历史
        self.debt_owed = 0.0              # 欠别人的总金额
        self.debt_owed_to = {}            # {债权人id: 金额}
        self.credit_score = 800           # 初始信用分

    def _init_params(self) -> dict:
        """根据角色类型初始化行为参数"""
        params_map = {
            "pigeon": {
                "default_prob": 0.92, "overpromise": 0.3,
                "collect_intensity": 0.05, "excuse_creativity": 0.85,
                "forget_rate": 0.1,
            },
            "pleaser": {
                "default_prob": 0.65, "overpromise": 0.95,
                "collect_intensity": 0.1, "excuse_creativity": 0.3,
                "forget_rate": 0.05,
            },
            "bookkeeper": {
                "default_prob": 0.05, "overpromise": 0.1,
                "collect_intensity": 0.98, "excuse_creativity": 0.05,
                "forget_rate": 0.0,
            },
            "fish": {
                "default_prob": 0.50, "overpromise": 0.6,
                "collect_intensity": 0.02, "excuse_creativity": 0.2,
                "forget_rate": 0.95,
            },
            "slacker": {
                "default_prob": 0.85, "overpromise": 0.15,
                "collect_intensity": 0.0, "excuse_creativity": 0.1,
                "forget_rate": 0.3,
            },
            "workaholic": {
                "default_prob": 0.88, "overpromise": 0.4,
                "collect_intensity": 0.2, "excuse_creativity": 0.6,
                "forget_rate": 0.15,
            },
        }
        base = params_map.get(self.id, params_map["pigeon"])
        # 基于性格微调
        return dict(base)

    def generate_excuse(self, week: int, shock_active: bool = False,
                        shock_info: Optional[str] = None) -> str:
        """根据参数生成借口"""
        creativity = self.params["excuse_creativity"]
        r = random.random()

        # 基础借口库
        basic_excuses = [
            "牙医预约", "临时加班", "身体不舒服", "家里有事",
            "路上堵车", "要陪爸妈", "有快递要收", "猫生病了",
            "下周一定", "下下周一定", "下个月一定",
        ]
        creative_excuses = [
            "我刚发现我的水瓶座水逆了今天不宜社交",
            "我的量子物理课作业还没交，教授说了不交就挂科",
            "我室友的猫的闺蜜的狗要生了，我得去帮忙接生",
            "今天出门的时候发现鞋带断了，这是个bad omen，我不能出门",
            "我的第二自我今天需要独处时间来进行内在对话",
            "我刚在短视频里看到今天不宜聚餐，会破财",
            "我的塔罗牌说今天如果出门会有血光之灾(指钱包出血)",
            "我发现我其实社恐，但不是普通的社恐，是量子叠加态社恐",
        ]

        if shock_active and shock_info:
            return f"({shock_info}) 而且我真的没办法！不是借口！"

        if r < creativity * 0.6:
            return random.choice(creative_excuses)
        elif r < creativity * 0.6 + 0.3:
            return f"{random.choice(basic_excuses)}，真的不是故意的！下次一定！"
        else:
            return f"{random.choice(['诶对了我突然想起来','啊不好意思刚接到通知','是这样的'])}我{random.choice(['要出差','要开会','有急事','突然不舒服'])}，{random.choice(['下周','下下周','下个月'])}一定！"

    def make_promise(self, amount: float) -> bool:
        """是否做出承诺（决定是否产生新债务）"""
        # 过度承诺倾向越高越容易答应
        threshold = 1.0 - self.params["overpromise"] * 0.7
        decision = random.random() > threshold
        if decision:
            self.total_promises_made += 1
        return decision

    def keep_promise(self) -> bool:
        """是否兑现承诺"""
        default_prob = self.params["default_prob"]
        # 信用分越低越容易违约
        effective_prob = default_prob + (800 - self.credit_score) * 0.0003
        kept = random.random() > effective_prob
        if kept:
            self.total_promises_kept += 1
        return kept

    def forget_debt(self) -> bool:
        """是否忘记债务（鱼系特征）"""
        return random.random() < self.params["forget_rate"]

    def collect_debt(self, week: int) -> float:
        """债权追索行为：返回追回金额"""
        intensity = self.params["collect_intensity"]
        # 正常追索
        if random.random() < intensity * 0.3:
            # 追回部分债务
            total_owed_to = sum(self.debt_owed_to.values())
            if total_owed_to > 0:
                recovery = total_owed_to * random.uniform(0.05, 0.2)
                return recovery
        return 0.0


def get_agents_for_group(agents_config: List[dict]) -> List[SimulationAgent]:
    """从配置创建agent实例列表"""
    return [SimulationAgent(cfg) for cfg in agents_config]
