# becc-root-cause-analysis

用于把 debug 过程强制拆成 symptom、evidence、hypotheses、checks 与 current status。

## 模板

```md
## Symptom
- 

## Evidence
- 
- 

## Hypotheses
1. 
2. 
3. 

## Checks / Falsification
- Hypothesis 1:
- Hypothesis 2:
- Hypothesis 3:

## Root Cause Status
- confirmed | candidate | blocked

## Next Action
- gather more evidence | narrow hypotheses | implement fix | stop

## Verified
- 

## Not Run
- 
```

## 使用要求

- 不要把 symptom 当 root cause
- 每个 hypothesis 都应有依据
- 若未执行关键检查，不要跳过 `Not Run`
- 只有证据支持时才能把状态写成 `confirmed`
