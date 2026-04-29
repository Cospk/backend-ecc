# market-server Code Map

这份 Code Map 的目标不是解释所有实现细节，而是帮助快速确定：某类需求或问题应该先看哪些文件。

## 一、启动与依赖注入

### 服务启动入口
- `cmd/market-server/main.go`
  - API 服务启动入口
  - 加载配置、初始化基础依赖、调用 `wireApp`

### consumer 启动入口
- `cmd/market-consumer/main.go`
  - 消费侧启动入口

### wire 注入定义
- `cmd/market-server/wire.go`
- `cmd/market-server/wire_gen.go`
- `cmd/market-consumer/wire.go`
- `cmd/market-consumer/wire_gen.go`

## 二、server 组装层

### server provider 注册
- `internal/server/server.go`

### 各球种 match router 构造
- `internal/server/matchrouter.go`

### HTTP / gRPC server
- `internal/server/http.go`
- `internal/server/grpc.go`

### consumer / producer
- `internal/server/consumer.go`
- `internal/server/producer.go`

## 三、对外服务层

### 盘口相关接口入口
- `internal/service/market.go`

### 事件处理入口
- `internal/service/event.go`

### 其他服务入口
- `internal/service/service.go`
- `internal/service/champion_market.go`
- `internal/service/manual_match_market.go`
- `internal/service/test.go`

## 四、球种业务实现层

### 公共业务逻辑
- `internal/biz/common/helper.go`
- `internal/biz/common/market.go`
- `internal/biz/common/market_update_status.go`
- `internal/biz/common/process/match_router.go`
- `internal/biz/common/process/match_runner.go`
- `internal/biz/common/process/market_runner.go`
- `internal/biz/common/process/market_filter.go`

### 典型球种实现
- `internal/biz/football/*`
- `internal/biz/basketball/*`
- `internal/biz/tennis/*`
- `internal/biz/efootball/*`
- `internal/biz/ebasketball/*`
- `internal/biz/baseball/*`
- `internal/biz/badminton/*`
- `internal/biz/tableTennis/*`

## 五、数据、配置与消息
- `internal/data/*`
- `internal/conf/config.go`
- `internal/pkg/mq/*`
- `internal/pkg/cpush/*`
- `pkg/pod/*`

## 六、当前高频定位建议

### 修改接口
优先看：
- `internal/service/market.go`
- 对应球种 `internal/biz/<sport>/market.go`

### 修改事件链路
优先看：
- `internal/service/event.go`
- 对应球种 `internal/biz/<sport>/process/*`

### 修改推送逻辑
优先看：
- `internal/pkg/cpush/odds_diff_match.go`
- `internal/pkg/mq/kafka.go`

### 修改配置或 topic
优先看：
- `internal/conf/config.go`
- 相关 `configs/*.yaml`
