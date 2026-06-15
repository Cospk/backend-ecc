# Hooks

当前 `backend-ecc` 的 hooks 层定位为：

- **轻量 hook 资产**
- **模板与占位结构**
- **未来运行时治理的预留接口**

而不是完整的 hooks runtime 系统。

## 当前状态

v0.1 阶段：

- `hooks/hooks.json` 仅提供最小空壳配置
- 不默认启用完整 SessionStart / PreToolUse / PostToolUse 运行时链
- 不依赖额外的 Node hook 脚本、dispatcher 或 governance 管线

这样设计的目的是：

- 避免在当前版本引入过重的 hook 依赖
- 避免在插件加载时触发不存在脚本的运行时错误
- 保留 hooks 层的目录与未来扩展位置

## 当前推荐用法

- 把 hooks 视为轻量资产与模板
- 当前版本优先验证内容层、插件层与安装层
- 若未来要引入更完整的 hooks runtime，应单独设计并验证

## 后续扩展方向

如果 backend-ecc 后续进入更成熟阶段，可以考虑逐步增加：

- 轻量质量门 hook
- 安全提示 hook
- 简单的 SessionStart bootstrap
- 更完整的运行时治理

但这些都不属于 v0.1 的默认交付范围。
