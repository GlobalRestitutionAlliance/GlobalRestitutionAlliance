#!/usr/bin/env python3
"""Reconcile LATAM 8-repo browser captures/no-captures into repo manifests/indexes."""
from __future__ import annotations
import csv, json, hashlib, datetime, os
from pathlib import Path
import importlib.util

BASE = Path(r"W:\Legal")
W1 = BASE / ".opencode" / "pilot_batch_latam8_wave1.py"
NC_PATH = BASE / ".opencode" / "tmp_l1_nocapture.json"

spec = importlib.util.spec_from_file_location("l1", str(W1))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
REPOS = [str(BASE / "LATIN_AMERICA" / k) if not os.path.isabs(k) else k for k in m.REPOS.keys()]

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
    # alias normalization
    if not meta.get("http_status") and meta.get("status") is not None:
        meta["http_status"] = meta.get("status"); changed = True
    if not meta.get("fetched_at") and meta.get("captured_at"):
        meta["fetched_at"] = meta.get("captured_at"); changed = True
    prov = str(meta.get("provenance") or "")
    is_browser = prov == "browser-rendered-outerHTML" or prov.startswith("browser-rendered outerHTML") or str(meta.get("http_status")) == "unknown_browser_outerhtml_capture"
    if is_browser:
        if "browser-rendered" not in str(meta.get("provenance") or ""):
            meta["provenance"] = "browser-rendered-outerHTML"; changed = True
        if meta.get("capture_access") != "PUBLIC_CAPTURE_UNAUTHENTICATED":
            meta["capture_access"] = "PUBLIC_CAPTURE_UNAUTHENTICATED"; changed = True
        if meta.get("legal_review_status") != "PENDING_LEGAL_REVIEW":
            meta["legal_review_status"] = "PENDING_LEGAL_REVIEW"; changed = True
    # derive bytes
    b = meta.get("bytes")
    try: b_int = int(b) if b is not None and str(b).strip() != "" else None
    except Exception: b_int = None
    sha = str(meta.get("sha256") or "")
    empty_sha = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    headers = meta.get("headers") or {}
    hdr_text = json.dumps(headers).lower() if isinstance(headers, dict) else str(headers).lower()
    challenge = any(x in hdr_text for x in ["x-amzn-waf-action", "cf-chl", "challenge"])
    qf = str(meta.get("quality_flag") or "")
    note = str(meta.get("annotation_note") or "")
    looks_nonsub = qf.startswith("NOT_SUBSTANTIVE") or qf.startswith("NO_CAPTURE") or "Pending recapture" in note or "pending recapture" in note.lower()
    if b_int == 0 or sha == empty_sha or challenge:
        looks_nonsub = True
        if not qf.startswith("NO_CAPTURE"):
            meta["quality_flag"] = "NOT_SUBSTANTIVE_CHALLENGE_PENDING_RECAPTURE" if challenge else "NOT_SUBSTANTIVE_EMPTY_PENDING_RECAPTURE"; changed = True
            qf = meta["quality_flag"]
        if not note:
            meta["annotation_note"] = "Empty/challenge capture detected; not substantive evidence. Pending recapture."; changed = True
    if looks_nonsub:
        if meta.get("substantive") is not False:
            meta["substantive"] = False; changed = True
        if meta.get("legal_review_status") != "PENDING_LEGAL_REVIEW":
            meta["legal_review_status"] = "PENDING_LEGAL_REVIEW"; changed = True
    # normal artifact-backed capture: make substantive explicit
    if not looks_nonsub and sha and sha != empty_sha:
        if meta.get("substantive") is None or meta.get("substantive") == "":
            meta["substantive"] = True; changed = True
        if not str(meta.get("quality_flag") or "").strip():
            meta["quality_flag"] = "SUBSTANTIVE_CAPTURE_PENDING_REVIEW"; changed = True
        if not str(meta.get("capture_access") or "").strip():
            meta["capture_access"] = "PUBLIC_CAPTURE_UNAUTHENTICATED"; changed = True
    if str(meta.get("legal_review_status","")).upper() == "VERIFIED" and not meta.get("human_signoff"):
        meta["legal_review_status"] = "PENDING_LEGAL_REVIEW"; changed = True
    if changed:
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return meta


def load_existing_citation_ids(repo: Path):
    by_artifact={}; by_key={}
    for p in [repo/"99_Archives_and_Manifests"/"CITATION_INDEX.csv", repo/"03_Evidentiary_Exhibits"/"CITATION_INDEX.csv"]:
        _, rows = read_csv(p)
        for r in rows:
            cid=str(r.get("citation_id","") or "").strip()
            if not cid: continue
            art=str(r.get("local_artifact","") or r.get("local_path","") or "").strip()
            url=str(r.get("url","") or "").strip()
            qf=str(r.get("quality_flag","") or "").strip()
            st=str(r.get("http_status","") or "").strip()
            if art: by_artifact.setdefault(art,cid)
            by_key.setdefault((url,art,qf,st),cid)
            if art=="" or st=="NO_CAPTURE" or qf.startswith("NO_CAPTURE"):
                by_key.setdefault((url,"","NO_CAPTURE_PENDING_RECAPTURE","NO_CAPTURE"),cid)
    return by_artifact, by_key


def build_citation_rows(repo: Path):
    led = repo / "03_Evidentiary_Exhibits" / "Immutable_Ledger"
    by_artifact, by_key = load_existing_citation_ids(repo)
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
            qf=str(meta.get("quality_flag","") or "")
            status=str(meta.get("http_status","") or "")
            cid = by_artifact.get(rel) or by_key.get((str(meta.get("url","") or ""), rel, qf, status)) or hashlib.sha256((str(meta.get("url",""))+"|"+rel).encode("utf-8")).hexdigest()[:16]
            vstatus = str(meta.get("verification_status","") or "PENDING_LEGAL_REVIEW")
            if vstatus.upper()=="VERIFIED" and not meta.get("human_signoff"):
                vstatus = "PENDING_LEGAL_REVIEW"
            prov=str(meta.get("provenance","") or "")
            if not prov and sha:
                prov="browser-rendered-outerHTML" if str(status)=="unknown_browser_outerhtml_capture" else "direct-http-fetch"
            cap_acc=str(meta.get("capture_access","") or "") or ("PUBLIC_CAPTURE_UNAUTHENTICATED" if sha else "")
            subval=meta.get("substantive")
            if subval is None or str(subval).strip()=="":
                if qf.startswith("NO_CAPTURE") or qf.startswith("NOT_SUBSTANTIVE"):
                    subval=False
                elif sha:
                    subval=True
            if sha and not str(qf).strip() and subval is True:
                qf="SUBSTANTIVE_CAPTURE_PENDING_REVIEW"
            rows.append({
                "citation_id": cid,
                "title": meta.get("title", art.stem),
                "url": meta.get("url", ""),
                "final_url": meta.get("final_url", meta.get("url", "")),
                "local_path": rel,
                "local_artifact": rel,
                "sha256": sha,
                "http_status": status,
                "content_type": meta.get("content_type", ""),
                "fetched_at": meta.get("fetched_at", ""),
                "provenance": prov,
                "capture_access": cap_acc,
                "legal_review_status": meta.get("legal_review_status", "PENDING_LEGAL_REVIEW"),
                "verification_status": vstatus,
                "verification_rule": str(meta.get("verification_rule","") or "NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT"),
                "substantive": subval,
                "quality_flag": qf,
                "annotation_note": meta.get("annotation_note", ""),
            })
    for nc in nc_by_repo.get(repo.name, []):
        url = nc.get("url","")
        qf="NO_CAPTURE_PENDING_RECAPTURE"; status="NO_CAPTURE"
        cid = by_key.get((url,"",qf,status)) or by_key.get((url,"","NO_CAPTURE_PENDING_RECAPTURE","NO_CAPTURE")) or hashlib.sha256((url+"|NO_CAPTURE|"+str(nc.get('title',''))).encode("utf-8")).hexdigest()[:16]
        rows.append({
            "citation_id": cid,
            "title": nc.get("title", ""),
            "url": url,
            "final_url": url,
            "local_path": "",
            "local_artifact": "",
            "sha256": "",
            "http_status": status,
            "content_type": "",
            "fetched_at": nc.get("recorded_at", ""),
            "provenance": "browser-navigation-failed",
            "capture_access": "PUBLIC_CAPTURE_UNAUTHENTICATED",
            "legal_review_status": "PENDING_LEGAL_REVIEW",
            "verification_status": "PENDING_LEGAL_REVIEW",
            "verification_rule": "NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT",
            "substantive": False,
            "quality_flag": qf,
            "annotation_note": f"No-capture: {nc.get('error','')[:300]}",
        })
    seen=set(); dedup=[]
    for r in rows:
        k=(r.get("url"),r.get("local_path"),r.get("quality_flag"),str(r.get("http_status")))
        if k in seen: continue
        seen.add(k); dedup.append(r)
    return dedup


def write_citation_indexes(repo: Path, rows):
    fields=["citation_id","title","url","final_url","local_path","local_artifact","sha256","http_status","content_type","fetched_at","provenance","capture_access","legal_review_status","verification_status","verification_rule","substantive","quality_flag","annotation_note"]
    for out_dir in [repo/"99_Archives_and_Manifests", repo/"03_Evidentiary_Exhibits"]:
        out_dir.mkdir(parents=True, exist_ok=True)
        # preserve any existing extra fields by merging
        _, existing = read_csv(out_dir/"CITATION_INDEX.csv")
        ex_by_key={}
        for er in existing:
            k=(er.get('url',''),er.get('local_artifact','') or er.get('local_path',''),er.get('quality_flag',''),str(er.get('http_status','')))
            ex_by_key[k]=er
        merged=[]
        seen_keys=set()
        for r in rows:
            k=(r.get('url',''),r.get('local_artifact','') or r.get('local_path',''),r.get('quality_flag',''),str(r.get('http_status','')))
            er=ex_by_key.get(k,{})
            out=dict(er)
            out.update(r)
            out['verification_status']=str(out.get('verification_status') or 'PENDING_LEGAL_REVIEW')
            out['verification_rule']=str(out.get('verification_rule') or 'NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT')
            if str(out.get('verification_status')).upper()=='VERIFIED' and not str(out.get('human_signoff','')).strip():
                out['verification_status']='PENDING_LEGAL_REVIEW'
            merged.append(out); seen_keys.add(k)
        # preserve unmatched existing rows (normalize, do not drop silently)
        for k,er in ex_by_key.items():
            if k in seen_keys: continue
            out=dict(er)
            out['verification_status']=str(out.get('verification_status') or 'PENDING_LEGAL_REVIEW')
            out['verification_rule']=str(out.get('verification_rule') or 'NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT')
            if str(out.get('verification_status')).upper()=='VERIFIED' and not str(out.get('human_signoff','')).strip():
                out['verification_status']='PENDING_LEGAL_REVIEW'
            out.setdefault('legal_review_status','PENDING_LEGAL_REVIEW')
            qf=str(out.get('quality_flag') or '')
            sub=str(out.get('substantive') if out.get('substantive') is not None else '').strip().lower()
            local=str(out.get('local_artifact') or out.get('local_path') or '').strip()
            sha=str(out.get('sha256') or '').strip()
            if qf.startswith('NO_CAPTURE') or qf.startswith('NOT_SUBSTANTIVE'):
                out['substantive']=False
            elif local and sha and sub not in ('true','1','false','0'):
                out['substantive']=True
                if not qf: out['quality_flag']='SUBSTANTIVE_CAPTURE_PENDING_REVIEW'
            if local and sha and not str(out.get('provenance') or '').strip():
                out['provenance']='direct-http-fetch'
            if local and sha and not str(out.get('capture_access') or '').strip():
                out['capture_access']='PUBLIC_CAPTURE_UNAUTHENTICATED'
            merged.append(out)
        write_csv(out_dir/"CITATION_INDEX.csv", fields, merged)
        lines=["# Citation Index","","| Citation ID | Title | URL | Local Path | SHA256 | Status | Substantive | Quality Flag | Legal Review | Verification |","|---|---|---|---|---|---|---|---|---|---|"]
        for r in merged:
            lines.append(f"| {r.get('citation_id','')} | {r.get('title','')} | {r.get('url','')} | {r.get('local_path','')} | {r.get('sha256','')} | {r.get('http_status','')} | {r.get('substantive','')} | {r.get('quality_flag','')} | {r.get('legal_review_status','')} | {r.get('verification_status','')} |")
        (out_dir/"CITATION_INDEX.md").write_text("\n".join(lines)+"\n", encoding="utf-8")


def update_pending_recapture(repo: Path, rows):
    p = repo/"99_Archives_and_Manifests"/"PENDING_RECAPTURE_REGISTER.csv"
    fields, existing = read_csv(p)
    base_fields=["citation_id","url","title","status","reason","recorded_at","repo","local_artifact","annotation_note"]
    for bf in base_fields:
        if bf not in fields: fields.append(bf)
    if not fields: fields=base_fields
    by_url={r.get("url"):r for r in existing if r.get("url")}
    for r in rows:
        qf=str(r.get("quality_flag") or ""); sub=r.get("substantive")
        if not ((sub is False) or qf.startswith("NOT_SUBSTANTIVE") or qf.startswith("NO_CAPTURE")):
            continue
        url=r.get("url","")
        if not url: continue
        rec=dict(by_url.get(url,{}))
        rec.update({
            "citation_id": r.get("citation_id", rec.get("citation_id","")),
            "url":url,"title":r.get("title",""),"status":"PENDING_RECAPTURE",
            "reason":qf or "NOT_SUBSTANTIVE_PENDING_RECAPTURE",
            "recorded_at": rec.get("recorded_at") or r.get("fetched_at") or datetime.datetime.utcnow().isoformat()+"Z",
            "repo":repo.name,
            "local_artifact": r.get("local_artifact",""),
            "annotation_note":r.get("annotation_note","")
        })
        by_url[url]=rec
    # keep only rows relevant to this repo or with no repo; do not drop others blindly
    out_rows=list(by_url.values())
    write_csv(p, fields, out_rows)


def append_intake_log(repo: Path, rows):
    led = repo/"03_Evidentiary_Exhibits"/"Immutable_Ledger"
    led.mkdir(parents=True, exist_ok=True)
    p = led/"HARVEST_INTAKE_LOG.csv"
    fields, existing = read_csv(p)
    if not fields:
        fields=["timestamp_utc","url","final_url","status","content_type","bytes","sha256","saved_path","note","provenance","capture_access","legal_review_status"]
    for bf in ["provenance","capture_access","legal_review_status"]:
        if bf not in fields: fields.append(bf)
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
            "note": r.get("quality_flag") or r.get("annotation_note") or "LATAM 8 reconcile",
            "provenance": r.get("provenance",""), "capture_access": r.get("capture_access",""),
            "legal_review_status": r.get("legal_review_status","PENDING_LEGAL_REVIEW"),
        })
        seen.add(key)
    write_csv(p, fields, existing)


def refresh_manifest(repo: Path):
    manifests = repo/"99_Archives_and_Manifests"
    manifests.mkdir(parents=True, exist_ok=True)
    manifest_csv = manifests/"MANIFEST_SHA256.csv"
    def build_entries(exclude_extra=set()):
        entries=[]
        for pth in sorted(repo.rglob("*")):
            if pth.is_dir(): continue
            rel=pth.relative_to(repo).as_posix()
            if rel.startswith(".git/"): continue
            if rel == "99_Archives_and_Manifests/MANIFEST_SHA256.csv": continue
            if rel in exclude_extra: continue
            try: st=pth.stat()
            except Exception: continue
            entries.append({"path":rel,"bytes":st.st_size,"sha256":sha256_file(pth),"mtime_utc":datetime.datetime.utcfromtimestamp(st.st_mtime).isoformat()+"Z"})
        return entries
    entries=build_entries(exclude_extra={"VERIFICATION_KEYS/sha256_manifest.txt"})
    write_csv(manifest_csv, ["path","bytes","sha256","mtime_utc"], entries)
    vk = repo/"VERIFICATION_KEYS"/"sha256_manifest.txt"
    if vk.exists():
        lines=[f"{e['sha256']}  {e['path']}" for e in entries]
        vk.write_text("\n".join(lines)+"\n", encoding="utf-8")
        # add legacy manifest entry with accurate hash
        st=vk.stat()
        entries.append({"path":"VERIFICATION_KEYS/sha256_manifest.txt","bytes":st.st_size,"sha256":sha256_file(vk),"mtime_utc":datetime.datetime.utcfromtimestamp(st.st_mtime).isoformat()+"Z"})
        entries.sort(key=lambda e:e['path'])
        write_csv(manifest_csv, ["path","bytes","sha256","mtime_utc"], entries)


def enforce_valuation_tbd(repo: Path):
    candidates=[repo/"00_Master_Knowledge_Base"/"VALUATION_WORKSHEET.csv", repo/"03_Evidentiary_Exhibits"/"VALUATION_WORKSHEET.csv"]
    found=[p for p in candidates if p.exists()]
    if not found:
        raise FileNotFoundError(f"Missing VALUATION_WORKSHEET.csv in canonical/legacy paths for {repo}")
    for p in found:
        fields, rows = read_csv(p)
        changed=False
        for r in rows:
            for k in ["low_usd","base_usd","high_usd"]:
                if k in fields and str(r.get(k,"")).strip().upper() != "TBD":
                    r[k]="TBD"; changed=True
            if "valuation_status" in fields and str(r.get("valuation_status","")).strip().upper() != "TBD":
                r["valuation_status"]="TBD"; changed=True
            if "review_status" in fields and str(r.get("review_status","")).strip() != "PENDING_LEGAL_REVIEW":
                r["review_status"]="PENDING_LEGAL_REVIEW"; changed=True
        if changed: write_csv(p, fields, rows)


def enforce_vector_flags(repo: Path):
    candidates=[repo/"99_Archives_and_Manifests"/"claim_vector_registry_3000.json", repo/"02_Evidence_Vectors"/"claim_vector_registry_3000.json"]
    found=[p for p in candidates if p.exists()]
    if not found:
        raise FileNotFoundError(f"Missing claim_vector_registry_3000.json in canonical/legacy paths for {repo}")
    for p in found:
        try:
            obj=json.loads(p.read_text(encoding='utf-8'))
        except Exception:
            continue
        changed=False
        def _fix(v):
            nonlocal changed
            if not isinstance(v,dict): return
            if v.get("valuation_status") != "TBD": v["valuation_status"]="TBD"; changed=True
            if v.get("evidence_mapping_status") not in ("AUTO_CANDIDATE_PENDING_REVIEW","PENDING_EVIDENCE_MAPPING_REVIEW"):
                v["evidence_mapping_status"]="AUTO_CANDIDATE_PENDING_REVIEW"; changed=True
            if v.get("review_status") != "PENDING_LEGAL_REVIEW": v["review_status"]="PENDING_LEGAL_REVIEW"; changed=True
        if isinstance(obj,list):
            for v in obj: _fix(v)
        elif isinstance(obj,dict):
            for key in ['vectors','claims','items','registry']:
                vecs=obj.get(key)
                if isinstance(vecs,list):
                    for v in vecs: _fix(v)
        if changed:
            p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    summary=[]; errors=[]
    for rp in REPOS:
        repo=Path(rp)
        if not repo.exists():
            errors.append(f"MISSING:{repo}"); summary.append((repo.name,"MISSING")); continue
        try:
            enforce_valuation_tbd(repo)
            enforce_vector_flags(repo)
            rows=build_citation_rows(repo)
            write_citation_indexes(repo, rows)
            update_pending_recapture(repo, rows)
            append_intake_log(repo, rows)
            refresh_manifest(repo)
            summary.append((repo.name,len(rows)))
        except Exception as e:
            errors.append(f"{repo.name}:{e}")
            summary.append((repo.name,f"ERROR:{e}"))
    for n,c in summary: print(f"{n}: {c}")
    print(f"NO_CAPTURE_ENTRIES: {len(ncs)}")
    if errors:
        print("ERRORS:")
        for e in errors: print(" -",e)
        raise SystemExit(2)

if __name__ == "__main__":
    main()
