# /becc-go-test

用于在 Go 任务中显式进入 testing / TDD / verification 路径，而不是把测试留到最后补跑。

---

## 何时使用

以下场景优先使用 `/becc-go-test`：

- 新增 Go 逻辑，需要先写测试再实现
- bug 修复，需要先补失败测试或最小复现
- 已经完成实现，但还没形成可信验证路径
- 需要把 scope 结果转成最小 Go 验证计划

如果当前问题本身还没 framing 清楚，先走：
- `becc-problem-framing`

如果当前影响范围还不清楚，先走：
- `becc-impact-scope`

如果当前是故障归因但根因未明，先走：
- `becc-debug-root-cause`

---

## 默认流程

执行 `/becc-go-test` 时，按以下顺序推进：

### 1. 明确 verification target
先说明：
- 本次要验证什么行为
- 为什么这是关键验证点

### 2. 选择测试策略
至少明确：
- 新增测试还是复用现有测试
- 最小相关 package / test target 是什么
- 是否采用 table-driven / subtests

### 3. 确认失败态或当前基线
如果是 bug 修复或 TDD：
- 优先确认 RED
- 或至少说明当前已有失败态是什么

### 4. 实施最小修复或最小实现
只在验证目标明确后进入改动。

### 5. 复跑相关测试
修复或实现后：
- 重跑最相关测试
- 明确结果是否翻转为 GREEN

### 6. 再决定是否扩大验证面
根据影响范围决定是否继续：
- 跑更多 package
- 加 `-race`
- 看 coverage

---

## 输出格式

`/becc-go-test` 的输出至少应包含：

### 1. Verification Target
- 当前要验证的行为

### 2. Test Strategy
- 测试入口
- 最小测试范围
- 预期测试模式

### 3. RED Status
- 是否已观察到失败态
- 如果没有，为什么

### 4. GREEN Status
- 修复或实现后复跑了什么
- 当前是否已经通过

### 5. Extended Validation
- 还需要哪些更广泛验证
- 哪些尚未运行

### 6. Overall
- ready | not ready | partial | blocked

---

## 输出边界

`/becc-go-test` 不负责：
- 在验证目标不清时直接写测试代码
- 跳过失败态就宣称完成了 TDD
- 用大范围测试替代相关测试思考

它负责的是：

> 把 Go 变更收敛成一条最小、相关、可复跑的测试验证路径。
