#!/usr/bin/env python3
import argparse
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any

SPORT_PATTERNS = [
    (1, [r"足球.*總表", r"足球.*总表"]),
    (2, [r"籃球.*總表", r"篮球.*总表"]),
    (3, [r"網球.*總表", r"网球.*总表"]),
    (4, [r"棒球.*總表", r"棒球.*总表"]),
    (9, [r"羽毛球.*總表", r"羽毛球.*总表"]),
    (18, [r"板球.*總表", r"板球.*总表"]),
    (39, [r"乒乓球.*總表", r"乒乓球.*总表"]),
    (101, [r"電競足球.*總表", r"电竞足球.*总表"]),
    (102, [r"電競籃球.*總表", r"电竞篮球.*总表"]),
    (103, [r"LOL.*總表", r"LOL.*总表"]),
    (104, [r"Dota2.*總表", r"Dota2.*总表"]),
    (105, [r"CS2.*總表", r"CS2.*总表"]),
    (106, [r"King of Glory-王者榮耀", r"王者榮耀.*總表", r"王者荣耀.*总表"]),
    (107, [r"Valorant-无畏契约", r"特戰英豪.*總表", r"无畏契约.*总表"]),
    (108, [r"eIce Hockey-电竞冰球", r"電競冰球.*總表", r"电竞冰球.*总表"]),
    (109, [r"Rainbow Six-彩虹六号", r"虹彩6號.*總表", r"彩虹六号.*总表"]),
    (110, [r"Overwatch-守望先锋", r"鬥陣特攻.*總表", r"守望先锋.*总表"]),
    (111, [r"Call of Duty-使命召唤", r"決勝時刻.*總表", r"使命召唤.*总表"]),
    (112, [r"StarCraft-星际争霸", r"星海爭霸.*總表", r"星际争霸.*总表"]),
    (113, [r"Hearthstone-炉石传说", r"爐石戰記.*總表", r"炉石传说.*总表"]),
    (114, [r"Rocket League-火箭联盟", r"火箭聯盟.*總表", r"火箭联盟.*总表"]),
    (115, [r"ESport Arena of Valor-传说对决", r"傳說對決.*總表", r"传说对决.*总表"]),
    (116, [r"Wild Rift-英雄联盟手游", r"英雄聯盟手游.*總表", r"英雄联盟手游.*总表"]),
]
EXCLUDED = ["mapping", "模板", "目录", "工作表", "盤點", "盘点", "副本", "玩法總表", "玩法总表", "投註項", "投注项", "新收單規則", "新收单规则"]
NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


class WorkbookReader:
    def __init__(self, path: Path):
        self.path = path
        self.zip = zipfile.ZipFile(path)
        self.shared_strings = self._load_shared_strings()
        self.sheet_targets = self._load_sheet_targets()
        self.sheetnames = list(self.sheet_targets.keys())

    def _load_shared_strings(self) -> list[str]:
        if "xl/sharedStrings.xml" not in self.zip.namelist():
            return []
        root = ET.fromstring(self.zip.read("xl/sharedStrings.xml"))
        values = []
        for si in root.findall("a:si", NS):
            values.append("".join(t.text or "" for t in si.iterfind(".//a:t", NS)))
        return values

    def _load_sheet_targets(self) -> dict[str, str]:
        workbook = ET.fromstring(self.zip.read("xl/workbook.xml"))
        rels = ET.fromstring(self.zip.read("xl/_rels/workbook.xml.rels"))
        rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
        targets = {}
        for sheet in workbook.find("a:sheets", NS):
            name = sheet.attrib["name"]
            rid = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
            target = rel_map[rid]
            if not target.startswith("xl/"):
                target = "xl/" + target
            targets[name] = target
        return targets

    def _cell_value(self, cell: ET.Element) -> str:
        cell_type = cell.attrib.get("t")
        value = cell.find("a:v", NS)
        if cell_type == "s" and value is not None:
            idx = int(value.text)
            return self.shared_strings[idx] if idx < len(self.shared_strings) else ""
        if cell_type == "inlineStr":
            return "".join(t.text or "" for t in cell.iterfind(".//a:t", NS))
        return "" if value is None else (value.text or "")

    def get_rows(self, sheet_name: str) -> list[list[str]]:
        root = ET.fromstring(self.zip.read(self.sheet_targets[sheet_name]))
        sheet_data = root.find("a:sheetData", NS)
        rows: list[list[str]] = []
        for row in sheet_data.findall("a:row", NS):
            values = [self._cell_value(cell) for cell in row.findall("a:c", NS)]
            while values and values[-1] == "":
                values.pop()
            rows.append(values)
        return rows


def normalize_header(value: Any) -> str:
    s = str(value or "").replace("\n", "").replace(" ", "")
    s = s.replace("（", "(").replace("）", ")")
    return s.strip().lower()


def parse_int(value: Any) -> int | None:
    if value is None:
        return None
    s = str(value).strip().replace("（1231新增）", "")
    if not s:
        return None
    try:
        return int(float(s))
    except ValueError:
        return None


def detect_sheets(workbook: WorkbookReader) -> list[tuple[str, int]]:
    results = []
    for name in workbook.sheetnames:
        lower = name.lower()
        if any(token.lower() in lower for token in EXCLUDED):
            continue
        for sid, patterns in SPORT_PATTERNS:
            if any(re.search(pattern, name, re.I) for pattern in patterns):
                results.append((name, sid))
                break
    return results


def resolve_sheet(candidates: list[tuple[str, int]], requested_sheet: str, requested_sid: int) -> tuple[str, int]:
    if requested_sheet:
        for name, sid in candidates:
            if name == requested_sheet:
                return name, sid
        raise SystemExit(f"requested sheet not found in detected sport sheets: {requested_sheet}")
    if requested_sid:
        matches = [(name, sid) for name, sid in candidates if sid == requested_sid]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise SystemExit(f"multiple sheets matched sid {requested_sid}: {[name for name, _ in matches]}")
        raise SystemExit(f"no detected sport sheet matched sid {requested_sid}")
    if len(candidates) == 1:
        return candidates[0]
    raise SystemExit(f"multiple sport sheets detected; use --sheet or --sid: {[name for name, _ in candidates]}")


def parse_mapping(value: str) -> tuple[str, int]:
    sheet_name, separator, sid_text = value.rpartition(":")
    if not separator or not sheet_name.strip() or not sid_text.strip():
        raise SystemExit(f"invalid --map value: {value}; expected <sheetName:sid>")
    sid = parse_int(sid_text)
    if sid is None:
        raise SystemExit(f"invalid sid in --map value: {value}")
    return sheet_name.strip(), sid


def build_header_index(header_row: list[Any]) -> dict[str, int]:
    index = {
        "nwid": -1,
        "name": -1,
        "jp": -1,
        "pair_group": -1,
        "adjust_rule": -1,
        "advance": -1,
        "market_class": -1,
        "sort_note": -1,
        "red_black_code": -1,
    }
    for i, cell in enumerate(header_row):
        h = normalize_header(cell)
        if "nwid" in h:
            index["nwid"] = i
        elif any(token in h for token in ["操盤中文名稱", "操盘中文名称", "操盘中文名称(简体)"]) and index["name"] == -1:
            index["name"] = i
        elif any(token in h for token in ["jp盤口代號", "jp盘口代号", "jp盘口代號"]):
            index["jp"] = i
        elif any(token in h for token in ["操盤玩法分組", "操盘玩法分组"]):
            index["pair_group"] = i
        elif any(token in h for token in ["操盤調水規則(產品維護)", "操盘调水规则(产品维护)", "操盤調水規則", "操盘调水规则"]):
            index["adjust_rule"] = i
        elif any(token in h for token in ["提前結算(產品維護)", "提前结算(产品维护)", "提前結算", "提前结算"]) and index["advance"] == -1:
            index["advance"] = i
        elif any(token in h for token in ["玩法分類", "玩法分类"]):
            index["market_class"] = i
        elif any(token in h for token in ["備註-排序規則", "备注-排序规则", "排序規則", "排序规则"]):
            index["sort_note"] = i
        elif any(token in h for token in ["紅黑馬", "红黑马", "紅黑碼", "红黑码"]) or "redblackcode" in h:
            index["red_black_code"] = i
    if index["nwid"] < 0 or index["pair_group"] < 0 or index["adjust_rule"] < 0:
        raise SystemExit(f"required headers missing: {index}")
    return index


def safe_cell(row: list[Any], idx: int) -> Any:
    if idx < 0 or idx >= len(row):
        return None
    return row[idx]


def parse_rows(rows: list[list[str]], sheet_name: str) -> tuple[list[dict[str, Any]], dict[str, int]]:
    if not rows:
        raise SystemExit(f"sheet {sheet_name} is empty")
    header_index = build_header_index(list(rows[0]))
    parsed = []
    for row in rows[1:]:
        nwid = parse_int(safe_cell(row, header_index["nwid"]))
        if nwid is None:
            continue
        parsed.append({
            "nwid": nwid,
            "name": str(safe_cell(row, header_index["name"]) or "").strip(),
            "jp": str(safe_cell(row, header_index["jp"]) or "").strip(),
            "pair_group": parse_int(safe_cell(row, header_index["pair_group"])) or 0,
            "adjust_rule": parse_int(safe_cell(row, header_index["adjust_rule"])) or 0,
            "advance": parse_int(safe_cell(row, header_index["advance"])) or 0,
            "market_class": parse_int(safe_cell(row, header_index["market_class"])) or 0,
            "sort_note": str(safe_cell(row, header_index["sort_note"]) or "").strip(),
            "red_black_code": str(safe_cell(row, header_index["red_black_code"]) or "").strip(),
        })
    return parsed, header_index


def uniq_sorted(values: list[int]) -> list[int]:
    return sorted(set(values))


def load_current_config(path: Path) -> tuple[list[dict[str, Any]], dict[int, list[dict[str, Any]]]]:
    data = json.loads(path.read_text())
    bucket: dict[int, list[dict[str, Any]]] = {}
    for item in data:
        bucket.setdefault(int(item["sid"]), []).append(item)
    return data, bucket


def analyze(rows: list[dict[str, Any]], sid: int) -> dict[str, Any]:
    handicap, over_under, odd_even, yes_no, home_away = [], [], [], [], []
    advance, ah, red_black_code = [], [], []
    full_handicap = 0
    full_handicap_names = {"讓球", "讓分", "讓盤", "讓局-總局數"}

    for row in rows:
        if row["pair_group"] == 1 and row["adjust_rule"] == 2:
            handicap.append(row["nwid"])
        elif row["pair_group"] == 1 and row["adjust_rule"] == 3:
            over_under.append(row["nwid"])
        elif row["pair_group"] == 1 and row["adjust_rule"] == 4:
            odd_even.append(row["nwid"])
        elif row["pair_group"] == 1 and row["adjust_rule"] == 5:
            yes_no.append(row["nwid"])
        elif row["pair_group"] == 1 and row["adjust_rule"] == 6:
            home_away.append(row["nwid"])

        if row["advance"] == 1:
            advance.append(row["nwid"])

        if row["market_class"] == 2:
            ah.append(row["nwid"])

        if row["red_black_code"]:
            red_black_code.append(row["nwid"])

        if row["name"] in full_handicap_names:
            if full_handicap and full_handicap != row["nwid"]:
                raise SystemExit(f"multiple fullHandicap candidates found for sid={sid}: {full_handicap}, {row['nwid']}")
            full_handicap = row["nwid"]

    return {
        "sid": sid,
        "pairMarketType": {
            "handicap": uniq_sorted(handicap),
            "overUnder": uniq_sorted(over_under),
            "oddEven": uniq_sorted(odd_even),
            "yesNo": uniq_sorted(yes_no),
            "homeAway": uniq_sorted(home_away),
        },
        "advanceSettleGuardMap": uniq_sorted(advance),
        "sortByOddsAsc": [],
        "sortBySrcOddsAsc": [],
        "sortByOddsAndSelectType": [],
        "sortByParamAsc": [],
        "selectionSortByParamAsc": [],
        "sortByParamAscAndSelection": [],
        "ah": uniq_sorted(ah),
        "manual": [],
        "redBlackCode": uniq_sorted(red_black_code),
        "fullHandicap": full_handicap,
    }


def build_write_payload(generated: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(generated))


def write_sid_config(config_path: Path, sid: int, payload: dict[str, Any], current_bucket: dict[int, list[dict[str, Any]]]) -> None:
    if len(current_bucket.get(sid, [])) > 1:
        raise SystemExit(f"refuse to write: duplicate sid entries found for sid={sid}")
    data = json.loads(config_path.read_text())
    replaced = False
    for i, item in enumerate(data):
        if int(item["sid"]) == sid:
            data[i] = payload
            replaced = True
            break
    if not replaced:
        data.append(payload)
    config_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def process_sheet(workbook: WorkbookReader, sheet_name: str, sid: int, current_bucket: dict[int, list[dict[str, Any]]]) -> dict[str, Any]:
    if sheet_name not in workbook.sheet_targets:
        raise SystemExit(f"sheet not found in workbook: {sheet_name}")

    sheet_rows = workbook.get_rows(sheet_name)
    rows, header_index = parse_rows(sheet_rows, sheet_name)
    current_entries = current_bucket.get(sid, [])
    generated = analyze(rows, sid)
    diff_lines = []
    if not current_entries:
        diff_lines.append("no current sid config found; this would be a new entry")
    elif len(current_entries) > 1:
        diff_lines.append(f"duplicate sid entries found in current game_conf: {len(current_entries)}")
    else:
        diff_lines.append(f"current sid={sid} entry found")
    diff_lines.extend([
        f"pairMarketType.handicap => {len(generated['pairMarketType']['handicap'])}",
        f"pairMarketType.overUnder => {len(generated['pairMarketType']['overUnder'])}",
        f"pairMarketType.oddEven => {len(generated['pairMarketType']['oddEven'])}",
        f"pairMarketType.yesNo => {len(generated['pairMarketType']['yesNo'])}",
        f"pairMarketType.homeAway => {len(generated['pairMarketType']['homeAway'])}",
        f"advanceSettleGuardMap => {len(generated['advanceSettleGuardMap'])}",
        f"ah => {len(generated['ah'])}",
        f"redBlackCode => {len(generated['redBlackCode'])}",
    ])
    write_payload = build_write_payload(generated)
    return {
        "sheet": sheet_name,
        "sid": sid,
        "rowsParsed": len(rows),
        "headerIndex": header_index,
        "currentCount": len(current_entries),
        "generated": generated,
        "writePayload": write_payload,
        "diffSummary": diff_lines,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel", required=True)
    parser.add_argument("--sheet", default="")
    parser.add_argument("--sid", type=int, default=0)
    parser.add_argument("--map", action="append", default=[])
    parser.add_argument("--json-output", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--config", default="conf_file/conf/game_conf.json")
    args = parser.parse_args()

    workbook_path = Path(args.excel)
    if not workbook_path.is_absolute():
        workbook_path = Path.cwd() / workbook_path
    workbook = WorkbookReader(workbook_path)

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = Path.cwd() / config_path
    _, current_bucket = load_current_config(config_path)

    mappings = [parse_mapping(value) for value in args.map]
    if not mappings:
        candidates = detect_sheets(workbook)
        mappings = [resolve_sheet(candidates, args.sheet, args.sid)]

    results = []
    for sheet_name, sid in mappings:
        result = process_sheet(workbook, sheet_name, sid, current_bucket)
        results.append(result)
        if args.write:
            write_sid_config(config_path, sid, result["writePayload"], current_bucket)
            current_bucket[sid] = [result["writePayload"]]

    if args.json_output:
        payload: dict[str, Any] = {"workbook": str(workbook_path), "config": str(config_path), "results": results}
        if len(results) == 1:
            payload.update(results[0])
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print(f"Workbook: {workbook_path}")
    print(f"Config: {config_path}")
    for result in results:
        print(f"Sheet: {result['sheet']}")
        print(f"SID: {result['sid']}")
        print(f"Rows parsed: {result['rowsParsed']}")
        print(f"Header index: {result['headerIndex']}")
        print("Generated fields:")
        print(f"- pairMarketType.handicap: {len(result['generated']['pairMarketType']['handicap'])}")
        print(f"- pairMarketType.overUnder: {len(result['generated']['pairMarketType']['overUnder'])}")
        print(f"- pairMarketType.oddEven: {len(result['generated']['pairMarketType']['oddEven'])}")
        print(f"- pairMarketType.yesNo: {len(result['generated']['pairMarketType']['yesNo'])}")
        print(f"- pairMarketType.homeAway: {len(result['generated']['pairMarketType']['homeAway'])}")
        print(f"- advanceSettleGuardMap: {len(result['generated']['advanceSettleGuardMap'])}")
        print(f"- ah: {len(result['generated']['ah'])}")
        print(f"- redBlackCode: {len(result['generated']['redBlackCode'])}")
        print("Defaulted fields:")
        print("- fullHandicap: 0")
        print("- manual: []")
        print("- sort fields: []")
        print("Diff summary:")
        for line in result["diffSummary"]:
            print(f"- {line}")
        if args.write:
            print(f"Write complete: updated sid={result['sid']} in {config_path}")


if __name__ == "__main__":
    main()
