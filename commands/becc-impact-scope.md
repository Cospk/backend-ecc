# /becc-impact-scope

用于在实现、重构或非平凡修复前，先收敛影响系统、可能代码路径与验证风险。

---

## 何时使用

以下场景优先使用 `/becc-impact-scope`：

- 问题已基本 framing 清楚，但不知道改哪些模块
- 需要先判断是否会波及相邻系统
- 需要在写代码前先控制 diff 触达范围
- 需要把 scope 结果转成后续验证面

如果问题本身还不清楚，先走：
- `becc-problem-framing`
- 或 `becc-evidence-capture`

---

## 默认流程

执行 `/becc-impact-scope` 时，按以下顺序收敛：

### 1. 简述当前问题
先用一句话说明：
- 当前要解决什么问题
- 当前已知约束是什么

### 2. 优先做图谱路由
如果仓库已有 Graphify / understand-anything 能力，优先用它们定位：

- affected systems
- likely modules
- 关键调用链
- 与当前任务最接近的路径

### 3. 查相似模式
继续查找：
- 相似 feature pattern
- 相似 structural pattern
- 相似 integration pattern
- 相似 validation pattern

### 4. 收敛影响面
输出至少包括：
- primary affected system
- directly affected modules / files
- likely adjacent systems
- likely not affected areas

### 5. 给出代码路径假设
如果可以，补充：
- entry point
- likely execution path
- data / config / external touchpoints
- risk surface

### 6. 明确后续验证面
至少说明：
- 本次需要验证哪些路径
- 哪些风险如果不验证，不能声称完成

---

## 输出格式

`/becc-impact-scope` 的输出至少应包含：

### 1. Problem Summary
一句话问题摘要。

### 2. Affected Systems
- 主要系统
- 直接影响模块
- 间接影响模块
- 明确不受影响区域

### 3. Code Path Hypothesis
- 可能入口
- 可能执行链
- 关键分支点

### 4. Risk Surface
- regression risk
- config / data risk
- rollout risk
- validation risk

### 5. Verification Surface
- 必须覆盖的验证面
- 当前仍待补证据的点

---

## 输出边界

`/becc-impact-scope` 只负责范围与验证面分析，不负责：

- 直接给出最终实现方案
- 直接写代码
- 直接宣称 root cause 已确定
- 把猜测表述成事实

如果 scope 明确后还需要方案比较，再进入 design；如果当前是故障归因任务，再进入 root-cause debugging。

---

## 与其他资产的关系

`/becc-impact-scope` 典型会联动：

- `becc-impact-discovery`
- `becc-problem-framing`
- `becc-evidence-capture`
- `becc-graph-first-analysis`
- `becc-verification-gate`

它的目标不是把仓库读遍，而是：

> 在真正动手修改前，用最小阅读量收敛最可能正确的影响范围与验证面。
