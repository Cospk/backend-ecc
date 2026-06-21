# becc-pr-summary

用于把一次变更收敛成面向 PR 或 review 的最小摘要。

## 模板

```md
## Summary
- What changed:
- Why:

## Scope
- Files / modules touched:
- Explicitly not changed:

## Verification
- Build / test / checks run:
- Results:

## Risks
- Remaining risks:
- Not run:

## Review Focus
- Key points for reviewer:
- Highest-risk files or paths:

## Open Questions
- 
```

## 使用要求

- 不要把未执行验证写成已验证
- 要明确 scope，而不是只写“大概改了什么”
- reviewer 应该能从这份摘要快速知道看哪里、担心什么
- 要明确哪些问题仍未解决，而不是只写已完成项
