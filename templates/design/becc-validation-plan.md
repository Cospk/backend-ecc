# becc-validation-plan

用于把设计选择直接绑定到实现前后的最小验证路径。

## 模板

```md
## Validation Target
- What must be proven:

## Minimal Checks
- Build / compile:
- Relevant tests:
- Runtime / config checks:

## Risk-Focused Checks
- Edge case:
- Regression surface:
- Data / config risk:

## Not Yet Covered
- 
- 

## Completion Signal
- What result allows implementation to be considered verified:
```

## 使用要求

- 验证计划必须跟当前推荐方案绑定
- 不要只写泛化的“跑测试”
- 要明确哪些风险尚未覆盖
