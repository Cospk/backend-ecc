# backend-ecc v1 骨架蓝图

## 一、目标

backend-ecc v1 的目标不是继续扩张 skill catalog，也不是回到一轮未经充分审核的 workflow-first 草稿。

它当前要解决的是：

- 保留已经验证过的仓库骨架与安装治理能力
- 保留当前仍有现实价值的 isolated domain skills
- 建立一组最小、可信的 generic becc capability assets
- 以 capability-first / loop-aware 的方式逐步吸收后续素材与经验

当前保留的专项 skill：

- `market-add-sports`
- `market-game-conf`
- `cps-add-sport`

继续作为 isolated domain skills 保留，不要求在当前阶段强制重构进通用骨架。

---

## 二、设计原则

backend-ecc 当前按以下原则设计：

1. **Claude Code 主导**
2. **Go 后端主方向优先**
3. **浏览器只读证据采集优先于深 SaaS API 集成**
4. **Graphify / understand-anything 作为分析前置增强**
5. **模板、协议、规则优先于运行时壳层**
6. **先建立可信 capability，再扩通用资产面**
7. **先 loop 可验证，再补 workflow 叙事**
8. **isolated domain skills 并存，但不反向主导通用主链**

---

## 三、当前 capability map（第一批）

第一批只重建最小 generic capability 集：

### 1. Problem Framing
目标：
- 先收敛问题定义、约束、未知点与成功标准

### 2. Evidence Capture
目标：
- 把页面、日志、文档、导出材料转成结构化事实与歧义点

### 3. Impact Discovery
目标：
- 在修改前收敛影响系统、代码路径与验证面

### 4. Verification Gating
目标：
- 强制区分 Changed / Verified / Not Run / Risks
- 未验证不宣称完成

### 5. Root-Cause Debugging
目标：
- 把 symptom、evidence、hypotheses、falsification 与 root cause 状态分开

### 6. Go Testing / TDD Validation
目标：
- 把 Go 验证从事后补跑，改为带有 RED/GREEN/复跑逻辑的主执行路径

### 7. Go Review / Delivery Verdict
目标：
- 在 Go 变更完成后，用 correctness、error handling、context/concurrency、安全与验证面给出是否可交付的结构化结论

### 8. Backend Design / Tradeoff Selection
目标：
- 在 scope 之后、编码之前，给出最小可行方案比较、推荐路径与验证计划

### 9. Session Handoff / Closeout
目标：
- 在一个阶段结束时，把已完成、改动、验证、未执行项、风险与下一步收口成可继续推进的交接产物

---

## 四、当前 loop map（第一批）

### 1. Problem Convergence Loop
- `evidence -> framing -> unknowns -> more evidence or stop`

用途：
- 先把问题收敛到可行动状态

### 2. Impact & Validation Loop
- `framed problem -> impact discovery -> validation surface -> implement/inspect -> adjust`

用途：
- 在编码前控制范围，并明确验证面

### 3. Root-Cause Loop
- `symptom -> evidence -> hypotheses -> falsification -> confirmed cause or continue`

用途：
- 在故障与 debug 场景中防止症状修补

---

## 五、当前最小通用资产集

### Commands
- `becc-impact-scope`
- `becc-debug-root-cause`
- `becc-go-test`
- `becc-go-review`
- `becc-backend-design`
- `becc-session-handoff`

### Skills
- `becc-problem-framing`
- `becc-evidence-capture`
- `becc-impact-discovery`
- `becc-root-cause-debugging`
- `becc-go-testing`
- `becc-go-review`
- `becc-backend-design`
- `becc-session-handoff`

### Rules
- `becc-verification-gate`
- `becc-graph-first-analysis`
- `becc-code-review`
- `becc-testing`

### Templates
- `becc-problem-statement`
- `becc-impact-map`
- `becc-root-cause-analysis`
- `becc-tradeoff-analysis`
- `becc-validation-plan`
- `becc-pr-summary`
- `becc-session-handoff`

### Agents
当前第一批 **不引入通用 agent**。

原因：
- agent 层最容易过早抽象
- 当前优先验证 capability 本身是否成立
- 避免重走“先命名很多角色、后怀疑可信度”的老路

---

## 六、当前 v1 范围内真实成立的内容

当前可被视为“真实成立”的内容是：

- install / doctor / repair / uninstall
- plugin declaration
- profile / manifest / adapter 机制
- 第一批最小 generic becc assets
- blueprint / architecture / boundaries / verification 文档
- isolated domain skills

当前仍不应宣称已存在的内容是：

- 完整通用 becc workflow 链
- 已经蒸馏完成的 raw 素材库通用体系

---

## 七、后续演进方式

下一轮不应直接大规模补文件。

更合理顺序是：

1. 在当前最小基线上验证行为与结构
2. 再查看 `/Users/xie/go/src/gitlab/raw` 中已有素材
3. 用当前 capability/loop 框架判断：
   - 哪些可吸收
   - 哪些只适合作为素材
   - 哪些不兼容，应放弃
4. 再逐步扩展 design / review / closeout 等能力

---

## 八、当前结论

backend-ecc 当前更准确的定义是：

> 一个以 Claude Code 为主执行器、面向 Go 后端开发方向、已具备安装治理与插件声明骨架、并完成第一批最小 generic becc capability assets 重建的仓库。

它当前的价值不在于“资产很多”，而在于：

- 边界清楚
- 命名清楚
- 第一批通用能力已回到 shipping surface
- 后续可以用 capability/loop 框架逐步蒸馏 raw 素材
