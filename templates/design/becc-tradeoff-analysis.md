# becc-tradeoff-analysis

用于把非平凡 Go/backend 改动的方案比较压缩成最小可读结构。

## 模板

```md
## Design Problem
- 

## Option A
- Summary:
- Scope:
- Advantages:
- Costs:
- Failure modes:

## Option B
- Summary:
- Scope:
- Advantages:
- Costs:
- Failure modes:

## Comparison
- Simplicity vs flexibility:
- Local change size:
- Operational risk:
- Validation cost:

## Recommendation
- Preferred option:
- Why now:
```

## 使用要求

- 至少比较两个方案，除非明确说明只有一个现实可行方案
- 不要只写优点，不写代价
- 推荐结论必须和当前 scope 约束一致
