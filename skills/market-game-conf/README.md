# market-game-conf assets

这个目录包含 `market-game-conf` skill 的本地资产：

- `SKILL.md`：skill 说明与执行约束
- `rules.yaml`：归类规则的单一事实来源（sheet 映射、表头识别、归类规则、默认值、sid 特殊覆盖）
- `nw_game_conf_import.py`：读取 rules.yaml + NW workbook，生成 `game_conf.json` 候选对象的脚本

## 两种使用方式

### 1. 独立运行（不依赖 AI）

确保已安装 `pyyaml`：
```bash
pip install pyyaml
```

使用默认参数直接运行（默认 workbook：`NW 玩法相关表.xlsx`，默认输出：`./output/game_conf_result.json`）：
```bash
python3 ./skills/market-game-conf/nw_game_conf_import.py
```

显式指定同样的默认值运行：
```bash
python3 ./skills/market-game-conf/nw_game_conf_import.py \
  --excel "NW 玩法相关表.xlsx" \
  --output ./output/game_conf_result.json
```

手动覆盖 sheet 映射：
```bash
python3 ./skills/market-game-conf/nw_game_conf_import.py \
  --excel "篮球&网球新增玩法.xlsx" \
  --map "篮球新增玩法:2" \
  --map "网球新增玩法:3" \
  --output ./output/game_conf_result.json
```

### 2. AI 调用模式

Dry-run 输出到 stdout：
```bash
python3 ./skills/market-game-conf/nw_game_conf_import.py \
  --excel "篮球&网球新增玩法.xlsx" \
  --json-output
```

Write 模式（写回 game_conf.json）：
```bash
python3 ./skills/market-game-conf/nw_game_conf_import.py \
  --excel "篮球&网球新增玩法.xlsx" \
  --write
```

### 自定义 rules 和 config 路径

```bash
python3 ./skills/market-game-conf/nw_game_conf_import.py \
  --excel "<workbook-path>" \
  --rules "<path-to-rules.yaml>" \
  --config "<path-to-game_conf.json>" \
  --output ./output/result.json
```

## 维护规则

当需要新增球种、调整归类逻辑、修改表头别名，或为某个 `sid` 增加特殊默认值（例如 `sid=1` 的 `manual`）时，**只需编辑 `rules.yaml`**，无需改动 Python 脚本。

## 资产边界

这些文件属于 `backend-ecc` 资产仓。
但脚本处理的目标文件通常位于 `market-server` 仓库，例如：

- `conf_file/conf/game_conf.json`
- `internal/biz/common/gameCode_conf.go`
