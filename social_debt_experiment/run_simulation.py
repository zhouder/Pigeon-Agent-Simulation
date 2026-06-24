#!/usr/bin/env python3
"""
《"薛定谔的鸽子"演化模型：当代社交承诺中"下次一定"的次贷危机推演》
多智能体群聊推演脚本 v1.0
"""

from anthropic import Anthropic
import os
import json
import re

# ======================== API 客户端配置 ========================
api_key = os.environ.get("OPENMODEL_API_KEY")
if not api_key:
    raise ValueError("请先设置环境变量: export OPENMODEL_API_KEY=your_key_here")

client = Anthropic(
    api_key=api_key,
    base_url="https://api.openmodel.ai"
)

MODEL = "deepseek-v4-flash"

# ======================== 人物设定 ========================
CHARACTERS = [
    {
        "name": "小鸽",
        "nickname": "鸽王本王",
        "personality": "习惯性放鸽子爱好者，每次约饭前总有'突发状况'，但态度极其诚恳。口头禅：'下次一定！'、'今天真不是故意的！'。",
        "debt_style": "欠债不还型——永远在许诺下一顿，但从不兑现。"
    },
    {
        "name": "阿讨好",
        "nickname": "好好先生",
        "personality": "重度讨好型人格，不管谁约都说'好好好！'，但实际内心并不想去，答应了之后又疯狂后悔。口头禅：'没问题！'、'都行都行！'。",
        "debt_style": "过度承诺型——同时答应所有人的饭局，结果分身乏术。"
    },
    {
        "name": "记账狂",
        "nickname": "账本本",
        "personality": "记仇+记账狂魔，每个人欠他什么都用小本本记下来，精确到'2024年3月15日小鸽欠我一杯奶茶（少冰少糖）'。口头禅：'我记下了。'、'这是第37次了。'。",
        "debt_style": "债权积累型——永远在等别人还债，但越等债务越多。"
    },
    {
        "name": "摆烂仔",
        "nickname": "爱谁谁",
        "personality": "佛系摆烂青年，对一切约饭持'都可以但大概率去不了'态度。从不主动约人，但被约时回复'到时候看吧'。口头禅：'随意'、'到时候看'、'再说'。",
        "debt_style": "债务黑洞型——既欠别人也被别人欠，但毫不在意。"
    },
    {
        "name": "卷王",
        "nickname": "时间管理大师",
        "personality": "超级大忙人，日程表以15分钟为单位切割。每次都说'等我忙完这阵子'，但永远忙不完。口头禅：'等我这个DDL过了'、'最近在搞一个大项目'。",
        "debt_style": "延期支付型——用工作当挡箭牌无限期推迟社交承诺。"
    }
]

# ======================== Prompt 模板 ========================

WEEKLY_PROMPT_TEMPLATE = """
你是群聊"【周末约饭小分队(5)】"的群聊记录生成器。这个群有5个成员，以下是他们的人物设定：

{character_descriptions}

## 当前周次：第 {week} 周
## 当前社交债务情况：
{social_debt_table}

请生成以下三部分内容（用 ===SECTION=== 分隔）：

===CHAT===
生成一段这个群本周的真实聊天记录。本周{week}前积累的"下次一定"债务已经到了临界点。请模拟5个人在群里的对话，包含：
1. 有人发起本周的约饭提议
2. 其他人各种花式找借口推脱
3. 发明新的"下次一定"变体（比如"下下周一定"、"下个月一定"、"等天气好了再说"）
4. 记账狂魔的精确统计暴击
5. 每个人都在说自己"这周真的特殊情况"，但理由越来越离谱
请让对话生动、真实、搞笑，使用中文网络聊天风格，带上人物昵称。

===DEBT===
生成本周最新的"社交债务清算表"，格式为JSON数组：
[
  {{"债权人": "人名", "债务人": "人名", "原由": "具体事由", "金额(元)": 数值, "拖欠时长(周)": 数值, "是否已处于'下次一定'状态": true/false}}
]
请根据本周的聊天内容更新债务表，加入新的债务，并更新拖欠时长。总债务条目至少8条。

===BUBBLE===
生成本周的"社交泡沫破裂指数"，格式为JSON：
{{
  "本周泡沫指数": 0-100的数值,
  "上周指数": {prev_bubble},
  "变化趋势": "上升/下降/持平",
  "风险预警": "绿色/黄色/橙色/红色/深红",
  "分析": "一段对该指数变化的分析"
}}
泡沫指数的计算依据：债务总量、债务人的违约次数、债权人耐心消耗程度、社会信用通胀率等因素。指数应该逐周上升，呈现庞氏特征。
"""

# ======================== 模拟引擎 ========================

def build_character_descriptions():
    lines = []
    for i, c in enumerate(CHARACTERS, 1):
        lines.append(f"{i}. {c['name']}（{c['nickname']}）：{c['personality']}\n   债务风格：{c['debt_style']}")
    return "\n\n".join(lines)


def format_debt_table(debt_records):
    """将债务记录格式化为可读表格"""
    if not debt_records:
        return "暂无债务记录——纯洁的友谊从无债务！(假的)"

    lines = ["| 债权人 | 债务人 | 原由 | 金额(元) | 拖欠(周) | 下次一定? |", "|--------|--------|------|----------|----------|-----------|"]
    for d in debt_records:
        status = "✅ 是" if d.get("是否已处于'下次一定'状态", False) else "❌ 否"
        lines.append(f"| {d['债权人']} | {d['债务人']} | {d['原由']} | {d['金额(元)']} | {d['拖欠时长(周)']}周 | {status} |")
    return "\n".join(lines)


def call_llm(prompt):
    """调用大模型"""
    response = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        temperature=0.95,
        system="你是一个社会学实验模拟器，擅长生成真实幽默的微信群聊内容和社交债务数据。请严格按照要求的格式输出。",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    # 处理可能存在 ThinkingBlock 的情况——从 content 中提取纯文本块
    text_parts = []
    for block in response.content:
        if hasattr(block, 'text'):
            text_parts.append(block.text)
        # ThinkingBlock 没有 .text，跳过
    return "\n".join(text_parts)


def parse_llm_output(text):
    """解析大模型输出"""
    # 提取聊天记录
    chat_match = re.search(r'===CHAT===\s*(.*?)\s*===DEBT===', text, re.DOTALL)
    chat = chat_match.group(1).strip() if chat_match else "（聊天记录解析失败）"

    # 提取债务表
    debt_match = re.search(r'===DEBT===\s*(.*?)\s*===BUBBLE===', text, re.DOTALL)
    debt_text = debt_match.group(1).strip() if debt_match else "[]"

    # 尝试解析债务 JSON
    debt_records = []
    try:
        debt_records = json.loads(debt_text)
    except json.JSONDecodeError:
        # 尝试从文本中提取 JSON 数组
        json_match = re.search(r'\[.*?\]', debt_text, re.DOTALL)
        if json_match:
            try:
                debt_records = json.loads(json_match.group())
            except json.JSONDecodeError:
                debt_records = []

    # 提取泡沫指数
    bubble_match = re.search(r'===BUBBLE===\s*(.*)', text, re.DOTALL)
    bubble_text = bubble_match.group(1).strip() if bubble_match else "{}"

    bubble_data = {}
    try:
        bubble_data = json.loads(bubble_text)
    except json.JSONDecodeError:
        json_match = re.search(r'\{.*\}', bubble_text, re.DOTALL)
        if json_match:
            try:
                bubble_data = json.loads(json_match.group())
            except json.JSONDecodeError:
                bubble_data = {"本周泡沫指数": 0, "分析": "解析失败"}

    return chat, debt_records, bubble_data


def run_simulation():
    """主模拟循环"""
    print("=" * 70)
    print('  《“薛定谔的鸽子”演化模型》多智能体推演')
    print('  当代社交承诺中“下次一定”的次贷危机')
    print("=" * 70)

    all_records = []
    debt_records = []
    prev_bubble = 0
    all_output = []

    char_desc = build_character_descriptions()

    for week in range(1, 6):
        print(f"\n{'='*50}")
        print(f"  📅 第 {week} 周推演开始...")
        print(f"{'='*50}")

        debt_table_str = format_debt_table(debt_records)

        prompt = WEEKLY_PROMPT_TEMPLATE.format(
            character_descriptions=char_desc,
            week=week,
            social_debt_table=debt_table_str,
            prev_bubble=prev_bubble
        )

        print("  🤖 正在调用大模型生成群聊内容...")
        raw_output = call_llm(prompt)

        chat, new_debts, bubble = parse_llm_output(raw_output)

        # 更新债务记录
        if new_debts:
            debt_records = new_debts

        current_bubble = bubble.get("本周泡沫指数", 0)
        prev_bubble = current_bubble

        # 组装本周输出
        week_output = f"""
{'='*70}
📅 第 {week} 周推演结果
{'='*70}

💬 群聊记录：
{chat}

📊 社交债务清算表：
{format_debt_table(debt_records)}

📈 社交泡沫破裂指数：
  本周指数：{bubble.get('本周泡沫指数', 'N/A')}
  上周指数：{bubble.get('上周指数', 'N/A')}
  变化趋势：{bubble.get('变化趋势', 'N/A')}
  风险预警：{bubble.get('风险预警', 'N/A')}
  分析：{bubble.get('分析', 'N/A')}
"""
        print(week_output)
        all_output.append(week_output)

        all_records.append({
            "week": week,
            "chat": chat,
            "debt": debt_records,
            "bubble": bubble
        })

    # 最终总结
    summary = generate_summary(all_records)
    all_output.append(summary)

    # 写入文件
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simulation_results.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(all_output))

    print(f"\n📁 结果已保存至: {output_path}")
    print(summary)

    return all_records


def generate_summary(records):
    """生成模拟总结"""
    if not records:
        return "\n\n⚠️ 无模拟数据可总结。"

    last_bubble = records[-1]["bubble"]
    debts = records[-1]["debt"]

    total_debt = sum(d.get("金额(元)", 0) for d in debts)
    total_promises = sum(1 for d in debts if d.get("是否已处于'下次一定'状态", False))

    summary = f"""

{'='*70}
📋 五周推演总结：社交债务次贷危机全景报告
{'='*70}

💰 期末债务总额：{total_debt:.0f} 元
🕊️ 处于"下次一定"状态的债务：{total_promises}/{len(debts)} 笔
📈 最终泡沫指数：{last_bubble.get('本周泡沫指数', 'N/A')} / 100
🚨 最终风险预警：{last_bubble.get('风险预警', 'N/A')}

🔑 核心发现：
1. "下次一定"本质上是一种无抵押社交信用衍生品
2. 每多一个"下次"，社交信用就经历一次微型通胀
3. 当"下次"的承诺速度超过"兑现"速度时，庞氏结构正式形成
4. 社交泡沫破裂的前兆：记账狂魔开始用电子表格管理债务

🧠 结论：当代社交承诺中的"薛定谔的鸽子"现象，
    验证了"下次一定"作为一种情感次贷产品的系统脆弱性。
"""
    return summary


if __name__ == "__main__":
    run_simulation()
