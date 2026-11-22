import csv, hashlib, json, datetime
from pathlib import Path

TODAY = datetime.date.today().isoformat()
REPOS = [
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS",
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-gb-reparations-master-litigation",
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-pt-reparations-master-litigation",
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-nl-reparations-master-litigation",
    r"W:\Legal\US_DOMESTIC_VICTIMS\US_DW_NUCLEAR_DOWNWINDERS",
    r"W:\Legal\PACIFIC\US_MH_MARSHALL_ISLANDS",
    r"W:\Legal\US_DOMESTIC_VICTIMS\US_JA_JAPANESE_AMERICAN_INTERNEES",
    r"W:\Legal\US_TURTLE_ISLAND_NATIVES\NAVAJO\US_AZ_NAVAJO_NATION_ARIZONA_NEW_MEXICO_UTAH",
]


def sha256p(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


for path in REPOS:
    repo = Path(path)
    ex = repo / "03_Evidentiary_Exhibits"
    ledger = ex / "Immutable_Ledger"
    if not ledger.exists():
        print("MISS", repo.name)
        continue
    logp = ex / "EVIDENCE_INTAKE_LOG.md"
    logtxt = (
        logp.read_text(encoding="utf-8", errors="ignore")
        if logp.exists()
        else "# Evidence Intake Log\n\n| date | artifact | source_url | custodian | sha256 | status | notes |\n|---|---|---|---|---|---|---|\n\n## Intake Rules\n"
    )
    newrows = []
    for mp in sorted(ledger.glob("*.meta.json")):
        try:
            meta = json.loads(mp.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            continue
        art = Path(str(mp).replace(".meta.json", ""))
        if not art.exists():
            continue
        sha = meta.get("sha256", "")
        url = meta.get("url", "")
        prov = meta.get("provenance", "")
        # only add browser captures not already logged by sha or filename
        if prov != "browser-rendered-outerHTML":
            continue
        if sha and sha in logtxt:
            continue
        if art.name in logtxt:
            continue
        cust = meta.get("custodian", "OpenCode/browser-fallback")
        status = "PUBLIC_CAPTURE_UNAUTHENTICATED"
        notes = f"browser-fallback status={meta.get('status', '')} bytes={meta.get('bytes', '')} final_url={meta.get('final_url', '')}"
        newrows.append(
            f"| {TODAY} | {art.name} | {url} | {cust} | {sha} | {status} | {notes} |"
        )
    if newrows:
        m = "## Intake Rules"
        if m in logtxt:
            logtxt = logtxt.replace(m, "\n".join(newrows) + "\n\n" + m, 1)
        else:
            logtxt = logtxt + "\n" + "\n".join(newrows) + "\n"
        logp.write_text(logtxt, encoding="utf-8", newline="\n")

    # rebuild citations
    cites = []
    for mp in sorted(ledger.glob("*.meta.json")):
        try:
            meta = json.loads(mp.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            continue
        art = Path(str(mp).replace(".meta.json", ""))
        if not art.exists():
            continue
        cites.append(
            {
                "citation_id": f"CIT-{len(cites) + 1:04d}",
                "url": meta.get("url", ""),
                "local_artifact": str(art.relative_to(repo)).replace("\\", "/"),
                "sha256": meta.get("sha256", ""),
                "verification_status": "PENDING_LEGAL_REVIEW",
                "verification_rule": "NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT",
            }
        )
    with (ex / "CITATION_INDEX.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "citation_id",
                "url",
                "local_artifact",
                "sha256",
                "verification_status",
                "verification_rule",
            ],
        )
        w.writeheader()
        w.writerows(cites)
    (ex / "CITATION_INDEX.md").write_text(
        "# Citation Index\n\nRule: NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT. All PENDING_LEGAL_REVIEW.\n\n"
        + "\n".join(
            [
                f"- {c['citation_id']}: {c['url']} | `{c['local_artifact']}` | `{c['sha256'][:16]}...` | {c['verification_status']}"
                for c in cites
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    # rebuild manifest
    lines = []
    for fp in sorted(repo.rglob("*")):
        if not fp.is_file():
            continue
        rel = fp.relative_to(repo).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel == "VERIFICATION_KEYS/sha256_manifest.txt":
            continue
        try:
            lines.append(f"{sha256p(fp)}  {rel}")
        except Exception:
            pass
    (repo / "VERIFICATION_KEYS/sha256_manifest.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"{repo.name} browser_rows={len(newrows)} cites={len(cites)}", flush=True)
