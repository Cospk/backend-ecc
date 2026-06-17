---
name: add-sport-market
description: 按固定的输入收集、确认、接线与验证流程，将一个或多个球种接入 market-server。适用于领域专项的球种接入任务，不适用于通用编码任务。
origin: ECC
---

# Add Sport Market

用于将一个或多个新球种接入 `market-server` 的固定工作流。

## 何时使用

当用户要做以下事情时启用本 skill：
- 在 `market-server` 中新增一个球种
- 基于同一个模板球种批量新增多个球种
- 将已有的新增球种需求从输入收集推进到代码接线
- 判断一个新增球种需求是否已经具备执行条件

不要把这个 skill 用于通用 Go 功能开发、普通 API 开发或代码审查。

## 核心意图

这不是一个通用编码提示词，而是一套领域工作流。它有三个目标：

1. 在修改代码前先收集球种接入所需的最小定义
2. 对所有业务敏感值强制执行显式确认
3. 将机械性的复制/替换工作与业务判断、最终接线区分开

## 不可妥协的规则

在进行任何复制、替换或接线之前，助手必须：
1. 索取目标球种及其真实依赖定义
2. 检查最小输入是否完整
3. 将允许自动补全的字段整理成结构化草稿
4. 将该结构化草稿展示给用户
5. 等待用户明确确认

助手不得：
- 猜 SID、球种常量、topic 名、配置后缀或 Mongo 后缀
- 在用户未明确授权默认规则前，依据命名习惯推断正式业务值
- 默认复制业务白名单或高级能力
- 在存在未确认业务能力时宣称工作已全部完成

## 最小必需输入

对每个目标球种，至少收集以下字段：
- `nameZh`
- `internalName`
- `sid`
- `sportConst`
- `templateSport`

若缺少 `packageName`，默认使用 `internalName` 转小写。

若用户明确授权按默认规则补全，助手还可以自动展开：
- `ruleReuseFrom = templateSport`
- `configSuffix = esport-<packageName>`
- `mergeMarketTopic = nw.aggregatorServer.mergeMarket.esport-<packageName>.topic`
- `sourceOffOnTopic = nw.aggregatorServer.sourceOfflineOnline.esport-<packageName>.topic`
- `oddsDiffTopic = nw.marketServer.oddsDiffEsport<UPPER_INTERNAL_NAME>`
- `mongoCollectionSuffix = final_historical_odds_esport_<packageName>`

如果没有显式授权，这些值仍视为未确认，不能当作正式值使用。

## 标准输入收集提示词

开始时应输出与下述含义等价的话：

> 我会按 add-sport-market 工作流执行。请先给我每个目标球种在 `sport-lib` 中的真实定义。最少需要：中文名、内部名称、SID、球种常量、模板球种。如果你希望我按默认规则补全 packageName、configSuffix、topic 名和 Mongo 后缀，请明确说明，我会先整理成结构化草稿给你确认。

## 确认草稿格式

在开始执行前，先给出类似下面的标准化结构：

```yaml
sports:
  - nameZh: 王者榮耀
    internalName: HoK
    packageName: hok
    sid: 106
    sportConst: SidHoK
    templateSport: badminton
    ruleReuseFrom: badminton
    hasChampion: true
    configSuffix: esport-hok
    mergeMarketTopic: nw.aggregatorServer.mergeMarket.esport-hok.topic
    sourceOffOnTopic: nw.aggregatorServer.sourceOfflineOnline.esport-hok.topic
    oddsDiffTopic: nw.marketServer.oddsDiffEsportHOK
    mongoCollectionSuffix: final_historical_odds_esport_hok
```

在用户明确确认这份结构化草稿前，不得进入执行阶段。

## 工作流阶段

### 阶段 1：输入门禁
- 收集最小输入
- 拒绝不完整输入
- 确认默认规则是否可作为正式值
- 确认是否存在需要单独确认的业务能力

### 阶段 2：结构化确认
- 将所有球种整理为一个结构化 YAML 块
- 清楚标出所有未确认字段
- 等待明确确认

### 阶段 3：影响范围审查
围绕模板球种审查并识别：
- 哪些目录可以安全复制
- 哪些文件必须手工接线
- 哪些残留风险较高：包前缀、中文文本、模板常量、裸 SID 片段、模板专属日志、未支持能力复制

通常应检查的文件包括：
- `internal/biz/<templateSport>`
- `internal/service/market.go`
- `internal/service/event.go`
- `internal/service/service.go`
- `cmd/market-server/wire.go`
- `cmd/market-consumer/wire.go`
- `internal/server/server.go`
- `internal/server/matchrouter.go`
- `pkg/pod/task.go`
- `pkg/pod/manage.go`
- `internal/conf/config.go`
- `configs/*.yaml`
- `internal/pkg/mq/kafka.go`
- `internal/pkg/cpush/odds_diff_match.go`
- `internal/server/consumer.go`
- `internal/server/producer.go`

### 阶段 4：机械成型
以下机械工作应尽量脚本化：
- 目录复制
- package / import / 类型前缀替换
- 常量替换
- 模板中文文本替换
- 残留扫描

如果某个操作已经符合现有可重复模式，不要临场编造一大段一次性脚本。

### 阶段 5：手工接线
手工完成以下事项：
- usecase 暴露
- router 暴露
- provider 接线
- event handler 接线
- task 注册
- config 字段与 yaml key 对齐
- producer / consumer / topic 接线
- common / cache / data 层补齐

### 阶段 6：业务能力审查
不要默认继承模板球种的业务行为。必须显式判断是否接入：
- champion
- sourceOffOn
- 调水白名单
- 多盘口联动白名单
- 赛果过滤
- 次要标签
- 未支持能力相关复制

### 阶段 7：最小验证
在汇报完成前，至少验证：
- 该替换的模板包前缀已无残留
- 该替换的模板中文球种名已无残留
- provider 链完整
- router 链完整
- topic / config 命名对齐
- 新生成或新接入的文件内部保持一致

## 汇报格式

最后用清晰的状态汇报收尾：

```text
ADD-SPORT-MARKET RESULT
Sports: <count>
Template: <template sport(s)>

Completed:
- ...

Not included:
- ...

Needs confirmation:
- ...

Risks:
- ...

Verification:
- ...
```

汇报中必须明确区分：
- 哪些已经完成
- 哪些是有意不纳入本次范围
- 哪些仍需要用户确认

## 停下来询问的规则

遇到以下情况必须停下并询问用户：
- 球种最小必需字段不完整
- 最终 topic / config / mongo 值未确认，且用户也未授权按默认规则补全
- 模板行为中涉及 champion / 白名单 / 过滤 / 未支持能力逻辑，会改变业务行为
- 任务即将进入某个未确认的业务能力范围

## 推荐搭配资产

这个 skill 最好搭配：
- 一份详细 playbook 文档，承载脚本模板和锚点级插入说明
- 一份可选的领域 rules 文件，只保留硬性业务禁止项

保持这个 skill 聚焦于工作流编排，不要把它写成一个巨大的脚本仓库。
