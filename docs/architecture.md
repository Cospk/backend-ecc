# backend-ecc 架构说明

## 一、整体定位

backend-ecc 是一个面向 **Claude Code** 与 **Codex** 的精简 Go 后端开发工作流生态。

当前版本聚焦于：

- Go 后端开发闭环
- 基础安装生命周期治理
- 面向 Claude / Codex 的最小插件声明层

当前目标是提供：

- 可安装
- 可裁剪
- 可巡检
- 可恢复
- 可卸载

的基础插件生态能力。

---

## 二、核心设计原则

backend-ecc 当前遵循四条核心原则：

1. **只聚焦 Go 后端开发闭环**
2. **内容层与安装治理层分离**
3. **插件优先（plugin-first），安装器兜底（installer-backed）**
4. **v0.1 阶段优先保证可安装、可验证、可维护，不追求大而全**

---

## 三、分层结构

backend-ecc 当前可以分为五层：

### 1. 内容层（Content Layer）
负责真正的开发工作流内容。

包括：
- `commands/`
- `agents/`
- `skills/`
- `rules/`
- `hooks/`

作用：
- command 作为用户入口
- agent 作为专职角色
- skill 提供模式与工作流知识
- rule 提供长期约束
- hook 提供轻量运行时资产

---

### 2. 元数据层（Metadata Layer）
负责声明安装面和能力集合。

包括：
- `VERSION`
- `manifest.json`
- `profiles/*.json`
- `adapters/*/install-map.json`

作用：
- 定义仓库版本
- 定义可安装内容
- 定义不同 profile 的能力边界
- 定义不同 target 的安装路径

---

### 3. 安装治理层（Installer Layer）
负责 backend-ecc 的生命周期管理。

包括：
- `install/install.sh`
- `install/doctor.sh`
- `install/repair.sh`
- `install/uninstall.sh`
- `install/lib.sh`

作用：
- 安装内容
- 巡检安装结果
- 恢复缺失内容与 metadata
- 卸载安装结果

---

### 4. 插件层（Plugin Layer）
负责对目标 harness 暴露插件声明面。

包括：
- `.claude-plugin/`
- `.codex-plugin/`

作用：
- 声明 backend-ecc 可作为目标平台插件内容源
- 定义默认 target / profile
- 将插件安装体验与底层安装器逻辑连接起来

当前阶段，插件层主要是**最小声明面**，不承担完整 marketplace 协议能力。

---

### 5. 文档层（Documentation Layer）
负责让用户和维护者理解整个生态。

包括：
- `README.md`
- `docs/verification.md`
- `docs/current-state.md`
- `docs/architecture.md`
- `docs/profiles.md`

作用：
- 解释安装方式
- 解释 profile 边界
- 解释当前阶段状态
- 解释验证标准与后续路线

---

## 四、plugin-first + installer-backed

backend-ecc 当前采用：

- **plugin-first**：优先提供插件声明面
- **installer-backed**：实际安装仍由 `install.sh` 执行

这意味着：

- 对外体验上，backend-ecc 更像一个插件
- 对内维护上，install 脚本仍然是统一底座

这样做的好处是：
- 可以保留插件安装语义
- 同时避免在 v0.1 过早绑定复杂 marketplace 协议
- 方便本地验证、调试、回滚与修复

---

## 五、当前范围

当前版本范围聚焦于：

- Go 后端开发闭环
- Claude / Codex 双目标
- 安装、巡检、恢复、卸载的最小生命周期治理
- 最小插件声明层

以下能力暂不纳入当前版本范围：

- 多 harness 扩展（除 Claude / Codex）
- 完整 control-plane
- GUI / dashboard
- sqlite / state store
- auto-update
- 大规模 catalog 扩展
- 完整 hooks runtime 治理

---

## 六、当前阶段结论

当前 backend-ecc 可被视为：

> 一个具备内容层、元数据层、插件层、安装治理层与基本验收规范的 v0.1 插件生态原型。

它已经完成了安装生命周期基础能力，但仍需进一步做真实运行时行为归因验证与真实插件导入链路验证。
