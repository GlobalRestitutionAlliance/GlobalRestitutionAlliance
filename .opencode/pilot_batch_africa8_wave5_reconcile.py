import json, csv, datetime, importlib.util, re
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "w5", r"W:\Legal\.opencode\pilot_batch_africa8_wave5.py"
)
w5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w5)

NO_CAPTURE = [
    {
        "repo_key": "US_RW_RWANDA",
        "source_label": "UNESCO Memory of the World",
        "url": "https://www.unesco.org/en/memory-world",
        "attempted_method": "browser-rendered-outerHTML",
        "failure_reason": "NO_CAPTURE_ERR_EMPTY_RESPONSE",
        "notes": "Browser navigation failed with ERR_EMPTY_RESPONSE (-324); no artifact fabricated. Pending recapture.",
    }
]


def now_utc_date():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d")


def normalize_meta(meta_path: Path):
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return None, False
    changed = False
    # normalize substantive null -> true for browser captures that are not flagged non-substantive
    qf = str(meta.get("quality_flag") or "").upper()
    ann = str(meta.get("annotation_note") or "").upper()
    non_sub = False
    if meta.get("substantive") is False:
        non_sub = True
    if any(
        x in qf
        for x in ["NOT_SUBSTANTIVE", "EMPTY", "CHALLENGE", "404", "PENDING_RECAPTURE"]
    ):
        non_sub = True
    if any(x in ann for x in ["NOT SUBSTANTIVE", "CHALLENGE", "EMPTY CAPTURE", "404"]):
        non_sub = True
    prov = str(meta.get("provenance") or "")
    if (
        meta.get("substantive") is None
        and prov.startswith("browser-rendered")
        and not non_sub
    ):
        # if size tiny, mark non-substantive
        try:
            size = int(meta.get("bytes") or 0)
        except Exception:
            size = 0
        if size < 800:
            meta["substantive"] = False
            meta["quality_flag"] = (
                meta.get("quality_flag") or "NOT_SUBSTANTIVE_EMPTY_PENDING_RECAPTURE"
            )
            meta["annotation_note"] = (
                meta.get("annotation_note")
                or "Capture too small/empty; not substantive evidence. Pending recapture."
            )
        else:
            meta["substantive"] = True
        changed = True
    # ensure required flags
    if prov.startswith("browser-rendered"):
        if meta.get("http_status") != "unknown_browser_outerhtml_capture":
            # don't overwrite if already unknown_browser_outerhtml_capture; keep honest
            pass
        if meta.get("capture_access") != "PUBLIC_CAPTURE_UNAUTHENTICATED":
            meta["capture_access"] = "PUBLIC_CAPTURE_UNAUTHENTICATED"
            changed = True
        if meta.get("provenance") != "browser-rendered-outerHTML":
            meta["provenance"] = "browser-rendered-outerHTML"
            changed = True
    if meta.get("legal_review_status") != "PENDING_LEGAL_REVIEW":
        # keep PENDING_LEGAL_REVIEW as default
        if not meta.get("legal_review_status"):
            meta["legal_review_status"] = "PENDING_LEGAL_REVIEW"
            changed = True
    if changed:
        meta_path.write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return meta, changed


def build_pending_register(repo: Path, repo_key: str):
    ledger = repo / "03_Evidentiary_Exhibits" / "Immutable_Ledger"
    reg_path = repo / "99_Archives_and_Manifests" / "PENDING_RECAPTURE_REGISTER.csv"
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    seen = set()
    if ledger.exists():
        for mp in sorted(ledger.glob("*.meta.json")):
            meta, _ = normalize_meta(mp)
            if not meta:
                continue
            qf = str(meta.get("quality_flag") or "").upper()
            non_sub = meta.get("substantive") is False or any(
                x in qf
                for x in [
                    "NOT_SUBSTANTIVE",
                    "EMPTY",
                    "CHALLENGE",
                    "404",
                    "PENDING_RECAPTURE",
                ]
            )
            if not non_sub:
                continue
            url = meta.get("url") or meta.get("final_url") or ""
            key = (url, qf)
            if key in seen:
                continue
            seen.add(key)
            rows.append(
                {
                    "repo": repo_key,
                    "source_label": meta.get("title") or mp.name,
                    "url": url,
                    "attempted_method": "browser-rendered-outerHTML"
                    if str(meta.get("provenance", "")).startswith("browser-rendered")
                    else "direct-capture",
                    "failure_reason": str(
                        meta.get("quality_flag") or "NOT_SUBSTANTIVE_PENDING_RECAPTURE"
                    ),
                    "first_attempt_utc": str(meta.get("fetched_at") or "")[:10]
                    or now_utc_date(),
                    "last_attempt_utc": now_utc_date(),
                    "status": "PENDING_RECAPTURE",
                    "owner": "UNASSIGNED",
                    "next_action": "Retry browser/direct capture; if blocked, manual/FOIA/custodian path; do not fabricate.",
                    "notes": str(
                        meta.get("annotation_note")
                        or "Pending recapture; not substantive."
                    ),
                }
            )
    # add no-capture entries
    for nc in NO_CAPTURE:
        if nc["repo_key"] != repo_key:
            continue
        key = (nc["url"], nc["failure_reason"])
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            {
                "repo": repo_key,
                "source_label": nc["source_label"],
                "url": nc["url"],
                "attempted_method": nc["attempted_method"],
                "failure_reason": nc["failure_reason"],
                "first_attempt_utc": now_utc_date(),
                "last_attempt_utc": now_utc_date(),
                "status": "PENDING_RECAPTURE",
                "owner": "UNASSIGNED",
                "next_action": "Retry browser/direct capture; if blocked, manual/FOIA/custodian path; do not fabricate.",
                "notes": nc["notes"],
            }
        )
    fields = [
        "repo",
        "source_label",
        "url",
        "attempted_method",
        "failure_reason",
        "first_attempt_utc",
        "last_attempt_utc",
        "status",
        "owner",
        "next_action",
        "notes",
    ]
    with reg_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return len(rows)


def refresh_manifest(repo: Path):
    # reuse w5.refresh_manifest if present
    if hasattr(w5, "refresh_manifest"):
        return w5.refresh_manifest(repo)
    man = repo / "99_Archives_and_Manifests"
    man.mkdir(parents=True, exist_ok=True)
    return None


def rebuild_citations(repo: Path):
    if hasattr(w5, "rebuild_citations"):
        return w5.rebuild_citations(repo)
    return []


def update_intake(repo: Path, pending_count: int, capture_count: int):
    ex = repo / "03_Evidentiary_Exhibits"
    ex.mkdir(parents=True, exist_ok=True)
    p = ex / "EVIDENCE_INTAKE_LOG.md"
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    line = f"\n- {ts} Wave 5 reconciliation: captures_meta={capture_count}, pending_recapture={pending_count}; all statuses PENDING_LEGAL_REVIEW; no VERIFIED without local hashed artifact + human sign-off.\n"
    if p.exists():
        txt = p.read_text(encoding="utf-8", errors="ignore")
        if "Wave 5 reconciliation" not in txt:
            p.write_text(txt.rstrip() + line, encoding="utf-8")
    else:
        p.write_text("# Evidence Intake Log\n" + line, encoding="utf-8")


def main():
    summary = []
    for rp, cfg in w5.REPOS.items():
        repo = Path(rp)
        repo_key = repo.name
        # normalize all metas
        ledger = repo / "03_Evidentiary_Exhibits" / "Immutable_Ledger"
        cap_count = 0
        if ledger.exists():
            for mp in ledger.glob("*.meta.json"):
                normalize_meta(mp)
                cap_count += 1
        pending = build_pending_register(repo, repo_key)
        rebuild_citations(repo)
        refresh_manifest(repo)
        update_intake(repo, pending, cap_count)
        summary.append(
            {"repo": repo_key, "captures_meta": cap_count, "pending_recapture": pending}
        )
    out = Path(r"W:\Legal\.opencode\tmp_w5_reconcile_summary.json")
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    for s in summary:
        print(s)


if __name__ == "__main__":
    main()
