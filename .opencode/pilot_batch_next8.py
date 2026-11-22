import csv, hashlib, json, re, datetime, urllib.request, shutil
from pathlib import Path

TODAY = datetime.date.today().isoformat()
ROOT = Path(r"W:\Legal")
UA = "Mozilla/5.0 (compatible; GlobalRestitutionAlliance/1.0; evidence-harvest)"

REPOS = {
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-actor-dutch-wic-reparations-master-litigation": {
        "domain": "Dutch West India Company / Netherlands transatlantic slavery and colonial extraction",
        "sources": [
            (
                "Nationaal Archief - Dutch Atlantic slavery",
                "https://www.nationaalarchief.nl/onderzoeken/zoekhulpen/slavernijverleden",
            ),
            ("UNESCO Slave Route", "https://www.unesco.org/en/routes-enslaved-peoples"),
            (
                "Library of Congress - Slavery",
                "https://www.loc.gov/classroom-materials/immigration/african/slavery/",
            ),
            ("HathiTrust Digital Library", "https://babel.hathitrust.org/"),
            ("Chronicling America LOC", "https://chroniclingamerica.loc.gov/"),
            ("UN OHCHR", "https://www.ohchr.org/"),
            ("UN Digital Library", "https://digitallibrary.un.org/"),
            (
                "World Bank Netherlands/Open Data",
                "https://data.worldbank.org/country/netherlands",
            ),
            ("Justia", "https://www.justia.com/"),
            ("CourtListener", "https://www.courtlistener.com/"),
        ],
    },
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-actor-royal-african-company-reparations-master-litigation": {
        "domain": "Royal African Company / British transatlantic slavery and colonial extraction",
        "sources": [
            (
                "UK National Archives - slavery",
                "https://www.nationalarchives.gov.uk/help-with-your-research/research-guides/slavery-or-slave-owners/",
            ),
            (
                "UK Parliament - slavery abolition",
                "https://www.parliament.uk/about/living-heritage/transformingsociety/tradeindustry/slavetrade/",
            ),
            (
                "Library of Congress - Slavery",
                "https://www.loc.gov/classroom-materials/immigration/african/slavery/",
            ),
            ("HathiTrust Digital Library", "https://babel.hathitrust.org/"),
            ("Chronicling America LOC", "https://chroniclingamerica.loc.gov/"),
            ("UN OHCHR", "https://www.ohchr.org/"),
            ("UN Digital Library", "https://digitallibrary.un.org/"),
            (
                "World Bank UK/Open Data",
                "https://data.worldbank.org/country/united-kingdom",
            ),
            ("Justia", "https://www.justia.com/"),
            ("CourtListener", "https://www.courtlistener.com/"),
        ],
    },
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-br-reparations-master-litigation": {
        "domain": "Brazil / Portuguese-Brazilian transatlantic slavery, quilombos, post-abolition harms",
        "sources": [
            ("UN OHCHR Brazil", "https://www.ohchr.org/en/countries/brazil"),
            ("UN Digital Library", "https://digitallibrary.un.org/"),
            (
                "Library of Congress - Brazil",
                "https://www.loc.gov/item/?q=brazil+slavery",
            ),
            ("HathiTrust Digital Library", "https://babel.hathitrust.org/"),
            ("Chronicling America LOC", "https://chroniclingamerica.loc.gov/"),
            ("World Bank Brazil", "https://data.worldbank.org/country/brazil"),
            ("UNESCO Slave Route", "https://www.unesco.org/en/routes-enslaved-peoples"),
            ("Justia", "https://www.justia.com/"),
            ("CourtListener", "https://www.courtlistener.com/"),
            ("IBGE Brazil", "https://www.ibge.gov.br/en/home-eng.html"),
        ],
    },
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-dk-reparations-master-litigation": {
        "domain": "Denmark / Danish transatlantic slavery and Caribbean colonial extraction",
        "sources": [
            ("Danish National Archives", "https://www.rigsarkivet.dk/"),
            ("UN OHCHR", "https://www.ohchr.org/"),
            ("UN Digital Library", "https://digitallibrary.un.org/"),
            ("Library of Congress", "https://www.loc.gov/"),
            ("HathiTrust Digital Library", "https://babel.hathitrust.org/"),
            ("Chronicling America LOC", "https://chroniclingamerica.loc.gov/"),
            ("World Bank Denmark", "https://data.worldbank.org/country/denmark"),
            ("UNESCO Slave Route", "https://www.unesco.org/en/routes-enslaved-peoples"),
            ("Justia", "https://www.justia.com/"),
            ("CourtListener", "https://www.courtlistener.com/"),
        ],
    },
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-es-reparations-master-litigation": {
        "domain": "Spain / Spanish transatlantic slavery and colonial extraction",
        "sources": [
            (
                "Archivo General de Indias portal",
                "https://www.culturaydeporte.gob.es/cultura/areas/archivos/mc/archivos/agi/portada.html",
            ),
            ("UN OHCHR", "https://www.ohchr.org/"),
            ("UN Digital Library", "https://digitallibrary.un.org/"),
            ("Library of Congress", "https://www.loc.gov/"),
            ("HathiTrust Digital Library", "https://babel.hathitrust.org/"),
            ("Chronicling America LOC", "https://chroniclingamerica.loc.gov/"),
            ("World Bank Spain", "https://data.worldbank.org/country/spain"),
            ("UNESCO Slave Route", "https://www.unesco.org/en/routes-enslaved-peoples"),
            ("Justia", "https://www.justia.com/"),
            ("CourtListener", "https://www.courtlistener.com/"),
        ],
    },
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-fr-reparations-master-litigation": {
        "domain": "France / French transatlantic slavery, Code Noir, colonial extraction",
        "sources": [
            (
                "Archives Nationales France",
                "https://www.archives-nationales.culture.gouv.fr/",
            ),
            ("UN OHCHR", "https://www.ohchr.org/"),
            ("UN Digital Library", "https://digitallibrary.un.org/"),
            ("Library of Congress", "https://www.loc.gov/"),
            ("HathiTrust Digital Library", "https://babel.hathitrust.org/"),
            ("Chronicling America LOC", "https://chroniclingamerica.loc.gov/"),
            ("World Bank France", "https://data.worldbank.org/country/france"),
            ("UNESCO Slave Route", "https://www.unesco.org/en/routes-enslaved-peoples"),
            ("Justia", "https://www.justia.com/"),
            ("CourtListener", "https://www.courtlistener.com/"),
        ],
    },
    r"W:\Legal\US_DOMESTIC_VICTIMS\US_ER_EXTRAORDINARY_RENDITION_VICTIMS": {
        "domain": "Extraordinary rendition, CIA detention, torture, and accountability gaps",
        "sources": [
            (
                "ACLU - Torture/Rendition",
                "https://www.aclu.org/issues/national-security/torture",
            ),
            (
                "Senate Intelligence Committee - Torture Report Executive Summary",
                "https://www.intelligence.senate.gov/study/cia-detention-and-interrogation-program",
            ),
            ("UN OHCHR - Torture", "https://www.ohchr.org/en/torture"),
            ("UN Digital Library", "https://digitallibrary.un.org/"),
            ("Library of Congress", "https://www.loc.gov/"),
            ("HathiTrust Digital Library", "https://babel.hathitrust.org/"),
            ("Chronicling America LOC", "https://chroniclingamerica.loc.gov/"),
            ("CourtListener", "https://www.courtlistener.com/"),
            ("Justia", "https://www.justia.com/"),
            ("National Archives", "https://www.archives.gov/"),
        ],
    },
    r"W:\Legal\US_DOMESTIC_VICTIMS\US_GT_GUANTANAMO_DETAINEES": {
        "domain": "Guantanamo detention, habeas, due process, torture, and arbitrary detention",
        "sources": [
            ("DoD Military Commissions", "https://www.mc.mil/"),
            (
                "ACLU - Guantanamo",
                "https://www.aclu.org/issues/national-security/detention/guantanamo-bay-detention-camp",
            ),
            (
                "UN OHCHR - Guantanamo",
                "https://www.ohchr.org/en/press-releases/2022/01/guantanamo-bay-ugly-chapter-unrelenting-human-rights-violations-un-experts",
            ),
            ("UN Digital Library", "https://digitallibrary.un.org/"),
            ("CourtListener", "https://www.courtlistener.com/"),
            ("Justia", "https://www.justia.com/"),
            ("Library of Congress", "https://www.loc.gov/"),
            ("HathiTrust Digital Library", "https://babel.hathitrust.org/"),
            ("Chronicling America LOC", "https://chroniclingamerica.loc.gov/"),
            ("National Archives", "https://www.archives.gov/"),
        ],
    },
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
            "notes": "Pilot batch next8 source registry; verify before legal reliance.",
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
            ext = ".html"
            if "pdf" in ctype.lower() or final_url.lower().endswith(".pdf"):
                ext = ".pdf"
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
    return len(out_rows)


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
                "valuation_status": "TBD",
                "review_status": "PENDING_LEGAL_REVIEW",
            }
        )
    vp.write_text(json.dumps(vecs, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(vecs)


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
        ncit = rebuild_citations(repo)
        refresh_manifest(repo)
        print(
            f"{repo.name}: src={len(srcs)} harvest_ok={ok} fail={fail} skip={skip} cites={ncit} vec={nvec}",
            flush=True,
        )


if __name__ == "__main__":
    main()
