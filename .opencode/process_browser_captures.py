import json, hashlib, datetime
from pathlib import Path

inp = Path(r"W:\Legal\.opencode\browser_capture_results.jsonl")
ts = datetime.datetime.utcnow().isoformat() + "Z"
today = datetime.date.today().isoformat()
count = 0
ok = 0
fail = 0
for line in inp.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    r = json.loads(line)
    if r.get("test"):
        continue
    count += 1
    cdir = Path(r["cdir"])
    capdir = cdir / "03_Evidentiary_Exhibits" / "Immutable_Ledger"
    capdir.mkdir(parents=True, exist_ok=True)
    log = cdir / "03_Evidentiary_Exhibits" / "EVIDENCE_INTAKE_LOG.md"
    if not r.get("ok"):
        row = f"| {today} | {r.get('artifact', '')} | {r.get('url', '')} | OpenCode/browser-fallback | N/A | CAPTURE_FAILED | {str(r.get('error', ''))[:200]} |"
        fail += 1
    else:
        html = r.get("html", "")
        if (
            isinstance(html, str)
            and len(html) > 1
            and html[0] == '"'
            and html[-1] == '"'
        ):
            try:
                html = json.loads(html)
            except:
                pass
        b = html.encode("utf-8", errors="ignore")
        h = hashlib.sha256(b).hexdigest()
        base = r.get("artifact", "capture") + "_browser.html"
        out = capdir / base
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
            "provenance": "browser-rendered outerHTML; WARC-like metadata sidecar; PUBLIC_CAPTURE_UNAUTHENTICATED; not certified original",
        }
        out.with_suffix(out.suffix + ".meta.json").write_text(
            json.dumps(meta, indent=2, ensure_ascii=False),
            encoding="utf-8",
            newline="\n",
        )
        row = f"| {today} | {out.name} | {r.get('url', '')} | OpenCode/browser-fallback | {h} | PUBLIC_CAPTURE_UNAUTHENTICATED | status={r.get('status')}; bytes={len(b)}; captured={ts}; browser=brave |"
        ok += 1
    if log.exists():
        txt = log.read_text(encoding="utf-8")
        marker = "## Intake Rules"
        txt = (
            txt.replace(marker, row + "\n\n" + marker, 1)
            if marker in txt
            else txt + "\n" + row + "\n"
        )
        log.write_text(txt, encoding="utf-8", newline="\n")
print(f"processed={count} ok={ok} fail={fail}")
