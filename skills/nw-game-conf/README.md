# nw-game-conf assets

这个目录包含 `nw-game-conf` skill 的本地资产：

- `SKILL.md`：skill 说明与执行约束
- `nw_game_conf_import.py`：用于读取 NW workbook 并生成 `game_conf.json` 候选对象的脚本

## 资产边界

这些文件属于 `backend-ecc` 资产仓。
但脚本处理的目标文件通常位于当前工作区里的 `market-server` 仓库，例如：

- `conf_file/conf/game_conf.json`
- `internal/biz/common/gameCode_conf.go`

因此：
- 脚本路径是本目录内路径
- 输出与校验目标路径是消费端工作区路径

## 常见调用方式

在目标 `market-server` 工作区执行：

```bash
python3 ./skills/nw-game-conf/nw_game_conf_import.py \
  --excel "篮球&网球新增玩法.xlsx" \
  --map "篮球新增玩法:2" \
  --map "网球新增玩法:3" \
  --json-output
```

如需写回目标配置：

```bash
python3 ./skills/nw-game-conf/nw_game_conf_import.py \
  --excel "篮球&网球新增玩法.xlsx" \
  --map "篮球新增玩法:2" \
  --write
```

如果当前工作区的配置文件不在默认位置，可显式传入：

```bash
python3 ./skills/nw-game-conf/nw_game_conf_import.py \
  --excel "<workbook-path>" \
  --map "<sheet-name>:<sid>" \
  --config "<path-to-game_conf.json>" \
  --json-output
```
