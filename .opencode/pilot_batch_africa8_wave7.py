import csv, hashlib, json, re, datetime, urllib.request
from pathlib import Path

TODAY = datetime.date.today().isoformat()
UA = "Mozilla/5.0 (compatible; GlobalRestitutionAlliance/1.0; evidence-harvest)"

REPOS = {
    r"W:\Legal\AFRICA\US_TG_TOGO": {"domain":"Togo","sources":[
        ("UN OHCHR Togo","https://www.ohchr.org/en/countries/togo"),
        ("UN Digital Library","https://digitallibrary.un.org/"),
        ("Library of Congress - Togo","https://www.loc.gov/item/?q=togo+colonial+forced+labor+german+french"),
        ("HathiTrust Digital Library","https://babel.hathitrust.org/"),
        ("Chronicling America LOC","https://chroniclingamerica.loc.gov/"),
        ("World Bank Togo","https://data.worldbank.org/country/togo"),
        ("UNESCO Slave Route","https://www.unesco.org/en/routes-enslaved-peoples"),
        ("French National Archives (public portal)","https://www.archives-nationales.culture.gouv.fr/"),
        ("Justia","https://www.justia.com/"),
        ("CourtListener","https://www.courtlistener.com/"),
    ]},
    r"W:\Legal\AFRICA\US_TN_TUNISIA": {"domain":"Tunisia","sources":[
        ("UN OHCHR Tunisia","https://www.ohchr.org/en/countries/tunisia"),
        ("UN Digital Library","https://digitallibrary.un.org/"),
        ("Library of Congress - Tunisia","https://www.loc.gov/item/?q=tunisia+colonial+forced+labor+slavery"),
        ("HathiTrust Digital Library","https://babel.hathitrust.org/"),
        ("Chronicling America LOC","https://chroniclingamerica.loc.gov/"),
        ("World Bank Tunisia","https://data.worldbank.org/country/tunisia"),
        ("UNESCO Slave Route","https://www.unesco.org/en/routes-enslaved-peoples"),
        ("French National Archives (public portal)","https://www.archives-nationales.culture.gouv.fr/"),
        ("Justia","https://www.justia.com/"),
        ("CourtListener","https://www.courtlistener.com/"),
    ]},
    r"W:\Legal\AFRICA\US_TZ_TANZANIA": {"domain":"Tanzania","sources":[
        ("UN OHCHR Tanzania","https://www.ohchr.org/en/countries/tanzania"),
        ("UN Digital Library","https://digitallibrary.un.org/"),
        ("Library of Congress - Tanzania","https://www.loc.gov/item/?q=tanzania+tanganyika+colonial+slavery+forced+labor"),
        ("HathiTrust Digital Library","https://babel.hathitrust.org/"),
        ("Chronicling America LOC","https://chroniclingamerica.loc.gov/"),
        ("World Bank Tanzania","https://data.worldbank.org/country/tanzania"),
        ("UNESCO Slave Route","https://www.unesco.org/en/routes-enslaved-peoples"),
        ("UK National Archives - Tanzania","https://discovery.nationalarchives.gov.uk/"),
        ("Justia","https://www.justia.com/"),
        ("CourtListener","https://www.courtlistener.com/"),
    ]},
    r"W:\Legal\AFRICA\US_UG_UGANDA": {"domain":"Uganda","sources":[
        ("UN OHCHR Uganda","https://www.ohchr.org/en/countries/uganda"),
        ("UN Digital Library","https://digitallibrary.un.org/"),
        ("Library of Congress - Uganda","https://www.loc.gov/item/?q=uganda+colonial+forced+labor"),
        ("HathiTrust Digital Library","https://babel.hathitrust.org/"),
        ("Chronicling America LOC","https://chroniclingamerica.loc.gov/"),
        ("World Bank Uganda","https://data.worldbank.org/country/uganda"),
        ("UNESCO Slave Route","https://www.unesco.org/en/routes-enslaved-peoples"),
        ("UK National Archives - Uganda","https://discovery.nationalarchives.gov.uk/"),
        ("Justia","https://www.justia.com/"),
        ("CourtListener","https://www.courtlistener.com/"),
    ]},
    r"W:\Legal\AFRICA\US_ZM_ZAMBIA": {"domain":"Zambia","sources":[
        ("UN OHCHR Zambia","https://www.ohchr.org/en/countries/zambia"),
        ("UN Digital Library","https://digitallibrary.un.org/"),
        ("Library of Congress - Zambia","https://www.loc.gov/item/?q=zambia+northern+rhodesia+colonial+forced+labor"),
        ("HathiTrust Digital Library","https://babel.hathitrust.org/"),
        ("Chronicling America LOC","https://chroniclingamerica.loc.gov/"),
        ("World Bank Zambia","https://data.worldbank.org/country/zambia"),
        ("UNESCO Slave Route","https://www.unesco.org/en/routes-enslaved-peoples"),
        ("UK National Archives - Zambia","https://discovery.nationalarchives.gov.uk/"),
        ("Justia","https://www.justia.com/"),
        ("CourtListener","https://www.courtlistener.com/"),
    ]},
    r"W:\Legal\AFRICA\US_ZW_ZIMBABWE": {"domain":"Zimbabwe","sources":[
        ("UN OHCHR Zimbabwe","https://www.ohchr.org/en/countries/zimbabwe"),
        ("UN Digital Library","https://digitallibrary.un.org/"),
        ("Library of Congress - Zimbabwe","https://www.loc.gov/item/?q=zimbabwe+rhodesia+colonial+forced+labor"),
        ("HathiTrust Digital Library","https://babel.hathitrust.org/"),
        ("Chronicling America LOC","https://chroniclingamerica.loc.gov/"),
        ("World Bank Zimbabwe","https://data.worldbank.org/country/zimbabwe"),
        ("UNESCO Slave Route","https://www.unesco.org/en/routes-enslaved-peoples"),
        ("UK National Archives - Zimbabwe","https://discovery.nationalarchives.gov.uk/"),
        ("Justia","https://www.justia.com/"),
        ("CourtListener","https://www.courtlistener.com/"),
    ]},
}


def sha256p(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sanitize_md(s: str) -> str:
    return (
        str(s or "").replace("|", "\\|").replace("\n", " ").replace("\r", " ").strip()
    )


def safe_slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_")[:80] or "capture"


def ensure_source_registry(repo: Path, sources):
    kb = repo / "00_Master_Knowledge_Base"
    kb.mkdir(parents=True, exist_ok=True)
    reg = kb / "SOURCE_REGISTRY.csv"
    rows = []
    if reg.exists():
        with reg.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
    by_url = {str(r.get("url", "")).strip(): r for r in rows}
    for title, url in sources:
        if url in by_url:
            continue
        by_url[url] = {
            "source_id": f"SRC-{len(by_url) + 1:04d}",
            "title": title,
            "url": url,
            "source_type": "PUBLIC_WEB",
            "access_method": "direct_or_browser_fallback",
            "verification_status": "PENDING_LEGAL_REVIEW",
            "notes": "Pilot batch africa8_wave6 source registry; verify before legal reliance.",
        }
    out = list(by_url.values())
    for i, r in enumerate(out, 1):
        r["source_id"] = f"SRC-{i:04d}"
    with reg.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "source_id",
                "title",
                "url",
                "source_type",
                "access_method",
                "verification_status",
                "notes",
            ],
        )
        w.writeheader()
        w.writerows(out)
    return out


def harvest(repo: Path, sources):
    ex = repo / "03_Evidentiary_Exhibits"
    ledger = ex / "Immutable_Ledger"
    ledger.mkdir(parents=True, exist_ok=True)
    logp = ex / "EVIDENCE_INTAKE_LOG.md"
    if not logp.exists():
        logp.write_text(
            "# Evidence Intake Log\n\n| date | artifact | source_url | custodian | sha256 | status | notes |\n|---|---|---|---|---|---|---|\n\n## Intake Rules\n",
            encoding="utf-8",
            newline="\n",
        )
    logtxt = logp.read_text(encoding="utf-8", errors="ignore")
    results = []
    for title, url in sources:
        slug = safe_slug(title)[:60]
        existing_meta = None
        for mp in ledger.glob("*.meta.json"):
            try:
                m = json.loads(mp.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                continue
            if m.get("url") == url:
                existing_meta = mp
                break
        if existing_meta:
            results.append({"url": url, "title": title, "status": "SKIP_EXISTS"})
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as resp:
                final_url = resp.geturl()
                ctype = resp.headers.get("Content-Type", "")
                http_status = getattr(resp, "status", 200)
                max_bytes = 15 * 1024 * 1024
                chunks = []
                total = 0
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > max_bytes:
                        raise ValueError(f"response_too_large>{max_bytes}")
                    chunks.append(chunk)
                data = b"".join(chunks)
            ext = (
                ".pdf"
                if ("pdf" in ctype.lower() or final_url.lower().endswith(".pdf"))
                else ".html"
            )
            art = ledger / f"{slug}{ext}"
            if art.exists():
                art = ledger / f"{slug}_{sha256_bytes(url.encode())[:8]}{ext}"
            art.write_bytes(data)
            sha = sha256_bytes(data)
            art.with_name(art.name + ".meta.json").write_text(
                json.dumps(
                    {
                        "url": url,
                        "final_url": final_url,
                        "title": title,
                        "fetched_at": datetime.datetime.utcnow().isoformat() + "Z",
                        "http_status": http_status,
                        "content_type": ctype,
                        "bytes": len(data),
                        "sha256": sha,
                        "provenance": "direct-http-capture",
                        "custodian": "OpenCode/harvest",
                        "legal_review_status": "PENDING_LEGAL_REVIEW",
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            row = f"| {TODAY} | {sanitize_md(art.name)} | {sanitize_md(url)} | OpenCode/harvest | {sha} | PUBLIC_CAPTURE_UNAUTHENTICATED | direct-http http_status={http_status} bytes={len(data)} final_url={sanitize_md(final_url)} |"
            if sha not in logtxt and art.name not in logtxt:
                marker = "## Intake Rules"
                logtxt = (
                    logtxt.replace(marker, row + "\n\n" + marker, 1)
                    if marker in logtxt
                    else logtxt + "\n" + row + "\n"
                )
            results.append(
                {"url": url, "title": title, "status": "OK", "http_status": http_status}
            )
        except Exception as e:
            results.append(
                {"url": url, "title": title, "status": "FAIL", "error": str(e)[:200]}
            )
    logp.write_text(logtxt, encoding="utf-8", newline="\n")
    return results


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
    for req in [
        "citation_id",
        "url",
        "local_artifact",
        "sha256",
        "verification_status",
        "verification_rule",
    ]:
        if req not in fields:
            fields.append(req)
    nid = 1
    for r in old_rows:
        try:
            nid = max(nid, int(str(r.get("citation_id", "")).split("-")[-1]) + 1)
        except:
            pass
    merged = dict(by_art)
    if ledger.exists():
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
                prev.get("verification_rule")
                or "NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT"
            )
            allowed_status = {
                "PENDING_LEGAL_REVIEW",
                "VERIFIED_WITH_LOCAL_HASHED_ARTIFACT_AND_HUMAN_SIGNOFF",
            }
            prev_status = str(prev.get("verification_status") or "").strip()
            row["verification_status"] = (
                prev_status if prev_status in allowed_status else "PENDING_LEGAL_REVIEW"
            )
            if not row.get("citation_id"):
                row["citation_id"] = f"CIT-{nid:04d}"
                nid += 1
            merged[rel] = row
    out_rows = sorted(
        merged.values(),
        key=lambda r: (str(r.get("citation_id", "")), str(r.get("local_artifact", ""))),
    )
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


def ensure_valuation(repo: Path, domain: str):
    kb = repo / "00_Master_Knowledge_Base"
    kb.mkdir(parents=True, exist_ok=True)
    ws = kb / "VALUATION_WORKSHEET.csv"
    if not ws.exists():
        with ws.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(
                f,
                fieldnames=[
                    "vector_id",
                    "domain",
                    "harm_category",
                    "low_usd",
                    "base_usd",
                    "high_usd",
                    "currency",
                    "evidence_basis",
                    "citation_ids",
                    "evidence_mapping_status",
                    "valuation_status",
                    "review_status",
                    "notes",
                ],
            )
            w.writeheader()
            for i in range(1, 3001):
                w.writerow(
                    {
                        "vector_id": f"VEC-{i:04d}",
                        "domain": domain,
                        "harm_category": "TBD",
                        "low_usd": "",
                        "base_usd": "",
                        "high_usd": "",
                        "currency": "USD",
                        "evidence_basis": "PENDING_EVIDENCE_LINK",
                        "citation_ids": "",
                        "evidence_mapping_status": "PENDING_EVIDENCE_MAPPING",
                        "valuation_status": "TBD",
                        "review_status": "PENDING_LEGAL_REVIEW",
                        "notes": "No published amount; valuation pending evidence-backed review.",
                    }
                )
    return ws


def ensure_vectors(repo: Path, domain: str):
    man = repo / "99_Archives_and_Manifests"
    man.mkdir(parents=True, exist_ok=True)
    vp = man / "claim_vector_registry_3000.json"
    if vp.exists():
        try:
            data = json.loads(vp.read_text(encoding="utf-8", errors="ignore"))
            if isinstance(data, list) and len(data) >= 3000:
                return len(data)
        except Exception:
            pass
    vecs = []
    for i in range(1, 3001):
        vecs.append(
            {
                "vector_id": f"VEC-{i:04d}",
                "domain": domain,
                "harm_class": "PENDING_CLASSIFICATION",
                "evidence_ids": [],
                "evidence_mapping_status": "PENDING_EVIDENCE_MAPPING",
                "valuation_status": "TBD",
                "review_status": "PENDING_LEGAL_REVIEW",
            }
        )
    vp.write_text(json.dumps(vecs, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(vecs)


def enrich(repo: Path, domain: str, cites):
    ids = [c["citation_id"] for c in cites if c.get("citation_id")]
    ws = repo / "00_Master_Knowledge_Base/VALUATION_WORKSHEET.csv"
    if ws.exists():
        with ws.open("r", encoding="utf-8", newline="") as f:
            r = csv.DictReader(f)
            fields = list(r.fieldnames or [])
            rows = list(r)
        for req in [
            "vector_id",
            "domain",
            "harm_category",
            "low_usd",
            "base_usd",
            "high_usd",
            "currency",
            "evidence_basis",
            "citation_ids",
            "evidence_mapping_status",
            "valuation_status",
            "review_status",
            "notes",
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
                pick = ids[i % len(ids)]
                row["citation_ids"] = pick
                row["evidence_mapping_status"] = "AUTO_CANDIDATE_PENDING_REVIEW"
                row["evidence_basis"] = (
                    f"AUTO_CANDIDATE_CITATION {pick}; mapping PENDING_EVIDENCE_MAPPING_REVIEW"
                )
            else:
                row["citation_ids"] = ""
                row["evidence_mapping_status"] = "PENDING_EVIDENCE_MAPPING"
                row["evidence_basis"] = "PENDING_EVIDENCE_LINK"
            row["notes"] = (
                "No published amount; valuation pending evidence-backed review."
            )
        with ws.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
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
    p.write_text(
        f"""# Valuation Methodology Pilot

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
- Agency/department records requests (FOIA/public records equivalents) for contracts, policies, communications, and records where applicable.
- Corporate successor/registry records where private actor liability is alleged.

## Valuation Workflow
1. Link each claim vector to at least one reviewed evidence artifact/citation ID.
2. Build low/base/high scenarios with explicit assumptions and uncertainty bands.
3. Separate documented damages from modeled extrapolations.
4. Require human legal + quantitative review before publishing any amount.
""",
        encoding="utf-8",
        newline="\n",
    )


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
        except Exception:
            pass
    (vk / "sha256_manifest.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )


def main():
    for rp, cfg in REPOS.items():
        repo = Path(rp)
        if not repo.exists():
            print("MISS", repo)
            continue
        srcs = ensure_source_registry(repo, cfg["sources"])
        harvest_results = harvest(repo, cfg["sources"])
        ok = sum(1 for r in harvest_results if r["status"] == "OK")
        fail = sum(1 for r in harvest_results if r["status"] == "FAIL")
        skip = sum(1 for r in harvest_results if r["status"] == "SKIP_EXISTS")
        ensure_valuation(repo, cfg["domain"])
        nvec = ensure_vectors(repo, cfg["domain"])
        cites = rebuild_citations(repo)
        enrich(repo, cfg["domain"], cites)
        write_methodology(repo, cfg["domain"])
        refresh_manifest(repo)
        print(
            f"{repo.name}: src={len(srcs)} harvest_ok={ok} fail={fail} skip={skip} cites={len(cites)} vec={nvec}",
            flush=True,
        )


if __name__ == "__main__":
    main()
