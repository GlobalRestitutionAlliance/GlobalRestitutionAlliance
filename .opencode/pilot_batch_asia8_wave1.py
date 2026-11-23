#!/usr/bin/env python3
"""ASIA 8-repo full-enrichment wave: scaffold, harvest, enrich, manifests."""

from __future__ import annotations
import csv, json, hashlib, os, re, datetime, urllib.request, urllib.error, ssl
from pathlib import Path

BASE = Path(r"W:\Legal")
REGION = "ASIA"
REPOS = {
    "US_VN_VIETNAM": [
        (
            "National Archives - Vietnam War Records",
            "https://www.archives.gov/research/vietnam-war",
        ),
        (
            "Library of Congress - Vietnam",
            "https://www.loc.gov/search/?q=vietnam+war+united+states",
        ),
        (
            "State Dept FRUS - Vietnam",
            "https://history.state.gov/historicaldocuments/frus1964-68v01",
        ),
        (
            "Yale Avalon - Paris Peace Accords 1973",
            "https://avalon.law.yale.edu/20th_century/paris.asp",
        ),
        (
            "UN Digital Library - Vietnam",
            "https://digitallibrary.un.org/search?ln=en&p=vietnam",
        ),
        (
            "ICRC - Vietnam",
            "https://www.icrc.org/en/where-we-work/asia-pacific/vietnam",
        ),
        ("World Bank - Vietnam", "https://data.worldbank.org/country/viet-nam"),
        ("UNHCR - Vietnam", "https://www.unhcr.org/countries/viet-nam"),
        ("HRW - Vietnam", "https://www.hrw.org/asia/vietnam"),
        (
            "Amnesty - Vietnam",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-east-asia-and-the-pacific/viet-nam/",
        ),
    ],
    "US_PH_PHILIPPINES": [
        (
            "National Archives - Philippine-American War",
            "https://www.archives.gov/research/military/philippine-american-war",
        ),
        (
            "Library of Congress - Philippines",
            "https://www.loc.gov/search/?q=philippines+united+states+colonial",
        ),
        (
            "State Dept FRUS - Philippines",
            "https://history.state.gov/countries/philippines",
        ),
        (
            "Yale Avalon - Treaty of Paris 1898",
            "https://avalon.law.yale.edu/19th_century/sp1898.asp",
        ),
        (
            "UN Digital Library - Philippines",
            "https://digitallibrary.un.org/search?ln=en&p=philippines",
        ),
        ("Official Gazette - Philippines", "https://www.officialgazette.gov.ph/"),
        ("World Bank - Philippines", "https://data.worldbank.org/country/philippines"),
        ("UNHCR - Philippines", "https://www.unhcr.org/countries/philippines"),
        ("HRW - Philippines", "https://www.hrw.org/asia/philippines"),
        (
            "Amnesty - Philippines",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-east-asia-and-the-pacific/philippines/",
        ),
    ],
    "US_ID_INDONESIA": [
        (
            "National Archives - Indonesia",
            "https://www.archives.gov/research/guide-fed-records/groups/263.html",
        ),
        (
            "Library of Congress - Indonesia",
            "https://www.loc.gov/search/?q=indonesia+united+states+1965",
        ),
        (
            "State Dept FRUS - Indonesia 1964-68",
            "https://history.state.gov/historicaldocuments/frus1964-68v26",
        ),
        (
            "UN Digital Library - Indonesia",
            "https://digitallibrary.un.org/search?ln=en&p=indonesia",
        ),
        ("World Bank - Indonesia", "https://data.worldbank.org/country/indonesia"),
        ("UNHCR - Indonesia", "https://www.unhcr.org/countries/indonesia"),
        ("HRW - Indonesia", "https://www.hrw.org/asia/indonesia"),
        (
            "Amnesty - Indonesia",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-east-asia-and-the-pacific/indonesia/",
        ),
        (
            "ICRC - Indonesia",
            "https://www.icrc.org/en/where-we-work/asia-pacific/indonesia",
        ),
        (
            "National Security Archive - Indonesia",
            "https://nsarchive.gwu.edu/briefing-book/indonesia/2017-10-17/indonesia-mass-murder-1965-us-embassy-files",
        ),
    ],
    "US_KR_SOUTH_KOREA": [
        (
            "National Archives - Korean War",
            "https://www.archives.gov/research/military/korean-war",
        ),
        (
            "Library of Congress - Korea",
            "https://www.loc.gov/search/?q=korea+united+states+military",
        ),
        ("State Dept FRUS - Korea", "https://history.state.gov/countries/korea"),
        (
            "Yale Avalon - Armistice Agreement 1953",
            "https://avalon.law.yale.edu/20th_century/kor001.asp",
        ),
        (
            "UN Digital Library - Korea",
            "https://digitallibrary.un.org/search?ln=en&p=republic+of+korea",
        ),
        ("World Bank - Korea", "https://data.worldbank.org/country/korea-rep"),
        ("UNHCR - Korea", "https://www.unhcr.org/countries/republic-korea"),
        ("HRW - South Korea", "https://www.hrw.org/asia/south-korea"),
        (
            "Amnesty - South Korea",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/east-asia/south-korea/",
        ),
        ("USFK - United States Forces Korea", "https://www.usfk.mil/"),
    ],
    "US_IQ_IRAQ": [
        (
            "National Archives - Iraq",
            "https://www.archives.gov/research/military/iraq-war",
        ),
        (
            "Library of Congress - Iraq",
            "https://www.loc.gov/search/?q=iraq+war+united+states",
        ),
        ("State Dept - Iraq", "https://www.state.gov/countries-areas/iraq/"),
        (
            "UN Digital Library - Iraq",
            "https://digitallibrary.un.org/search?ln=en&p=iraq",
        ),
        ("UNHCR - Iraq", "https://www.unhcr.org/countries/iraq"),
        ("World Bank - Iraq", "https://data.worldbank.org/country/iraq"),
        ("HRW - Iraq", "https://www.hrw.org/middle-east/north-africa/iraq"),
        (
            "Amnesty - Iraq",
            "https://www.amnesty.org/en/location/middle-east-and-north-africa/middle-east/iraq/",
        ),
        ("ICRC - Iraq", "https://www.icrc.org/en/where-we-work/middle-east/iraq"),
        ("UNAMI - UN Assistance Mission for Iraq", "https://unami.unmissions.org/"),
    ],
    "US_AF_AFGHANISTAN": [
        (
            "National Archives - Afghanistan",
            "https://www.archives.gov/research/military/afghanistan-war",
        ),
        (
            "Library of Congress - Afghanistan",
            "https://www.loc.gov/search/?q=afghanistan+united+states+war",
        ),
        (
            "State Dept - Afghanistan",
            "https://www.state.gov/countries-areas/afghanistan/",
        ),
        (
            "UN Digital Library - Afghanistan",
            "https://digitallibrary.un.org/search?ln=en&p=afghanistan",
        ),
        ("UNHCR - Afghanistan", "https://www.unhcr.org/countries/afghanistan"),
        ("World Bank - Afghanistan", "https://data.worldbank.org/country/afghanistan"),
        ("HRW - Afghanistan", "https://www.hrw.org/asia/afghanistan"),
        (
            "Amnesty - Afghanistan",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-asia/afghanistan/",
        ),
        (
            "ICRC - Afghanistan",
            "https://www.icrc.org/en/where-we-work/asia-pacific/afghanistan",
        ),
        (
            "UNAMA - UN Assistance Mission in Afghanistan",
            "https://unama.unmissions.org/",
        ),
    ],
    "US_IR_IRAN": [
        (
            "National Archives - Iran",
            "https://www.archives.gov/research/guide-fed-records/groups/263.html",
        ),
        (
            "Library of Congress - Iran",
            "https://www.loc.gov/search/?q=iran+united+states+1953+coup",
        ),
        (
            "State Dept FRUS - Iran 1952-54",
            "https://history.state.gov/historicaldocuments/frus1952-54v10",
        ),
        (
            "Yale Avalon - Algiers Accords 1981",
            "https://avalon.law.yale.edu/20th_century/algiers.asp",
        ),
        (
            "UN Digital Library - Iran",
            "https://digitallibrary.un.org/search?ln=en&p=iran",
        ),
        ("World Bank - Iran", "https://data.worldbank.org/country/iran-islamic-rep"),
        ("UNHCR - Iran", "https://www.unhcr.org/countries/iran-islamic-republic"),
        ("HRW - Iran", "https://www.hrw.org/middle-east/north-africa/iran"),
        (
            "Amnesty - Iran",
            "https://www.amnesty.org/en/location/middle-east-and-north-africa/middle-east/iran/",
        ),
        (
            "National Security Archive - Iran",
            "https://nsarchive.gwu.edu/briefing-book/iran/2018-02-12/cia-confirms-role-1953-iran-coup",
        ),
    ],
    "US_KH_CAMBODIA": [
        (
            "National Archives - Cambodia",
            "https://www.archives.gov/research/military/vietnam-war/cambodia",
        ),
        (
            "Library of Congress - Cambodia",
            "https://www.loc.gov/search/?q=cambodia+bombing+united+states",
        ),
        ("State Dept FRUS - Cambodia", "https://history.state.gov/countries/cambodia"),
        (
            "Yale Avalon - Paris Peace Agreements 1991",
            "https://avalon.law.yale.edu/20th_century/cambodia.asp",
        ),
        (
            "UN Digital Library - Cambodia",
            "https://digitallibrary.un.org/search?ln=en&p=cambodia",
        ),
        (
            "ECCC - Extraordinary Chambers in Courts of Cambodia",
            "https://www.eccc.gov.kh/en",
        ),
        ("World Bank - Cambodia", "https://data.worldbank.org/country/cambodia"),
        ("UNHCR - Cambodia", "https://www.unhcr.org/countries/cambodia"),
        ("HRW - Cambodia", "https://www.hrw.org/asia/cambodia"),
        (
            "Amnesty - Cambodia",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-east-asia-and-the-pacific/cambodia/",
        ),
    ],
}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, fields, rows):
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_csv(path: Path):
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        return list(r.fieldnames or []), list(r)


def ensure_source_registry(repo: Path, sources):
    p = repo / "00_Master_Knowledge_Base" / "SOURCE_REGISTRY.csv"
    fields = [
        "source_id",
        "title",
        "url",
        "publisher",
        "source_type",
        "access",
        "notes",
        "legal_review_status",
    ]
    rows = []
    for i, (title, url) in enumerate(sources, 1):
        rows.append(
            {
                "source_id": f"SRC-{i:03d}",
                "title": title,
                "url": url,
                "publisher": title.split(" - ")[0],
                "source_type": "PUBLIC_WEB",
                "access": "PUBLIC",
                "notes": "Pending legal review; captured only as public source reference.",
                "legal_review_status": "PENDING_LEGAL_REVIEW",
            }
        )
    write_csv(p, fields, rows)
    # md
    md = repo / "00_Master_Knowledge_Base" / "SOURCE_REGISTRY.md"
    lines = [
        "# Source Registry",
        "",
        "| ID | Title | URL | Status |",
        "|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['source_id']} | {r['title']} | {r['url']} | {r['legal_review_status']} |"
        )
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def ensure_valuation(repo: Path):
    p = repo / "00_Master_Knowledge_Base" / "VALUATION_WORKSHEET.csv"
    fields = [
        "vector_id",
        "category",
        "claim_summary",
        "low_usd",
        "base_usd",
        "high_usd",
        "currency",
        "valuation_status",
        "review_status",
        "evidence_mapping_status",
        "notes",
    ]
    _, existing = read_csv(p)
    by_id = {r.get("vector_id"): r for r in existing if r.get("vector_id")}
    rows = []
    for i in range(1, 3001):
        vid = f"V-{i:04d}"
        er = by_id.get(vid, {})
        rows.append(
            {
                "vector_id": vid,
                "category": er.get("category", "GENERAL"),
                "claim_summary": er.get(
                    "claim_summary", "TBD - pending legal/evidentiary review"
                ),
                "low_usd": "TBD",
                "base_usd": "TBD",
                "high_usd": "TBD",
                "currency": "USD",
                "valuation_status": "TBD",
                "review_status": "PENDING_LEGAL_REVIEW",
                "evidence_mapping_status": er.get(
                    "evidence_mapping_status", "AUTO_CANDIDATE_PENDING_REVIEW"
                ),
                "notes": er.get(
                    "notes",
                    "No published valuation amount; pending cited workbook and human review.",
                ),
            }
        )
    write_csv(p, fields, rows)
    meth = repo / "00_Master_Knowledge_Base" / "VALUATION_METHODOLOGY_PILOT.md"
    if not meth.exists():
        meth.write_text(
            "# Valuation Methodology (Pilot)\n\nStatus: PENDING_LEGAL_REVIEW\n\nAll valuation figures are `TBD (valuation pending)`. No published amounts without versioned cited workbook and human review.\n",
            encoding="utf-8",
        )


def ensure_vectors(repo: Path):
    p = repo / "99_Archives_and_Manifests" / "claim_vector_registry_3000.json"
    obj = None
    if p.exists():
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            obj = None
    vecs = []
    if isinstance(obj, list):
        vecs = obj
    elif isinstance(obj, dict):
        for k in ["vectors", "claims", "items", "registry"]:
            if isinstance(obj.get(k), list):
                vecs = obj[k]
                break
    by_id = {}
    for v in vecs:
        if isinstance(v, dict):
            vid = v.get("vector_id") or v.get("id")
            if vid:
                by_id[str(vid)] = v
    out = []
    for i in range(1, 3001):
        vid = f"V-{i:04d}"
        v = dict(by_id.get(vid, {}))
        v["vector_id"] = vid
        v["valuation_status"] = "TBD"
        v["review_status"] = "PENDING_LEGAL_REVIEW"
        v["evidence_mapping_status"] = v.get(
            "evidence_mapping_status", "AUTO_CANDIDATE_PENDING_REVIEW"
        )
        v.setdefault("claim_summary", "TBD - pending legal/evidentiary review")
        out.append(v)
    ensure_dir(p.parent)
    p.write_text(
        json.dumps(
            {"version": 1, "status": "PENDING_LEGAL_REVIEW", "vectors": out},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def fetch_url(url: str, timeout=25):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; GRA-EvidenceHarvest/1.0; +public-records)"
        },
    )
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        data = resp.read()
        ct = resp.headers.get("Content-Type", "")
        status = getattr(resp, "status", 200)
        final = resp.geturl()
        return status, ct, final, data


def harvest(repo: Path, sources):
    led = repo / "03_Evidentiary_Exhibits" / "Immutable_Ledger"
    ensure_dir(led)
    logp = led / "HARVEST_INTAKE_LOG.csv"
    fields, rows = read_csv(logp)
    for f in [
        "timestamp_utc",
        "url",
        "final_url",
        "status",
        "content_type",
        "bytes",
        "sha256",
        "saved_path",
        "note",
        "provenance",
        "capture_access",
        "legal_review_status",
    ]:
        if f not in fields:
            fields.append(f)
    existing_urls = {(r.get("url"), r.get("status")) for r in rows}
    for title, url in sources:
        # skip if we already have any OK meta for this url
        have = False
        for mp in led.glob("*.meta.json"):
            try:
                m = json.loads(mp.read_text(encoding="utf-8", errors="ignore"))
                if m.get("url") == url and m.get("sha256"):
                    have = True
                    break
            except Exception:
                pass
        if have:
            continue
        ts = datetime.datetime.utcnow().isoformat() + "Z"
        try:
            status, ct, final, data = fetch_url(url)
            safe = re.sub(r"[^A-Za-z0-9._-]+", "_", title).strip("_")[:80] or "capture"
            ext = (
                ".html"
                if "html" in ct.lower() or data[:200].lower().find(b"<html") >= 0
                else ".bin"
            )
            art = led / f"{safe}{ext}"
            if art.exists():
                art = (
                    led / f"{safe}_{hashlib.sha256(url.encode()).hexdigest()[:8]}{ext}"
                )
            art.write_bytes(data)
            sha = hashlib.sha256(data).hexdigest()
            meta = {
                "url": url,
                "final_url": final,
                "title": title,
                "fetched_at": ts,
                "http_status": status,
                "content_type": ct,
                "bytes": len(data),
                "sha256": sha,
                "provenance": "direct-http-fetch",
                "custodian": "GRA-evidence-harvester",
                "capture_access": "PUBLIC_CAPTURE_UNAUTHENTICATED",
                "legal_review_status": "PENDING_LEGAL_REVIEW",
                "note": "Direct harvest capture; pending legal review/authentication.",
            }
            low = data.lower()
            if len(data) < 800 or b"captcha" in low or b"access denied" in low:
                meta["substantive"] = False
                meta["quality_flag"] = "NOT_SUBSTANTIVE_CHALLENGE_PENDING_RECAPTURE"
                meta["annotation_note"] = (
                    "Possible challenge/empty capture; pending recapture."
                )
            art.with_name(art.name + ".meta.json").write_text(
                json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            rows.append(
                {
                    "timestamp_utc": ts,
                    "url": url,
                    "final_url": final,
                    "status": status,
                    "content_type": ct,
                    "bytes": len(data),
                    "sha256": sha,
                    "saved_path": art.relative_to(repo).as_posix(),
                    "note": "direct harvest",
                    "provenance": "direct-http-fetch",
                    "capture_access": "PUBLIC_CAPTURE_UNAUTHENTICATED",
                    "legal_review_status": "PENDING_LEGAL_REVIEW",
                }
            )
            print("OK", repo.name, title, status)
        except Exception as e:
            rows.append(
                {
                    "timestamp_utc": ts,
                    "url": url,
                    "final_url": url,
                    "status": "ERROR",
                    "content_type": "",
                    "bytes": "",
                    "sha256": "",
                    "saved_path": "",
                    "note": str(e)[:300],
                    "provenance": "direct-http-fetch",
                    "capture_access": "PUBLIC_CAPTURE_UNAUTHENTICATED",
                    "legal_review_status": "PENDING_LEGAL_REVIEW",
                }
            )
            print("FAIL", repo.name, title, str(e)[:120])
    write_csv(logp, fields, rows)


def build_citation_indexes(repo: Path):
    led = repo / "03_Evidentiary_Exhibits" / "Immutable_Ledger"
    rows = []
    if led.exists():
        for mp in sorted(led.glob("*.meta.json")):
            try:
                meta = json.loads(mp.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                continue
            art = mp.with_name(mp.name[: -len(".meta.json")])
            rel = (
                art.relative_to(repo).as_posix()
                if art.exists()
                else mp.relative_to(repo).as_posix()
            )
            sha = meta.get("sha256") or (
                sha256_file(art) if art.exists() and art.is_file() else ""
            )
            vstatus = str(meta.get("verification_status") or "PENDING_LEGAL_REVIEW")
            if vstatus.upper() == "VERIFIED" and not meta.get("human_signoff"):
                vstatus = "PENDING_LEGAL_REVIEW"
            rows.append(
                {
                    "citation_id": hashlib.sha256(
                        (str(meta.get("url", "")) + "|" + rel).encode()
                    ).hexdigest()[:16],
                    "title": meta.get("title", art.stem),
                    "url": meta.get("url", ""),
                    "final_url": meta.get("final_url", meta.get("url", "")),
                    "local_path": rel,
                    "local_artifact": rel,
                    "sha256": sha,
                    "http_status": meta.get("http_status", ""),
                    "content_type": meta.get("content_type", ""),
                    "fetched_at": meta.get("fetched_at", ""),
                    "provenance": meta.get("provenance", ""),
                    "capture_access": meta.get("capture_access", ""),
                    "legal_review_status": meta.get(
                        "legal_review_status", "PENDING_LEGAL_REVIEW"
                    ),
                    "verification_status": vstatus,
                    "verification_rule": meta.get(
                        "verification_rule", "NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT"
                    ),
                    "substantive": meta.get("substantive", ""),
                    "quality_flag": meta.get("quality_flag", ""),
                    "annotation_note": meta.get("annotation_note", ""),
                }
            )
    fields = [
        "citation_id",
        "title",
        "url",
        "final_url",
        "local_path",
        "local_artifact",
        "sha256",
        "http_status",
        "content_type",
        "fetched_at",
        "provenance",
        "capture_access",
        "legal_review_status",
        "verification_status",
        "verification_rule",
        "substantive",
        "quality_flag",
        "annotation_note",
    ]
    for out_dir in [
        repo / "99_Archives_and_Manifests",
        repo / "03_Evidentiary_Exhibits",
    ]:
        write_csv(out_dir / "CITATION_INDEX.csv", fields, rows)
        lines = [
            "# Citation Index",
            "",
            "| Citation ID | Title | URL | Local Path | SHA256 | Status | Substantive | Quality Flag | Legal Review | Verification |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
        for r in rows:
            lines.append(
                f"| {r['citation_id']} | {r.get('title', '')} | {r.get('url', '')} | {r.get('local_path', '')} | {r.get('sha256', '')} | {r.get('http_status', '')} | {r.get('substantive', '')} | {r.get('quality_flag', '')} | {r.get('legal_review_status', '')} | {r.get('verification_status', '')} |"
            )
        (out_dir / "CITATION_INDEX.md").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )
    # pending recapture register
    pr_rows = []
    for r in rows:
        qf = str(r.get("quality_flag") or "")
        sub = str(r.get("substantive")).lower()
        if (
            sub == "false"
            or qf.startswith("NOT_SUBSTANTIVE")
            or qf.startswith("NO_CAPTURE")
        ):
            pr_rows.append(
                {
                    "citation_id": r.get("citation_id", ""),
                    "url": r.get("url", ""),
                    "title": r.get("title", ""),
                    "status": "PENDING_RECAPTURE",
                    "reason": qf or "NOT_SUBSTANTIVE_PENDING_RECAPTURE",
                    "recorded_at": r.get("fetched_at", ""),
                    "repo": repo.name,
                    "local_artifact": r.get("local_artifact", ""),
                    "annotation_note": r.get("annotation_note", ""),
                }
            )
    pr_fields = [
        "citation_id",
        "url",
        "title",
        "status",
        "reason",
        "recorded_at",
        "repo",
        "local_artifact",
        "annotation_note",
    ]
    write_csv(
        repo / "99_Archives_and_Manifests" / "PENDING_RECAPTURE_REGISTER.csv",
        pr_fields,
        pr_rows,
    )


def refresh_manifest(repo: Path):
    manifests = repo / "99_Archives_and_Manifests"
    ensure_dir(manifests)
    mcsv = manifests / "MANIFEST_SHA256.csv"
    entries = []
    for p in sorted(repo.rglob("*")):
        if p.is_dir():
            continue
        rel = p.relative_to(repo).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel == "99_Archives_and_Manifests/MANIFEST_SHA256.csv":
            continue
        if rel == "VERIFICATION_KEYS/sha256_manifest.txt":
            continue
        try:
            st = p.stat()
        except Exception:
            continue
        entries.append(
            {
                "path": rel,
                "bytes": st.st_size,
                "sha256": sha256_file(p),
                "mtime_utc": datetime.datetime.utcfromtimestamp(st.st_mtime).isoformat()
                + "Z",
            }
        )
    vk = repo / "VERIFICATION_KEYS" / "sha256_manifest.txt"
    if vk.exists() or True:
        ensure_dir(vk.parent)
        vk.write_text(
            "\n".join(f"{e['sha256']}  {e['path']}" for e in entries) + "\n",
            encoding="utf-8",
        )
        st = vk.stat()
        entries.append(
            {
                "path": "VERIFICATION_KEYS/sha256_manifest.txt",
                "bytes": st.st_size,
                "sha256": sha256_file(vk),
                "mtime_utc": datetime.datetime.utcfromtimestamp(st.st_mtime).isoformat()
                + "Z",
            }
        )
    entries.sort(key=lambda e: e["path"])
    write_csv(mcsv, ["path", "bytes", "sha256", "mtime_utc"], entries)


def main():
    for name, sources in REPOS.items():
        repo = BASE / REGION / name
        if not repo.exists():
            print("MISSING", repo)
            continue
        ensure_source_registry(repo, sources)
        ensure_valuation(repo)
        ensure_vectors(repo)
        harvest(repo, sources)
        build_citation_indexes(repo)
        refresh_manifest(repo)
        print("DONE", name)


if __name__ == "__main__":
    main()
