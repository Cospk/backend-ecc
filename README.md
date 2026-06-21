# backend-ecc

backend-ecc 是一个面向 **Claude Code** 与 **Codex** 的 Go 后端开发资产骨架仓库。

它当前不是一个已经补齐的大通用 workflow catalog，而是一个已经完成 skeleton reset、并开始按 **capability-first / loop-aware** 方式重建的最小通用资产仓。

当前状态下，仓库主要承载三类内容：

- 已验证的安装 / profile / plugin / doctor 基础设施
- 第一批最小通用 `becc-*` capability assets
- 当前仍在使用的 isolated domain skills

当前 generic core 已经覆盖：问题定义、证据收敛、影响分析、设计比较、测试验证、专项 review、根因调试与阶段性交接收口。

---

## 当前支持的目标环境

- Claude Code
- Codex

---

## 安装方式

backend-ecc 当前继续采用：

- **plugin-first**
- **installer-backed**

也就是说：

- 对外仍保留插件声明面
- 实际安装仍由 `install/install.sh` 完成

### Claude Code

```bash
bash install/install.sh --target claude --profile backend-go
```

### Codex

```bash
bash install/install.sh --target codex --profile backend-go
```

### 本地开发测试

```bash
claude --plugin-dir /path/to/backend-ecc
```

---

## 当前资产结构

backend-ecc 当前内容分为三部分：

### 1. Skeleton / Maintenance Assets
当前保留：

- `manifest.json`
- `profiles/`
- `adapters/`
- `install/`
- `.claude-plugin/`
- `.codex-plugin/`
- `docs/`
- `templates/`

这些资产负责：
- 安装声明
- profile 裁剪
- doctor / repair / uninstall 生命周期治理
- blueprint、边界与演进说明

### 2. Generic Capability Assets（第一批）
当前第一批通用 becc 资产包括：

#### Commands
- `becc-impact-scope`
- `becc-debug-root-cause`
- `becc-go-test`
- `becc-go-review`
- `becc-backend-design`
- `becc-session-handoff`

#### Skills
- `becc-problem-framing`
- `becc-evidence-capture`
- `becc-impact-discovery`
- `becc-root-cause-debugging`
- `becc-go-testing`
- `becc-go-review`
- `becc-backend-design`
- `becc-session-handoff`

#### Rules
- `becc-verification-gate`
- `becc-graph-first-analysis`
- `becc-code-review`
- `becc-testing`（golang）

#### Templates
- `becc-problem-statement`
- `becc-impact-map`
- `becc-root-cause-analysis`
- `becc-tradeoff-analysis`
- `becc-validation-plan`
- `becc-pr-summary`
- `becc-session-handoff`

这批资产不是按完整 workflow 铺满，而是围绕最小 capability 与 loop 先建立一组可信基线。

### 3. Isolated Domain Skills
当前继续保留：

- `market-add-sports`
- `market-game-conf`
- `cps-add-sport`

这些内容服务于当前明确在用的专项流程，不强行抽象为通用 Go 后端主链能力。

---

## 当前 capability / loop 核心

第一批重建当前聚焦 9 个 capability：

- problem framing
- evidence capture
- impact discovery
- verification gating
- root-cause debugging
- go testing / tdd validation
- go review / delivery verdict
- backend design / tradeoff selection
- session handoff / closeout

当前主要围绕 3 条 loop 工作：

1. **Problem Convergence Loop**
   - `evidence -> framing -> unknowns -> more evidence or stop`
2. **Impact & Validation Loop**
   - `framed problem -> impact discovery -> validation surface -> implement/inspect -> adjust`
3. **Root-Cause Loop**
   - `symptom -> evidence -> hypotheses -> falsification -> confirmed cause or continue`

---

## Profiles

### `minimal`
最小 capability/loop 骨架 profile。

目标：
- 验证最小通用 becc 资产是否可安装、可发现、可约束行为

### `backend-go`
默认 profile。

目标：
- 承载第一批最小通用 becc 资产
- 继续兼容当前保留的 isolated domain skills

### `author`
维护者 profile。

目标：
- 面向 backend-ecc 本身维护
- 包含 docs / install / adapters / profiles / templates 等维护资产

---

## 设计原则

- 只聚焦 Go 后端开发主方向
- Claude Code 作为主执行器
- 浏览器只读证据采集优先于深 SaaS API 集成
- Graphify / understand-anything 作为 analysis 前置增强
- 模板、协议、规则优先于复杂运行时壳层
- 保留 isolated domain skills，但不让其反向主导通用骨架
- 先 capability，再 loop，再决定最小资产落盘
- 不再回到 workflow-first catalog 膨胀

---

## 当前状态

当前仓库处于 **v0.1 minimal generic rebuild** 阶段。

已经具备：
- install / doctor / repair / uninstall
- Claude / Codex 插件声明面
- profile / manifest / adapter 基础机制
- 第一批最小通用 becc 资产
- 当前仍在使用的 isolated domain skills

当前明确仍未做：
- 大规模通用 becc 资产扩张
- agent 层通用抽象重建
- raw 素材库的系统蒸馏与后续二轮优化

---

## 下一步

下一步推荐顺序：

1. 先在当前最小基线上验证行为与结构是否成立
2. 再查看 `/Users/xie/go/src/gitlab/raw` 中已有素材
3. 按当前 capability/loop 框架逐步蒸馏可吸收内容
4. 再做第二轮扩展，而不是直接批量搬运

---

## 进一步阅读

- `docs/blueprint-v1.md` — 当前蓝图与 capability/loop 重建方向
- `docs/content-boundaries.md` — 当前内容边界
- `docs/architecture.md` — 当前结构分层
- `docs/profiles.md` — profile 语义说明
- `docs/current-state.md` — 当前阶段状态记录
- `docs/asset-authoring-workflow.md` — 后续资产重建时的维护流程
- `docs/verification.md` — 当前验收边界
