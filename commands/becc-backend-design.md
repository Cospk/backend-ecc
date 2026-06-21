# /becc-backend-design

用于在 scope 已明确后，对 Go/backend 非平凡改动先做最小设计比较，而不是直接开始实现。

---

## 何时使用

以下场景优先使用 `/becc-backend-design`：

- 当前已经知道可能影响哪些模块，但还不确定怎么改最合适
- 有多个实现路径，需要做 tradeoff
- 改动会影响 handler / service / repository / config 等多个层面
- 需要先明确验证计划，再决定实现路径

如果当前问题定义还不清楚，先走：
- `becc-problem-framing`

如果当前影响范围还不清楚，先走：
- `becc-impact-scope`

---

## 默认流程

执行 `/becc-backend-design` 时，按以下顺序推进：

### 1. 说明 design problem
先明确：
- 当前真正要做的设计判断是什么
- 当前 scope 已经收敛到了什么程度

### 2. 给出可行方案
至少给出：
- Option A
- Option B

若确实只有一个现实可行方案，必须说明为什么没有第二个合理方案。

### 3. 比较 tradeoff
每个方案至少比较：
- 改动范围
- 简单性 vs 灵活性
- 失败模式
- 验证成本

### 4. 给出 recommendation
最终明确：
- 当前推荐哪条路径
- 推荐理由是什么

### 5. 绑定 validation plan
在进入实现前说明：
- 需要验证什么
- 最小验证路径是什么
- 哪些风险还需额外验证

---

## 输出格式

`/becc-backend-design` 的输出至少应包含：

### 1. Design Problem
- 当前设计问题

### 2. Options
- Option A
- Option B

### 3. Tradeoffs
- scope
- complexity
- failure modes
- validation cost

### 4. Recommendation
- 推荐路径与理由

### 5. Validation Plan
- 最小验证面
- 风险验证点

---

## 输出边界

`/becc-backend-design` 不负责：
- 在 scope 未稳时强行做方案比较
- 跳过 tradeoff 直接给唯一答案
- 直接进入实现代码

它负责的是：

> 在 scope 之后、编码之前，把设计决策压缩成可执行、可验证的最小方案。
