# backend-ecc Codex 插件层

这是 backend-ecc 面向 **Codex** 的最小插件声明面。

## 作用

- 声明该仓库可作为 Codex 的插件内容源
- 指向现有的 `install/install.sh` 安装逻辑
- 默认使用 `backend-go` profile

## 关系

插件层本身不拥有 commands / agents / skills / rules / hooks 的业务内容。
它只负责：

- 声明插件身份
- 指向安装入口
- 约定默认 target 与默认 profile

真正的内容资产仍然位于仓库根目录：

- `commands/`
- `agents/`
- `skills/`
- `rules/`
- `hooks/`

## 当前策略

当前采取：

- **plugin-first**：优先保留插件安装入口
- **installer-backed**：实际安装仍由 `install/install.sh` 执行

也就是说，插件层是声明面，安装器是执行面。

## 默认安装语义

默认等价于：

```bash
bash install/install.sh --target codex --profile backend-go
```

## 当前状态

v0.1 阶段插件层仅提供最小声明，不包含 marketplace 元数据与完整 bootstrap 逻辑。
