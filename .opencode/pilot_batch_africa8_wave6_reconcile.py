#!/usr/bin/env python3
"""Reconcile Africa Wave 6 browser captures/no-captures into repo manifests/indexes."""

from __future__ import annotations
import csv, json, hashlib, os, datetime, re
from pathlib import Path

BASE = Path(r"W:\Legal")
W6 = BASE / ".opencode" / "pilot_batch_africa8_wave6.py"
NC_PATH = BASE / ".opencode" / "tmp_w6_nocapture.json"

# load repos
import importlib.util

spec = importlib.util.spec_from_file_location("w6", str(W6))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
REPOS = list(m.REPOS.keys())

ncs = json.loads(NC_PATH.read_text(encoding="utf-8")) if NC_PATH.exists() else []
nc_by_repo = {}
for x in ncs:
    nc_by_repo.setdefault(x["repo_key"], []).append(x)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path: Path):
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        rows = list(r)
        return r.fieldnames or [], rows


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)


def normalize_meta(meta_path: Path):
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    changed = False
    # normalize browser outerhtml metas
    if (
        meta.get("provenance") == "browser-rendered-outerHTML"
        or meta.get("http_status") == "unknown_browser_outerhtml_capture"
    ):
        meta.setdefault("capture_access", "PUBLIC_CAPTURE_UNAUTHENTICATED")
        meta.setdefault("legal_review_status", "PENDING_LEGAL_REVIEW")
        # substantive null -> true only when no challenge/quality flag indicates non-substantive
        qf = str(meta.get("quality_flag") or "")
        note = str(meta.get("annotation_note") or "")
        is_nonsub = (
            meta.get("substantive") is False
            or qf.startswith("NOT_SUBSTANTIVE")
            or "Pending recapture" in note
        )
        if meta.get("substantive") is None and not is_nonsub:
            meta["substantive"] = True
            changed = True
        for k, v in [
            ("capture_access", "PUBLIC_CAPTURE_UNAUTHENTICATED"),
            ("legal_review_status", "PENDING_LEGAL_REVIEW"),
        ]:
            if meta.get(k) != v:
                meta[k] = v
                changed = True
    if changed:
        meta_path.write_text(
            json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return meta


def build_citation_index(repo: Path):
    led = repo / "03_Evidentiary_Exhibits" / "Immutable_Ledger"
    manifests = repo / "99_Archives_and_Manifests"
    manifests.mkdir(parents=True, exist_ok=True)
    rows = []
    for mp in sorted(led.glob("*.meta.json")):
        meta = normalize_meta(mp)
        if not meta:
            continue
        art = mp.with_name(mp.name[: -len(".meta.json")])
        if not art.exists():
            # try common artifact names
            candidates = list(led.glob(mp.stem.replace(".meta", "") + "*"))
            art = candidates[0] if candidates else mp
        rel = (
            art.relative_to(repo).as_posix()
            if art.exists()
            else mp.relative_to(repo).as_posix()
        )
        sha = meta.get("sha256") or (
            sha256_file(art) if art.exists() and art.is_file() else ""
        )
        qf = meta.get("quality_flag", "")
        ann = meta.get("annotation_note", "")
        substantive = meta.get("substantive")
        rows.append(
            {
                "title": meta.get("title", art.stem),
                "url": meta.get("url", ""),
                "final_url": meta.get("final_url", meta.get("url", "")),
                "local_path": rel,
                "sha256": sha,
                "http_status": meta.get("http_status", ""),
                "content_type": meta.get("content_type", ""),
                "fetched_at": meta.get("fetched_at", ""),
                "provenance": meta.get("provenance", ""),
                "capture_access": meta.get("capture_access", ""),
                "legal_review_status": meta.get(
                    "legal_review_status", "PENDING_LEGAL_REVIEW"
                ),
                "substantive": substantive,
                "quality_flag": qf,
                "annotation_note": ann,
            }
        )
    # include no-capture entries as index rows without artifact
    rk = None
    for k in nc_by_repo:
        # map by repo name prefix
        pass
    repo_key = repo.name
    for nc in nc_by_repo.get(repo_key, []):
        rows.append(
            {
                "title": nc.get("title", ""),
                "url": nc.get("url", ""),
                "final_url": nc.get("url", ""),
                "local_path": "",
                "sha256": "",
                "http_status": "NO_CAPTURE",
                "content_type": "",
                "fetched_at": nc.get("recorded_at", ""),
                "provenance": "browser-navigation-failed",
                "capture_access": "PUBLIC_CAPTURE_UNAUTHENTICATED",
                "legal_review_status": "PENDING_LEGAL_REVIEW",
                "substantive": False,
                "quality_flag": "NO_CAPTURE_PENDING_RECAPTURE",
                "annotation_note": f"No-capture: {nc.get('error', '')[:300]}",
            }
        )
    # dedupe by url+local_path
    seen = set()
    dedup = []
    for r in rows:
        k = (r.get("url"), r.get("local_path"), r.get("quality_flag"))
        if k in seen:
            continue
        seen.add(k)
        dedup.append(r)
    fields = [
        "title",
        "url",
        "final_url",
        "local_path",
        "sha256",
        "http_status",
        "content_type",
        "fetched_at",
        "provenance",
        "capture_access",
        "legal_review_status",
        "substantive",
        "quality_flag",
        "annotation_note",
    ]
    write_csv(manifests / "CITATION_INDEX.csv", fields, dedup)
    # md
    lines = [
        "# Citation Index",
        "",
        "| Title | URL | Local Path | SHA256 | Status | Substantive | Quality Flag | Legal Review |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in dedup:
        lines.append(
            f"| {r['title']} | {r['url']} | {r['local_path']} | {r['sha256']} | {r['http_status']} | {r['substantive']} | {r['quality_flag']} | {r['legal_review_status']} |"
        )
    (manifests / "CITATION_INDEX.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    return dedup


def update_pending_recapture(repo: Path, citation_rows):
    manifests = repo / "99_Archives_and_Manifests"
    p = manifests / "PENDING_RECAPTURE_REGISTER.csv"
    fields, rows = read_csv(p)
    if not fields:
        fields = ["url", "title", "status", "reason", "recorded_at", "repo"]
    # index existing by url
    by_url = {r.get("url"): r for r in rows if r.get("url")}
    changed = False
    for r in citation_rows:
        qf = str(r.get("quality_flag") or "")
        sub = r.get("substantive")
        is_pending = (
            (sub is False)
            or qf.startswith("NOT_SUBSTANTIVE")
            or qf.startswith("NO_CAPTURE")
        )
        if not is_pending:
            continue
        url = r.get("url", "")
        if not url:
            continue
        rec = by_url.get(url, {})
        rec.update(
            {
                "url": url,
                "title": r.get("title", ""),
                "status": "PENDING_RECAPTURE",
                "reason": qf or "NOT_SUBSTANTIVE_PENDING_RECAPTURE",
                "recorded_at": rec.get("recorded_at")
                or r.get("fetched_at")
                or datetime.datetime.utcnow().isoformat() + "Z",
                "repo": repo.name,
                "annotation_note": r.get("annotation_note", ""),
            }
        )
        by_url[url] = rec
        changed = True
    # ensure annotation_note field
    if "annotation_note" not in fields:
        fields.append("annotation_note")
    if changed or not p.exists():
        write_csv(p, fields, list(by_url.values()))


def refresh_manifest(repo: Path):
    manifests = repo / "99_Archives_and_Manifests"
    manifests.mkdir(parents=True, exist_ok=True)
    entries = []
    for p in sorted(repo.rglob("*")):
        if p.is_dir():
            continue
        rel = p.relative_to(repo).as_posix()
        if rel.startswith(".git/"):
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
    write_csv(
        manifests / "MANIFEST_SHA256.csv",
        ["path", "bytes", "sha256", "mtime_utc"],
        entries,
    )


def append_intake_log(repo: Path, citation_rows):
    led = repo / "03_Evidentiary_Exhibits" / "Immutable_Ledger"
    led.mkdir(parents=True, exist_ok=True)
    p = led / "HARVEST_INTAKE_LOG.csv"
    fields, rows = read_csv(p)
    if not fields:
        fields = [
            "timestamp_utc",
            "url",
            "final_url",
            "status",
            "content_type",
            "bytes",
            "sha256",
            "saved_path",
            "note",
        ]
    existing = {(r.get("url"), r.get("saved_path")) for r in rows}
    now = datetime.datetime.utcnow().isoformat() + "Z"
    for r in citation_rows:
        key = (r.get("url"), r.get("local_path"))
        if key in existing:
            continue
        rows.append(
            {
                "timestamp_utc": r.get("fetched_at") or now,
                "url": r.get("url", ""),
                "final_url": r.get("final_url", r.get("url", "")),
                "status": r.get("http_status", ""),
                "content_type": r.get("content_type", ""),
                "bytes": "",
                "sha256": r.get("sha256", ""),
                "saved_path": r.get("local_path", ""),
                "note": r.get("quality_flag")
                or r.get("annotation_note")
                or "Wave 6 reconciliation",
            }
        )
        existing.add(key)
    write_csv(p, fields, rows)


def main():
    summary = []
    for rp in REPOS:
        repo = Path(rp)
        if not repo.exists():
            summary.append((repo.name, "MISSING_REPO"))
            continue
        citation_rows = build_citation_index(repo)
        update_pending_recapture(repo, citation_rows)
        append_intake_log(repo, citation_rows)
        refresh_manifest(repo)
        summary.append((repo.name, len(citation_rows)))
    for name, n in summary:
        print(f"{name}: {n}")
    print(f"NO_CAPTURE_ENTRIES: {len(ncs)}")


if __name__ == "__main__":
    main()
