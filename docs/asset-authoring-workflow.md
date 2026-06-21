# backend-ecc 资产编写标准流程

## 一、目的

本文档是 backend-ecc 维护者与 AI 助手在新增、删除、重建或蒸馏仓库资产时必须遵守的标准流程。

当前仓库已经完成两步：

1. 清退低信任旧 becc workflow 草稿
2. 重建第一批最小 capability-first / loop-aware generic assets

因此当前流程的目标不是回到“先批量生成，再回头怀疑可信度”，而是：

- 先定义 capability
- 再定义 loop 位置
- 再落最小资产
- 最后才考虑让素材进入 shipping surface

---

## 二、适用范围

本文档适用于以下资产的新增、删除与修改：

- `commands/`
- `agents/`
- `skills/`
- `rules/`
- `templates/`
- `profiles/`
- 与安装、发现、默认 profile 相关的 metadata / docs
- 从 `raw/` 或其他来源蒸馏进来的候选素材

---

## 三、当前核心原则

### 1. 先 capability，后蒸馏

即使 `raw/` 中已有相似素材，也不要先看名字决定继承。

优先做的是：
- 明确当前要增强什么 capability
- 明确它属于哪条 loop
- 再判断现有素材能否提供有价值片段

### 2. 素材可以吸收，结构不能直接照搬

`raw/` 中已有内容可以作为：
- 约束来源
- 输出结构来源
- 失败模式来源
- 检查清单来源

但不应直接决定：
- backend-ecc 的目录结构
- capability 划分
- 命名方式
- shipping surface

### 3. 不是每个能力都要五件套

不要默认每个能力都必须同时生成：
- command
- agent
- skill
- rule
- template

只在必要时新增正确承载类型。

### 4. shipping surface 必须真实

如果一个资产还未审核、未验证、只是蒸馏候选稿，就不应进入：
- `manifest.json`
- `profiles/*.json`
- install / doctor 的正式验证面

---

## 四、强制执行顺序

### Step 1：先定义 capability
先回答：
- 这个资产增强什么 capability
- 它所在的 loop 是什么
- 它的输入 / 输出 / 退出条件是什么

### Step 2：判断是否需要从 raw 吸收素材
优先判断：
- 当前是否缺约束
- 当前是否缺模板
- 当前是否缺失败模式
- raw 中是否存在可蒸馏的高价值片段

### Step 3：再决定资产类型
只在必要时新增：
- command
- agent
- skill
- rule
- template

### Step 4：内容创建或蒸馏后，决定是否允许进入 shipping surface
只有在人工审核后，才允许进入：
- `manifest.json`
- `profiles/*.json`

### Step 5：检查 install / adapter / plugin 假设是否仍成立
重点检查：
- `install/install.sh`
- `install/doctor.sh`
- `install/repair.sh`
- `adapters/claude/install-map.json`
- `adapters/codex/install-map.json`
- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`

### Step 6：更新文档
至少检查是否需要更新：
- `README.md`
- `docs/blueprint-v1.md`
- `docs/content-boundaries.md`
- `docs/architecture.md`
- `docs/profiles.md`
- `docs/current-state.md`
- `docs/verification.md`

### Step 7：执行验证
至少做：
1. 结构验证
2. 安装验证
3. 发现验证（若进入 shipping surface）
4. 恢复验证（若影响安装面）
5. 行为验证（若宣称该 capability 已可用）

---

## 五、当前结论

backend-ecc 当前不再接受：
- 先批量生成一组 becc 通用资产，再事后判断质量
- 或直接把 raw 素材整体搬进来

更准确的流程应是：

> 先 capability，后 loop，再做最小资产落盘，最后才逐步蒸馏 raw 素材并决定是否纳管。
