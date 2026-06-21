---
paths:
  - "**/*.go"
  - "**/go.mod"
  - "**/go.sum"
---
# becc-testing

> 这条规则扩展通用 `becc-verification-gate`，为 Go 代码变更提供最小但硬性的测试约束。

## 目标

在 Go 代码变更中，优先采用最小、相关、可复跑的验证路径，而不是事后笼统说“应该没问题”。

## 强制要求

当任务涉及 Go 代码逻辑变更、bug 修复或测试补齐时，助手应优先考虑：

1. **最小相关测试范围**
   - 优先跑最相关 package / test target
   - 不要默认一上来就跑全仓 `go test ./...`

2. **TDD / Failure-first 倾向**
   - 对 bug 修复，优先补失败测试或最小复现
   - 至少说明当前是否观察到了 RED 或已有失败态

3. **Idiomatic Go tests**
   - 优先使用 table-driven tests
   - 适合时使用 subtests
   - helper 要明确使用 `t.Helper()`

4. **Go 专项验证线**
   - 相关测试通过
   - 需要时考虑 `-race`
   - 需要时考虑 coverage，而不是空泛声称“测过了”

## 推荐命令

根据最小验证范围选择，而不是盲目放大：

```bash
# 跑相关 package
go test ./path/to/package

# 跑相关测试并带详细输出
go test -run TestName ./path/to/package -v

# 需要时做 race 检查
go test -race ./path/to/package

# 需要时看 coverage
go test -cover ./path/to/package
```

## 禁止项

助手不得：
- 没有说明验证目标，就直接堆测试命令
- 在 bug 修复场景下跳过失败态确认
- 把“代码能编译”当成“逻辑已验证”
- 在未跑相关测试时写成“修复完成”

## 与其他资产的关系

这条规则通常配合：
- `becc-go-testing`
- `becc-go-test`
- `becc-verification-gate`
- `becc-root-cause-debugging`

它的目标是：

> 让 Go 代码改动至少经过一条最小、相关、可解释的测试验证路径。
