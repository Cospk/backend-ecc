---
name: becc-impact-discovery
description: 在实现、重构或排障前，先收敛可能受影响的系统、模块、代码路径与风险面。适用于需要控制触达范围的 Go 后端任务。
origin: backend-ecc
---

# becc-impact-discovery

用于在开始修改前，先识别最可能受影响的代码面与相邻风险。

## 何时使用

以下场景优先使用这个 skill：
- 需求或 bug 已经大致明确，但不知道改哪些模块
- 改动可能跨 handler / service / repository / config / migration
- 需要先判断哪些系统会受影响
- 需要先找相似路径和关键调用链
- 希望先控制 diff 触达范围，再决定怎么改

不要把这个 skill 用于：
- 问题本身还没 framing 清楚的任务
- 已经定位到单文件小修的简单任务

## 核心意图

这个 skill 的目标不是“把仓库搜一遍”，而是收敛出：

1. primary affected system
2. directly affected modules/files
3. likely adjacent systems
4. likely execution path
5. risk surface
6. confidence / unknowns

## 所在 loop

这个 skill 主要位于：
- **Impact & Validation Loop**

典型循环：
- 输入已 framing 的问题
- 先做图谱或结构路由
- 查相似模式
- 收敛影响面
- 输出验证需要覆盖的风险面

## 不可妥协的规则

助手必须：
1. 优先收敛影响面，而不是追求“全读完”
2. 如果图谱工具可用，优先使用 Graphify / understand-anything
3. 在扩大源码阅读前，先做一次搜索前置检查：
   - repo 内是否已有相似实现路径
   - 当前可用的结构化路由渠道有哪些
   - 哪些渠道当前不可用，必须诚实说明
4. 区分直接影响与相邻影响
5. 明确指出置信度与未知点
6. 明确指出哪些区域大概率不受影响

助手不得：
- 跳过已有模式查找，直接假设需要新建路径或新抽象
- 把“可能相关”全部堆成大清单
- 在没有足够依据时声称 root cause 已确定
- 把查到的所有代码都当成必须修改范围

## 输入

输入通常来自：
- `becc-problem-framing` 的输出
- 已知错误现象或需求描述
- graph query 结果
- 相似实现模式
- 搜索前置检查得到的 repo 内现有路径候选

## 输出

输出至少应包含：

### 1. Problem Summary
一句话问题摘要。

### 2. Affected Systems
- primary affected system
- directly affected modules / files
- likely adjacent systems
- likely not affected areas

### 3. Code Path Hypothesis
- 可能入口
- 可能执行链
- 关键分支点
- 关键依赖触点

### 4. Risk Surface
- regression risk
- config / data risk
- rollout risk
- validation risk

### 5. Confidence / Unknowns
- 当前判断置信度
- 仍需补证据的点
- 当前有哪些搜索/路由渠道不可用

## 停下来询问的条件

遇到以下情况必须停下：
- framing 不清，无法判断从哪里开始 scope
- 仓库边界不清，无法确认目标 module
- 图谱和代码读取得出冲突结论
- 关键路径仍有多种互斥解释

## 完成态要求

只有在以下条件成立时，才可把 impact discovery 视为完成：
- primary affected system 已收敛
- 直接影响面已收敛到可行动范围
- 相邻风险已列出
- 关键未知点已明确
- 后续验证面可由此推导

否则结果必须标记为：
- `partial`：已有候选路径，但范围仍不稳
- `blocked`：缺少仓库上下文或关键证据

## 与其他资产的关系

这个 skill 通常连接到：
- `becc-impact-scope`
- `becc-problem-statement`
- `becc-impact-map`
- `becc-verification-gate`
- 后续 design / verify 行为

它的职责是：

> 在真正改代码前，用最小阅读量收敛最可能正确的影响范围。
