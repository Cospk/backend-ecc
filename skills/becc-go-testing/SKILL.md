---
name: becc-go-testing
description: 用 Go idiomatic testing 与 TDD 节奏把验证从“补检查”变成主执行路径。适用于新功能、bug 修复与关键逻辑回归验证。
origin: backend-ecc
---

# becc-go-testing

用于在 Go 后端任务中，把测试与验证作为主路径推进，而不是作为事后补充。

## 何时使用

以下场景优先使用这个 skill：
- 新增 Go 函数、方法、handler 或 service 逻辑
- 修复 bug，且需要先写失败用例再修
- 需要补 Go 测试覆盖
- 需要证明某次修复不会回归
- 需要把验证从“凭感觉”变成可执行的 Go test 路径

不要把这个 skill 用于：
- 纯文档改动
- 与 Go 无关的前端/UI 验证
- 已有充分验证且本次不涉及逻辑变化的纯机械改动

## 核心意图

这个 skill 的目标不是“顺手跑个 go test”，而是把验证拆成明确节奏：

1. 明确要验证的行为
2. 优先写失败测试或补最小复现
3. 运行测试，确认 RED 或当前失败态
4. 写最小实现或最小修复
5. 重新运行相关测试，确认 GREEN
6. 再决定是否扩大验证面

## 所在 loop

这个 skill 主要位于：
- **Impact & Validation Loop**
- 与 **Root-Cause Loop** 在 bug 修复场景下联动

典型循环：
- framing / scope 后明确验证面
- 写测试或挑选现有测试
- 运行失败态
- 最小修复
- 复跑验证
- 再决定是否跑更广泛测试

## 不可妥协的规则

助手必须：
1. 优先说明本次要验证什么行为，而不是直接写测试代码
2. 若是 bug 修复，优先补失败测试或最小复现
3. 优先使用 Go idiomatic test pattern：
   - table-driven tests
   - subtests
   - 明确断言
4. 区分：
   - 相关测试
   - 扩展测试
   - 尚未运行的验证面
5. 在需要时明确说明 RED / GREEN 是否已被实际观察到

助手不得：
- 在没有验证目标的情况下堆测试
- 只写 happy path，不写边界或错误路径
- 没跑相关测试就把实现写成已验证完成
- 把大范围 `go test ./...` 当成默认第一步，而不考虑最小验证范围

## 输入

输入通常来自：
- `becc-problem-framing` 的成功标准
- `becc-impact-discovery` 的验证面
- `becc-root-cause-debugging` 的故障现象
- 已有 Go 代码与现有测试

## 输出

输出至少应包含：

### 1. Verification Target
- 本次要验证的行为是什么
- 为什么它是关键验证点

### 2. Test Strategy
- 新增测试还是复用现有测试
- 最小相关测试范围
- 是否采用 table-driven / subtests

### 3. RED Status
- 是否已经观察到失败态
- 如果没有，为什么

### 4. GREEN Status
- 修复后复跑了什么
- 当前是否已经通过

### 5. Extended Validation
- 是否需要继续跑更广测试
- 哪些验证还没做

### 6. Coverage / Risk Notes
- 当前覆盖的范围
- 仍然未覆盖的风险

## 停下来询问的条件

遇到以下情况必须停下：
- 当前验证目标不清楚
- 无法判断应该补哪类测试
- 仓库里已有测试模式与当前写法明显冲突
- 用户要求直接修，但当前 bug 仍没有失败复现或失败测试

## 完成态要求

只有在以下条件成立时，才可把 Go testing 视为完成：
- 验证目标明确
- 已执行至少一个直接相关的测试或复现检查
- 若有修复，已复跑并说明结果
- 已明确列出未执行的验证面

否则结果必须标记为：
- `partial`：已有测试或修复，但验证面仍不足
- `blocked`：缺少测试入口、环境或复现条件
- `not ready`：还不能宣称完成

## 与其他资产的关系

这个 skill 通常连接到：
- `becc-go-test`
- `becc-verification-gate`
- `becc-root-cause-debugging`
- `rules/golang/becc-testing`

它的职责是：

> 让 Go 验证从“最后补一跑”变成整个变更过程中的主路径。
