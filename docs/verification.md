# backend-ecc 验收标准（v0.1 skeleton reset）

## 目标

backend-ecc 当前阶段的目标不是证明“通用 becc workflow 已可用”，而是证明以下三件事：

1. 骨架仓本身自洽
2. install / doctor / repair / uninstall 仍然成立
3. 当前 shipping surface 真实、可解释、无低信任通用草稿污染

当前仅支持：

- Claude Code
- Codex

---

## 总体验收原则

当前阶段验收重点是：

1. 结构是否正确
2. 安装是否正确
3. shipping surface 是否与文档一致
4. 清退 becc 草稿后是否没有残留错误引用
5. 出现漂移或缺失时是否可发现并修复

因此，当前阶段验收拆分为五层：

1. 结构验证（Structure Validation）
2. 安装验证（Installation Validation）
3. 发现验证（Discoverability Validation）
4. 一致性验证（Truthfulness Validation）
5. 恢复验证（Repairability Validation）

---

## 一、结构验证

### 目的
证明 backend-ecc 源仓本身是自洽的。

### 验证对象
- `manifest.json`
- `profiles/*.json`
- `adapters/*/install-map.json`
- `skills/`
- `install/`
- `docs/`

### 验证项
1. `manifest.json` 可解析
2. 每个 profile 可解析
3. 每个 adapter install-map 可解析
4. 每个 profile 中引用的 skill 都存在
5. `VERSION` 存在且与 manifest 版本一致
6. 不再存在 profile/manifest 对已删除 becc commands / agents / skills / rules 的残留引用

### 验收标准
- PASS：以上全部成立
- FAIL：任一 profile/adapter/manifest 不可解析，或仍引用已清退 becc 资产

---

## 二、安装验证

### 目的
证明安装脚本能按 target + profile 正确落盘。

### 最小验证矩阵
必须至少覆盖：

- Claude Code + minimal
- Claude Code + backend-go

建议补充：

- Codex + minimal
- Codex + backend-go

### 验证项
1. 安装命令退出码为 0
2. 目标根目录存在
3. 安装路径与 adapter 定义一致
4. profile 声明的内容全部安装
5. profile 未声明的内容未被错误安装
6. `.install-meta.json` 被生成
7. metadata 中记录 version / target / profile / installed_at / installed_files

### 当前期望
- `minimal` 不安装通用 becc 内容资产
- `backend-go` 当前只安装保留中的 isolated domain skills

### 验收标准
- PASS：目标目录正确、内容齐全、无越界安装、metadata 正确
- FAIL：路径错误、缺文件、误装文件、metadata 缺失或错误

---

## 三、发现验证

### 目的
证明安装结果至少与当前 shipping surface 一致。

### 当前最低标准
- `minimal` 安装面为空或近空时，不应出现虚假 becc 内容
- `backend-go` 安装后应能看到当前保留的专项 skills
- 不应再出现已清退的 becc commands / agents / rules / skills

### 验收标准
- PASS：安装结果与 profile/manifest 描述一致
- FAIL：仍然存在被文档判定为已清退的 becc 资产，或保留专项 assets 丢失

---

## 四、一致性验证

### 目的
证明仓库叙事与实际 shipping surface 一致。

### 验证项
1. README 不再宣称已有一整套通用 becc workflow 资产
2. docs 不再把已清退 becc 资产描述成当前正式能力
3. profiles/manifest 与 docs 说法一致
4. 当前状态说明明确为 skeleton reset，而非通用能力完成态

### 验收标准
- PASS：文档、metadata、安装面一致
- FAIL：仍有明显自相矛盾叙事

---

## 五、恢复验证

### 目的
证明生态损坏后可发现、可修复。

### 最小验证对象
至少验证：

1. 删除一个当前保留 skill
2. 删除 `.install-meta.json`

### 预期
- doctor 能发现缺失
- repair 能恢复或给出明确处理路径

### 验收标准
- PASS：能发现主要缺失，并恢复关键安装面
- WARN：能发现但部分场景需要重新安装
- FAIL：缺失无法发现，或 repair 造成更严重漂移

---

## 六、当前阶段范围之外

以下内容不属于当前阶段必过项：

- 通用 becc capability 行为验证
- 通用 becc loop 验证
- 多 harness 扩展（除 Claude/Codex 外）
- 完整 hooks runtime 治理
- auto-update
- GUI / dashboard
- state store / sqlite
- marketplace 发布

---

## 七、当前最终通过条件

backend-ecc 当前阶段只有在以下条件成立时，才可视为“reset 完成”：

1. 结构验证 PASS
2. 安装验证 PASS（至少 Claude+minimal、Claude+backend-go）
3. 发现验证 PASS
4. 一致性验证 PASS
5. 恢复验证至少能覆盖关键安装面

若未达到以上条件，不应宣称当前 reset 已闭合。
