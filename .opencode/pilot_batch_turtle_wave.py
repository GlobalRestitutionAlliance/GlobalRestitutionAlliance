#!/usr/bin/env python3
"""TURTLE full-enrichment wave over explicit repo paths."""

from __future__ import annotations
import importlib.util, sys, csv, json, hashlib
from pathlib import Path

BASE = Path(r"W:\Legal")
spec = importlib.util.spec_from_file_location(
    "asiaw", str(BASE / ".opencode" / "pilot_batch_asia8_wave1.py")
)
asia = importlib.util.module_from_spec(spec)
spec.loader.exec_module(asia)
spec2 = importlib.util.spec_from_file_location(
    "recon", str(BASE / ".opencode" / "pilot_batch_asia8_reconcile.py")
)
recon = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(recon)


def load_json(p):
    try:
        return json.loads(p.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return None


def default_sources(name):
    # generic authoritative sources; repo-specific curation can be added later
    short = name.replace("US_", "").replace("_", " ")
    return [
        (
            f"Library of Congress - {short}",
            f"https://www.loc.gov/search/?q={short.replace(' ', '+')}",
        ),
        (f"DOI - Tribal Affairs", "https://www.bia.gov/"),
        (
            f"Federal Register - {short}",
            f"https://www.federalregister.gov/documents/search?conditions%5Bterm%5D={short.replace(' ', '+')}",
        ),
        (
            f"NARA - {short}",
            f"https://catalog.archives.gov/search?q={short.replace(' ', '%20')}",
        ),
        (
            f"US Code - Indian Affairs",
            "https://uscode.house.gov/browse/prelim@title25&edition=prelim",
        ),
        (
            f"GovInfo - {short}",
            f"https://www.govinfo.gov/app/search/%7B%22query%22%3A%22{short.replace(' ', '%20')}%22%7D",
        ),
        (f"DOJ - Indian Country", "https://www.justice.gov/otj"),
        (
            f"Indian Claims Commission",
            "https://library.cqpress.com/cqresearcher/document.php?id=cqresrre1949101900",
        ),
        (
            f"Census - Tribal",
            "https://www.census.gov/topics/population/american-indian-alaska-native.html",
        ),
        (f"HRW - Indigenous Rights", "https://www.hrw.org/topic/indigenous-peoples"),
    ]


def postprocess(repo):
    asia.ensure_vectors(repo)
    logp = repo / "03_Evidentiary_Exhibits/Immutable_Ledger/HARVEST_INTAKE_LOG.csv"
    if not logp.exists():
        return 0
    with logp.open(encoding="utf-8", errors="ignore", newline="") as f:
        rows = list(csv.DictReader(f))
    ok_urls = set()
    led = repo / "03_Evidentiary_Exhibits/Immutable_Ledger"
    for mp in led.glob("*.meta.json"):
        m = load_json(mp)
        if not isinstance(m, dict):
            continue
        sha = str(m.get("sha256") or "")
        if sha and str(m.get("http_status", "")) not in ("ERROR", ""):
            ok_urls.add(m.get("url"))
            ok_urls.add(m.get("final_url"))
    nc_rows = []
    seen = set()
    for r in rows:
        url = r.get("url") or r.get("final_url") or ""
        if not url or url in seen:
            continue
        status = str(r.get("status") or "")
        if url in ok_urls:
            continue
        is_fail = status == "ERROR" or status.startswith("4") or status.startswith("5")
        if not is_fail:
            continue
        seen.add(url)
        cid = hashlib.sha256((url + "|NO_CAPTURE").encode("utf-8")).hexdigest()[:16]
        nc_rows.append(
            {
                "citation_id": cid,
                "title": "NO_CAPTURE: " + url[:120],
                "url": url,
                "final_url": r.get("final_url") or url,
                "local_path": "",
                "local_artifact": "",
                "sha256": "",
                "http_status": status if status != "ERROR" else "NO_CAPTURE",
                "content_type": r.get("content_type", ""),
                "fetched_at": r.get("timestamp_utc", ""),
                "provenance": "direct-http-fetch-failed",
                "capture_access": "NO_CAPTURE_PENDING_RECAPTURE",
                "legal_review_status": "PENDING_LEGAL_REVIEW",
                "verification_status": "PENDING_LEGAL_REVIEW",
                "verification_rule": "NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT",
                "substantive": False,
                "quality_flag": "NO_CAPTURE_PENDING_RECAPTURE",
                "annotation_note": f"Harvest failed: {str(r.get('note', ''))[:200]}; pending recapture. No fabricated content.",
            }
        )
    rows_all = recon.build_citation_rows(repo)
    existing_ids = {str(r.get("citation_id") or "") for r in rows_all}
    existing_urls2 = {
        (str(r.get("url") or ""), str(r.get("quality_flag") or "")) for r in rows_all
    }
    for nr in nc_rows:
        k = (nr["url"], nr["quality_flag"])
        if nr["citation_id"] in existing_ids or k in existing_urls2:
            continue
        rows_all.append(nr)
        existing_ids.add(nr["citation_id"])
        existing_urls2.add(k)
    recon.write_citation_indexes(repo, rows_all)
    recon.update_pending_recapture(repo, rows_all)
    recon.append_intake_log(repo, rows_all)
    recon.refresh_manifest(repo)
    return len(nc_rows)


def main():
    paths = sys.argv[1:]
    for p in paths:
        repo = Path(p)
        if not repo.exists():
            print("MISS", p)
            continue
        sources = default_sources(repo.name)
        asia.ensure_source_registry(repo, sources)
        asia.ensure_valuation(repo)
        asia.ensure_vectors(repo)
        asia.harvest(repo, sources)
        asia.build_citation_indexes(repo)
        asia.refresh_manifest(repo)
        nc = postprocess(repo)
        print("DONE", repo.name, "nc", nc)


if __name__ == "__main__":
    main()
