---
name: becc-backend-design
description: 在 scope 已明确但实现路径仍有多种可能时，先收敛最小设计方案、tradeoff 与验证计划。适用于 Go 后端的非平凡改动。
origin: backend-ecc
---

# becc-backend-design

用于在 scope 已经清楚、但还不能直接编码时，先把设计决策最小化、结构化。

## 何时使用

以下场景优先使用这个 skill：
- 改动涉及多个模块或层次
- 有两种以上合理实现路径
- 需要在动手前明确 tradeoff
- 需要先把验证计划与实现方案绑定
- 若直接编码，容易因为路径选择错误而返工

不要把这个 skill 用于：
- scope 未明确的任务
- 单文件小修或显然只有一种实现方式的任务
- 已经有充分成熟方案，只差机械执行的任务

## 核心意图

这个 skill 的目标不是做大而全架构设计，而是收敛出：

1. 当前要解决的设计问题是什么
2. 至少两个可行方案
3. 每个方案的 tradeoff
4. 推荐路径及理由
5. 与之绑定的最小验证计划

## 所在 loop

这个 skill 主要位于：
- **Impact & Validation Loop** 的中段

典型循环：
- framing
- impact discovery / scope
- design comparison
- 选定方案
- 带着验证计划进入实现

## 不可妥协的规则

助手必须：
1. 先基于当前 scope 说清设计问题是什么
2. 至少给出两个方案（若确实只有一个可行方案，要明确说明原因）
3. 对每个方案说明：
   - 改动范围
   - 简单性 vs 灵活性
   - 失败模式
   - 错误处理策略（error propagation / wrapping / user-visible handling）
   - 接口与依赖边界（small interfaces、依赖注入、是否引入不必要抽象）
   - 验证成本
4. 最终必须给出推荐方案
5. 推荐方案后必须附最小验证计划

助手不得：
- 在多种路径存在时直接跳到编码
- 把“我更喜欢”当成设计理由
- 只列优点，不列代价和失败模式
- 把 scope 输出直接伪装成设计结论

## 输入

输入通常来自：
- `becc-problem-framing`
- `becc-impact-discovery`
- 当前仓库已有模式
- 当前 Go/backend 约束

## 输出

输出至少应包含：

### 1. Design Problem
- 当前真正要做的设计判断是什么

### 2. Option A
- 方案描述
- 优点
- 代价
- 失败模式

### 3. Option B
- 方案描述
- 优点
- 代价
- 失败模式

### 4. Recommendation
- 推荐哪个方案
- 为什么当前最合适
- 当前推荐的错误处理边界是什么
- 当前推荐的接口与依赖组织方式是什么

### 5. Validation Plan
- 要验证什么
- 最小验证路径
- 哪些风险需要额外验证
- 哪些错误路径或边界条件必须明确覆盖

## 停下来询问的条件

遇到以下情况必须停下：
- scope 仍不稳，无法比较方案
- 已有约束明显不足，设计判断会失真
- 用户偏好会直接影响方案选型，但尚未说明

## 完成态要求

只有在以下条件成立时，才可把 backend design 视为完成：
- 设计问题明确
- 至少两个方案已比较，或已明确只有一个现实可行方案
- 推荐路径明确
- 验证计划明确

否则结果必须标记为：
- `partial`：已有方向，但比较不足
- `blocked`：scope 或约束不足，无法可靠比较

## 与其他资产的关系

这个 skill 通常连接到：
- `becc-impact-scope`
- `becc-go-test`
- `becc-tradeoff-analysis`
- `becc-validation-plan`

它的职责是：

> 在真正写代码前，把“怎么做”收敛成一个最小、可验证、可解释的设计决定。
