# market-server 服务组总览

`market-server` 不是整个业务系统本体，而是推送组中的一个核心服务组。它承担多球种盘口相关的查询、更新、事件消费、状态变更处理和对下游分发职责。

## 服务组定位

结合当前系统认知，`market-server` 的定位应当理解为：

- 属于推送组范围
- 位于聚合之后
- 同时承接 API 请求和异步数据处理
- 更偏向盘口级数据处理与分发
- 向 Redis PubSub 与 Kafka 两类通道输出结果

## 服务形态

### 1. market-server server 服务
职责：
- 对外提供 API 接口
- 处理盘口相关查询与更新
- 通过 Redis PubSub 发送事件通知给 consumer

### 2. market-consumer consumer 服务
职责：
- 处理上游 Kafka 数据
- 处理 Redis PubSub 事件数据
- 将处理后的结果继续向下游 Kafka 推送，或通过 PubSub 推送数据

## 在整体系统中的位置

按当前已知系统链路，`market-server` 所处的位置大致如下：

- 上游数据商提供原始数据
- 水机完成预处理
- 聚合完成进一步纠错和完整性处理
- 聚合向推送组分发数据
- `market-consumer` 消费来自聚合的 Kafka 数据
- `market-server` / `market-consumer` 继续完成盘口侧处理与事件分发
- 下游再流向 `push-server-gw`、`c-push-server`、`go-stomp`、95e、订单、结算等系统

## 核心职责

- 盘口查询与修改接口
- 盘口状态变化处理
- 调水、跳水相关处理
- 多球种盘口数据分发
- Redis PubSub 事件协同
- Kafka 下游数据推送

## 当前相关下游

### push-server-gw
- 接收各组通过 PubSub 方式发送的数据
- 通过 WebSocket 协议向操盘页面推送数据

### c-push-server
- 接收各组数据
- 做进一步整理
- 继续向下游 Kafka 推送统一主题数据

### go-stomp
- 消费 `c-push-server` 推送的 Kafka 数据
- 通过 API / stomp 协议向 95e 用户推送数据

## 一条已知真实链路

### LOL 电竞盘口链路
- 上游 Topic：`nw.aggregatorServer.mergeMarket.esport-lol.topic`
- `market-consumer` 消费消息
- 输出到 Redis PubSub
- 输出到 Kafka Topic `nw.marketServer.oddsDiffEsportLOL`
- `push-server-gw` 接收后向操盘前端推送
- `c-push-server` 接收后继续推送统一 Topic `nw.cPushServer.oddsDiffMarket`
- `go-stomp` 消费统一 Topic
- `go-stomp` 通过 stomp 协议向用户推送数据

## 当前优先阅读路径

1. 先读 `00-system/system-overview.md`
2. 再读本文件
3. 再读 `20-services/market-server/code-map.md`

## 当前待补充

1. `market-server` server 与 consumer 的更细职责边界
2. PubSub 内部事件主题清单
3. Kafka 输出主题清单
4. push-server-gw 与 c-push-server 的更细分工
