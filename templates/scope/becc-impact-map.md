# becc-impact-map

用于把 scope 结果压缩为可执行的影响面与验证面。

## 模板

```md
## Problem Summary
- 

## Affected Systems
- Primary:
- Directly affected:
- Adjacent:
- Likely not affected:

## Code Path Hypothesis
- Entry point:
- Likely execution path:
- Key branches:
- Data / config / external touchpoints:

## Risk Surface
- Regression risk:
- Config / data risk:
- Rollout risk:
- Validation risk:

## Verification Surface
- Must verify:
- Good to verify:
- Not yet verified:

## Confidence / Unknowns
- Confidence:
- Unknowns:
```

## 使用要求

- 影响面要分主次，不要给无边界大清单
- 要明确哪些区域大概率不受影响
- 必须显式写出验证面，而不只是代码路径
