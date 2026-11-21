import csv, hashlib, json, re, datetime, urllib.request, shutil, subprocess, os
from pathlib import Path

TODAY = datetime.date.today().isoformat()
BASE = Path(r"W:\Legal")
TARGETS = [
    "US_AFRICAN_AMERICAN_REPARATIONS",
    "US_DW_NUCLEAR_DOWNWINDERS",
    "US_ER_EXTRAORDINARY_RENDITION_VICTIMS",
    "US_GT_GUANTANAMO_DETAINEES",
    "US_JA_JAPANESE_AMERICAN_INTERNEES",
]


def find_dir(name):
    for p in [BASE / name, BASE / "US_DOMESTIC_VICTIMS" / name]:
        if p.exists():
            return p
    return None


def sha256(b):
    return hashlib.sha256(b).hexdigest()


UA = "Mozilla/5.0"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(), getattr(r, "status", 200), dict(r.headers.items()), r.geturl()


# harvest
for name in TARGETS:
    cdir = find_dir(name)
    if not cdir:
        continue
    src = cdir / "03_Evidentiary_Exhibits/PRIMARY_PUBLIC_SOURCES.csv"
    ledger = cdir / "03_Evidentiary_Exhibits/Immutable_Ledger"
    ledger.mkdir(parents=True, exist_ok=True)
    log = cdir / "03_Evidentiary_Exhibits/EVIDENCE_INTAKE_LOG.md"
    rows = []
    if src.exists():
        with src.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for i, r in enumerate(reader):
                if i >= 8:
                    break
                url = r.get("url", "").strip()
                title = r.get("title", "source")
                try:
                    data, status, headers, final = fetch(url)
                    ct = headers.get("Content-Type", "")
                    ext = ".pdf" if "pdf" in ct.lower() else ".html"
                    base = (
                        f"{name[:2]}_{i + 1:02d}_{re.sub(r'[^A-Za-z0-9._-]+', '_', title)[:80]}"
                        + ext
                    )
                    out = ledger / base
                    n = 1
                    while out.exists():
                        out = ledger / (base.rsplit(".", 1)[0] + f"_{n}" + ext)
                        n += 1
                    out.write_bytes(data)
                    meta = {
                        "url": url,
                        "final_url": final,
                        "status": status,
                        "content_type": ct,
                        "bytes": len(data),
                        "sha256": sha256(data),
                        "captured_at": datetime.datetime.utcnow().isoformat() + "Z",
                        "custodian": "OpenCode/harvest",
                    }
                    out.with_suffix(out.suffix + ".meta.json").write_text(
                        json.dumps(meta, indent=2), encoding="utf-8"
                    )
                    rows.append(
                        f"| {TODAY} | {out.name} | {url} | OpenCode/harvest | {meta['sha256']} | PUBLIC_CAPTURE_UNAUTHENTICATED | status={status} bytes={len(data)} |"
                    )
                except Exception as e:
                    rows.append(
                        f"| {TODAY} | {title} | {url} | OpenCode/harvest | N/A | CAPTURE_FAILED | {e} |"
                    )
    if rows and log.exists():
        txt = log.read_text(encoding="utf-8")
        m = "## Intake Rules"
        log.write_text(
            txt.replace(m, "\n".join(rows) + "\n\n" + m, 1)
            if m in txt
            else txt + "\n" + "\n".join(rows),
            encoding="utf-8",
            newline="\n",
        )
    # citation index
    cites = []
    for p in sorted(ledger.glob("*.meta.json")):
        try:
            meta = json.loads(p.read_text(encoding="utf-8"))
        except:
            continue
        art = p.with_suffix("")
        if not art.exists():
            # .html.meta.json -> .html
            art = Path(str(p).replace(".meta.json", ""))
        if not art.exists():
            continue
        cites.append(
            {
                "citation_id": f"{name[:2]}-CIT-{len(cites) + 1:04d}",
                "title": meta.get("title", ""),
                "date": "",
                "authoring_body": "",
                "url": meta.get("url", ""),
                "local_artifact": str(art.relative_to(cdir)).replace("\\", "/"),
                "sha256": meta.get("sha256", ""),
                "captured_at": meta.get("captured_at", ""),
                "excerpt": "",
                "page_paragraph_ref": "",
                "verification_status": "PENDING_LEGAL_REVIEW",
                "verification_rule": "NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT",
            }
        )
    ex = cdir / "03_Evidentiary_Exhibits"
    with (ex / "CITATION_INDEX.csv").open("w", newline="", encoding="utf-8") as f:
        cols = [
            "citation_id",
            "title",
            "date",
            "authoring_body",
            "url",
            "local_artifact",
            "sha256",
            "captured_at",
            "excerpt",
            "page_paragraph_ref",
            "verification_status",
            "verification_rule",
        ]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(cites)
    md = [
        f"# Citation Index - {name}",
        "",
        "Rule: NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT. All PENDING_LEGAL_REVIEW.",
        "",
        "| ID | URL | Artifact | SHA-256 | Status |",
        "|---|---|---|---|---|",
    ]
    for c in cites:
        md.append(
            f"| {c['citation_id']} | {c['url']} | `{c['local_artifact']}` | `{c['sha256'][:16]}...` | {c['verification_status']} |"
        )
    (ex / "CITATION_INDEX.md").write_text(
        "\n".join(md) + "\n", encoding="utf-8", newline="\n"
    )
    # patch docs
    block = (
        "\n\n## Verified Source Citations (PENDING_LEGAL_REVIEW)\n\nRule: No citation marked VERIFIED without local hashed source artifact and human sign-off.\n\n"
        + "\n".join(
            [
                f"- {c['citation_id']}: {c['url']} | `{c['local_artifact']}` | `{c['sha256'][:16]}...` | {c['verification_status']}"
                for c in cites[:20]
            ]
        )
        + "\n"
    )
    for folder in [
        "01_Pleadings_and_Complaints",
        "02_Discovery_and_Evidentiary",
        "03_Motions_and_Briefs",
        "04_International_Tribunals",
        "05_Strategic_Doctrines_and_Red_Team",
        "06_Trial_and_Appellate_Prep",
        "07_Enforcement_and_Restitution",
        "00_Master_Knowledge_Base",
    ]:
        d = cdir / folder
        if not d.exists():
            continue
        for p in d.rglob("*.md"):
            txt = p.read_text(encoding="utf-8", errors="ignore")
            if "## Verified Source Citations (PENDING_LEGAL_REVIEW)" in txt:
                idx = txt.index("## Verified Source Citations (PENDING_LEGAL_REVIEW)")
                p.write_text(txt[:idx].rstrip() + block, encoding="utf-8", newline="\n")
            else:
                p.write_text(txt.rstrip() + block, encoding="utf-8", newline="\n")
    # manifest
    lines = []
    for fp in sorted(cdir.rglob("*")):
        if not fp.is_file():
            continue
        rel = fp.relative_to(cdir).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel == "VERIFICATION_KEYS/sha256_manifest.txt":
            continue
        lines.append(f"{hashlib.sha256(fp.read_bytes()).hexdigest()}  {rel}")
    (cdir / "VERIFICATION_KEYS/sha256_manifest.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )
    print("OK", name, "cites", len(cites))
print("DONE")
