# becc-verification-gate

## 目标

这条规则用于约束 backend-ecc 中所有通用 Go 后端能力：

> 未验证，不宣称完成。

它服务于所有 loop，尤其是：
- Impact & Validation Loop
- Root-Cause Loop

---

## 强制要求

当一次任务涉及：
- 代码修改
- 配置修改
- 依赖行为变化
- bug 修复
- 测试修复
- 调试结论

助手必须明确区分以下几类信息：

1. **Changed**
   - 哪些文件或行为实际被改动了

2. **Verified**
   - 哪些验证已经真正执行
   - 验证结果是什么

3. **Not Run**
   - 哪些本应做但本次未做

4. **Risks / Unknowns**
   - 当前仍未消除的风险或未知点

---

## 禁止项

助手不得：
- 在未执行关键验证时使用“已完成”“已验证通过”等完成态表述
- 把“我认为应该可以”写成“已经证明可以”
- 把 symptom 消失直接当成 root cause 已验证
- 隐去未执行验证项

---

## 最低完成态标准

只有在以下条件成立时，才可宣称任务完成：

1. 改动内容已明确
2. 至少一个与目标直接相关的验证已执行
3. 若任务属于 build / test / runtime 故障修复，验证应优先包含：
   - 触发过问题的构建、测试或检查重新执行
   - 修复后结果是否翻转
4. 结果中已明确列出未执行项（若存在）
5. 若验证不充分，状态必须降级为：
   - `partial`
   - `blocked`
   - `candidate`
   - `not ready`

---

## 推荐输出习惯

在收尾时，优先使用类似结构：

```text
Changed:
- ...

Verified:
- ...

Not run:
- ...

Risks:
- ...

Overall:
- ready | not ready | partial | blocked | candidate
```

如果没有执行必要验证，不要跳过 `Not run`。

---

## 适用说明

这条规则不负责定义“怎么 debug”或“怎么 scope”，
它只负责守住一个底线：

> 没有验证证据，就不要给完成态结论。
