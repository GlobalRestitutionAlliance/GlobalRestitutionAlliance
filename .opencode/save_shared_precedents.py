import json, hashlib, datetime
from pathlib import Path
from bolster_latam_deep import ROOT

inp = Path(r"W:\Legal\.opencode\browser_capture_results.jsonl")
lines = [l for l in inp.read_text(encoding="utf-8").splitlines() if l.strip()]
new = [json.loads(l) for l in lines[-4:]]
ts = datetime.datetime.utcnow().isoformat() + "Z"
shared = ROOT / "_SHARED_VERIFIED_PUBLIC_SOURCES"
shared.mkdir(parents=True, exist_ok=True)
for r in new:
    html = r.get("html", "")
    if isinstance(html, str) and len(html) > 1 and html[0] == '"' and html[-1] == '"':
        try:
            html = json.loads(html)
        except:
            pass
    b = html.encode("utf-8", errors="ignore")
    h = hashlib.sha256(b).hexdigest()
    name = r.get("label", "doc") + ".html"
    out = shared / name
    out.write_bytes(b)
    meta = {
        "url": r.get("url"),
        "final_url": r.get("final_url", r.get("url")),
        "title": r.get("title"),
        "sha256": h,
        "bytes": len(b),
        "captured_at": ts,
        "custodian": "OpenCode/browser",
        "provenance": "browser-rendered outerHTML; WARC-like metadata sidecar; PUBLIC_CAPTURE_UNAUTHENTICATED; verify citation before legal reliance",
    }
    out.with_suffix(".html.meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("SAVED", name, h[:16], len(b))
