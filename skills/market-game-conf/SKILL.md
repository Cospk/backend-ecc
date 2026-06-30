---
name: market-game-conf
description: Read rules.yaml for sheetName→sid mapping and classification rules, then organize NW workbook sheets into game_conf.json objects. Can run standalone without AI via Python script + YAML.
origin: market-server
---

# market-game-conf

当用户要你帮助整理 `conf_file/conf/game_conf.json` 时，使用这个 skill。

## 目标
这个 skill 的目标不是泛化分析 workbook，而是：
- 根据 `rules.yaml` 中的 sheet 映射确定要处理哪些球种
- 对每个映射的 sheet 逐行读取 `NWID`
- 根据 `rules.yaml` 中的归类规则，把 `NWID` 归类到目标 JSON 字段
- 最终生成一个或多个 `game_conf.json` 条目对象

映射表有多少条有效记录，就应该产出多少个对象。

## 规则的单一事实来源

所有归类规则、表头识别、sheet 映射均定义在：
- `skills/market-game-conf/rules.yaml`

修改规则时**只需编辑 `rules.yaml`**，无需改动 Python 脚本。

`rules.yaml` 包含以下部分：
- `sheet_mapping`：sheetName → sid 映射
- `headers`：表头列名的多种写法
- `required_headers`：必需列
- `classify_rules`：归类规则（来源列 + 匹配值 → 目标字段）
- `full_handicap_names`：fullHandicap 候选名称
- `defaults`：默认值
- `sid_overrides`：按 sid 覆盖默认值（例如 `sid=1` 的 `manual`）
- `output_template`：输出结构模板

## 前置输入 / 启动条件

**方式一：使用 rules.yaml 默认映射（推荐）**

`rules.yaml` 中的 `sheet_mapping` 已预定义了常用的 sheetName → sid 映射。脚本会自动匹配 workbook 中存在的 sheet，无需手动指定。

**方式二：命令行覆盖映射**

如果 workbook 中的 sheet 名称与 `rules.yaml` 不一致，可通过 `--map` 参数覆盖：

```text
--map "足球總表（11.11）:1" --map "Wild Rift-英雄联盟手游:116"
```

**方式三：向用户索取映射（AI 模式）**

当 `rules.yaml` 无法匹配且未提供 `--map` 时，向用户索取映射表。

## 依赖前提
这个 skill 的本地资产位于：
- `skills/market-game-conf/nw_game_conf_import.py`
- `skills/market-game-conf/rules.yaml`
- `skills/market-game-conf/README.md`

这个 skill 的目标工作区通常需要具备以下文件：
- `conf_file/conf/game_conf.json`（write 模式需要；dry-run 模式可选）
- 对应的 NW workbook 文件

Python 依赖：`pyyaml`（`pip install pyyaml`）

## 批量处理规则
- 映射中有多少条匹配记录，就整理多少个 sheet。
- 每条映射记录唯一确定：
  - 一个目标 `sid`
  - 一个来源 `sheetName`

## 目标输出结构
对每一条 `sheetName → sid` 映射，都要整理出一个标准对象（结构定义在 `rules.yaml` 的 `output_template`）：

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
- 再看 `rules.yaml` 中 `classify_rules` 定义的来源列和匹配值
- 如果命中，就把该行 `NWID` 放入对应目标字段数组

## 默认值与 sid 特殊规则
- 默认情况下：`manual = []`
- 特殊规则：当 `sid = 1` 时，`manual = [1103, 1104, 1105, 1106]`
- 这类按 sid 的特殊处理统一配置在 `rules.yaml` 的 `sid_overrides` 中

## Command patterns

### 独立运行（不依赖 AI）

使用 rules.yaml 默认映射，输出到 JSON 文件：
```bash
python3 ./skills/market-game-conf/nw_game_conf_import.py \
  --excel "<workbook-path>" \
  --output ./output/game_conf_result.json
```

手动指定映射，输出到 JSON 文件：
```bash
python3 ./skills/market-game-conf/nw_game_conf_import.py \
  --excel "<workbook-path>" \
  --map "<sheet-name-1>:<sid-1>" \
  --map "<sheet-name-2>:<sid-2>" \
  --output ./output/game_conf_result.json
```

### AI 调用模式

Dry-run 输出到 stdout：
```bash
python3 ./skills/market-game-conf/nw_game_conf_import.py \
  --excel "<workbook-path>" \
  --json-output
```

### Write 模式
Only run this if the user explicitly asks to update the JSON file.
```bash
python3 ./skills/market-game-conf/nw_game_conf_import.py \
  --excel "<workbook-path>" \
  --write
```

### 完整参数列表
| 参数 | 说明 |
|---:|---|
| `--excel` | NW workbook 路径（默认：`NW 玩法相关表.xlsx`） |
| `--rules` | rules.yaml 路径（默认：脚本同目录下） |
| `--map` | 覆盖 sheet 映射，可重复（格式：`sheetName:sid`） |
| `--config` | game_conf.json 路径（默认：`conf_file/conf/game_conf.json`） |
| `--output` | 输出 JSON 文件路径（默认：`./output/game_conf_result.json`，所有结果合并） |
| `--json-output` | 输出详细 JSON 到 stdout |
| `--write` | 写回 game_conf.json |

## Guardrails
- 如果 `rules.yaml` 中定义的 sheet 在 workbook 中不存在，会自动跳过（不报错），只处理匹配到的。
- 如果没有任何 sheet 匹配，脚本报错退出。
- 如果缺少 `rules.yaml` 中定义的必需表头，脚本报错退出。
- 对没有明确规则的字段，使用 `rules.yaml` 中的默认值。
- 如果当前 `game_conf.json` 中同一个 `sid` 存在多条记录，write 模式拒绝写入。
- 除非用户明确要求，否则不要使用 `--write`。

## Related files
- `skills/market-game-conf/rules.yaml`
- `skills/market-game-conf/nw_game_conf_import.py`
- `skills/market-game-conf/README.md`
- `conf_file/conf/game_conf.json`
- `internal/biz/common/gameCode_conf.go`
