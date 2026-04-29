# 核心链路总览

这份文档用于记录系统级关键链路。当前先保留最重要、最明确的一条样板链路，后续逐步补充更多高频链路。

## 链路 1：上游数据进入推送组并推送到用户

### 总体路径
1. 上游数据商推送赛事与盘口数据
2. 水机进行预处理和错误过滤
3. 水机通过 Kafka 推送到聚合
4. 聚合进一步纠错和补全
5. 聚合通过 Kafka 推送给推送组和操盘组
6. 推送组处理盘口信息并继续向多个下游分发

## 样板链路：LOL 电竞盘口链路

### 链路说明
- 触发源：聚合
- 上游 Topic：`nw.aggregatorServer.mergeMarket.esport-lol.topic`
- `market-consumer` 消费该消息
- `market-consumer` 输出到：
  - Redis PubSub
  - Kafka Topic `nw.marketServer.oddsDiffEsportLOL`
- `push-server-gw` 接收后向操盘前端推送数据
- `c-push-server` 接收后继续推送统一 Topic `nw.cPushServer.oddsDiffMarket`
- `go-stomp` 消费统一 Topic
- `go-stomp` 通过 stomp 协议向用户推送数据

## 当前链路价值

这条链路适合作为首个标准样板，因为它已经覆盖了：

- 上游 Kafka 输入
- 推送组内部处理
- Redis PubSub 协同
- 多下游分发
- 面向内部前端与 C 端用户的双出口

## 后续建议补充的链路

1. 一条赛事级信息链路（操盘组方向）
2. 一条盘口状态更新链路
3. 一条调水 / 跳水链路
4. 一条异常定位链路
