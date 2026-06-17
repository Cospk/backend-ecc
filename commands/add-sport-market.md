---
description: 作为 market-server 一个或多个球种接入任务的 add-sport-market 工作流入口。先收集最小输入，整理为确认草稿，再进入领域 skill。
argument-hint: "[球种定义 | 接入需求]"
---

# Add Sport Market Command

将这个 command 作为 `market-server` 新增球种工作的薄入口。

## 这个 Command 做什么

1. 切换到 add-sport-market 工作流
2. 收集球种接入所需的最小定义
3. 将输入整理成结构化确认草稿
4. 在任何复制、替换或接线动作之前等待用户明确确认
5. 在确认后进入 `add-sport-market` skill 的领域流程

## 必需输入

对每个目标球种，至少索取以下内容：
- 中文名
- 内部名称
- SID
- 球种常量
- 模板球种

如果用户希望 packageName / configSuffix / topics / mongo 后缀按默认规则补全，必须先获得明确授权，才能把这些值视为正式值。

## Command 行为

被调用后，助手应当：

1. 说明当前正在按 add-sport-market 工作流执行
2. 若最小输入缺失，先索取最小必需球种定义
3. 将输入整理成一个结构化 YAML 确认块
4. 停下来等待用户明确确认该确认块
5. 在确认后继续进入 add-sport-market skill 工作流

除非输入已经完整且得到明确确认，否则不要从这个 command 直接开始改代码。

## 确认块模板

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

## 配套资产

- 主工作流 skill：`skills/add-sport-market/SKILL.md`
- 详细 playbook：`docs/add-sport-market-playbook.md`

## 重要规则

- 不要猜 SID、常量、topic 名、配置后缀或 Mongo 后缀
- 不要默认继承高级业务行为
- 在用户没有明确确认前，不要越过确认门槛继续执行
