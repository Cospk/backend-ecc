# backend-ecc 验收标准（v0.1）

## 目标

backend-ecc v0.1 的目标不是复刻 ECC 全家桶，而是提供一个可安装、可裁剪、可验证、可修复的 Go 后端开发插件生态，当前仅支持：

- Claude Code
- Codex

覆盖的开发闭环：

1. 需求分析
2. 方案设计
3. Go 编码实现
4. Go 测试与验证
5. Bug 定位与修复
6. 提交前收口

---

## 总体验收原则

验收不是验证“文件是否存在”，而是验证以下四件事：

1. 安装是否正确
2. 内容是否可被目标 harness 发现
3. 安装后行为是否真实生效
4. 出现漂移或缺失时是否可发现并修复

因此，v0.1 验收拆分为五层：

1. 结构验证（Structure Validation）
2. 安装验证（Installation Validation）
3. 发现验证（Discoverability Validation）
4. 行为验证（Behavior Validation）
5. 恢复验证（Repairability Validation）

---

## 一、结构验证

### 目的
证明 backend-ecc 源仓本身是自洽的。

### 验证对象
- `manifest.json`
- `profiles/*.json`
- `adapters/*/install-map.json`
- `commands/`
- `agents/`
- `skills/`
- `rules/`
- `hooks/`

### 验证项
1. `manifest.json` 可解析
2. 每个 profile 可解析
3. 每个 adapter install-map 可解析
4. 每个 profile 中引用的 command 都存在
5. 每个 profile 中引用的 agent 都存在
6. 每个 profile 中引用的 skill 目录都存在且含 `SKILL.md`
7. 每个 profile 中引用的 rule 都存在
8. hooks 列表引用的 hook 文件都存在
9. `VERSION` 存在且与 manifest 版本一致

### 验收标准
- PASS：以上全部成立
- WARN：仅缺少可选项（例如可选 hook 模板）
- FAIL：任一 profile/adapter/manifest 不可解析，或引用丢失

---

## 二、安装验证

### 目的
证明安装脚本能按 target + profile 正确落盘。

### 最小验证矩阵
必须至少覆盖：

- Claude Code + minimal
- Claude Code + backend-go
- Codex + minimal
- Codex + backend-go

当 `backend-go` 新增独立 skill（例如 `nw-game-conf`）时，还必须额外确认：
- 安装结果中存在 `skills/nw-game-conf/SKILL.md`
- `minimal` profile 不会误装该 skill

### 验证项
1. 安装命令退出码为 0
2. 目标根目录存在
3. 安装路径与 adapter 定义一致
4. profile 声明的内容全部安装
5. profile 未声明的内容未被错误安装
6. `.install-meta.json` 被生成
7. metadata 中记录：
   - version
   - target
   - profile
   - installed_at
   - installed_files
8. reinstall 不应重复污染目录结构

### 验收标准
- PASS：目标目录正确、内容齐全、无越界安装、metadata 正确
- WARN：可选模块未安装但不影响 profile 核心闭环
- FAIL：路径错误、缺文件、误装文件、metadata 缺失或错误

---

## 三、发现验证

### 目的
证明安装结果不是“文件在磁盘上”，而是目标 harness 能看见。

### 验证对象
- Claude Code
- Codex

### 验证项
1. 安装后的 commands 处于目标 harness 可读路径
2. 安装后的 agents 处于目标 harness 可读路径
3. 安装后的 skills 处于目标 harness 可读路径
4. 安装后的 rules 处于目标 harness 可读路径
5. 至少一个 command、一个 agent、一个 skill 可以被目标 harness 读取或显式调用
6. 若某个 skill 仅属于特定 profile，需验证它不会泄漏到未声明该 skill 的 profile

### Claude Code 最低标准
- 能读取一个已安装 command
- 能读取一个已安装 skill
- 能读取一个已安装 agent

### Codex 最低标准
- 能读取一个已安装 command
- 能读取一个已安装 skill
- 能读取一个已安装 agent

### 验收标准
- PASS：Claude 与 Codex 都能发现并读取核心内容
- WARN：部分辅助内容不可见，但核心闭环可见
- FAIL：安装后内容存在，但 harness 无法发现或读取

---

## 四、行为验证

### 目的
证明 backend-ecc 安装后，开发行为真的发生变化。

### 验证原则
不验证全部功能，只验证 Go 后端主闭环。

### 金标场景

#### 场景 A：需求分析 / 计划
输入示例：
> 给这个 Go 服务加一个新的接口，先帮我分析影响范围并写计划

预期：
- 进入 plan 风格流程
- 先复述需求
- 识别风险和依赖
- 输出步骤化计划
- 不直接开始编码

通过标准：
- 输出中明确出现需求复述、风险、阶段计划、确认等待语义

---

#### 场景 B：Go review
输入示例：
> 请 review 当前改动的 Go 代码

预期：
- 走 Go 专项 review
- 关注 idiomatic Go、error handling、concurrency、security

通过标准：
- 不是泛化 code review
- 明确体现 Go-specific 维度

---

#### 场景 C：Go build 修复
输入示例：
> 当前 go build 失败了，帮我修

预期：
- 走 go-build 修复链路
- 先诊断，再逐项修复，再验证

通过标准：
- 输出体现 diagnostics → fix → rerun 的结构
- 倾向最小修复而不是大改

---

#### 场景 D：Go TDD
输入示例：
> 给这个函数补测试并按 TDD 修复 bug

预期：
- 走 go-test/TDD 流程
- 体现 RED → GREEN → REFACTOR
- 倾向 table-driven tests

通过标准：
- 先测试再实现
- 测试结构 idiomatic
- 有失败验证语义

---

#### 场景 E：通用代码审查
输入示例：
> 帮我检查当前 diff 是否还有问题

预期：
- 走 code-review
- 结合 common rules 和 Go context

通过标准：
- 覆盖 correctness / maintainability / security / testing
- 不是纯风格点评

---

#### 场景 F：提交前收口
输入示例：
> 改完了，帮我确认是否可以提 PR

预期：
- 走 verification/checkpoint/quality-gate 方向
- 输出剩余风险和未验证项

通过标准：
- 不会轻率直接“可以”
- 会检查 build / tests / diff / unintended changes / coverage

### 行为层总体验收标准
- PASS：6 个金标场景中至少 5 个达到预期行为
- WARN：能完成任务，但方法链偏弱或不稳定
- FAIL：行为不变、主链跑偏、或明显不符合设计目标

---

## 五、恢复验证

### 目的
证明生态损坏后可发现、可修复。

### 需要验证的故障

#### 故障 1：删掉一个 command
例如删除 `go-build.md`

预期：
- doctor 能发现缺失
- repair 能恢复

#### 故障 2：删掉一个 skill 目录
例如删除 `skills/golang-testing/`

预期：
- doctor 能发现目录缺失
- repair 能恢复整个 skill

#### 故障 3：adapter 落盘不完整
例如只有 commands，没有 agents

预期：
- doctor 能发现结构不完整
- repair 能补齐

#### 故障 4：metadata 丢失
例如删除 `.install-meta.json`

预期：
- doctor 能发现 metadata 缺失
- repair 能重建或要求重新安装

### 验收标准
- PASS：4 类故障均可发现，并至少能恢复 3 类
- WARN：能发现但不能自动修复某些问题
- FAIL：故障无法发现，或 repair 造成更严重漂移

---

## 六、v0.1 验收范围之外

以下内容不属于 v0.1 必过项：

- 多 harness 扩展（除 Claude/Codex 外）
- 完整 hooks runtime 治理
- auto-update
- session/loop/instinct/continuous-learning
- GUI / dashboard
- state store / sqlite
- marketplace 发布

---

## 七、v0.1 最终通过条件

backend-ecc v0.1 只有在以下条件全部满足时，才可视为“基本成型”：

1. 结构验证 PASS
2. 安装验证 PASS（Claude+minimal、Claude+backend-go、Codex+minimal、Codex+backend-go）
3. 发现验证 PASS
4. 行为验证至少 PASS 5/6 个金标场景
5. 恢复验证至少 PASS 3/4 类故障

若未达到以上条件，不应宣称为“可用生态”，只能称为“骨架原型”。
