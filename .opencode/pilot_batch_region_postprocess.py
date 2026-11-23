#!/usr/bin/env python3
"""Postprocess wave: add NO_CAPTURE rows for failed harvests, reconcile, manifest."""

from __future__ import annotations
import csv, json, hashlib, importlib.util, sys
from pathlib import Path

BASE = Path(r"W:\Legal")
# args: REGION repo1 repo2 ...
REGION = sys.argv[1]
REPOS = sys.argv[2:]

spec = importlib.util.spec_from_file_location(
    "recon", str(BASE / ".opencode" / "pilot_batch_asia8_reconcile.py")
)
recon = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recon)
spec2 = importlib.util.spec_from_file_location(
    "asiaw", str(BASE / ".opencode" / "pilot_batch_asia8_wave1.py")
)
asia = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(asia)


def load_json(p):
    try:
        return json.loads(p.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return None


def main():
    total_nc = 0
    for name in REPOS:
        repo = BASE / REGION / name
        if not repo.exists():
            print("MISS", name)
            continue
        asia.ensure_vectors(repo)
        logp = repo / "03_Evidentiary_Exhibits/Immutable_Ledger/HARVEST_INTAKE_LOG.csv"
        if not logp.exists():
            print("NOLOG", name)
            continue
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
            is_fail = (
                status == "ERROR" or status.startswith("4") or status.startswith("5")
            )
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
            (str(r.get("url") or ""), str(r.get("quality_flag") or ""))
            for r in rows_all
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
        total_nc += len(nc_rows)
        print("OK", name, "nc", len(nc_rows), "total_rows", len(rows_all))
    print("TOTAL_NC", total_nc)


if __name__ == "__main__":
    main()
