import csv, json, datetime, shutil, hashlib
from pathlib import Path

TODAY = datetime.date.today().isoformat()
REPOS = {
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-actor-dutch-wic-reparations-master-litigation": "Dutch West India Company / Netherlands transatlantic slavery and colonial extraction",
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-actor-royal-african-company-reparations-master-litigation": "Royal African Company / British transatlantic slavery and colonial extraction",
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-br-reparations-master-litigation": "Brazil / Portuguese-Brazilian transatlantic slavery, quilombos, post-abolition harms",
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-dk-reparations-master-litigation": "Denmark / Danish transatlantic slavery and Caribbean colonial extraction",
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-es-reparations-master-litigation": "Spain / Spanish transatlantic slavery and colonial extraction",
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-fr-reparations-master-litigation": "France / French transatlantic slavery, Code Noir, colonial extraction",
    r"W:\Legal\US_DOMESTIC_VICTIMS\US_ER_EXTRAORDINARY_RENDITION_VICTIMS": "Extraordinary rendition, CIA detention, torture, and accountability gaps",
    r"W:\Legal\US_DOMESTIC_VICTIMS\US_GT_GUANTANAMO_DETAINEES": "Guantanamo detention, habeas, due process, torture, and arbitrary detention",
}

REQUIRED = [
    "citation_id",
    "url",
    "local_artifact",
    "sha256",
    "verification_status",
    "verification_rule",
]


def sha256p(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def sanitize_md(s):
    return (
        str(s or "").replace("|", "\\|").replace("\n", " ").replace("\r", " ").strip()
    )


def rebuild_citations(repo: Path):
    ex = repo / "03_Evidentiary_Exhibits"
    ledger = ex / "Immutable_Ledger"
    cit_csv = ex / "CITATION_INDEX.csv"
    cit_md = ex / "CITATION_INDEX.md"
    old_rows = []
    old_fields = []
    if cit_csv.exists():
        with cit_csv.open("r", encoding="utf-8", newline="") as f:
            r = csv.DictReader(f)
            old_fields = list(r.fieldnames or [])
            old_rows = list(r)
    by_art = {}
    for r in old_rows:
        k = str(r.get("local_artifact", "")).replace("\\", "/")
        if k:
            by_art[k] = r
    fields = list(old_fields)
    for req in REQUIRED:
        if req not in fields:
            fields.append(req)
    nid = 1
    for r in old_rows:
        try:
            nid = max(nid, int(str(r.get("citation_id", "")).split("-")[-1]) + 1)
        except:
            pass
    merged = dict(by_art)
    for mp in sorted(ledger.glob("*.meta.json")):
        try:
            meta = json.loads(mp.read_text(encoding="utf-8", errors="ignore"))
        except:
            continue
        art = ledger / mp.name.removesuffix(".meta.json")
        if not art.exists():
            continue
        rel = art.relative_to(repo).as_posix()
        sha = sha256p(art)
        prev = merged.get(rel, {})
        row = dict(prev)
        row["local_artifact"] = rel
        row["url"] = meta.get("url", prev.get("url", ""))
        row["sha256"] = sha
        row["verification_rule"] = (
            prev.get("verification_rule") or "NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT"
        )
        row["verification_status"] = (
            prev.get("verification_status") or "PENDING_LEGAL_REVIEW"
        )
        if not row.get("citation_id"):
            row["citation_id"] = f"CIT-{nid:04d}"
            nid += 1
        merged[rel] = row
    out_rows = sorted(
        merged.values(),
        key=lambda r: (str(r.get("citation_id", "")), str(r.get("local_artifact", ""))),
    )
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    if cit_csv.exists():
        shutil.copy2(cit_csv, cit_csv.with_name(f"CITATION_INDEX.backup-{ts}.csv"))
    with cit_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in out_rows:
            w.writerow({k: r.get(k, "") for k in fields})
    cit_md.write_text(
        "# Citation Index\n\nRule: NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT. All entries PENDING_LEGAL_REVIEW unless explicitly verified through local hashed artifact + human sign-off.\n\n"
        + "\n".join(
            [
                f"- {sanitize_md(r.get('citation_id'))}: {sanitize_md(r.get('url'))} | `{sanitize_md(r.get('local_artifact'))}` | `{str(r.get('sha256', ''))[:16]}...` | {sanitize_md(r.get('verification_status'))}"
                for r in out_rows
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return out_rows


def enrich(repo: Path, domain: str, cites):
    ids = [c["citation_id"] for c in cites if c.get("citation_id")]
    # valuation worksheet
    ws = repo / "00_Master_Knowledge_Base/VALUATION_WORKSHEET.csv"
    if ws.exists():
        with ws.open("r", encoding="utf-8", newline="") as f:
            r = csv.DictReader(f)
            fields = list(r.fieldnames or [])
            rows = list(r)
        for req in [
            "vector_id","domain","harm_category","low_usd","base_usd","high_usd","currency",
            "evidence_basis","citation_ids","evidence_mapping_status","valuation_status","review_status","notes",
        ]:
            if req not in fields:
                fields.append(req)
        for i, row in enumerate(rows):
            row["domain"] = row.get("domain") or domain
            row["valuation_status"] = "TBD"
            row["review_status"] = "PENDING_LEGAL_REVIEW"
            row["currency"] = row.get("currency") or "USD"
            row["low_usd"] = ""
            row["base_usd"] = ""
            row["high_usd"] = ""
            if ids:
                # deterministic auto-candidate only; not reviewed evidentiary mapping
                pick = ids[i % len(ids)]
                row["citation_ids"] = pick
                row["evidence_mapping_status"] = "AUTO_CANDIDATE_PENDING_REVIEW"
                row["evidence_basis"] = f"AUTO_CANDIDATE_CITATION {pick}; mapping PENDING_EVIDENCE_MAPPING_REVIEW"
            else:
                row["citation_ids"] = ""
                row["evidence_mapping_status"] = "PENDING_EVIDENCE_MAPPING"
                row["evidence_basis"] = "PENDING_EVIDENCE_LINK"
            row["notes"] = "No published amount; valuation pending evidence-backed review."
        with ws.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
    # 3000 vectors
    vp = repo / "99_Archives_and_Manifests/claim_vector_registry_3000.json"
    if vp.exists():
        try:
            vecs = json.loads(vp.read_text(encoding="utf-8", errors="ignore"))
        except:
            vecs = []
    else:
        vecs = [{"vector_id": f"VEC-{i:04d}"} for i in range(1, 3001)]
    for i, v in enumerate(vecs):
        v["domain"] = domain
        v["valuation_status"] = "TBD"
        v["review_status"] = "PENDING_LEGAL_REVIEW"
        if ids:
            v["evidence_ids"] = [ids[i % len(ids)]]
            v["evidence_mapping_status"] = "AUTO_CANDIDATE_PENDING_REVIEW"
        else:
            v["evidence_ids"] = []
            v["evidence_mapping_status"] = "PENDING_EVIDENCE_MAPPING"
        v.setdefault("harm_class", "PENDING_CLASSIFICATION")
    vp.write_text(json.dumps(vecs, ensure_ascii=False, indent=2), encoding="utf-8")


def write_methodology(repo: Path, domain: str):
    kb = repo / "00_Master_Knowledge_Base"
    kb.mkdir(parents=True, exist_ok=True)
    p = kb / "VALUATION_METHODOLOGY_PILOT.md"
    content = f"""# Valuation Methodology Pilot

**Domain:** {domain}
**Date:** {TODAY}
**Status:** PILOT / PENDING_LEGAL_REVIEW

## Guardrails
- No published monetary amount without versioned cited workbook and human legal/quant review.
- All amounts remain `TBD (valuation pending)` until evidence-backed valuation is approved.
- Citations/evidence links are `PENDING_LEGAL_REVIEW`; no `VERIFIED` status without local hashed artifact + human sign-off.

## Damages Theories (framework only)
1. **Unjust enrichment / restitution** - quantify benefits traceable to documented harms where evidence supports.
2. **Lost labor/value extraction** - model only with defensible historical/economic sources and explicit assumptions.
3. **Property/land/resource deprivation** - requires title/land/asset records, concessions, or comparable documented takings.
4. **Personal injury / human rights harms** - requires victim records, medical/forensic evidence, or authoritative findings.
5. **Consequential/community harms** - intergenerational, cultural, health, and development impacts; use conservative, documented bases.

## Evidence Priorities
- Primary archival records (government, court, treaty, corporate, colonial administration, military, or institutional records).
- Authenticated victim declarations/affidavits and organization records.
- UN/OHCHR/court/commission findings with provenance.
- Peer-reviewed economic/history studies (as secondary support, not sole proof).

## FOIA / Records Targets (pending human filing)
- Relevant national archives and records repositories for the domain.
- Court dockets and judgments (certified copies where required).
- Agency/department records requests (FOIA/public records equivalents) for contracts, policies, communications, and detainee/treatment records where applicable.
- Corporate successor/registry records where private actor liability is alleged.

## Valuation Workflow
1. Link each claim vector to at least one reviewed evidence artifact/citation ID.
2. Build low/base/high scenarios with explicit assumptions and uncertainty bands.
3. Separate documented damages from modeled extrapolations.
4. Require human legal + quantitative review before publishing any amount.
"""
    p.write_text(content, encoding="utf-8", newline="\n")


def refresh_manifest(repo: Path):
    vk = repo / "VERIFICATION_KEYS"
    vk.mkdir(parents=True, exist_ok=True)
    lines = []
    for fp in sorted(repo.rglob("*")):
        if not fp.is_file():
            continue
        rel = fp.relative_to(repo).as_posix()
        if rel.startswith(".git/") or rel == "VERIFICATION_KEYS/sha256_manifest.txt":
            continue
        try:
            lines.append(f"{sha256p(fp)}  {rel}")
        except:
            pass
    (vk / "sha256_manifest.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )


for rp, domain in REPOS.items():
    repo = Path(rp)
    if not repo.exists():
        print("MISS", repo.name)
        continue
    cites = rebuild_citations(repo)
    enrich(repo, domain, cites)
    write_methodology(repo, domain)
    refresh_manifest(repo)
    print(f"{repo.name}: cites={len(cites)} enriched=3000 methodology=Y", flush=True)
