# cps-add-sport Playbook

## 目的

这份 playbook 是 `cps-add-sport` skill 的详细配套文档。

当任务已经完成输入收集和确认，并且你需要以下内容时，使用它：
- 更完整的字段参考
- 批量命令模板
- 读文件后手工接线的锚点说明
- 更细的最小验收集

skill 负责工作流编排，这份 playbook 负责执行参考。

## 输入契约参考

每个目标球种建议至少包含以下字段：

| 字段 | 含义 |
|---|---|
| `nameZh` | 中文显示名 |
| `packageName` | 小写包名 |
| `typeName` | 导出类型名前缀 |
| `sid` | `sport-lib` 中已有球种 SID |
| `templateSport` | 模板球种包名/目录名 |
| `consumerTopic` | 赔率变更消费 topic |
| `bubbleField` | `BubbleHandler` 中对应字段 |
| `sportConst` | `gconsts` 中对应常量 |
| `reuseTemplateLogic` | 是否先按模板复用逻辑 |

每个球种执行前至少需要：
- `packageName`
- `typeName`
- `sid`
- `templateSport`
- `consumerTopic`

## 操作分类

### A 类：批量命令操作
适合一次性处理：
- 复制模板目录
- 批量替换 package 名
- 批量替换 import 路径
- 批量替换类型前缀
- 全局搜索模板残留

### B 类：读文件后手工接线操作
必须阅读目标文件结构后再修改：
- 注册 usecase
- 注册 kafka consumer
- 补配置结构体字段
- 补任务分配范围
- 补泡泡过滤逻辑

原则：
- 能批量处理的，优先批量处理
- 影响运行链路的接入点，必须手工复核
- “脚本替换成功”不等于“新增球种已完成”

## 影响范围审查清单

通常应检查：
- `internal/biz/<templateSport>`
- `internal/biz/ball/match_odds_diff.go`
- `internal/server/consumer.go`
- `internal/conf/config.go`
- 对应运行配置 YAML 文件
- `pkg/pod/task.go`
- `pkg/pod/manage.go`
- `internal/biz/sportSwitch.go`

重点检查：
- 模板包名前缀残留
- 模板中文文本残留
- 模板常量残留
- `Dota2` / `Lol` / `Cs2` 这类错误大小写残留
- import alias 是否正确
- 模板专属日志或注释残留

## 脚本模板

### 1. 复制业务骨架

```bash
cp -R internal/biz/badminton internal/biz/dota2
cp -R internal/biz/badminton internal/biz/lol
cp -R internal/biz/badminton internal/biz/cs2
```

执行后，至少确认目标目录存在。

### 2. 第一轮结构替换

```python
python - <<'PY'
from pathlib import Path

replacements = {
    "internal/biz/dota2": [
        ("package badminton", "package dota2"),
        ("/internal/biz/badminton", "/internal/biz/dota2"),
        ("Badminton", "DOTA2"),
        ("gconsts.Badminton", "gconsts.DOTA2"),
    ],
    "internal/biz/lol": [
        ("package badminton", "package lol"),
        ("/internal/biz/badminton", "/internal/biz/lol"),
        ("Badminton", "LOL"),
        ("gconsts.Badminton", "gconsts.LOL"),
    ],
    "internal/biz/cs2": [
        ("package badminton", "package cs2"),
        ("/internal/biz/badminton", "/internal/biz/cs2"),
        ("Badminton", "CS2"),
        ("gconsts.Badminton", "gconsts.CS2"),
    ],
}

for root, rules in replacements.items():
    for path in Path(root).rglob("*.go"):
        text = path.read_text(encoding="utf-8")
        for old, new in rules:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")
PY
```

### 3. 残留扫描

```bash
rg "badminton|Badminton|gconsts.Badminton" internal/biz/dota2 internal/biz/lol internal/biz/cs2
rg "Dota2|Lol|Cs2" internal/biz/dota2 internal/biz/lol internal/biz/cs2
```

机械替换后，至少补一轮残留扫描。
发现残留时，继续清理或明确列入风险，不要直接按“已完成”汇报。

## 手工接线锚点

### `ball` 层 usecase 分发
必改文件：
- `internal/biz/ball/match_odds_diff.go`

目标：
- 注册 `SID(gconsts.DOTA2)` / `SID(gconsts.LOL)` / `SID(gconsts.CS2)`
- 补齐 import
- 确认构造参数与模板球种一致或已明确调整

### `consumer` 层 kafka 消费
必改文件：
- `internal/server/consumer.go`

目标：
- 新增赔率变更消费 topic
- handler 指向正确 usecase
- 写法与现有主流球种保持一致

### `config` 配置字段
必改文件：
- `internal/conf/config.go`
- 对应运行配置 YAML 文件

目标：
- 补字段
- 补 YAML key
- 字段名与 YAML key 命名一致

### `pod` 任务分配链路
必改文件：
- `pkg/pod/task.go`
- `pkg/pod/manage.go`

目标：
- 新球种加入 `sidList`
- 下线清理和任务分配逻辑都能覆盖新球种

### `sportSwitch` 泡泡过滤逻辑
必改文件：
- `internal/biz/sportSwitch.go`

目标：
- 新球种在 `BubbleHandler` 中有明确分支
- 统计字段已补
- `Total` 汇总逻辑未遗漏

## 最小验证

在汇报 `completed` 前，至少验证：
- 新增目录已完成复制和替换
- 模板残留已清理
- `ball` 层已注册新增球种
- `consumer.go` 已注册新 topic
- `config.go` 与 YAML 已对齐
- `pod` 任务分配链路已纳入新增球种
- `BubbleHandler` 已补齐新球种过滤逻辑
- 本次触达范围内要求检查的接线面已记录结果
- 至少完成一次最小构建或测试验证；如果未执行，必须明确写出

如果已修改文件但未完成上述验证，结果应标记为 `partial`，并明确写出“已修改，未验证”。

## 结果模板

```text
CPS-ADD-SPORT RESULT
Status: completed | partial | blocked | failed
Sports: <count>
Template: <template sport(s)>

Completed:
- ...

Changed:
- ...

Verified:
- ...

Not run:
- ...

Blocked by:
- ...

Needs confirmation:
- ...

Risks:
- ...
```
