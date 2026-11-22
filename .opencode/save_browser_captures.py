import json, re, hashlib, datetime, sys
from pathlib import Path

p = (
    Path(sys.argv[1])
    if len(sys.argv) > 1
    else Path(
        r"C:\Users\User\.local\share\opencode\tool-output\tool_204ec34720010opPaCW8WuPr1M"
    )
)
txt = p.read_text(encoding="utf-8", errors="ignore")
m = re.search(r"\[.*\]", txt, re.S)
if not m:
    print("no json")
    sys.exit(1)
data = json.loads(m.group(0))
for item in data:
    repo = Path(item["repo"])
    cap = item.get("captured")
    if not cap or item.get("error"):
        print("skip", item.get("source_url"), item.get("error"))
        continue
    if isinstance(cap, str):
        try:
            cap = json.loads(cap)
        except:
            cap = {
                "html": cap,
                "title": item.get("source_title", ""),
                "url": item.get("source_url", ""),
            }
    html = cap.get("html", "")
    url = item.get("source_url")
    title = item.get("source_title") or cap.get("title") or "capture"
    ledger = repo / "03_Evidentiary_Exhibits/Immutable_Ledger"
    ledger.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", title)[:70] + "_browser.html"
    out = ledger / safe
    n = 1
    while out.exists():
        out = ledger / (safe.rsplit(".", 1)[0] + f"_{n}.html")
        n += 1
    out.write_bytes(html.encode("utf-8"))
    h = hashlib.sha256(html.encode("utf-8")).hexdigest()
    meta = {
        "url": url,
        "final_url": cap.get("url", url),
        "status": 200,
        "title": cap.get("title", title),
        "bytes": len(html.encode("utf-8")),
        "sha256": h,
        "captured_at": datetime.datetime.utcnow().isoformat() + "Z",
        "custodian": "OpenCode/browser-fallback",
        "provenance": "browser-rendered-outerHTML",
        "batch": "pilot-browser-fallback",
    }
    out.with_suffix(out.suffix + ".meta.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )
    print("saved", out.name, h[:12])
