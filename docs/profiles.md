# backend-ecc Profiles 说明

## 一、Profiles 的作用

backend-ecc 通过 profile 控制安装范围。

当前 profile 的目标不是暴露一套完整通用 workflow 资产，而是：

- 保持安装面可解释
- 保持最小 generic core 可验证
- 保留当前仍在使用的专项 skill
- 为后续 capability/loop 扩展保留稳定承载面

---

## 二、当前可用 Profiles

### 1. `minimal`

`minimal` 是最小 capability/loop profile，适合：

- 初次试装
- 验证最小 generic becc 资产是否成立
- 验证当前仓库 install / doctor / plugin 机制是否与 generic core 一致

#### 当前包含

##### Commands
- `becc-impact-scope`
- `becc-go-test`
- `becc-go-review`
- `becc-backend-design`
- `becc-session-handoff`

##### Skills
- `becc-problem-framing`
- `becc-impact-discovery`
- `becc-go-testing`
- `becc-go-review`
- `becc-backend-design`
- `becc-session-handoff`

##### Rules
- `becc-verification-gate`
- `becc-graph-first-analysis`
- `becc-code-review`
- `becc-testing`

#### 特点

- 面最小
- 只验证 problem framing + impact discovery 这条最短 generic 路径
- 不默认安装专项 skill

---

### 2. `backend-go`

`backend-go` 是默认 profile，适合：

- 当前需要使用最小通用 generic assets 的 Go 后端项目
- 当前仍需要保留专项 skills 的场景
- 作为后续 capability/loop 扩展的默认安装面

#### 当前包含

##### Commands
- `becc-impact-scope`
- `becc-debug-root-cause`
- `becc-go-test`
- `becc-go-review`
- `becc-backend-design`
- `becc-session-handoff`

##### Skills
- `becc-problem-framing`
- `becc-evidence-capture`
- `becc-impact-discovery`
- `becc-root-cause-debugging`
- `becc-go-testing`
- `becc-go-review`
- `becc-backend-design`
- `becc-session-handoff`
- `market-add-sports`
- `market-game-conf`
- `cps-add-sport`

##### Rules
- `becc-verification-gate`
- `becc-graph-first-analysis`
- `becc-code-review`
- `becc-testing`

#### 特点

- 覆盖当前第一批 generic core
- 继续兼容保留专项 skills
- 当前不引入 generic agents
- 已包含 Go review 收口能力
- 已包含 backend design 决策能力
- 已包含 session handoff / closeout 能力

---

### 3. `author`

`author` 是维护者 profile，适合：

- backend-ecc 自身开发者
- 维护 install / docs / adapters / profiles / templates 的人

#### 当前包含
- 继承 `backend-go`
- 额外包括：
  - `docs`
  - `install`
  - `adapters`
  - `profiles`
  - `templates`
  - `hooks/templates`（若后续继续保留）

#### 特点

- 不面向普通使用者
- 面向生态维护工作
- 更适合维护当前 generic core 与后续蒸馏素材

---

## 三、如何选择

### 如果你只是验证当前 generic core
推荐从：
- `minimal`
开始

### 如果你需要当前最完整的 backend-ecc 安装面
使用：
- `backend-go`

### 如果你要维护 backend-ecc 本身
使用：
- `author`

---

## 四、当前不建议做的事

当前不建议：

- 在未验证当前第一批 generic core 前继续大规模扩充 becc 资产
- 过早引入通用 agent 层
- 在 capability/loop 边界未稳前扩充大量 profile
- 为未来假设场景提前设计 profile

---

## 五、当前结论

backend-ecc 当前的 profile 设计不是围绕“完整通用主链”，而是：

> 以最小 generic core + 专项保留为现实基础，为后续 capability-first / loop-aware 扩展保留稳定安装面。
