# backend-ecc 架构说明

## 一、整体定位

backend-ecc 是一个面向 **Claude Code** 与 **Codex** 的 Go 后端开发资产骨架仓库。

当前版本聚焦于：

- Go 后端主方向
- 安装 / 巡检 / 恢复 / 卸载基础设施
- profile / manifest / adapter 声明机制
- 最小插件声明层
- 第一批 capability-first / loop-aware generic becc assets
- isolated domain skills 保留

当前目标不是提供一个大 catalog，而是建立一组可信、可验证、可逐步扩展的最小通用能力底座。

---

## 二、核心设计原则

backend-ecc 当前遵循以下原则：

1. **只聚焦 Go 后端主方向**
2. **内容骨架与安装治理层分离**
3. **plugin-first，installer-backed**
4. **浏览器只读证据采集优先于深 SaaS API 集成**
5. **Graphify / understand-anything 作为分析前置增强**
6. **模板、协议、规则优先于复杂运行时壳层**
7. **isolated domain skills 可以并存，但不反向主导通用骨架**
8. **先 capability，再 loop，再决定最小资产落盘**

---

## 三、分层结构

backend-ecc 当前可以分为六层：

### 1. Skeleton / Maintenance Layer
负责仓库基础安装与维护能力。

包括：
- `manifest.json`
- `profiles/`
- `adapters/`
- `install/`
- `docs/`
- `templates/`

作用：
- 定义安装面
- 定义不同 profile 的能力边界
- 定义不同 target 的落盘路径
- 管理 install / doctor / repair / uninstall
- 维护 blueprint、边界与验证文档

### 2. Plugin Layer
负责对目标 harness 暴露插件声明面。

包括：
- `.claude-plugin/`
- `.codex-plugin/`

作用：
- 声明 backend-ecc 可作为目标平台插件内容源
- 定义默认 target / profile
- 将插件安装体验与底层安装器逻辑连接起来

### 3. Generic Capability Layer
负责通用 becc 资产。

当前第一批包括：
- `commands/becc-impact-scope.md`
- `commands/becc-debug-root-cause.md`
- `commands/becc-go-test.md`
- `commands/becc-go-review.md`
- `commands/becc-backend-design.md`
- `commands/becc-session-handoff.md`
- `skills/becc-problem-framing/SKILL.md`
- `skills/becc-evidence-capture/SKILL.md`
- `skills/becc-impact-discovery/SKILL.md`
- `skills/becc-root-cause-debugging/SKILL.md`
- `skills/becc-go-testing/SKILL.md`
- `skills/becc-go-review/SKILL.md`
- `skills/becc-backend-design/SKILL.md`
- `skills/becc-session-handoff/SKILL.md`
- `rules/common/becc-verification-gate.md`
- `rules/common/becc-graph-first-analysis.md`
- `rules/common/becc-code-review.md`
- `rules/golang/becc-testing.md`
- 对应 templates

作用：
- 提供最小通用能力
- 用 loop-aware 方式约束问题收敛、影响分析、验证与 debug

### 4. Isolated Domain Skills Layer
负责保留当前仍有现实价值的专项业务 skill。

当前包括：
- `market-add-sports`
- `market-game-conf`
- `cps-add-sport`

作用：
- 服务当前仍在使用的专项流程
- 不强制抽象为通用 Go 后端能力

### 5. Reserved Expansion Layer
负责为后续通用能力扩展保留边界。

包括：
- `agents/`
- 更多 `becc-*` namespace

作用：
- 等待后续在设计、review、closeout 等能力成熟后再进入
- 避免一次性铺满 catalog

### 6. Documentation / Blueprint Layer
负责让维护者理解当前最小通用重建状态与后续方向。

包括：
- `README.md`
- `docs/blueprint-v1.md`
- `docs/content-boundaries.md`
- `docs/current-state.md`
- `docs/architecture.md`
- `docs/profiles.md`
- `docs/asset-authoring-workflow.md`
- `docs/verification.md`

---

## 四、为什么第一批只重建最小 capability 集

当前第一批没有回到旧 workflow-first 的“整条主链补齐”，原因是：

- 一次性补全会很快回到低信任大草稿状态
- capability 边界需要先用最小样本验证
- agent 层与更大 catalog 需要晚于 capability 本体

因此当前策略是：

- 先重建 problem framing
- evidence capture
- impact discovery
- verification gating
- root-cause debugging
- go testing / tdd validation
- backend design / tradeoff selection
- session handoff / closeout

先让最小 generic core 成立，再逐步吸收更多素材。

---

## 五、当前范围

当前版本范围聚焦于：

- Claude / Codex 双目标
- install / doctor / repair / uninstall 的最小生命周期治理
- 最小插件声明层
- 第一批 generic becc capability assets
- isolated domain skills

以下能力暂不纳入当前版本的通用资产范围：

- 通用 agent 层
- design / review / closeout 的完整 generic 重建
- 多 harness 扩展（除 Claude / Codex）
- control-plane
- GUI / dashboard
- sqlite / state store
- auto-update
- 大规模 catalog 扩展
- 深 SaaS API 集成

---

## 六、当前阶段结论

当前 backend-ecc 可被视为：

> 一个具备安装治理、插件声明、文档边界、第一批最小通用 capability assets 与专项保留资产的 v0.1 minimal generic rebuild 仓库。

它的下一阶段重点是：

- 先验证这批最小 generic assets 是否真实成立
- 再查看 raw 素材并按 capability/loop 框架逐步蒸馏
- 再决定是否扩展 design / review / closeout 等更大通用能力
