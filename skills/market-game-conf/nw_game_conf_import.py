#!/usr/bin/env python3
import argparse
import copy
import json
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any

import yaml

NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


MAX_ARRAY_PER_LINE = 20


def load_rules(rules_path: Path) -> dict[str, Any]:
    with open(rules_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def compact_json_dumps(obj: Any, indent: int = 2) -> str:
    """JSON serialization with compact int arrays: up to MAX_ARRAY_PER_LINE elements per line."""

    def _is_int_list(v: Any) -> bool:
        return isinstance(v, list) and all(isinstance(x, int) for x in v)

    def _format(v: Any, level: int) -> str:
        pad = " " * (indent * level)
        pad_inner = " " * (indent * (level + 1))

        if v is None:
            return "null"
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, int):
            return str(v)
        if isinstance(v, float):
            return json.dumps(v)
        if isinstance(v, str):
            return json.dumps(v, ensure_ascii=False)

        if isinstance(v, list):
            if not v:
                return "[]"
            if _is_int_list(v):
                if len(v) <= MAX_ARRAY_PER_LINE:
                    return "[" + ", ".join(str(x) for x in v) + "]"
                lines = []
                for i in range(0, len(v), MAX_ARRAY_PER_LINE):
                    chunk = v[i:i + MAX_ARRAY_PER_LINE]
                    lines.append(pad_inner + ", ".join(str(x) for x in chunk))
                return "[\n" + ",\n".join(lines) + "\n" + pad + "]"
            items = [pad_inner + _format(x, level + 1) for x in v]
            return "[\n" + ",\n".join(items) + "\n" + pad + "]"

        if isinstance(v, dict):
            if not v:
                return "{}"
            items = []
            for k, val in v.items():
                key_str = json.dumps(k, ensure_ascii=False)
                val_str = _format(val, level + 1)
                items.append(f"{pad_inner}{key_str}: {val_str}")
            return "{\n" + ",\n".join(items) + "\n" + pad + "}"

        return json.dumps(v, ensure_ascii=False)

    return _format(obj, 0)


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


def build_header_index(header_row: list[Any], rules: dict[str, Any]) -> dict[str, int]:
    headers_config: dict[str, list[str]] = rules["headers"]
    required: list[str] = rules.get("required_headers", [])

    index = {key: -1 for key in headers_config}

    aliases_map: dict[str, str] = {}
    for key, aliases in headers_config.items():
        for alias in aliases:
            aliases_map[normalize_header(alias)] = key

    for i, cell in enumerate(header_row):
        h = normalize_header(cell)
        for alias_norm, key in aliases_map.items():
            if alias_norm in h and index[key] == -1:
                index[key] = i
                break

    missing = [r for r in required if index.get(r, -1) < 0]
    if missing:
        raise SystemExit(f"required headers missing: {missing}, resolved index: {index}")
    return index


def safe_cell(row: list[Any], idx: int) -> Any:
    if idx < 0 or idx >= len(row):
        return None
    return row[idx]


def parse_rows(rows: list[list[str]], sheet_name: str, rules: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    if not rows:
        raise SystemExit(f"sheet {sheet_name} is empty")
    header_index = build_header_index(list(rows[0]), rules)
    parsed = []
    for row in rows[1:]:
        nwid = parse_int(safe_cell(row, header_index["nwid"]))
        if nwid is None:
            continue
        record: dict[str, Any] = {"nwid": nwid}
        for key in header_index:
            if key == "nwid":
                continue
            raw = safe_cell(row, header_index[key])
            if key in ("name", "jp", "red_black_code"):
                record[key] = str(raw or "").strip()
            else:
                record[key] = parse_int(raw) or 0
        parsed.append(record)
    return parsed, header_index


def set_nested(obj: dict, path: str, value: Any) -> None:
    parts = path.split(".")
    for part in parts[:-1]:
        obj = obj.setdefault(part, {})
    obj.setdefault(parts[-1], []).append(value)


def uniq_sorted(values: list[int]) -> list[int]:
    return sorted(set(values))


def flatten_uniq_sort(obj: Any) -> Any:
    if isinstance(obj, list):
        if obj and all(isinstance(v, int) for v in obj):
            return uniq_sorted(obj)
        return [flatten_uniq_sort(v) for v in obj]
    if isinstance(obj, dict):
        return {k: flatten_uniq_sort(v) for k, v in obj.items()}
    return obj


def analyze(rows: list[dict[str, Any]], sid: int, rules: dict[str, Any]) -> dict[str, Any]:
    template = rules.get("output_template", {})
    defaults = rules.get("defaults", {})
    sid_overrides = rules.get("sid_overrides", {})
    sid_override = sid_overrides.get(sid, {}) or sid_overrides.get(str(sid), {}) or {}
    classify_rules: list[dict] = rules.get("classify_rules", [])
    full_handicap_names: list[str] = list(rules.get("full_handicap_names", []))
    full_handicap_candidates: dict[str, int] = {}

    result = copy.deepcopy(template)
    result["sid"] = sid

    for row in rows:
        for rule in classify_rules:
            col = rule["source_column"]
            match_val = rule["match_value"]
            target = rule["target"]

            cell_val = row.get(col)
            if match_val == "non_empty":
                if cell_val and str(cell_val).strip():
                    set_nested(result, target, row["nwid"])
            else:
                if cell_val == match_val:
                    set_nested(result, target, row["nwid"])

        name = row.get("name", "")
        if name in full_handicap_names and name not in full_handicap_candidates:
            full_handicap_candidates[name] = row["nwid"]

    for name in full_handicap_names:
        if name in full_handicap_candidates:
            result["fullHandicap"] = full_handicap_candidates[name]
            break

    result = flatten_uniq_sort(result)

    if not result.get("fullHandicap"):
        result["fullHandicap"] = defaults.get("fullHandicap", 0)

    manual = sid_override.get("manual", defaults.get("manual", []))
    result["manual"] = uniq_sorted(list(manual)) if manual else []

    return result


def load_current_config(path: Path) -> tuple[list[dict[str, Any]], dict[int, list[dict[str, Any]]]]:
    data = json.loads(path.read_text())
    bucket: dict[int, list[dict[str, Any]]] = {}
    for item in data:
        bucket.setdefault(int(item["sid"]), []).append(item)
    return data, bucket


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
    config_path.write_text(compact_json_dumps(data) + "\n")


def process_sheet(workbook: WorkbookReader, sheet_name: str, sid: int,
                  current_bucket: dict[int, list[dict[str, Any]]], rules: dict[str, Any]) -> dict[str, Any]:
    if sheet_name not in workbook.sheet_targets:
        raise SystemExit(f"sheet not found in workbook: {sheet_name}")

    sheet_rows = workbook.get_rows(sheet_name)
    rows, header_index = parse_rows(sheet_rows, sheet_name, rules)
    current_entries = current_bucket.get(sid, [])
    generated = analyze(rows, sid, rules)

    diff_lines = []
    if not current_entries:
        diff_lines.append("no current sid config found; this would be a new entry")
    elif len(current_entries) > 1:
        diff_lines.append(f"duplicate sid entries found in current game_conf: {len(current_entries)}")
    else:
        diff_lines.append(f"current sid={sid} entry found")

    for key, val in generated.items():
        if isinstance(val, dict):
            for sub_key, sub_val in val.items():
                if isinstance(sub_val, list):
                    diff_lines.append(f"{key}.{sub_key} => {len(sub_val)}")
        elif isinstance(val, list):
            diff_lines.append(f"{key} => {len(val)}")

    return {
        "sheet": sheet_name,
        "sid": sid,
        "rowsParsed": len(rows),
        "headerIndex": header_index,
        "currentCount": len(current_entries),
        "generated": generated,
        "writePayload": json.loads(json.dumps(generated)),
        "diffSummary": diff_lines,
    }


def resolve_mappings(rules: dict[str, Any], workbook: WorkbookReader,
                     cli_maps: list[str]) -> list[tuple[str, int]]:
    if cli_maps:
        mappings = []
        for value in cli_maps:
            sheet_name, sep, sid_text = value.rpartition(":")
            if not sep or not sheet_name.strip() or not sid_text.strip():
                raise SystemExit(f"invalid --map value: {value}; expected <sheetName:sid>")
            sid = parse_int(sid_text)
            if sid is None:
                raise SystemExit(f"invalid sid in --map value: {value}")
            mappings.append((sheet_name.strip(), sid))
        return mappings

    sheet_mapping: dict[str, int] = rules.get("sheet_mapping", {})
    if not sheet_mapping:
        raise SystemExit("no sheet mapping found in rules.yaml and no --map provided")

    available = set(workbook.sheetnames)
    mappings = [(name, sid) for name, sid in sheet_mapping.items() if name in available]
    if not mappings:
        raise SystemExit(
            f"no sheets from rules.yaml found in workbook.\n"
            f"  rules.yaml sheets: {list(sheet_mapping.keys())}\n"
            f"  workbook sheets: {workbook.sheetnames}"
        )
    return mappings


def main() -> None:
    parser = argparse.ArgumentParser(description="NW game_conf importer — driven by rules.yaml")
    parser.add_argument("--excel", default="NW 玩法相关表.xlsx", help="path to NW workbook (.xlsx)")
    parser.add_argument("--rules", default=None, help="path to rules.yaml (default: alongside this script)")
    parser.add_argument("--map", action="append", default=[], help="override sheet mapping: <sheetName:sid>, repeatable")
    parser.add_argument("--config", default="conf_file/conf/game_conf.json", help="path to current game_conf.json")
    parser.add_argument("--output", default="./output/game_conf_result.json", help="write merged JSON result to this file path")
    parser.add_argument("--json-output", action="store_true", help="print JSON to stdout")
    parser.add_argument("--write", action="store_true", help="write back to game_conf.json (use with caution)")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    rules_path = Path(args.rules) if args.rules else script_dir / "rules.yaml"
    if not rules_path.exists():
        raise SystemExit(f"rules file not found: {rules_path}")
    rules = load_rules(rules_path)

    workbook_path = Path(args.excel)
    if not workbook_path.is_absolute():
        workbook_path = Path.cwd() / workbook_path
    workbook = WorkbookReader(workbook_path)

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = Path.cwd() / config_path

    current_bucket: dict[int, list[dict[str, Any]]] = {}
    if config_path.exists():
        _, current_bucket = load_current_config(config_path)

    mappings = resolve_mappings(rules, workbook, args.map)

    results = []
    for sheet_name, sid in mappings:
        result = process_sheet(workbook, sheet_name, sid, current_bucket, rules)
        results.append(result)
        if args.write:
            if not config_path.exists():
                raise SystemExit(f"config file not found for write mode: {config_path}")
            write_sid_config(config_path, sid, result["writePayload"], current_bucket)
            current_bucket[sid] = [result["writePayload"]]

    merged = [r["generated"] for r in results]

    if args.json_output:
        payload: dict[str, Any] = {"workbook": str(workbook_path), "config": str(config_path), "results": results}
        if len(results) == 1:
            payload.update(results[0])
        print(compact_json_dumps(payload))
        return

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = Path.cwd() / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(compact_json_dumps(merged) + "\n")

    print(f"Workbook: {workbook_path}")
    print(f"Config: {config_path}")
    print(f"Mappings: {len(mappings)} sheets")
    print(f"Output: {output_path}")
    for result in results:
        print(f"\n--- Sheet: {result['sheet']}  SID: {result['sid']} ---")
        print(f"Rows parsed: {result['rowsParsed']}")
        print("Diff summary:")
        for line in result["diffSummary"]:
            print(f"  {line}")
        if args.write:
            print(f"Write complete: updated sid={result['sid']} in {config_path}")


if __name__ == "__main__":
    main()
