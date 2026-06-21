# backend-ecc 内容边界

## 一、目的

本文档用于定义 backend-ecc 当前哪些内容应该进入主安装面，哪些内容仍应留在未来扩展或蒸馏候选区。

当前目标不是继续扩张通用 workflow 资产，而是保证：

- 已验证骨架稳定
- 第一批 generic capability assets 清楚可控
- 当前专项技能继续可用
- 后续 `raw/` 素材蒸馏不污染当前最小通用基线

---

## 二、当前资产分类

backend-ecc 当前把内容资产分为四类：

### 1. Skeleton / Infrastructure Assets
指支撑仓库安装、裁剪、巡检、恢复和说明的资产。

包括：
- `manifest.json`
- `profiles/`
- `adapters/`
- `install/`
- `.claude-plugin/`
- `.codex-plugin/`
- `docs/`

### 2. Generic Capability Assets
指当前已经进入 shipping surface 的最小通用 `becc-*` 资产。

当前包括：
- `becc-problem-framing`
- `becc-evidence-capture`
- `becc-impact-discovery`
- `becc-root-cause-debugging`
- `becc-impact-scope`
- `becc-debug-root-cause`
- `becc-verification-gate`
- `becc-graph-first-analysis`
- 对应模板

### 3. Isolated Domain Skills
指当前有明确使用场景、仍在使用、但不应被误抽象成通用主链能力的 skill。

当前包括：
- `market-add-sports`
- `market-game-conf`
- `cps-add-sport`

### 4. Future Distillation Candidates
指未来会从 `/Users/xie/go/src/gitlab/raw` 或其他来源中逐步蒸馏的候选素材。

这些内容当前 **不应** 直接进入主安装面，除非已经按当前 capability/loop 框架完成重写与审核。

---

## 三、当前通用资产进入主安装面的前提

未来新的 becc 通用资产要进入主安装面，至少要满足：

1. 属于明确 capability，而不是模糊功能名词
2. 能落在真实 loop 的一个确定位置
3. 能说明它在真实会话中改变了什么行为
4. 经过人工审核，不是直接搬运或未审草稿
5. 能明确决定应被承载为 command / skill / rule / template / agent 中的哪一种
6. 进入后能同步更新 `manifest.json`、`profiles/*.json` 与相关 docs

如果无法满足这些条件，默认不要进入。

---

## 四、当前不纳入的内容

以下内容当前默认不进入 backend-ecc 的通用安装面：

- 未按当前 capability/loop 框架重写的 raw 素材
- 无明确 capability 边界的泛工作流说明
- 通用 agent 层的大规模命名扩张
- 前端 / UI 主链技能
- 深 SaaS API 写操作集成
- 多 harness 扩展层
- control-plane
- GUI / dashboard
- 为未来假设场景预留的大规模 profile

---

## 五、当前结论

backend-ecc 当前的边界不是：

- “已经拥有完整通用 becc 生态”

而是：

> 保留骨架与专项，重建第一批最小 generic capability assets，并以此作为后续 raw 素材蒸馏的基线。
