# /becc-go-review

用于在 Go 代码修改后，显式进入 Go/backend 专项 review 路径，而不是只做泛化代码点评。

---

## 何时使用

以下场景优先使用 `/becc-go-review`：

- 改完 Go 代码后准备提交
- 想检查当前 diff 是否还有 correctness / concurrency / error handling 风险
- 需要把 build/test/debug 之后的结果收口成 review verdict
- 需要判断当前改动是否达到可提交状态

如果当前还没做基本验证，先走：
- `becc-go-test`
- 或至少执行最小相关验证

如果当前根因仍未明，先走：
- `becc-debug-root-cause`

---

## 默认流程

执行 `/becc-go-review` 时，按以下顺序推进：

### 1. 明确 review scope
先说明：
- 当前 review 哪些 Go 文件或哪类改动
- 当前变更目标是什么

### 2. 回看验证结果
至少确认：
- 已执行了哪些 build / test / check
- 当前还有哪些验证没做

### 3. 按 Go/backend 维度审查
优先看：
- correctness
- error handling
- context / concurrency
- security / input boundary
- 当前验证面是否足够

### 4. 输出 findings
每条 finding 至少给出：
- severity
- location
- issue
- why it matters
- suggested direction

### 5. 给出 verdict
最终只能收敛到：
- `approve`
- `warning`
- `block`

---

## 输出格式

`/becc-go-review` 的输出至少应包含：

### 1. Review Scope
- 审查范围
- 当前已知验证结果

### 2. Findings
- critical / high / medium / note

### 3. Verification Gaps
- 尚未执行但重要的验证

### 4. Review Verdict
- approve / warning / block

---

## 输出边界

`/becc-go-review` 不负责：
- 在没有 Go 变更时硬做 review
- 在没有验证信息时轻率给 approve
- 把纯风格建议当成高优先级阻塞项

它负责的是：

> 把 Go 变更是否达到“可放心交付”状态收敛成结构化结论。
