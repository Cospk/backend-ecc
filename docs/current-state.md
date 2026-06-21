# backend-ecc 当前状态（v0.1 minimal generic rebuild）

## 一、当前定位

backend-ecc 当前定位为：

- 面向 **Claude Code** 与 **Codex** 的 Go 后端开发资产骨架仓库
- 采用 **plugin-first, installer-backed** 的设计思路
- 保留已验证骨架与专项 skill，并已重建第一批最小通用 becc capability assets

当前不是“完整通用主链已补齐”的状态，而是“最小 generic core 已重新进入 shipping surface”的状态。

---

## 二、当前已存在的真实内容

### 1. Generic becc Assets（第一批）

#### Commands
- `commands/becc-impact-scope.md`
- `commands/becc-debug-root-cause.md`
- `commands/becc-go-test.md`
- `commands/becc-go-review.md`
- `commands/becc-backend-design.md`
- `commands/becc-session-handoff.md`

#### Skills
- `skills/becc-problem-framing/SKILL.md`
- `skills/becc-evidence-capture/SKILL.md`
- `skills/becc-impact-discovery/SKILL.md`
- `skills/becc-root-cause-debugging/SKILL.md`
- `skills/becc-go-testing/SKILL.md`
- `skills/becc-go-review/SKILL.md`
- `skills/becc-backend-design/SKILL.md`
- `skills/becc-session-handoff/SKILL.md`

#### Rules
- `rules/common/becc-verification-gate.md`
- `rules/common/becc-graph-first-analysis.md`
- `rules/common/becc-code-review.md`
- `rules/golang/becc-testing.md`

#### Templates
- `templates/problem-definition/becc-problem-statement.md`
- `templates/scope/becc-impact-map.md`
- `templates/debugging/becc-root-cause-analysis.md`
- `templates/design/becc-tradeoff-analysis.md`
- `templates/design/becc-validation-plan.md`
- `templates/closeout/becc-pr-summary.md`
- `templates/closeout/becc-session-handoff.md`

### 2. Isolated Domain Skills
当前保留：
- `skills/market-add-sports/SKILL.md`
- `skills/market-game-conf/SKILL.md`
- `skills/cps-add-sport/SKILL.md`

### 3. 元数据层
已具备：
- `VERSION`
- `manifest.json`
- `profiles/minimal.json`
- `profiles/backend-go.json`
- `profiles/author.json`
- `adapters/claude/install-map.json`
- `adapters/codex/install-map.json`

### 4. 插件层
已具备：
- `.claude-plugin/plugin.json`
- `.claude-plugin/README.md`
- `.codex-plugin/plugin.json`
- `.codex-plugin/README.md`

### 5. 安装治理层
已具备：
- `install/install.sh`
- `install/doctor.sh`
- `install/repair.sh`
- `install/uninstall.sh`
- `install/lib.sh`

---

## 三、当前明确已做的事

已完成：
- install / doctor / repair / uninstall 基础能力
- Claude / Codex 插件声明层
- isolated domain skills 保留
- 低信任旧 becc workflow 草稿资产清退
- 第一批最小 generic becc capability assets 回接至 shipping surface
- Go testing / TDD capability 已补入 generic core
- Go review / delivery verdict capability 已补入 generic core
- Backend design / tradeoff capability 已补入 generic core
- Session handoff / closeout capability 已补入 generic core
- metadata / profiles / docs 与当前状态重新对齐

---

## 四、当前仍未宣称的事

当前不应宣称 backend-ecc 已经具备：

- 完整通用 becc workflow 链
- 通用 agent 体系
- 已完成对 `raw/` 素材库的系统蒸馏

这些内容属于下一轮扩展，而不是当前事实。

---

## 五、下一阶段重点

下一阶段重点应是：

1. 先验证当前第一批 generic assets 的结构与行为是否成立
2. 再查看 `/Users/xie/go/src/gitlab/raw` 中已有素材
3. 按 capability / loop 框架建立蒸馏对照
4. 再决定第二批扩展能力

---

## 六、当前结论

backend-ecc 当前已经不再只是“骨架 + 三个专项 skill”的状态，
但也还不是“完整 generic becc 生态”。

它更准确的定义是：

> 一个具备安装治理与插件声明基础能力、保留专项 skill、并已重建第一批最小 generic becc capability assets 的 v0.1 仓库。
