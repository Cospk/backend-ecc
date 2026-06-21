# /becc-debug-root-cause

用于在 build/test/runtime 故障场景下，强制按 root-cause loop 处理问题，而不是直接打补丁。

---

## 何时使用

以下场景优先使用 `/becc-debug-root-cause`：

- `go build` 失败
- `go test` 失败
- 服务运行时出现异常，但根因不清楚
- 已有一个猜测修法，但还没有证据证明它是真正根因

如果当前问题主要来自外部材料或页面证据，先走：
- `becc-evidence-capture`

如果当前问题定义本身还不稳，先走：
- `becc-problem-framing`

---

## 默认流程

执行 `/becc-debug-root-cause` 时，按以下顺序推进：

### 1. 写清 symptom
先明确：
- 当前失败现象是什么
- 在什么条件下出现

### 2. 提取证据
继续整理：
- 错误信息
- 日志
- 失败测试
- 关键代码事实

### 3. 列出候选原因
只列有证据支撑的候选原因，不列纯猜想。

### 4. 做反证或验证
对每个候选原因说明：
- 怎么验证
- 怎么反证
- 当前做到了哪一步

### 5. 小步修复与复跑
如果已经有足够证据支持某个候选原因，优先采用最小修复，并在每次修复后重新运行最相关的构建、测试或检查，而不是一次性大改后再统一回看。

### 6. 明确当前状态
最终只能收敛到：
- `confirmed`
- `candidate`
- `blocked`

### 7. 再决定下一步
下一步只允许是：
- 继续补证据
- 继续缩小假设
- 开始实施修复
- 暂停并说明阻塞

---

## 输出格式

`/becc-debug-root-cause` 的输出至少应包含：

### 1. Symptom
- 当前可观察的失败现象
- 触发条件

### 2. Evidence
- 已确认的日志、错误、代码事实

### 3. Hypotheses
- 候选原因列表
- 每个原因的依据

### 4. Checks / Falsification
- 已执行的验证或反证
- 尚未执行的验证

### 5. Repair / Rerun
- 如果已实施修复，改了什么
- 修复后重新运行了什么
- 结果是否翻转

### 6. Root Cause Status
- confirmed / candidate / blocked

### 7. Next Action
- 继续补证据 / 继续分析 / 开始修复 / 暂停

---

## 输出边界

`/becc-debug-root-cause` 不负责：

- 在没有证据时直接给修复方案
- 把第一个有效补丁当成根因修复
- 跳过未执行检查直接宣称完成

如果后续进入修复，也必须保留对验证面和未验证项的说明。

---

## 与其他资产的关系

`/becc-debug-root-cause` 典型会联动：

- `becc-root-cause-debugging`
- `becc-evidence-capture`
- `becc-root-cause-analysis`
- `becc-verification-gate`

它的目标不是“尽快改掉报错”，而是：

> 先证明根因，再决定是否修和怎么修。
