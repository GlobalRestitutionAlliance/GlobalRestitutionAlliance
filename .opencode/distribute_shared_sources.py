import json, hashlib, datetime, shutil, csv
from pathlib import Path
from bolster_latam_deep import ROOT, PROFILES, TODAY, backup_if_exists, write

# fix Kiobel from last jsonl line
inp = Path(r"W:\Legal\.opencode\browser_capture_results.jsonl")
lines = [l for l in inp.read_text(encoding="utf-8").splitlines() if l.strip()]
r = json.loads(lines[-1])
html = r.get("html", "")
if isinstance(html, str) and len(html) > 1 and html[0] == '"' and html[-1] == '"':
    try:
        html = json.loads(html)
    except:
        pass
b = html.encode("utf-8", errors="ignore")
h = hashlib.sha256(b).hexdigest()
shared = ROOT / "_SHARED_VERIFIED_PUBLIC_SOURCES"
shared.mkdir(parents=True, exist_ok=True)
out = shared / "Kiobel_v_Royal_Dutch_569_US_108.html"
out.write_bytes(b)
meta = {
    "url": r.get("url"),
    "final_url": r.get("final_url", r.get("url")),
    "title": r.get("title"),
    "sha256": h,
    "bytes": len(b),
    "captured_at": datetime.datetime.utcnow().isoformat() + "Z",
    "custodian": "OpenCode/browser",
    "provenance": "browser-rendered outerHTML; WARC-like metadata sidecar; PUBLIC_CAPTURE_UNAUTHENTICATED; verify citation before legal reliance",
}
out.with_suffix(".html.meta.json").write_text(
    json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
)
print("FIXED Kiobel", h[:16])

# distribute all shared to 33 countries
shared_files = sorted(shared.glob("*.html"))
for name, prof in PROFILES.items():
    if name == "US_CU_CUBA":
        continue
    cdir = ROOT / name
    ledger = cdir / "03_Evidentiary_Exhibits" / "Immutable_Ledger"
    ledger.mkdir(parents=True, exist_ok=True)
    log = cdir / "03_Evidentiary_Exhibits" / "EVIDENCE_INTAKE_LOG.md"
    new_rows = []
    for sf in shared_files:
        dest = ledger / sf.name
        if dest.exists():
            continue
        shutil.copy2(sf, dest)
        mj = sf.with_suffix(".html.meta.json")
        if mj.exists():
            shutil.copy2(mj, dest.with_suffix(".html.meta.json"))
            m = json.loads(mj.read_text(encoding="utf-8"))
        else:
            m = {}
        sha = m.get("sha256", hashlib.sha256(dest.read_bytes()).hexdigest())
        new_rows.append(
            f"| {TODAY} | {dest.name} | {m.get('url', '')} | OpenCode/browser-shared | {sha} | PUBLIC_CAPTURE_UNAUTHENTICATED | shared precedent/ICJ source; verify citation before reliance |"
        )
    if new_rows and log.exists():
        txt = log.read_text(encoding="utf-8")
        marker = "## Intake Rules"
        txt = (
            txt.replace(marker, "\n".join(new_rows) + "\n\n" + marker, 1)
            if marker in txt
            else txt + "\n" + "\n".join(new_rows) + "\n"
        )
        log.write_text(txt, encoding="utf-8", newline="\n")
    print("DIST", name, len(new_rows))
