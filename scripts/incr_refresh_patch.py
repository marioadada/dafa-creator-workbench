#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大发创作工作台 · 同日增量刷新补丁（不新增历史快照）

与 daily_refresh_patch.py 的区别：
  daily_refresh_patch.py 会把「刷新前的 DATA」按 lastUpdate 日期存进 DATA_HISTORY。
  但同一天内二次刷新时，old_date 与今天相同，会往历史里塞一条「今天」的快照，
  造成历史视图出现与当前数据重复的当日条目。
  本脚本用于同日增量补充：只改 DATA 的指定模块 + lastUpdate，DATA_HISTORY 一字不动。

保护：
  - english（30 天静态课程）、workouts（静态跟练清单）强制跳过。
  - 逻辑区（DATA_HISTORY 之后的全部代码）必须逐字节保持一致，否则不落盘。
  - 写入前自检 DATA / DATA_HISTORY 均可重新解析，模块无丢失。

用法:
  python3 incr_refresh_patch.py --html dafa-creator-workbench.html --data incr_data.json
"""
import re, json, argparse, datetime, sys, shutil, os

DATA_RE = r'const DATA = (\{[\s\S]*?\n\});'
HISTORY_RE = r'const DATA_HISTORY = (\[[\s\S]*?\n\]);'
PROTECTED = {"english", "workouts"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--backup", default="")
    args = ap.parse_args()

    with open(args.html, "r", encoding="utf-8") as f:
        text = f.read()
    with open(args.data, "r", encoding="utf-8") as f:
        incr = json.load(f)

    m = re.search(DATA_RE, text)
    if not m:
        sys.exit("找不到 const DATA 对象")
    data_obj = json.loads(m.group(1))

    hm = re.search(HISTORY_RE, text)
    if not hm:
        sys.exit("找不到 const DATA_HISTORY（同日增量要求历史块已存在）")
    history_before = hm.group(1)
    logic_before = text[hm.end():]          # 逻辑区快照，稍后逐字节比对
    history_dates_before = [x.get("date") for x in json.loads(history_before)]

    if args.backup:
        shutil.copy2(args.html, args.backup)

    changed = []

    # 1) 普通模块整体覆盖（跳过下划线开头的特殊指令键与受保护静态模块）
    for k, v in incr.items():
        if k.startswith("_") or k in PROTECTED:
            continue
        if k not in data_obj:
            sys.exit(f"DATA 中不存在模块 {k}，已中止")
        data_obj[k] = v
        changed.append(f"{k}(整体覆盖 {len(v) if isinstance(v, list) else 'dict'} 条)")

    # 2) painPoints：前置新痛点，尾部退一条，总数不变
    head = incr.get("_painPointsHead")
    if head:
        pp = data_obj["painPoints"]
        n = len(pp)
        pp = [head] + [x for x in pp if x.get("title") != head.get("title")]
        data_obj["painPoints"] = pp[:n]
        changed.append(f"painPoints(前置1条，保持{n}条)")

    # 3) finance.flash：按索引替换单条
    rep = incr.get("_financeFlashReplace")
    if rep:
        idx, item = rep["index"], rep["item"]
        flash = data_obj["finance"]["flash"]
        if not (0 <= idx < len(flash)):
            sys.exit(f"finance.flash 索引越界 {idx}/{len(flash)}")
        flash[idx] = item
        changed.append(f"finance.flash[{idx}](替换1条，共{len(flash)}条)")

    # 4) 序列化 DATA
    data_literal = "const DATA = " + json.dumps(data_obj, ensure_ascii=False, indent=2) + ";"
    text = text[:m.start()] + data_literal + text[m.end():]

    # 5) 更新 lastUpdate
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    text = re.sub(r'id="lastUpdate">[^<]*', f'id="lastUpdate">{now}', text)

    # 6) 自检
    chk_d = re.search(DATA_RE, text)
    chk_h = re.search(HISTORY_RE, text)
    if not chk_d or not chk_h:
        sys.exit("自检失败：DATA 或 DATA_HISTORY 无法重新定位，已中止（文件未写入）")
    try:
        d_after = json.loads(chk_d.group(1))
        h_after = json.loads(chk_h.group(1))
    except json.JSONDecodeError as e:
        sys.exit(f"自检失败：结果不是合法 JSON（{e}），已中止（文件未写入）")

    if chk_h.group(1) != history_before:
        sys.exit("自检失败：DATA_HISTORY 被改动，已中止（文件未写入）")
    if [x.get("date") for x in h_after] != history_dates_before:
        sys.exit("自检失败：历史快照日期变化，已中止（文件未写入）")
    if text[chk_h.end():] != logic_before:
        sys.exit("自检失败：逻辑区发生改动，已中止（文件未写入）")
    missing = [k for k in data_obj if k not in d_after]
    if missing:
        sys.exit(f"自检失败：模块丢失 {missing}，已中止（文件未写入）")
    for k in PROTECTED:
        if k in data_obj and len(d_after.get(k, [])) != len(data_obj[k]):
            sys.exit(f"自检失败：静态模块 {k} 条数变化，已中止（文件未写入）")

    with open(args.html, "w", encoding="utf-8") as f:
        f.write(text)

    print("同日增量刷新完成，DATA_HISTORY 未变（%d 条快照）。" % len(h_after))
    print("lastUpdate =", now)
    print("变更明细：")
    for c in changed:
        print("  -", c)
    print("静态模块保持：english=%d, workouts=%d" % (len(d_after.get("english", [])), len(d_after.get("workouts", []))))


if __name__ == "__main__":
    main()
