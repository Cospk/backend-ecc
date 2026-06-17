# backend-ecc 当前状态（v0.1）

## 一、当前定位

backend-ecc 当前定位为：

- 面向 **Claude Code** 与 **Codex** 的精简 Go 后端开发工作流生态
- 采用 **plugin-first, installer-backed** 的设计思路
- 是围绕 Go 后端开发闭环提供最小但完整的工作流能力

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
当前保留：
- `commands/add-sport-market.md`
- `skills/add-sport-market/SKILL.md`

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
- `docs/architecture.md`
- `docs/profiles.md`
- `docs/add-sport-market-playbook.md`
- `docs/asset-authoring-workflow.md`

---

## 三、当前已完成的收缩

已完成：
- 移除当前无实际价值的通用 workflow 内容资产
- 当前默认 profile 与最小 profile 的内容层已收缩到 add-sport-market
- 保留 profile / adapter / install / plugin 框架不变


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

## 四、当前仍需持续验证的点

### 1. 真实运行时行为归因验证
尚未完成：
- backend-ecc 在真实 Claude Code / Codex 会话中，是否独立改变了行为
- 当前保留的 command / skill 是否被真实运行时消费，而不只是被安装和定位

### 2. marketplace / GitHub 插件导入验证
当前状态：**未做**

说明：
- 当前已具备插件声明层
- 但尚未做真实 GitHub / marketplace 导入链路验证

### 3. 后续内容层扩展
当前状态：**待后续验证**

说明：
- 当前内容层已收敛到最小可用集
- 后续若要补回其他 workflow，应按标准流程逐步增加

---

## 五、当前阶段结论

backend-ecc 当前可以被定义为：

> **一个面向精简 Go 后端开发工作流生态、具备内容层、元数据层、插件层、安装层与基础恢复能力的 v0.1 插件生态原型**

它具备：
- 可安装
- 可巡检
- 可恢复
- 可卸载
- 可通过 profile 和 target 进行裁剪
