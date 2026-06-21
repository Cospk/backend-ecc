# becc-code-review

## 目标

这条规则用于约束 backend-ecc 中的通用 review 行为：

> review 不是复述 diff，也不是泛化点评；必须围绕风险、验证与交付判断输出结论。

它主要服务于：
- Impact & Validation Loop 的收口阶段

---

## 强制要求

当任务进入 review 阶段时，助手必须：

1. 先明确 review scope
   - 当前审查哪些文件或哪类改动
   - 当前变更目标是什么

2. 先回看验证信息
   - 已执行哪些验证
   - 尚未执行哪些验证
   - 验证不足本身也可能是问题

3. 发现问题时，至少说明：
   - severity
   - location
   - issue
   - why it matters

4. 最终必须给出明确 verdict：
   - `approve`
   - `warning`
   - `block`

---

## 禁止项

助手不得：
- 在没有 review scope 时直接给结论
- 在没有验证上下文时轻率给 approve
- 把泛化“可以优化”写成阻塞项
- 只做风格点评，不做风险判断

---

## Severity 约束

- `critical`：安全、数据损坏、严重并发/正确性问题，应阻断
- `high`：高概率 bug、验证明显不足、关键错误处理缺失，应强烈建议修复
- `medium`：可维护性或模式问题，建议修复
- `note`：轻量建议，不阻断

---

## 最低输出要求

结果至少应包含：
- Review Scope
- Findings
- Verification Gaps
- Review Verdict

如果当前没有发现问题，也必须说明：
- 审查范围是什么
- 依据了哪些验证结果
- 为什么当前能给 approve / warning

---

## 适用说明

这条规则本身不提供语言专项细节；
Go 相关专项 review 由：
- `becc-go-review`
- 以及相关 Go testing / verification 资产

共同完成。
