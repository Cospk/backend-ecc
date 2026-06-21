# /becc-session-handoff

用于在一次 Go/backend 任务阶段结束时，把当前状态收口成结构化 handoff，而不是只留口头总结。

---

## 何时使用

以下场景优先使用 `/becc-session-handoff`：

- 本次任务已经完成一个阶段，准备暂停或交接
- 需要把当前改动、验证、未执行项、风险与下一步整理清楚
- 需要形成 PR summary 或 session handoff 草稿

如果当前还没有任何实质进展，不需要使用这个 command。

---

## 默认流程

执行 `/becc-session-handoff` 时，按以下顺序推进：

### 1. 收敛当前阶段结果
先明确：
- 当前已经完成什么
- 当前还没完成什么

### 2. 回看实际改动
列出：
- 实际触达的文件 / 模块 / 资产

### 3. 回看验证结果
列出：
- 已执行的验证
- 当前通过了什么
- 还有什么没跑

### 4. 说明风险与 open questions
至少说明：
- 当前仍未消除的风险
- 仍需判断的问题

### 5. 给出 next steps
明确：
- 后续最优先的下一步
- 若交给别人，最少需要知道什么

### 6. 明确 resume point / reviewer focus
至少说明：
- 下一次会话最先应该看什么
- 如果这是 reviewer-facing 摘要，最值得重点看的范围是什么

---

## 输出格式

`/becc-session-handoff` 的输出至少应包含：

### 1. Completed
### 2. Changed
### 3. Verified
### 4. Not Run
### 5. Risks / Open Questions
### 6. Next Steps

### 7. Resume Point / Reviewer Focus

---

## 输出边界

`/becc-session-handoff` 不负责：
- 美化宣传语
- 隐藏未完成项
- 在验证不足时给“完全完成”结论

它负责的是：

> 把当前阶段结果变成后续能继续接手的结构化交接点。
