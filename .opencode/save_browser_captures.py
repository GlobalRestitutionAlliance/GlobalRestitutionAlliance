import json, hashlib, datetime, sys
from pathlib import Path
from bolster_latam_deep import backup_if_exists

inp = Path(sys.argv[1])
data = json.loads(inp.read_text(encoding="utf-8"))
ts = datetime.datetime.utcnow().isoformat() + "Z"
for r in data:
    cdir = Path(r["cdir"])
    capdir = cdir / "03_Evidentiary_Exhibits" / "Immutable_Ledger"
    capdir.mkdir(parents=True, exist_ok=True)
    log = cdir / "03_Evidentiary_Exhibits" / "EVIDENCE_INTAKE_LOG.md"
    if not r.get("ok"):
        row = f"| {datetime.date.today().isoformat()} | {r.get('artifact', '')} | {r.get('url', '')} | OpenCode/browser | N/A | CAPTURE_FAILED | {r.get('error', '')} |"
    else:
        html = r.get("html", "")
        if isinstance(html, str) and html.startswith('"') and html.endswith('"'):
            try:
                html = json.loads(html)
            except:
                pass
        b = html.encode("utf-8", errors="ignore")
        h = hashlib.sha256(b).hexdigest()
        name = r.get("artifact", "capture") + "_browser.html"
        out = capdir / name
        n = 1
        while out.exists():
            out = capdir / (r.get("artifact", "capture") + f"_browser_{n}.html")
            n += 1
        out.write_bytes(b)
        meta = {
            "url": r.get("url"),
            "final_url": r.get("final_url", r.get("url")),
            "status": r.get("status"),
            "title": r.get("title"),
            "bytes": len(b),
            "sha256": h,
            "captured_at": ts,
            "custodian": "OpenCode/browser-fallback",
            "country": r.get("country"),
            "iso": r.get("iso"),
            "provenance": "browser-eval-outerHTML; WARC-like metadata sidecar; not certified original",
        }
        out.with_suffix(out.suffix + ".meta.json").write_text(
            json.dumps(meta, indent=2), encoding="utf-8", newline="\n"
        )
        row = f"| {datetime.date.today().isoformat()} | {out.name} | {r.get('url', '')} | OpenCode/browser-fallback | {h} | PUBLIC_CAPTURE_UNAUTHENTICATED | status={r.get('status')}; bytes={len(b)}; captured={ts}; browser=brave |"
    if log.exists():
        txt = log.read_text(encoding="utf-8")
        marker = "## Intake Rules"
        txt = (
            txt.replace(marker, row + "\n\n" + marker, 1)
            if marker in txt
            else txt + "\n" + row + "\n"
        )
        log.write_text(txt, encoding="utf-8", newline="\n")
print("saved", len(data))
