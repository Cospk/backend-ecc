---
name: becc-go-review
description: 用 Go 语境下的 correctness、error handling、context/concurrency、安全与验证面来审查变更，避免泛化点评。适用于 Go 代码修改后的 review 收口。
origin: backend-ecc
---

# becc-go-review

用于在 Go 代码修改后，按 Go/backend 语境做结构化审查，而不是做泛化 code review。

## 何时使用

以下场景优先使用这个 skill：
- 修改了 Go 代码，准备提交前自查
- 需要 review 当前 diff 是否存在 correctness / concurrency / error handling 问题
- 需要对 Go 变更做结构化风险判断
- 需要在 bug 修复或测试通过后，再做一次 Go 专项审查

不要把这个 skill 用于：
- 无 Go 代码改动的纯文档任务
- 已知只是格式化变更，且没有行为变化的任务
- 泛化跨语言 review（这不属于它的职责）

## 核心意图

这个 skill 的目标不是“挑风格毛病”，而是围绕 Go/backend 变更判断：

1. correctness 是否成立
2. error handling 是否明确
3. context / concurrency 是否安全
4. 接口与依赖组织是否 idiomatic（small interfaces、依赖注入、避免无必要抽象）
5. 输入、边界与安全是否合理
6. 错误处理边界是否清楚（内部错误、用户错误、可恢复错误是否被正确区分）
7. 当前验证面是否支撑“可以交付”

## 所在 loop

这个 skill 主要位于：
- **Impact & Validation Loop** 的后段
- 作为实现与测试之后的 review 收口动作

## 不可妥协的规则

助手必须：
1. 先看当前变更的目标与验证结果，再做 review
2. 优先 review 行为与风险，而不是风格细枝末节
3. 区分 issue severity：
   - `critical`
   - `high`
   - `medium`
   - `note`
4. 如果当前没有足够验证证据，应把这本身作为 review 问题指出
5. 尽量用 Go 特有维度做判断，而不是泛化描述

助手不得：
- 在没有看变更目标或验证结果时直接给 review 结论
- 把“可以更优雅”当成高优先级问题
- 跳过 error handling / context / concurrency / security 这些 Go/backend 关键面
- 把未验证改动轻率写成可提交

## 输入

输入通常来自：
- 当前 diff 或变更文件
- 已执行的 build / test / verification 结果
- `becc-go-testing` 的验证输出
- `becc-root-cause-debugging` 的修复上下文

## 输出

输出至少应包含：

### 1. Review Scope
- 当前审查哪些文件 / 哪类改动
- 当前已知的验证结果是什么

### 2. Findings
每条发现应至少包含：
- severity
- location
- issue
- why it matters
- suggested direction

### 3. Verification Gaps
- 当前还缺哪些关键验证
- 哪些问题因为未验证而无法放心放行

### 4. Review Verdict
只允许收敛到：
- `approve`
- `warning`
- `block`

## 优先审查维度

### Critical
- SQL / command / path / unsafe 等安全问题
- race condition
- goroutine leak
- 严重错误处理遗漏

### High
- 缺少 error wrapping 或 context 传递
- 用户可见错误与内部错误混淆
- 关键边界条件未处理
- 修复后未复跑关键验证
- 不安全的共享状态或锁使用

### Medium
- 明显非 idiomatic Go 写法
- 接口过大、定义位置不合理或出现 interface pollution
- 全局可变状态、依赖注入边界不清
- 可维护性差但不直接致命的问题
- 测试模式可改进但不阻塞交付

### Note
- 风格建议
- 小型重构建议

## 停下来询问的条件

遇到以下情况必须停下：
- 当前没有可审查的 Go 变更
- 当前没有任何验证信息，且无法判断变更是否安全
- review 所需的 diff 或目标文件不可见

## 完成态要求

只有在以下条件成立时，才可把 Go review 视为完成：
- review scope 明确
- findings 已按严重级别输出
- verification gaps 已说明
- verdict 已明确

否则结果必须标记为：
- `partial`：已看部分，但上下文不足
- `blocked`：缺少 diff / 验证 / 文件上下文

## 与其他资产的关系

这个 skill 通常连接到：
- `becc-go-review`
- `becc-go-testing`
- `becc-verification-gate`
- `becc-code-review`

它的职责是：

> 用 Go/backend 语言把“这次改动还能不能放心交付”说清楚。
