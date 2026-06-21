---
name: becc-evidence-capture
description: 将浏览器页面、导出材料、日志片段或外部说明收敛为结构化事实、歧义点与后续路由建议。适用于证据先于代码搜索的 Go 后端任务。
origin: backend-ecc
---

# becc-evidence-capture

用于在进入代码搜索、范围分析或 debug 前，先把外部材料转成可消费证据。

## 何时使用

以下场景优先使用这个 skill：
- 用户给的是 Jira、Confluence、Figma、日志页、监控页、导出材料
- 问题描述主要来自截图、页面、文档或人工整理材料
- 当前关键输入在代码仓库之外
- 直接开始 grep / 读代码会导致错误理解问题

不要把这个 skill 用于：
- 纯代码内问题，且证据已在错误信息或测试输出里
- 已经有结构化事实，只差 scope/design/verify 的任务

## 核心意图

这个 skill 的目标不是“总结材料”，而是把材料转换成：

1. 可确认事实
2. 当前歧义点
3. 缺失证据
4. 下一步应该去哪条路径

## 所在 loop

这个 skill 主要位于：
- **Problem Convergence Loop**
- **Root-Cause Loop** 的前段

典型循环：
- 读取外部材料
- 提炼事实
- 标出歧义
- 判断是否还需补材料
- 再进入 framing / debugging / impact discovery

## 不可妥协的规则

助手必须：
1. 把“材料中明确出现的内容”与“推断”分开
2. 明确列出歧义点
3. 明确指出证据是否足以支持下一步
4. 如果证据不足，不要假装已经理解问题

助手不得：
- 把页面文案自动当作真实需求边界
- 把截图或文档里的模糊表述当成代码层事实
- 在证据不足时直接给设计或 root cause 结论

## 输入

输入通常来自：
- 浏览器页面
- 导出的 markdown / pdf / 文档摘要
- 日志页面或错误记录
- 人工复制的业务材料

## 输出

输出至少应包含：

### 1. Source Summary
- 当前材料来自哪里
- 材料覆盖了什么，不覆盖什么

### 2. Extracted Facts
- 可直接确认的事实
- 关键实体、字段、错误、状态、限制

### 3. Ambiguities
- 当前无法确定的点
- 哪些内容仍只是说法，不是证据

### 4. Missing Evidence
- 下一步还缺什么材料
- 是否需要更多页面、日志、配置、样本

### 5. Recommended Routing
只允许收敛到以下几类路径之一：
- 进入 `becc-problem-framing`
- 进入 `becc-impact-discovery`
- 进入 `becc-root-cause-debugging`
- 继续补证据

## 停下来询问的条件

遇到以下情况必须停下：
- 材料来源不清
- 材料明显不完整
- 关键信息只有截图局部，没有上下文
- 用户想直接进入设计或编码，但证据不足以支撑

## 完成态要求

只有在以下条件成立时，才可把 evidence capture 视为完成：
- 已提炼出结构化事实
- 已列出歧义点
- 已判断证据是否充足
- 已给出下一步路由建议

否则结果必须标记为：
- `partial`：已有事实，但材料仍明显不完整
- `blocked`：缺少关键材料，无法继续

## 与其他资产的关系

这个 skill 典型会连接到：
- `becc-problem-framing`
- `becc-impact-discovery`
- `becc-root-cause-debugging`

它的职责是：

> 先把外部材料变成可信证据，再进入代码侧推理。
