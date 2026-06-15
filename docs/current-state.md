# backend-ecc 当前状态（v0.1）

## 一、当前定位

backend-ecc 当前定位为：

- 面向 **Claude Code** 与 **Codex** 的精简 Go 后端开发工作流生态
- 采用 **plugin-first, installer-backed** 的设计思路
- 目标不是复刻完整 ECC，而是围绕 Go 后端开发闭环提供最小但完整的工作流能力

覆盖范围：

1. 需求分析
2. 方案设计
3. Go 编码实现
4. Go 测试与验证
5. Bug 定位与修复
6. 提交前收口

---

## 二、当前已完成的层次

### 1. 内容层
已具备：
- `commands/`
- `agents/`
- `skills/`
- `rules/`
- `hooks/`

### 2. 元数据层
已具备：
- `VERSION`
- `manifest.json`
- `profiles/minimal.json`
- `profiles/backend-go.json`
- `profiles/author.json`
- `adapters/claude/install-map.json`
- `adapters/codex/install-map.json`

### 3. 插件层
已具备：
- `.claude-plugin/plugin.json`
- `.claude-plugin/README.md`
- `.codex-plugin/plugin.json`
- `.codex-plugin/README.md`

### 4. 安装治理层
已具备：
- `install/install.sh`
- `install/doctor.sh`
- `install/repair.sh`
- `install/uninstall.sh`
- `install/lib.sh`

### 5. 文档层
已具备：
- `README.md`
- `docs/verification.md`
- `docs/current-state.md`

---

## 三、已通过的验证

### 1. 结构验证
结果：**PASS**

说明：
- `manifest.json`、`profiles/`、`adapters/` 与实际文件一致
- commands / agents / skills / rules / hooks 引用完整
- `VERSION` 与 `manifest.json` 版本一致

### 2. 安装验证矩阵
结果：**PASS**

已通过：
- Claude Code + minimal
- Claude Code + backend-go
- Codex + minimal
- Codex + backend-go

说明：
- `install.sh` 能按 target + profile 正确落盘
- `.install-meta.json` 能正确生成
- `minimal` 与 `backend-go` 的安装边界符合预期

### 3. 路径层发现验证
结果：**PASS**

说明：
- Claude 与 Codex 两侧安装结果中，至少一个 command、一个 skill、一个 agent 均处于正确路径并可读取

### 4. doctor 验证
结果：**PASS**（至少已验证 Claude + backend-go）

说明：
- `doctor.sh` 能正确识别安装根目录、metadata 与 profile 声明内容

### 5. repair 验证
结果：**PASS**

已验证：
- 删除 `commands/go-build.md` 后可恢复
- 删除 `.install-meta.json` 后可重建

说明：
- `repair.sh` 当前已具备最小恢复能力：缺失文件恢复 + metadata 重建

---

## 四、当前未完成项

### 1. 真实运行时行为归因验证
尚未完成：
- backend-ecc 在真实 Claude Code / Codex 会话中，是否独立改变了行为
- command / skill / agent 是否被真实运行时消费，而不只是被安装和定位

说明：
- 当前全局与项目级规则会污染 `plan` 类场景的归因
- 后续需要在尽量干净的测试环境中做真实 smoke test / 行为验收

### 2. 完整 hooks runtime
当前状态：**未做**

说明：
- hooks 目前主要作为内容资产存在
- 尚未形成完整的运行时治理系统
- 这符合 v0.1 的边界约束

### 3. marketplace / GitHub 插件导入验证
当前状态：**未做**

说明：
- 当前已具备插件声明层
- 但尚未做真实 GitHub / marketplace 导入链路验证

### 4. 复杂恢复能力
当前状态：**未做**

说明：
- 当前 repair 只恢复缺失文件，不覆盖被修改文件
- 不做冲突合并，不做漂移智能修复

---

## 五、当前阶段结论

backend-ecc 当前可以被定义为：

> **具备内容层、元数据层、插件层、安装层与基础恢复能力的 v0.1 插件生态原型**

它已经不是单纯的目录包，也不是只有 install 的半成品。
它具备：
- 可安装
- 可巡检
- 可恢复
- 可卸载
- 可通过 profile 和 target 进行裁剪

但它还**不能**被定义为“最终可用插件产品”，因为还缺：
- 真实运行时行为验收
- 插件导入链路验收
- 更完整的 hooks/repair 治理

---

## 六、建议的下一阶段路线

### Phase 1：真实运行时行为验证
优先目标：
- 在干净环境下验证 backend-ecc 的 plugin-first + installer-backed 是否真的会影响 Claude/Codex 行为
- 重点验证少量高价值场景，而不是大而全场景

### Phase 2：插件导入链路验证
优先目标：
- GitHub 仓库 + 插件入口导入
- 确认 plugin.json 是否足以支撑真实安装体验

### Phase 3：文档补强
建议补：
- `docs/architecture.md`
- `docs/profiles.md`
- README 中的 quickstart / plugin layer / non-goals 说明

### Phase 4：install 层增强（可选）
可选后续：
- 更细粒度 doctor
- 更智能 repair
- 可选 hooks runtime

---

## 七、不建议当前阶段做的事

以下内容当前不建议推进：

- 扩更多语言生态
- 增加大量 skill/catalog
- 做 GUI / dashboard
- 引入 sqlite / state store
- 做 auto-update
- 做完整 multi-harness 抽象
- 引入复杂 control-plane

原因：
- 这些会快速把 backend-ecc 重新推向 ECC 全家桶复杂度
- 当前最值钱的工作不是扩张，而是收敛和验证
