---
name: becc-session-handoff
description: 在一次 Go 后端开发会话结束时，把已完成项、改动、验证、未执行项、风险与下一步交接成可继续推进的结构化产物。
origin: backend-ecc
---

# becc-session-handoff

用于在一次任务阶段结束时，把当前结果收敛成可交接、可续做、可复盘的 closeout 产物。

## 何时使用

以下场景优先使用这个 skill：
- 一次实现、修复或设计阶段已经结束
- 需要把当前会话交给后续自己或他人继续
- 需要生成 PR summary、handoff 或阶段性收口说明
- 当前任务还没完全结束，但必须把 done / not done / risks 说清楚

不要把这个 skill 用于：
- 任务刚开始，当前没有实质进展
- 当前还没形成任何改动、验证或设计结论

## 核心意图

这个 skill 的目标不是“写一段总结”，而是明确区分：

1. 已完成什么
2. 实际改了什么
3. 验证了什么
4. 没做什么
5. 风险还剩什么
6. 下一步应该由谁接着做什么
7. 如果交给 reviewer 或下一次会话，最少需要知道什么

## 所在 loop

这个 skill 主要位于：
- 所有 loop 的收口阶段
- 尤其是 Impact & Validation Loop 的交付末段

## 不可妥协的规则

助手必须：
1. 区分 Completed / Changed / Verified / Not Run / Risks
2. 不把未验证项包装成已完成
3. 如果任务未完成，明确说明当前是阶段性收口，而非最终完成
4. 给出后续接手所需的最小上下文
5. 明确推荐的 resume point：下一次最先应看的文件、结果或问题是什么
6. 若面向 reviewer，总结必须突出 review 应重点关注的范围

助手不得：
- 用笼统总结掩盖未完成项
- 把“应该可以”写成“已经完成”
- 跳过 open risks 或下一步建议

## 输入

输入通常来自：
- 当前会话的变更与验证结果
- `becc-verification-gate` 的输出
- `becc-go-review` 的 verdict
- 相关设计、调试、测试产物

## 输出

输出至少应包含：

### 1. Completed
- 当前阶段已经完成什么

### 2. Changed
- 实际修改了哪些文件 / 资产 / 路径

### 3. Verified
- 已执行的验证与结果

### 4. Not Run
- 尚未执行但仍重要的检查

### 5. Risks / Open Questions
- 当前还剩哪些风险或未解问题

### 6. Next Steps
- 后续谁应接着做什么
- 哪一步最优先

### 7. Resume Point
- 下一位接手时最先应查看什么
- 从哪里继续最省上下文重建成本

### 8. Reviewer Focus（如适用）
- reviewer 应优先看哪些文件 / 风险点

## 停下来询问的条件

遇到以下情况必须停下：
- 当前没有足够事实支持 handoff
- 变更与验证信息不完整，无法可靠总结
- 用户要求“直接说完成”，但当前明显仍有 open items

## 完成态要求

只有在以下条件成立时，才可把 handoff 视为完成：
- 当前阶段结果已结构化
- 已完成与未完成已分开
- 风险与下一步已明确

否则结果必须标记为：
- `partial`：已有部分总结，但上下文仍不足
- `blocked`：无法形成可靠交接材料

## 与其他资产的关系

这个 skill 通常连接到：
- `becc-session-handoff`
- `becc-pr-summary`
- `becc-verification-gate`
- `becc-go-review`

它的职责是：

> 把一次任务阶段变成后续还能继续推进的明确交接点。
