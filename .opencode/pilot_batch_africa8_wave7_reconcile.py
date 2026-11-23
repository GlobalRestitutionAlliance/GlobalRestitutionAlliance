#!/usr/bin/env python3
"""Reconcile Africa Wave 7 browser captures/no-captures into repo manifests/indexes."""
from __future__ import annotations
import csv, json, hashlib, datetime
from pathlib import Path
import importlib.util

BASE = Path(r"W:\Legal")
W7 = BASE / ".opencode" / "pilot_batch_africa8_wave7.py"
NC_PATH = BASE / ".opencode" / "tmp_w7_nocapture.json"

spec = importlib.util.spec_from_file_location("w7", str(W7))
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
        return list(r.fieldnames or []), rows


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
    if (
        meta.get("provenance") == "browser-rendered-outerHTML"
        or meta.get("http_status") == "unknown_browser_outerhtml_capture"
    ):
        if meta.get("capture_access") != "PUBLIC_CAPTURE_UNAUTHENTICATED":
            meta["capture_access"] = "PUBLIC_CAPTURE_UNAUTHENTICATED"; changed = True
        if meta.get("legal_review_status") != "PENDING_LEGAL_REVIEW":
            meta["legal_review_status"] = "PENDING_LEGAL_REVIEW"; changed = True
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
    if changed:
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return meta


def build_citation_rows(repo: Path):
    led = repo / "03_Evidentiary_Exhibits" / "Immutable_Ledger"
    rows = []
    if led.exists():
        for mp in sorted(led.glob("*.meta.json")):
            meta = normalize_meta(mp)
            if not meta:
                continue
            art = mp.with_name(mp.name[:-len(".meta.json")])
            if not art.exists():
                candidates = [c for c in led.glob(mp.stem.replace(".meta", "") + "*") if not c.name.endswith('.meta.json')]
                art = candidates[0] if candidates else mp
            rel = art.relative_to(repo).as_posix() if art.exists() else mp.relative_to(repo).as_posix()
            sha = meta.get("sha256") or (sha256_file(art) if art.exists() and art.is_file() else "")
            rows.append({
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
                "legal_review_status": meta.get("legal_review_status", "PENDING_LEGAL_REVIEW"),
                "substantive": meta.get("substantive"),
                "quality_flag": meta.get("quality_flag", ""),
                "annotation_note": meta.get("annotation_note", ""),
            })
    for nc in nc_by_repo.get(repo.name, []):
        rows.append({
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
            "annotation_note": f"No-capture: {nc.get('error','')[:300]}",
        })
    seen = set(); dedup=[]
    for r in rows:
        k=(r.get("url"),r.get("local_path"),r.get("quality_flag"),r.get("http_status"))
        if k in seen: continue
        seen.add(k); dedup.append(r)
    return dedup


def write_citation_indexes(repo: Path, rows):
    fields=["title","url","final_url","local_path","sha256","http_status","content_type","fetched_at","provenance","capture_access","legal_review_status","substantive","quality_flag","annotation_note"]
    for out_dir in [repo/"99_Archives_and_Manifests", repo/"03_Evidentiary_Exhibits"]:
        out_dir.mkdir(parents=True, exist_ok=True)
        write_csv(out_dir/"CITATION_INDEX.csv", fields, rows)
        lines=["# Citation Index","","| Title | URL | Local Path | SHA256 | Status | Substantive | Quality Flag | Legal Review |","|---|---|---|---|---|---|---|---|"]
        for r in rows:
            lines.append(f"| {r.get('title','')} | {r.get('url','')} | {r.get('local_path','')} | {r.get('sha256','')} | {r.get('http_status','')} | {r.get('substantive','')} | {r.get('quality_flag','')} | {r.get('legal_review_status','')} |")
        (out_dir/"CITATION_INDEX.md").write_text("\n".join(lines)+"\n", encoding="utf-8")


def update_pending_recapture(repo: Path, rows):
    p = repo/"99_Archives_and_Manifests"/"PENDING_RECAPTURE_REGISTER.csv"
    fields, existing = read_csv(p)
    if not fields:
        fields=["url","title","status","reason","recorded_at","repo","annotation_note"]
    if "annotation_note" not in fields: fields.append("annotation_note")
    by_url={r.get("url"):r for r in existing if r.get("url")}
    for r in rows:
        qf=str(r.get("quality_flag") or ""); sub=r.get("substantive")
        if not ((sub is False) or qf.startswith("NOT_SUBSTANTIVE") or qf.startswith("NO_CAPTURE")):
            continue
        url=r.get("url","")
        if not url: continue
        rec=dict(by_url.get(url,{}))
        rec.update({
            "url":url,"title":r.get("title",""),"status":"PENDING_RECAPTURE",
            "reason":qf or "NOT_SUBSTANTIVE_PENDING_RECAPTURE",
            "recorded_at": rec.get("recorded_at") or r.get("fetched_at") or datetime.datetime.utcnow().isoformat()+"Z",
            "repo":repo.name,"annotation_note":r.get("annotation_note","")
        })
        by_url[url]=rec
    write_csv(p, fields, list(by_url.values()))


def append_intake_log(repo: Path, rows):
    led = repo/"03_Evidentiary_Exhibits"/"Immutable_Ledger"
    led.mkdir(parents=True, exist_ok=True)
    p = led/"HARVEST_INTAKE_LOG.csv"
    fields, existing = read_csv(p)
    if not fields:
        fields=["timestamp_utc","url","final_url","status","content_type","bytes","sha256","saved_path","note"]
    seen={(r.get("url"),r.get("saved_path"),str(r.get("status"))) for r in existing}
    now=datetime.datetime.utcnow().isoformat()+"Z"
    for r in rows:
        key=(r.get("url"),r.get("local_path"),str(r.get("http_status")))
        if key in seen: continue
        existing.append({
            "timestamp_utc": r.get("fetched_at") or now,
            "url": r.get("url",""),"final_url": r.get("final_url",r.get("url","")),
            "status": r.get("http_status",""),"content_type": r.get("content_type",""),
            "bytes":"", "sha256": r.get("sha256",""), "saved_path": r.get("local_path",""),
            "note": r.get("quality_flag") or r.get("annotation_note") or "Wave 7 reconciliation"
        })
        seen.add(key)
    write_csv(p, fields, existing)


def refresh_manifest(repo: Path):
    manifests = repo/"99_Archives_and_Manifests"
    manifests.mkdir(parents=True, exist_ok=True)
    entries=[]
    for p in sorted(repo.rglob("*")):
        if p.is_dir(): continue
        rel=p.relative_to(repo).as_posix()
        if rel.startswith(".git/"): continue
        try: st=p.stat()
        except Exception: continue
        entries.append({
            "path":rel,"bytes":st.st_size,"sha256":sha256_file(p),
            "mtime_utc":datetime.datetime.utcfromtimestamp(st.st_mtime).isoformat()+"Z"
        })
    write_csv(manifests/"MANIFEST_SHA256.csv", ["path","bytes","sha256","mtime_utc"], entries)


def main():
    summary=[]
    for rp in REPOS:
        repo=Path(rp)
        if not repo.exists():
            summary.append((repo.name,"MISSING")); continue
        rows=build_citation_rows(repo)
        write_citation_indexes(repo, rows)
        update_pending_recapture(repo, rows)
        append_intake_log(repo, rows)
        refresh_manifest(repo)
        summary.append((repo.name,len(rows)))
    for n,c in summary: print(f"{n}: {c}")
    print(f"NO_CAPTURE_ENTRIES: {len(ncs)}")

if __name__ == "__main__":
    main()
