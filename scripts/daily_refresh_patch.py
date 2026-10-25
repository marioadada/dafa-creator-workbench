#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大发创作工作台 · 每日联网数据刷新（含历史存档）

用法:
  python3 daily_refresh_patch.py --html dafa-creator-workbench.html --data new_data.json

职责:
  1. 读取当前 HTML 中的 DATA 对象。
  2. 把「刷新前」的旧数据（7 个联网模块）作为快照写入 DATA_HISTORY，
     键名为刷新前的 lastUpdate 日期 -> 实现「历史日期查阅」功能。
  3. 用 new_data.json 里的模块值覆盖 DATA 对应模块。
  4. 更新页面顶部 lastUpdate 为当前时间。
  5. 写回 HTML，保持结构/样式/本地存储键不变。

注意:
  - english 字段现在是「30 天新概念第一册锚定课程体系」（Day1 开场 + L1-L28 + Day30 总复习），
    为静态预载、按日期解锁，本脚本【不覆盖、不快照】english（见下方 ENGLISH_STATIC 保护）。
    若 new_data.json 误带 english，也会被跳过，绝不破坏课程。
  - 历史快照只存会被覆盖的联网模块；workouts / english 为静态模块，
    在历史视图里自动回退到最新 DATA（getViewData 合并逻辑）。
  - 2026-08-11 起：painPoints（AI编程痛点教程）与 finance（财经快讯：利好利空 flash + 财经常识 knowledge）
    均纳入每日联网刷新，并进入历史快照；new_data.json 需提供这两个键。
"""
import re, json, argparse, datetime, sys

# 每日联网刷新的模块（含历史快照覆盖）
MODULE_KEYS = ["aiCodingNews", "aiCodingTopics", "opcNews", "opcTopics",
               "novelTracks", "hotVideos", "painPoints", "finance"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--data", required=True)
    args = ap.parse_args()

    with open(args.html, "r", encoding="utf-8") as f:
        text = f.read()

    with open(args.data, "r", encoding="utf-8") as f:
        new_data = json.load(f)

    # 1) 解析当前 DATA
    m = re.search(r'const DATA = (\{[\s\S]*?\n\});', text)
    if not m:
        sys.exit("找不到 const DATA 对象")
    data_obj = json.loads(m.group(1))

    # 2) 旧数据快照（刷新前）
    lu = re.search(r'id="lastUpdate">([^<]*)', text)
    old_date = lu.group(1).split()[0] if lu else datetime.date.today().isoformat()
    snapshot = {"date": old_date, "data": {k: data_obj[k] for k in MODULE_KEYS if k in data_obj}}

    # 3) 读取/更新 DATA_HISTORY
    # 注意：锚点用 \n\]; （行首闭合方括号），避免正文字符串里的 "];" 造成误截断
    HISTORY_RE = r'const DATA_HISTORY = (\[[\s\S]*?\n\]);'
    hm = re.search(HISTORY_RE, text)
    if hm:
        history = json.loads(hm.group(1))
    else:
        history = []
    # 同日期去重，避免重复快照
    history = [h for h in history if h.get("date") != old_date]
    history.insert(0, snapshot)
    history = history[:30]  # 最多保留 30 天
    history_literal = "const DATA_HISTORY = " + json.dumps(history, ensure_ascii=False, indent=2) + ";"

    # 4) 覆盖模块（english 为静态课程，强制跳过，绝不破坏）
    for k, v in new_data.items():
        if k == "english":
            continue
        data_obj[k] = v

    # 5) 序列化写回
    data_literal = "const DATA = " + json.dumps(data_obj, ensure_ascii=False, indent=2) + ";"
    text = text[:m.start()] + data_literal + text[m.end():]

    if hm:
        # 关键：DATA 替换后文本长度已变，必须在「新文本」上重新定位历史块，
        # 不能复用旧 hm 的偏移量（否则会把历史块插进 DATA 内部的字符串里，文件直接损坏）
        hm2 = re.search(HISTORY_RE, text)
        if not hm2:
            sys.exit("DATA 替换后找不到 DATA_HISTORY，已中止（文件未写入）")
        text = text[:hm2.start()] + history_literal + text[hm2.end():]
    else:
        # 没有历史块则在 DATA 后插入
        anchor = re.search(r'\};\n\n// ================== 本地存储数据', text)
        insert_at = anchor.start() + len("};\n\n")
        text = text[:insert_at] + history_literal + "\n\n" + text[insert_at:]

    # 6) 更新 lastUpdate
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    text = re.sub(r'id="lastUpdate">[^<]*', f'id="lastUpdate">{now}', text)

    # 7) 写入前自检：两个数据块都必须能重新解析出来，否则一律不落盘
    chk_d = re.search(r'const DATA = (\{[\s\S]*?\n\});', text)
    chk_h = re.search(HISTORY_RE, text)
    if not chk_d or not chk_h:
        sys.exit("自检失败：DATA 或 DATA_HISTORY 无法重新定位，已中止（文件未写入）")
    try:
        d_after = json.loads(chk_d.group(1))
        json.loads(chk_h.group(1))
    except json.JSONDecodeError as e:
        sys.exit(f"自检失败：结果不是合法 JSON（{e}），已中止（文件未写入）")
    missing = [k for k in data_obj if k not in d_after]
    if missing:
        sys.exit(f"自检失败：模块丢失 {missing}，已中止（文件未写入）")

    with open(args.html, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"已刷新数据并写入历史快照（{old_date}），当前历史共 {len(history)} 条。")
    print("覆盖模块:", list(new_data.keys()))

if __name__ == "__main__":
    main()
