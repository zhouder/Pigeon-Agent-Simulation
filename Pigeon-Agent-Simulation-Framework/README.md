# 🕊️ Pigeon-Agent-Simulation-Framework

## 基于多智能体博弈的"薛定谔的鸽子"演化模型

### 当代社交承诺中"下次一定"的次贷危机推演

[![OpenModel](https://img.shields.io/badge/powered%20by-OpenModel.ai-blue)](https://api.openmodel.ai)
[![LaTeX](https://img.shields.io/badge/compiled%20with-XeLaTeX-brightgreen)](https://tug.org/xelatex)
[![Python](https://img.shields.io/badge/python-3.12%2B-yellow)](https://python.org)
[![DOI](https://img.shields.io/badge/DOI-10.13140%2FSHIT.2.1.144514-red)](https://shitspace.xyz)

---

## 📋 项目概述

本项目通过**多智能体平行宇宙推演实验**，系统研究了社交网络中"下次一定"这一语言承诺行为的宏观动力学特征。我们构建了两个互相独立的52周模拟世界：

| 实验组 | 角色配置 | 关键发现 |
|--------|---------|---------|
| **对照组** | 记账狂(理性审计者) + 小鸽 + 阿讨好 + 摆烂仔 + 卷王 | 债务1,372元，SBBI=97.6(深红) |
| **消融实验组** | 阿鱼(鱼系青年) + 小鸽 + 阿讨好 + 摆烂仔 + 卷王 | 债务501元，SBBI=50.8(橙色) |

**核心发现：透明度悖论**——记账狂的存在反而使债务规模扩大173.9%，泡沫指数高出近一倍。

---

## 📁 项目结构

```
Pigeon-Agent-Simulation-Framework/
├── src/                     # 源代码
│   ├── config.py            # Agent角色配置与外部冲击计划
│   ├── agents.py            # 智能体行为模型(违约/承诺/借口生成)
│   ├── simulation.py        # 52周仿真引擎核心
│   ├── export.py            # CSV/JSON数据导出工具
│   ├── plot_results.py      # 数据可视化(生成4张图表)
│   └── run_experiment.py    # 主入口(运行两组模拟)
├── results/                 # 模拟结果数据
│   ├── control_weekly.csv   # 对照组每周快照
│   ├── control_debts.csv    # 对照组债务明细
│   ├── control_summary.json # 对照组摘要
│   ├── ablation_weekly.csv  # 实验组每周快照
│   ├── ablation_debts.csv   # 实验组债务明细
│   └── ablation_summary.json# 实验组摘要
├── figures/                 # 生成图表PDF
│   ├── fig1_debt_kline.pdf
│   ├── fig2_excuse_heatmap.pdf
│   ├── fig3_phase_diagram.pdf
│   └── fig4_credit_decay.pdf
└── README.md                # 本文件
```

---

## 🚀 快速开始

### 环境要求

- Python 3.12+
- 依赖库: `pip install matplotlib seaborn pandas numpy anthropic`

### 运行模拟

```bash
# 1. 运行完整52周双组模拟
cd Pigeon-Agent-Simulation-Framework
python src/run_experiment.py

# 2. 生成可视化图表
python src/plot_results.py
```

### 编译论文

```bash
cd SHIT-中文LaTeX模版（请用XeLaTeX编译）
xelatex "SHIT Template.tex"
xelatex "SHIT Template.tex"  # 两次编译以更新交叉引用
```

---

## 🧠 方法论

### 社交债务随机微分方程

$$
dD_t = \mu D_t\,dt + \sigma D_t\,dW_t + J_t\,dN_t
$$

### "薛定谔的鸽子"叠加态

$$
|\Psi\rangle_{\text{鸽子}} = \alpha|\text{会来}\rangle + \beta|\text{鸽子}\rangle
$$

### 社交泡沫破裂指数(SBBI)

$$
\text{SBBI}(t) = w_1 f_D(D_t) + w_2 f_\tau(\tau_t) + w_3 f_C(C_t) + w_4 f_G(G_t) + \eta \cdot \mathbb{1}_{\text{冲击}}
$$

---

## 📊 实验结果

### 债务演化轨迹
对照组呈现"阶梯式增长"：每经历一次外部冲击债务跃升且无法回落。实验组通过阿鱼的"忘记"属性系统性注销债务。

### 透明度悖论 (核心发现)
记账狂(理性审计者)通过四种机制加速崩溃：
1. **债务显性化**：隐性债务被纳入资产负债表
2. **复利膨胀**：每周5%复利使名义债务指数增长
3. **信用加速衰减**：信用降幅42.6%
4. **挤兑螺旋**：大规模追索触发集体违约

### 外部冲击效应
| 冲击事件 | 效应持续时间 | 主要影响 |
|---------|------------|---------|
| 双十一购物节 | 3周 | 违约率+200% |
| 年终述职季 | 2周 | 工作借口占41% |
| 水星逆行 | 2周 | 玄学借口占34% |
| 春节催婚潮 | 5周 | 家庭借口>50% |
| 流感大爆发 | 3周 | 医疗借口55% |

---

## 🔬 参考文献

完整参考文献列表见论文第IV节，共20篇参考文献，涵盖量子社会学、拖延心理学、情感经济学和社交网络动力学等领域。

---

## 📄 开源协议

本项目基于S.H.I.T. Open License发布——你可以自由使用、修改和传播，但须注明原始作者为"鸽子博弈研究组"。

**本研究由"下次一定"国家自然科学基金资助（项目编号：NEXT-TIME-114514）**

---

*"有时候，忘记才是维持社会关系的最好方式。"*
