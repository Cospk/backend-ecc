---
name: nw-game-conf
description: Ask for a manual sheetName-to-sid mapping, then organize mapped NW workbook sheets into one or more game_conf.json objects. Default to dry-run output; only write when explicitly requested.
origin: market-server
---

# nw-game-conf

当用户要你帮助整理 `conf_file/conf/game_conf.json` 时，使用这个 skill。

## 目标
这个 skill 的目标不是泛化分析 workbook，而是：
- 先向用户索取人工维护映射表 `sheetName -> sid`
- 根据映射表确定要处理哪些球种
- 对每个映射的 sheet 逐行读取 `NWID`
- 根据已确定规则，把 `NWID` 归类到目标 JSON 字段
- 最终生成一个或多个 `game_conf.json` 条目对象

映射表有多少条有效记录，就应该产出多少个对象。

## 前置输入 / 启动条件
在执行任何读取、分析或导入动作之前，必须先向用户索取一份**人工维护映射表**。

推荐格式：

```text
sheetName: 足球總表（11.11）, sid: 1
sheetName: Wild Rift-英雄联盟手游, sid: 116
```

在拿到这份映射表之前：
- 不读取 workbook
- 不推断目标球种
- 不运行 importer

这份映射表用于明确两件事：
- 需要整理哪些球种
- 每个球种对应从哪个 sheet 获取数据

## 依赖前提
这个 skill 的本地资产位于：
- `skills/nw-game-conf/nw_game_conf_import.py`
- `skills/nw-game-conf/README.md`

这个 skill 的目标工作区通常需要具备以下文件：
- `conf_file/conf/game_conf.json`
- `internal/biz/common/gameCode_conf.go`
- 对应的 NW workbook 文件

如果当前工作区不存在这些目标文件：
- 不要继续假设默认路径可用
- 必须停下并要求用户提供真实路径，或确认当前工作区是否就是目标 `market-server` 仓库

## 批量处理规则
- 映射表中有多少条有效记录，就整理多少个 sheet。
- 每条映射记录唯一确定：
  - 一个目标 `sid`
  - 一个来源 `sheetName`
- 默认按映射表逐个 sheet 处理，而不是扫描整个 workbook 后自行决定处理范围。

## 真实数据来源
- 拿到人工映射表后，再读取真实 workbook
- 数据来源以映射表指定的 sheet 为准
- 不要根据 `NWID` 猜测 `sid`
- 不要跳过映射表直接扫全表决定目标球种

## 目标输出结构
对每一条 `sheetName -> sid` 映射，都要整理出一个标准对象：

```json
{
  "sid": {{sid}},
  "pairMarketType": {
    "handicap": [],
    "overUnder": [],
    "oddEven": [],
    "yesNo": [],
    "homeAway": []
  },
  "advanceSettleGuardMap": [],
  "sortByOddsAsc": [],
  "sortBySrcOddsAsc": [],
  "sortByOddsAndSelectType": [],
  "sortByParamAsc": [],
  "selectionSortByParamAsc": [],
  "sortByParamAscAndSelection": [],
  "ah": [],
  "manual": [],
  "redBlackCode": [],
  "fullHandicap": 0
}
```

## 归类动作的统一语义
对任意一行：
- 先拿这行的 `NWID`
- 再看目标规则列
- 如果该列值命中某条规则
- 就把该行 `NWID` 放入对应字段数组

也就是说，这个 skill 的核心动作是：
- **按规则命中**
- **把命中行的 NWID 收集到目标字段集合中**

## 已确定规则

### 1) `pairMarketType.*`
来源列：`操盤調水規則（產品維護）`

| 列值 | 目标字段 |
|---:|---|
| `2` | `pairMarketType.handicap` |
| `3` | `pairMarketType.overUnder` |
| `4` | `pairMarketType.oddEven` |
| `5` | `pairMarketType.yesNo` |
| `6` | `pairMarketType.homeAway` |

动作：
- 命中时，将该行 `NWID` 放入对应数组

补充：
- 值 `1` 当前不归类
- 不要擅自放入任何字段

### 2) `advanceSettleGuardMap`
来源列：`提前結算（產品維護）`

| 列值 | 目标字段 |
|---:|---|
| `1` | `advanceSettleGuardMap` |

动作：
- 命中时，将该行 `NWID` 放入数组
- 值 `0` 不处理

### 3) `ah`
来源列：`玩法分類`

| 列值 | 目标字段 |
|---:|---|
| `2` | `ah` |

动作：
- 命中时，将该行 `NWID` 放入数组

### 4) `redBlackCode`
来源列：`redBlackCode`

命中条件：
- 单元格有数据

动作：
- 命中时，将该行 `NWID` 放入 `redBlackCode` 数组

## 当前默认值规则
以下字段当前没有稳定规则，先按默认值输出：

- `fullHandicap`
  - 固定输出 `0`
- `manual`
  - 固定输出 `[]`
- 排序相关字段
  - `sortByOddsAsc = []`
  - `sortBySrcOddsAsc = []`
  - `sortByOddsAndSelectType = []`
  - `sortByParamAsc = []`
  - `selectionSortByParamAsc = []`
  - `sortByParamAscAndSelection = []`

## 当前不确定但已知存在的信息
以下内容目前知道“存在”，但当前不参与自动归类：

- `操盤玩法分組`
  - `1 = 雙面盤`
  - `2 = MG`
  - `3 = 不可設置`
  - 目前未定义其目标字段用途

- `備註-排序規則`
  - 已知是排序规则描述
  - 当前规则未定，不自动生成排序字段

- `操盤調水規則（產品維護） = 1`
  - 已知含义为 `所有皆可調`
  - 当前未定义目标字段

## 这个 skill 会做什么
- 索取并校验用户提供的 `sheetName -> sid` 人工映射表。
- 根据映射表逐个处理目标 sheet。
- 逐行读取 `NWID` 并按**已确定规则**归类到目标 JSON 字段。
- 对未定义规则的字段使用默认值。
- 默认输出 dry-run 结果；只有在用户明确要求时，才执行写入。

## Inputs
- 人工维护映射表：`sheetName -> sid`
- Workbook path，例如：`NW 玩法相关表 (1).xlsx`
- 可选参数 `--map <sheetName:sid>`，可重复使用
- 可选参数 `--json-output`
- 可选参数 `--write`，但只能在用户明确表达意图时使用

## Command patterns
> 下面的命令示例只表示工具能力，不代表可以跳过“先向用户索取人工映射表”这一步。

### Default dry-run style output
```bash
python3 ./skills/nw-game-conf/nw_game_conf_import.py --excel "<workbook-path>" --map "<sheet-name-1>:<sid-1>" --json-output
```

### Multiple mapped sheets
```bash
python3 ./skills/nw-game-conf/nw_game_conf_import.py --excel "<workbook-path>" --map "<sheet-name-1>:<sid-1>" --map "<sheet-name-2>:<sid-2>" --json-output
```

### Write mode
Only run this if the user explicitly asks to update the JSON file.
```bash
python3 ./skills/nw-game-conf/nw_game_conf_import.py --excel "<workbook-path>" --map "<sheet-name>:<sid>" --write
```

## Expected output summary
向用户汇报时，应按每个 `sid / sheet` 输出以下部分：
- workbook / sheet / sid chosen
- parsed row counts and warnings
- generated fields:
  - `pairMarketType.*`
  - `advanceSettleGuardMap`
  - `ah`
  - `redBlackCode`
- defaulted fields:
  - `fullHandicap = 0`
  - `manual = []`
  - all current sort fields = `[]`
- JSON candidate object or write result

## Guardrails
- 必须先从用户获取人工维护映射表，再开始任何读取、分析或导入动作。
- 不要根据 `NWID` 猜测 `sid`；优先使用用户提供的 `sheetName -> sid` 映射。
- 除非用户明确要求，否则不要使用 `--write`。
- 如果缺少人工映射表，应停止执行并要求用户补充。
- 如果映射表中的 sheet 在 workbook 中不存在，应停止执行并报告。
- 如果一个 `sid` 对应多个 sheet，或者一个 sheet 匹配出多个目标而无法唯一确定，应停止执行并报告该歧义。
- 如果缺少必需表头，应停止执行并报告。
- 对没有明确规则的字段，不要猜测填充；使用当前默认值。
- 如果当前 `game_conf.json` 中同一个 `sid` 存在多条记录，write 模式必须拒绝写入。

## Related files
- `skills/nw-game-conf/nw_game_conf_import.py`
- `skills/nw-game-conf/README.md`
- `conf_file/conf/game_conf.json`
- `internal/biz/common/gameCode_conf.go`
