<div align="center">

# 🕊️ 薛定谔的鸽子 · Schrödinger's Pigeon

### 基于多智能体博弈的"下次一定"次贷危机推演

[![arXiv](https://img.shields.io/badge/Paper-S.H.I.T.-violet)](https://github.com/zhouder/Pigeon-Agent-Simulation)
[![Python](https://img.shields.io/badge/python-3.12%2B-yellow)](https://python.org)
[![LaTeX](https://img.shields.io/badge/XeLaTeX-compiled-brightgreen)](https://tug.org/xelatex)
[![DOI](https://img.shields.io/badge/DOI-10.13140%2FSHIT.2.1.144514-red)](https://shitspace.xyz)
[![License](https://img.shields.io/badge/license-S.H.I.T.-blue)](LICENSE)

**当一个人说出"下次一定"时，在观测发生之前，该承诺同时处于"会兑现"与"不会兑现"的叠加态。**

</div>

---

## 📋 项目概述

本项目通过 **52周多智能体平行宇宙推演实验**，系统研究了社交网络中"下次一定"这一语言承诺行为的宏观动力学特征。我们构建了两个互相独立的模拟世界进行消融实验：

| 实验组 | 第3号Agent | 期末债务 | 泡沫指数 | 风险级 |
|--------|-----------|:--------:|:--------:|:-----:|
| **对照组** | 记账狂（理性审计者） | **1,372 元** | **97.6** | 🔴 深红 |
| **消融组** | 阿鱼（鱼系青年·七秒记忆） | **501 元** | **50.8** | 🟠 橙色 |

**核心发现：透明度悖论（Transparency Paradox）**——系统中存在绝对理性的审计者时，因其高效率记录和追索行为，反而加速了承诺-兑现的剪刀差膨胀，导致社交信用体系更快崩溃。简单说：**记住一切的人，让关系崩得更快。**

---

## 📁 仓库结构

```
📦 Pigeon-Agent-Simulation/
├── 📜 Paper.pdf                           ← 最终论文PDF（7页）
├── 📜 SHIT Template.tex                   ← LaTeX源码（可编译）
├── 📂 Pigeon-Agent-Simulation-Framework/  ← 多智能体仿真框架
│   ├── src/
│   │   ├── config.py         # Agent配置 + 外部冲击事件
│   │   ├── agents.py         # 智能体行为模型（违约/承诺/借口生成）
│   │   ├── simulation.py     # 52周仿真引擎
│   │   ├── export.py         # CSV/JSON数据导出
│   │   ├── plot_results.py   # 数据可视化（生成4张图表）
│   │   └── run_experiment.py # 主入口
│   ├── results/              # 52周模拟数据
│   ├── figures/              # 自动生成图表PDF
│   └── README.md             # 框架详细文档
├── 📂 social_debt_experiment/  ← 早期5周原型
└── .gitignore
```

---

## 🚀 快速运行

```bash
# 1. 安装依赖
pip install matplotlib seaborn pandas numpy

# 2. 运行52周双组模拟
cd Pigeon-Agent-Simulation-Framework
python src/run_experiment.py

# 3. 生成可视化图表
python src/plot_results.py

# 4. 编译论文（需XeLaTeX）
xelatex "SHIT Template.tex"
xelatex "SHIT Template.tex"
```

---

## 🧠 数学模型

### 社交债务随机微分方程

$$dD_t = \mu D_t\,dt + \sigma D_t\,dW_t + J_t\,dN_t$$

| 符号 | 含义 | 单位 |
|:---:|------|:----:|
| $D_t$ | 社交债务存量 | 元 |
| $\mu$ | 承诺生成率 | 周$^{-1}$ |
| $\sigma$ | 借口感生波动率 | 周$^{-1/2}$ |
| $dW_t$ | 维纳过程（借口随机涨落） | — |
| $J_t$ | 外部冲击跳跃幅度 | 无量纲 |

### "薛定谔的鸽子"叠加态

$$|\Psi\rangle_{\text{鸽子}} = \alpha|\text{会来}\rangle + \beta|\text{鸽子}\rangle, \quad |\alpha|^2 + |\beta|^2 = 1$$

**当 $t \to \infty$ 时，$\overline{|\beta|^2} \to 1$，波函数必然坍缩为鸽子态。**

### 社交泡沫破裂指数

$$\text{SBBI}(t) = w_1 f_D(D_t) + w_2 f_\tau(\tau_t) + w_3 f_C(C_t) + w_4 f_G(G_t) + \eta \cdot \mathbb{1}_{\text{冲击}}$$

| 区间 | 预警 | 含义 |
|:---:|:----:|------|
| 0-20 | 🟢 绿色 | 友谊健康，继续画饼 |
| 21-40 | 🟡 黄色 | 朋友开始小声抱怨 |
| 41-60 | 🟠 橙色 | 记账狂开启小本本 |
| 61-85 | 🔴 红色 | 全员信用评分崩塌 |
| 86-100 | ⚫ 深红 | **群聊濒临解散** |

---

## 🔬 外部冲击协议

| 周次 | 事件 | 效应 |
|:---:|------|:----:|
| 第11周 | 🛍️ 双十一购物节 | 违约率+200% |
| 第23周 | 📊 年终述职季 | 借口复杂度+100% |
| 第30周 | ♌ 水星逆行 | 玄学借口+300% |
| 第37周 | 🧧 春节催婚潮 | 家庭借口>50% |
| 第45周 | 🤧 倒春寒流感 | 医疗借口达峰值 |

---

## 📖 参考文献（节选）

本论文的参考文献已全面重构为互联网UGC平台真实来源：

> [1] 小红书用户"momo". (2024). *关于我鸽了闺蜜三次被拉黑这件事*.
> [2] Bilibili弹幕网. (2023). *"下次一定"考据：从白嫖UP主到当代青年的社交退避*.
> [3] 知乎匿名用户. (2025). *如何优雅地在微信上回复"改天请你吃饭"而不显得敷衍？*
> [4] 百度贴吧"弱智吧"吧友. (2024). *如果我每次都说下次一定，是不是就拥有了无数个平行的下次？*

共20篇，涵盖小红书、知乎、B站、豆瓣、贴吧、虎扑、微博、抖音等全平台。

---

## 🏛️ 作者

**鸽子博弈研究组** · 薛定谔大学 社会信用研究所 · 中国广西南宁

- 通讯作者：鸽王（never-show-up@shitspace.xyz）
- 基金项目：NEXT-TIME-114514（"下次一定"国家自然科学基金）

---

<div align="center">

**"有时候，忘记才是维持社会关系的最好方式。"**

⭐ 如果你觉得这个研究有用，欢迎 Star！

</div>
