---
name: becc-root-cause-debugging
description: 将 symptom、证据、假设、反证与确认根因分开处理，避免把补丁误当根因修复。适用于 Go 后端的 build/test/runtime/debug 任务。
origin: backend-ecc
---

# becc-root-cause-debugging

用于在 bug、构建失败、测试失败或运行时异常场景下，强制走根因归因闭环。

## 何时使用

以下场景优先使用这个 skill：
- `go build` / `go test` 失败
- 线上或本地出现明确 symptom，但原因不清
- 已有一个猜测修法，但还没证明它是真正根因
- 需要避免“先改了再说”的症状修补

不要把这个 skill 用于：
- 已确认根因且只差机械修复的小问题
- 纯需求开发且无 symptom/故障输入的任务

## 核心意图

这个 skill 的目标不是“找个能 work 的修法”，而是明确区分：

1. symptom
2. evidence
3. hypotheses
4. falsification
5. confirmed root cause

只有证据支持的原因，才可称为根因。

## 所在 loop

这个 skill 主要位于：
- **Root-Cause Loop**

典型循环：
- 记录 symptom
- 收集证据
- 提出候选原因
- 逐个尝试反证
- 确认根因，或继续收集证据

## 不可妥协的规则

助手必须：
1. 把 symptom 与 root cause 分开写
2. 每个假设都要有证据基础
3. 在证据不足时明确标记“候选原因”
4. 在分析原因时，区分：
   - 用户可见错误
   - 内部诊断错误
   - 可恢复错误
   - 不可恢复错误
5. 若已经进入修复，优先采用最小修复并重新运行最相关的 build/test/check，而不是一次性扩大改动面
6. 修复后至少说明它验证了什么，而不是只说“好了”

助手不得：
- 把第一个能让报错消失的补丁直接称为根因修复
- 没有反证步骤就宣布问题已定位
- 跳过失败路径与未验证项
- 在没有复跑最相关检查前，把修复表述为已确认完成

## 输入

输入通常来自：
- build/test/runtime 错误信息
- 日志、trace、panic、报错页面
- 已尝试过的修法
- 相关代码与配置上下文

## 输出

输出至少应包含：

### 1. Symptom
- 当前可观察到的失败现象
- 复现条件或触发条件

### 2. Evidence
- 已确认日志/错误/代码事实
- 哪些是直接证据
- 当前错误是内部诊断信息，还是用户可见/接口可见行为

### 3. Hypotheses
- 候选原因列表
- 每个原因为什么值得怀疑
- 它属于哪类错误：输入问题、依赖问题、状态问题、边界处理问题、内部实现问题

### 4. Falsification / Checks
- 每个假设如何验证或反证
- 哪些检查已执行
- 哪些还未执行

### 5. Root Cause Status
只允许以下几类状态：
- `confirmed`
- `candidate`
- `blocked`

### 6. Next Action
- 继续补证据
- 继续缩小假设
- 开始实施修复
- 重新运行关键检查
- 当前无法继续

## 停下来询问的条件

遇到以下情况必须停下：
- symptom 本身不稳定或不可复现
- 当前证据不足以提出有效假设
- 用户要求直接修，但当前还没有足够证据支撑修法
- 外部依赖、环境、权限问题阻止关键验证

## 完成态要求

只有在以下条件成立时，才可把 root-cause debugging 视为完成：
- symptom 已明确
- 证据已结构化
- 假设与反证路径已列出
- 至少一个候选原因已被证据支持或反证排除
- 当前状态被明确标记为 confirmed / candidate / blocked 之一

否则结果必须标记为：
- `partial`：已有候选假设，但验证不足
- `blocked`：无法继续验证

## 与其他资产的关系

这个 skill 通常连接到：
- `becc-debug-root-cause`
- `becc-evidence-capture`
- `becc-verification-gate`
- `becc-root-cause-analysis`

它的职责是：

> 先证明原因，再谈修复；先区分证据，再谈结论。
