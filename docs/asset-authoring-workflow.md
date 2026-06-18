# backend-ecc 资产编写标准流程

## 一、目的

本文档是 backend-ecc 维护者与 AI 助手在新增或修改仓库资产时必须遵守的标准流程。

当前仓库已经收缩为少量高价值专项 skill，因此本文档的目标不是支撑一个大 catalog，而是防止出现以下错误：

- 只写了内容文件，没有登记 `manifest.json`
- 更新了 `manifest.json`，但没有进入正确 profile
- 把资产加入了 profile，却没有检查安装与发现链路
- 修改了安装语义，却没有回看 plugin declaration
- 做完内容修改后，没有补文档与验证

backend-ecc 当前采用的是：

- **plugin-first**
- **installer-backed**

因此，新增一个 asset 从来都不只是“多一个文件”。

---

## 二、适用范围

本文档适用于以下资产的新增、删除与修改：

- `commands/`
- `skills/`
- `profiles/`
- 与安装、发现、默认 profile 相关的 metadata / docs

当前默认不提供：

- 通用 agents
- 通用 rules
- 默认 shipping hooks

如果未来重新引入这些类别，也必须遵守本文档。

---

## 三、核心原则

### 1. 内容层不是交付完成

在 backend-ecc 中，新增一个内容文件只代表你改了 **内容层**，不代表该能力已经真正纳入生态。

一个完整的 asset 改动，至少要经过以下五层检查：

1. 内容层（Content Layer）
2. 元数据层（Metadata Layer）
3. 安装治理层（Installer Layer）
4. 插件声明层（Plugin Layer）
5. 文档与验证层（Documentation / Verification Layer）

### 2. 单用途边界优先

新增资产前先问：

- 它是否真的服务于当前已确定的专项 skill 方向
- 它是否会把仓库重新带回“通用 workflow 插件”方向
- 它是否只是临时觉得“以后可能有用”

如果答案偏向通用化、抽象化或预留化，默认不要加。

### 3. 普通新增通常不改 plugin.json，但必须显式检查

普通新增 command / skill，通常 **不需要** 改：

- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`

但以下情况必须回看 plugin declaration：

- 修改默认 profile
- 修改 install script 或参数
- 修改 content root
- 引入新的 installable category
- 增加新的 target harness

---

## 四、backend-ecc 的五层检查面

### 1. 内容层
当前主要负责：

- `commands/`
- `skills/`

### 2. 元数据层
负责“仓库里声明有哪些能力”：

- `manifest.json`
- `profiles/*.json`
- `adapters/*/install-map.json`

### 3. 安装治理层
负责把 profile 声明的资产正确落盘：

- `install/install.sh`
- `install/doctor.sh`
- `install/repair.sh`
- `install/uninstall.sh`

### 4. 插件声明层
负责对 Claude Code / Codex 暴露插件入口：

- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`

### 5. 文档与验证层
负责让维护者知道怎么写、怎么装、怎么验：

- `README.md`
- `docs/architecture.md`
- `docs/profiles.md`
- `docs/verification.md`
- `docs/current-state.md`
- `docs/market-add-sports-playbook.md`

---

## 五、资产类型矩阵

| 资产类型 | 内容文件 | 必须登记 | 必须做 profile 决策 | 必须审查 install / plugin | 最低验证 |
|---|---|---|---|---|---|
| Command | `commands/<name>.md` | `manifest.json` | 是 | 是 | 结构 + 安装 + 发现 |
| Skill | `skills/<name>/SKILL.md` | `manifest.json` | 是 | 是 | 结构 + 安装 + 发现 |
| Profile | `profiles/<name>.json` | 视情况更新 `manifest.json` / docs | 不适用 | 是 | 结构 + 安装 + repair |
| 维护型附加资产 | docs / install / adapters / plugin docs | 视情况 | 是 | 是 | 一致性 + 安装验证 |

---

## 六、强制执行顺序

### Step 1：先定义资产目标与边界
先回答清楚：

- 这个资产是否直接服务当前已确定的专项 skill
- 它是用户入口、工作流说明，还是维护辅助资产
- 它是否会扩大产品边界

### Step 2：创建或修改内容文件
按资产类型落到正确位置：

- command → `commands/<name>.md`
- skill → `skills/<name>/SKILL.md`
- profile → `profiles/<name>.json`

### Step 3：更新 `manifest.json`
所有 installable asset 都必须检查 `manifest.json`：

- `content.commands`
- `content.skills`
- `defaultProfile`

### Step 4：更新目标 profile
当前优先检查：

- `profiles/minimal.json`
- `profiles/backend-go.json`
- `profiles/author.json`

### Step 5：检查 install / adapter 假设是否仍成立
重点检查：

- `install/install.sh`
- `install/doctor.sh`
- `install/repair.sh`
- `adapters/claude/install-map.json`
- `adapters/codex/install-map.json`

### Step 6：检查 plugin declaration 是否需要变化
必须审查：

- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`

### Step 7：更新文档
至少检查是否需要更新：

- `README.md`
- `docs/architecture.md`
- `docs/profiles.md`
- `docs/verification.md`
- `docs/current-state.md`
- `docs/market-add-sports-playbook.md`

### Step 8：执行验证
至少做：

1. 结构验证
2. 安装验证
3. 发现验证
4. 恢复验证

### Step 9：满足 Definition of Done 后才算完成
在 DoD 没闭合之前，不得宣称“这个 asset 已完成”。

---

## 七、Definition of Done

以下条件全部成立后，asset 变更才算完成：

- [ ] 内容文件已创建或修改完成
- [ ] `manifest.json` 已同步登记
- [ ] 目标 `profiles/*.json` 已完成显式决策
- [ ] install / adapter / plugin declaration 已完成审查
- [ ] 相关文档已更新
- [ ] 结构验证已完成
- [ ] 安装验证已完成
- [ ] 发现验证已完成（对 command / skill 为强制）
- [ ] 恢复验证已考虑或已执行
- [ ] 没有把仓库重新扩张回通用 workflow 方向
