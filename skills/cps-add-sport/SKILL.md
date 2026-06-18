---
name: cps-add-sport
description: 按固定的输入收集、确认、接线与验证流程，将一个或多个电竞球种接入 c-push-server。适用于 c-push-server 的新增球种任务，不适用于 market-server 或通用 Go 开发任务。
origin: ECC
---

# cps-add-sport

用于将一个或多个新球种接入 `c-push-server` 的固定工作流。

## 何时使用

当用户要做以下事情时启用本 skill：
- 在 `c-push-server` 中新增一个球种
- 基于同一个模板球种批量新增多个电竞球种
- 将已有的新增球种需求从输入收集推进到代码接线
- 判断一个 `c-push-server` 新增球种需求是否已经具备执行条件

不要把这个 skill 用于 `market-server` 的新增球种流程、普通 API 开发或通用代码审查。

## 核心意图

这不是一个通用编码提示词，而是一套领域工作流。它有三个目标：

1. 在修改代码前先收集 `c-push-server` 接入所需的最小定义
2. 将批量复制/替换与读文件后手工接线区分开
3. 在汇报完成前，明确哪些接入点已经检查、哪些尚未验证

## 不可妥协的规则

在进行任何复制、替换或接线之前，助手必须：
1. 索取目标球种及其真实依赖定义
2. 检查最小输入是否完整
3. 将允许执行的字段整理成结构化草稿
4. 将该结构化草稿展示给用户
5. 等待用户明确确认

助手不得：
- 猜 SID、topic 名、bubble 字段、上游 proto 字段或 sport-lib 常量
- 在未确认 `sport-lib` 已提供依赖前，宣称该球种可以直接接入
- 把 `market-server` 的接入步骤当成 `c-push-server` 的接入步骤
- 在存在未验证接线面的情况下宣称工作已全部完成

## 最小必需输入

对每个目标球种，至少收集以下字段：
- `nameZh`
- `packageName`
- `typeName`
- `sid`
- `templateSport`
- `consumerTopic`

如果涉及泡泡过滤，还应确认：
- `bubbleField`
- 上游是否已提供对应字段

如果用户希望直接按模板复用逻辑，也必须先明确：
- 是否完全复用模板 usecase 逻辑
- 是否完全复用模板 consumer 接入方式
- 是否完全复用模板 bubble 过滤逻辑

## 标准输入收集提示词

开始时应输出与下述含义等价的话：

> 我会按 cps-add-sport 工作流执行。请先给我每个目标球种在 `sport-lib` 中的真实定义，以及 `c-push-server` 需要的接入参数。最少需要：中文名、package 名、导出类型名、SID、模板球种、consumer topic。如果涉及泡泡过滤，还需要确认对应 bubble 字段以及上游是否已提供该字段。我会先整理成结构化草稿给你确认。

## 确认草稿格式

在开始执行前，先给出类似下面的标准化结构：

```yaml
sports:
  - nameZh: DOTA2
    packageName: dota2
    typeName: DOTA2
    sid: 101
    templateSport: badminton
    consumerTopic: oddsDiffDOTA2Match
    bubbleField: DOTA2
    sportConst: gconsts.DOTA2
    reuseTemplateLogic: true
```

在用户明确确认这份结构化草稿前，不得进入执行阶段。

## 工作流阶段

### 阶段 1：输入门禁
- 收集最小输入
- 拒绝不完整输入
- 确认 `sport-lib` 常量 / proto / 字段是否已存在
- 确认是否存在需要单独确认的 bubble 字段或模板复用差异

### 阶段 2：结构化确认
- 将所有球种整理为一个结构化 YAML 块
- 清楚标出所有未确认字段
- 等待明确确认

### 阶段 3：模板与影响范围审查
围绕模板球种审查并识别：
- 哪些目录可以安全复制
- 哪些文件必须手工接线
- 哪些残留风险较高：包前缀、中文文本、模板常量、错误大小写、模板专属日志

通常应检查的文件包括：
- `internal/biz/<templateSport>`
- `internal/biz/ball/match_odds_diff.go`
- `internal/server/consumer.go`
- `internal/conf/config.go`
- `pkg/pod/task.go`
- `pkg/pod/manage.go`
- `internal/biz/sportSwitch.go`
- 对应运行配置 YAML 文件

### 阶段 4：机械成型
以下机械工作应尽量脚本化：
- 目录复制
- package / import / 类型前缀替换
- 常量替换
- 模板中文文本替换
- 残留扫描
- 拷贝后确认目标目录存在
- 替换后至少执行一轮残留扫描
- 残留扫描至少覆盖模板包名、模板中文名、模板常量和错误大小写
- 发现残留时继续清理，或明确列入风险；不要直接将该阶段表述为已完成

### 阶段 5：手工接线
手工完成以下事项：
- `ball` 层 usecase 分发
- `consumer` 层 kafka 消费
- `config` 与 YAML 字段
- `pod` 任务分配链路
- `sportSwitch` 泡泡过滤逻辑
- 对本次触达范围，明确检查 usecase / consumer / config / pod / bubble 接线
- 未检查的接线面在结果中标记为 `Not run`，不要直接将该阶段表述为已完成

### 阶段 6：上游依赖审查
不要默认上游依赖已经齐全。必须显式判断：
- `sport-lib` 是否已提供 SID 常量
- `sport-lib` 是否已提供 proto / 消息结构
- bubble 过滤所需字段是否已存在
- 是否存在需要先补上游再继续的阻塞项

### 阶段 7：最小验证
在汇报 `completed` 前，至少验证：
- 模板残留已清理
- `ball` 层已注册新增球种
- `consumer.go` 已注册对应 topic
- `config.go` 与 YAML 已对齐
- `task.go` 与 `manage.go` 已纳入新增球种
- `sportSwitch` 已补齐对应分支
- 本次触达范围内要求检查的接线面已记录结果
- 至少完成一次最小构建或测试验证；如果未执行，必须明确写出

如果已修改文件但未完成上述验证，结果必须标记为 `partial`，并明确写出“已修改，未验证”。

## 汇报格式

最后用清晰的状态汇报收尾：

```text
CPS-ADD-SPORT RESULT
Status: completed | partial | blocked | failed
Sports: <count>
Template: <template sport(s)>

Completed:
- ...

Changed:
- ...

Verified:
- ...

Not run:
- ...

Blocked by:
- ...

Needs confirmation:
- ...

Risks:
- ...
```

汇报中必须明确区分：
- 哪些已经完成
- 哪些文件或目录实际发生了变更
- 哪些检查已经实际执行
- 哪些步骤本次未执行
- 哪些仍需要用户确认
- 没有执行所需检查时，不要使用“已完成”“已验证通过”等完成态表述

## 停下来询问的规则

遇到以下情况必须停下并询问用户：
- 球种最小必需字段不完整
- `sport-lib` 依赖未确认或不存在
- bubble 过滤字段未确认
- consumer topic / config 字段未确认
- 任务即将进入某个未确认的上游依赖范围

## 推荐搭配资产

这个 skill 最好搭配：
- 一份详细 playbook 文档，承载命令模板和文件锚点说明
- 一份可选的领域 rules 文件，只保留硬性业务禁止项

保持这个 skill 聚焦于 `c-push-server` 新增球种工作流，不要把它写成一个巨大的脚本仓库。
