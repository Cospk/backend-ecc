# backend-ecc

backend-ecc 是一个面向 **Claude Code** 与 **Codex** 的精简 Go 后端开发工作流生态。

它聚焦一条最小但完整的 Go 后端开发闭环：

- 需求分析
- 实现方案设计
- Go 编码实现
- Go 测试验证
- Bug 定位与修复
- 提交 PR 前收口

当前版本聚焦 Go 后端开发闭环与基础安装治理能力，适合作为 Claude Code / Codex 下的精简工作流插件生态。

当前正式源仓：
- `https://github.com/Cospk/backend-ecc`

---

## 当前支持的目标环境

- Claude Code
- Codex

---

## 安装方式

backend-ecc 当前采用：

- **插件优先（plugin-first）**
- **安装器兜底（installer-backed）**

也就是说：
- 对外优先提供插件声明面
- 实际安装仍由 `install/install.sh` 完成

### 推荐方式：插件方式理解、安装器方式落地

当前 v0.1 阶段，推荐先使用安装器完成落地：

#### Claude Code

```bash
bash install/install.sh --target claude --profile backend-go
```

#### Codex

```bash
bash install/install.sh --target codex --profile backend-go
```

### 本地开发测试：直接加载插件目录

如果你在本地开发和验证当前分支内容，推荐直接使用 Claude Code 官方支持的本地插件目录方式：

```bash
claude --plugin-dir /path/to/backend-ecc
```

这更适合：
- 当前分支开发
- 插件目录加载验证
- 本地行为 smoke test

### 高级/测试用法：指定目标目录

如果你在做隔离验证或 smoke test，可以显式指定安装目标目录：

```bash
bash install/install.sh --target claude --profile backend-go --dest /path/to/test-repo
```

说明：
- `--dest` 主要用于测试、隔离验证和高级场景
- 普通安装场景下，不需要显式指定它

---

## Profiles

### `minimal`
最小可用的 Go 后端工作流，适合先试装：

- `plan`
- `go-build`
- `go-review`
- `go-test`
- `code-review`

特点：
- 不带 hooks
- 不带 `browser-qa`
- 不带 `repo-scan`
- 更适合轻量项目或首次试用

### `backend-go`
默认 profile，覆盖 Go 后端开发完整主链：

- 规划
- Go 构建修复
- Go 专项审查
- Go 测试
- 覆盖率
- checkpoint
- PR 前收口

特点：
- 带完整最小内容集
- 当前 hooks 只作为轻量资产存在，不提供完整 runtime
- 是当前推荐的默认安装 profile

### `author`
维护者 profile，用于维护 backend-ecc 本身：

- 包含 `backend-go` 全部能力
- 额外包含 docs / adapters / install / profile 资产

---

## 仓库结构

- `manifest.json` — 内容清单与默认 profile 元数据
- `profiles/` — 安装 profile 定义（`minimal`、`backend-go`、`author`）
- `adapters/` — Claude / Codex 的目标路径映射
- `commands/` — 面向用户的命令入口
- `agents/` — 可委派的专职角色
- `skills/` — 可复用的工作流与模式知识
- `rules/` — 通用基线规则与 Go 专项规则
- `hooks/` — 轻量 hook 资产与模板
- `install/` — install / uninstall / doctor / repair 脚本
- `.claude-plugin/` — Claude Code 插件声明面
- `.codex-plugin/` — Codex 插件声明面
- `docs/verification.md` — v0.1 验收与验证标准

---

## 设计原则

- 内容层只聚焦 Go 后端开发闭环
- 内容层与安装/适配逻辑严格分离
- v0.1 保持 hooks 轻量，不让其成为复杂度中心
- 优先保证可安装、可发现、可验证、可修复

---

## 当前状态

当前仓库处于 **v0.1 原型阶段**。

已经具备：
- 内容层
- profile
- adapter
- install / doctor / repair / uninstall
- Claude/Codex 插件声明面

但仍未完成：
- 真实插件运行时行为归因验证
- marketplace / GitHub 导入链路验证
- 更完整的 hooks runtime

---

## 验证与维护文档

- `docs/verification.md` — 验收与验证标准
- `docs/current-state.md` — 当前阶段状态记录

---

## 当前明确不做的事

v0.1 阶段不做：

- 多 harness 扩展（除 Claude/Codex 外）
- 完整 control-plane
- GUI / dashboard
- sqlite / state store
- auto-update
- 大规模 catalog 扩张

---

## 进一步阅读

- `docs/architecture.md` — backend-ecc 的分层设计
- `docs/profiles.md` — profiles 的边界与选择建议
- `docs/verification.md` — 验收与验证标准
- `docs/current-state.md` — 当前阶段状态记录
