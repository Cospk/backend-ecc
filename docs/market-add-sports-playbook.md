# Add Sport Market Playbook

## 目的

这份 playbook 是 `market-add-sports` skill 的详细配套文档。

当任务已经完成输入收集和确认，并且你需要以下内容时，使用它：
- 更完整的字段参考
- 锚点级插入说明
- 可重复机械操作的脚本模板
- 更细的接线检查点
- 最小验证细则

skill 仍然负责工作流编排，这份 playbook 负责执行参考。

## 输入契约参考

每个目标球种可以包含以下字段：

| 字段 | 含义 |
|---|---|
| `nameZh` | 中文显示名 |
| `internalName` | 内部导出类型名 |
| `packageName` | 小写包名 |
| `sid` | 依赖库中的目标 SID |
| `sportConst` | 依赖库中的目标球种常量 |
| `templateSport` | 模板球种包名/目录名 |
| `ruleReuseFrom` | 状态/标签/基础规则复用来源球种 |
| `hasChampion` | 是否需要接 champion |
| `configSuffix` | 配置后缀 |
| `mergeMarketTopic` | 聚合盘口 topic |
| `sourceOffOnTopic` | 数据源上下线 topic |
| `oddsDiffTopic` | 盘口变更 topic |
| `mongoCollectionSuffix` | Mongo 后缀 |

每个球种执行前至少需要：
- `internalName`
- `sid`
- `sportConst`
- `templateSport`

## 执行边界

### 优先脚本化的操作
以下操作优先用脚本完成：
- 目录复制
- package/import/类型前缀替换
- 常量替换
- 模板中文文本替换
- 残留扫描

机械替换后，至少补一轮残留扫描。
残留扫描至少覆盖模板包名、模板中文名；必要时覆盖模板常量或类型名。
发现残留时，继续清理或明确列入风险，不要直接按“已完成”汇报。

### 必须人工判断的操作
以下内容默认不要自动化：
- champion 继承
- 行为白名单继承
- sourceOffOn 是否接入
- 调水 / 多盘口联动能力继承
- 赛果过滤
- 次要标签行为
- 未支持能力相关复制

## 影响范围审查清单

在做大改动前，至少检查：
- `internal/biz/<templateSport>`
- `internal/service/market.go`
- `internal/service/event.go`
- `internal/service/service.go`
- `cmd/market-server/wire.go`
- `cmd/market-consumer/wire.go`
- `cmd/market-consumer/main.go`
- `internal/server/server.go`
- `internal/server/matchrouter.go`
- `pkg/pod/task.go`
- `pkg/pod/manage.go`
- `internal/conf/config.go`
- `configs/*.yaml`
- `internal/pkg/mq/kafka.go`
- `internal/pkg/cpush/odds_diff_match.go`
- `internal/server/consumer.go`
- `internal/server/producer.go`
- `internal/biz/common/*`
- `internal/biz/game_info.go`
- `sql/.../mongo.js`

重点检查：
- 模板包前缀残留
- 模板中文文本残留
- 模板常量残留
- 裸 SID 片段残留
- 模板专属日志
- 未支持能力相关文本或逻辑
- process 层是否仍引用模板包 helper

## 脚本模板

### 1. 复制业务骨架

```python
python - <<'PY'
from pathlib import Path
import shutil

ROOT = Path(r"C:/Users/admin/GolandProjects/market-server")
SPORTS = [
    {"packageName": "hok", "templateSport": "badminton"},
]

for sport in SPORTS:
    src = ROOT / "internal" / "biz" / sport["templateSport"]
    dst = ROOT / "internal" / "biz" / sport["packageName"]
    if not src.exists():
        raise SystemExit(f"template not exists: {src}")
    if dst.exists():
        raise SystemExit(f"target exists: {dst}")
    shutil.copytree(src, dst)
    print(f"copied: {src} -> {dst}")
PY
```

### 2. 第一轮结构替换

```python
python - <<'PY'
from pathlib import Path

ROOT = Path(r"C:/Users/admin/GolandProjects/market-server")
SPORTS = [
    {
        "packageName": "hok",
        "internalName": "HoK",
        "nameZh": "王者榮耀",
        "templateSport": "badminton",
        "templateTypeName": "Badminton",
        "templateNameZh": "羽毛球",
        "templateConst": "gconsts.Badminton",
        "sportConst": "gconsts.HoK",
    },
]

for sport in SPORTS:
    target = ROOT / "internal" / "biz" / sport["packageName"]
    rules = [
        (f"package {sport['templateSport']}", f"package {sport['packageName']}"),
        (f'"market-server/internal/biz/{sport["templateSport"]}"', f'"market-server/internal/biz/{sport["packageName"]}"'),
        (sport["templateConst"], sport["sportConst"]),
        (sport["templateTypeName"], sport["internalName"]),
        (f"*{sport['templateSport']}.", f"*{sport['packageName']}."),
        (f"{sport['templateSport']}.", f"{sport['packageName']}."),
        (sport["templateNameZh"], sport["nameZh"]),
    ]

    for path in target.rglob("*.go"):
        text = path.read_text(encoding="utf-8")
        updated = text
        for old, new in rules:
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(f"updated: {path}")
PY
```

### 3. 残留扫描

```python
python - <<'PY'
from pathlib import Path

ROOT = Path(r"C:/Users/admin/GolandProjects/market-server")
SPORTS = [
    {
        "packageName": "hok",
        "nameZh": "王者榮耀",
        "templateSport": "badminton",
        "templateNameZh": "羽毛球",
    },
]

for sport in SPORTS:
    target = ROOT / "internal" / "biz" / sport["packageName"]
    keywords = [sport["templateSport"], sport["templateNameZh"]]
    print(f"=== {sport['packageName']} ===")

    found = False
    for path in sorted(target.rglob("*.go")):
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if any(keyword in line for keyword in keywords):
                found = True
                print(f"{path}:{line_no}: {line.strip()}")

    if not found:
        print("clean")
    print()
PY
```

### 4. 残留替换

```python
python - <<'PY'
from pathlib import Path

ROOT = Path(r"C:/Users/admin/GolandProjects/market-server")
SPORTS = [
    {
        "packageName": "hok",
        "nameZh": "王者榮耀",
        "templateSport": "badminton",
        "templateNameZh": "羽毛球",
    },
]

for sport in SPORTS:
    target = ROOT / "internal" / "biz" / sport["packageName"]

    for path in sorted(target.rglob("*.go")):
        text = path.read_text(encoding="utf-8")
        updated = text.replace(sport["templateSport"], sport["packageName"])
        updated = updated.replace(sport["templateNameZh"], sport["nameZh"])

        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(f"updated: {path}")
PY
```

## 接线锚点

### 系统入口接线
以下文件按需修改并验证：
- `internal/service/market.go`
- `internal/service/event.go`
- `internal/service/service.go`
- `cmd/market-server/wire.go`
- `cmd/market-consumer/wire.go`
- `cmd/market-consumer/main.go`
- `internal/server/server.go`
- `internal/server/matchrouter.go`
- 生成产物 `wire_gen.go`

预期动作：
- 暴露 usecase
- 暴露 router
- 补 provider 接线
- 补 wrapper 注册
- 在需要时重新生成 wire 结果
- 对本次触达范围，明确检查 provider / router 暴露

### 运行链路接线
以下文件按需检查和接线：
- `pkg/pod/task.go`
- `pkg/pod/manage.go`
- `internal/conf/config.go`
- `configs/market-consumer-config.yaml`
- `configs/market-consumer-config-tpl.yaml`
- `internal/pkg/mq/kafka.go`
- `internal/server/producer.go`
- `internal/pkg/cpush/odds_diff_match.go`
- `internal/server/consumer.go`

预期动作：
- 按 SID / sport const 补 task 映射
- 对齐 config 字段与 yaml key
- 补 odds diff 发送函数
- 补 producer 发布接线
- 补 cpush 分支
- 补 consumer 订阅与 handler
- 对本次范围内触达的 task / config / topic / producer / consumer 接线明确检查结果

## 最小验证

在宣称 `completed` 前，至少验证：
- 该清理的模板包名/类型名/常量残留已处理
- 该清理的模板中文文本残留已处理
- provider 链闭合
- router 链闭合
- task 映射纳入每个新增 SID
- config 与 yaml 命名对齐
- producer / consumer / topic 接线对齐
- 需要刷新的生成文件已刷新

如果已修改文件但未完成上述验证，结果应标记为 `partial`，并明确写出“已修改，未验证”。

## 结果模板

```text
MARKET-ADD-SPORTS RESULT
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

Not included:
- ...

Risks:
- ...
```
