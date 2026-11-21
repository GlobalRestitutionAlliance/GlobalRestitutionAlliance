import csv, hashlib, json, os, re, time, datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bolster_pacific_full import ROOT, PROFILES, TODAY, backup_if_exists

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
TIMEOUT = 25
MAX_PER_COUNTRY = 12  # keep reasonable; prioritize first entries


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def safe_name(s):
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_")
    return s[:180] or "artifact"


def fetch(url):
    req = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urlopen(req, timeout=TIMEOUT) as r:
        data = r.read()
        status = getattr(r, "status", 200)
        headers = dict(r.headers.items())
        final_url = r.geturl()
    return data, status, headers, final_url


def guess_ext(url, content_type):
    ct = (content_type or "").lower()
    if "pdf" in ct or url.lower().endswith(".pdf"):
        return ".pdf"
    if "html" in ct or "xml" in ct:
        return ".html"
    if "json" in ct:
        return ".json"
    if "csv" in ct:
        return ".csv"
    if "text/plain" in ct:
        return ".txt"
    return ".bin"


def append_log(log_path, rows):
    if not log_path.exists():
        log_path.write_text(
            "# Evidence Intake Log\n\n| Date | Artifact | Source URL | Retrieved By | SHA-256 | Custody Status | Notes |\n|---|---|---|---|---|---|---|\n",
            encoding="utf-8",
            newline="\n",
        )
    txt = log_path.read_text(encoding="utf-8")
    marker = "## Intake Rules"
    block = "\n".join(rows)
    if marker in txt:
        txt = txt.replace(marker, block + "\n\n" + marker, 1)
    else:
        txt += "\n" + block + "\n"
    log_path.write_text(txt, encoding="utf-8", newline="\n")


def refresh_manifest(cdir):
    manifest = cdir / "VERIFICATION_KEYS/sha256_manifest.txt"
    backup_if_exists(manifest, cdir)
    lines = []
    for fp in sorted(cdir.rglob("*")):
        if not fp.is_file():
            continue
        rel = fp.relative_to(cdir).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel == "VERIFICATION_KEYS/sha256_manifest.txt":
            continue
        lines.append(f"{sha256(fp.read_bytes())}  {rel}")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main():
    summary = []
    for name, prof in PROFILES.items():
        if name == "US_CU_CUBA":
            continue
        cdir = ROOT / name
        src_csv = cdir / "03_Evidentiary_Exhibits" / "PRIMARY_PUBLIC_SOURCES.csv"
        if not src_csv.exists():
            summary.append((name, 0, 0, 0))
            continue
        ledger = cdir / "03_Evidentiary_Exhibits" / "Immutable_Ledger"
        ledger.mkdir(parents=True, exist_ok=True)
        log = cdir / "03_Evidentiary_Exhibits" / "EVIDENCE_INTAKE_LOG.md"
        rows = []
        ok = fail = skip = 0
        seen = set()
        with src_csv.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for i, r in enumerate(reader):
                if ok + fail >= MAX_PER_COUNTRY:
                    break
                url = (r.get("url") or "").strip()
                title = (r.get("title") or "source").strip()
                if not url or url in seen:
                    skip += 1
                    continue
                seen.add(url)
                # skip obvious search pages? keep them but they may be html; still useful capture
                ts = datetime.datetime.utcnow().isoformat() + "Z"
                base = safe_name(f"{prof['iso']}_{i + 1:02d}_{title}")[:120]
                try:
                    data, status, headers, final_url = fetch(url)
                    ct = headers.get("Content-Type", "")
                    ext = guess_ext(final_url or url, ct)
                    out = ledger / (base + ext)
                    # avoid overwrite collision
                    n = 1
                    while out.exists():
                        out = ledger / (base + f"_{n}" + ext)
                        n += 1
                    out.write_bytes(data)
                    meta = {
                        "url": url,
                        "final_url": final_url,
                        "status": status,
                        "content_type": ct,
                        "bytes": len(data),
                        "sha256": sha256(data),
                        "captured_at": ts,
                        "custodian": "OpenCode/harvest_public_sources.py",
                        "country": prof["country"],
                        "iso": prof["iso"],
                        "title": title,
                        "headers": {k: v for k, v in list(headers.items())[:30]},
                    }
                    out.with_suffix(out.suffix + ".meta.json").write_text(
                        json.dumps(meta, indent=2), encoding="utf-8", newline="\n"
                    )
                    rows.append(
                        f"| {TODAY} | {out.name} | {url} | OpenCode/harvest_public_sources.py | {meta['sha256']} | PUBLIC_CAPTURE_UNAUTHENTICATED | status={status}; ct={ct}; bytes={len(data)}; final={final_url} |"
                    )
                    ok += 1
                except Exception as e:
                    rows.append(
                        f"| {TODAY} | {base} | {url} | OpenCode/harvest_public_sources.py | N/A | CAPTURE_FAILED | {e} |"
                    )
                    fail += 1
                time.sleep(0.2)
        if rows:
            append_log(log, rows)
        refresh_manifest(cdir)
        summary.append((name, ok, fail, skip))
        print(f"HARVEST {name} ok={ok} fail={fail} skip={skip}")
    print("DONE")
    for n, o, f, s in summary:
        print(f"SUM {n} {o} {f} {s}")


if __name__ == "__main__":
    main()
