import csv, json, os, subprocess, re, hashlib
from pathlib import Path

ROOT = Path(r"W:\Legal")

PACIFIC8 = [
    ROOT/"PACIFIC"/"US_AS_AMERICAN_SAMOA",
    ROOT/"PACIFIC"/"US_CK_COOK_ISLANDS",
    ROOT/"PACIFIC"/"US_FJ_FIJI",
    ROOT/"PACIFIC"/"US_FM_MICRONESIA_FSM",
    ROOT/"PACIFIC"/"US_GU_GUAM",
    ROOT/"PACIFIC"/"US_KI_KIRIBATI",
    ROOT/"PACIFIC"/"US_MP_NORTHERN_MARIANA_ISLANDS",
    ROOT/"PACIFIC"/"US_NR_NAURU",
]


def find_repos():
    repos = []
    for base in ["AFRICA", "ASIA", "PACIFIC", "US_DOMESTIC_VICTIMS"]:
        p = ROOT / base
        if p.exists():
            for d in p.iterdir():
                if d.is_dir() and (d / ".git").exists():
                    repos.append(d)
    ti = ROOT / "US_TURTLE_ISLAND_NATIVES"
    if ti.exists():
        for gd in ti.rglob(".git"):
            if gd.is_dir():
                repos.append(gd.parent)
    for n in ["US_AFRICAN_AMERICAN_REPARATIONS"]:
        p = ROOT / n
        if p.exists() and (p / ".git").exists():
            repos.append(p)
        if p.exists():
            for d in p.iterdir():
                if d.is_dir() and (d / ".git").exists():
                    repos.append(d)
    # include PACIFIC8 untracked targets explicitly
    for d in PACIFIC8:
        if d.exists():
            repos.append(d)
    seen = set()
    out = []
    for r in repos:
        k = str(r).lower()
        if k not in seen:
            seen.add(k)
            out.append(r)
    return sorted(out)


def sha256_file(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1<<16), b''):
            h.update(chunk)
    return h.hexdigest()


def check(repo):
    issues = []
    # legacy manifest
    if (repo/"VERIFICATION_KEYS/sha256_manifest.txt").exists() or (repo/".git").exists():
        if not (repo/"VERIFICATION_KEYS/sha256_manifest.txt").exists() and (repo/".git").exists():
            # some git repos may not have it; keep original strictness only when expected? original: missing_manifest
            issues.append("missing_manifest")
    # new manifest layout
    mcsv = repo/"99_Archives_and_Manifests"/"MANIFEST_SHA256.csv"
    if mcsv.exists():
        with mcsv.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                rel=(row.get('path') or '').replace('\\','/')
                if rel == '99_Archives_and_Manifests/MANIFEST_SHA256.csv':
                    issues.append('manifest_self_entry_present')
                    break
                fp = repo/rel
                if fp.exists() and fp.is_file():
                    try:
                        if sha256_file(fp) != (row.get('sha256') or ''):
                            issues.append('manifest_hash_mismatch')
                            break
                    except Exception:
                        issues.append('manifest_hash_error')
                        break
    # citation index: no VERIFIED, required fields present for PACIFIC8-like layout
    for ci in [repo/"03_Evidentiary_Exhibits/CITATION_INDEX.csv", repo/"99_Archives_and_Manifests/CITATION_INDEX.csv"]:
        if ci.exists():
            with ci.open("r", encoding="utf-8", newline="") as f:
                reader=csv.DictReader(f)
                fields=set(reader.fieldnames or [])
                if mcsv.exists():
                    for req in ["verification_status","verification_rule","legal_review_status","quality_flag","substantive"]:
                        if req not in fields:
                            issues.append(f"citation_missing_field:{req}")
                            break
                for row in reader:
                    vs=(row.get("verification_status") or "").strip().upper()
                    lrs=(row.get("legal_review_status") or "").strip().upper()
                    if vs == "VERIFIED" or lrs == "VERIFIED":
                        issues.append("verified_citation_without_gate")
                        break
                    qf=(row.get('quality_flag') or '')
                    sub=(row.get('substantive') or '').strip().lower()
                    if qf.startswith('NO_CAPTURE') or qf.startswith('NOT_SUBSTANTIVE'):
                        if sub not in ('false','0',''):
                            pass
                if "verified_citation_without_gate" in issues:
                    break
    # valuation workbook legacy
    wb = repo/"00_Master_Knowledge_Base/VALUATION_WORKBOOK.csv"
    if wb.exists():
        with wb.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                vs = (row.get("verification_status") or "").strip().upper()
                for k in ["low", "base", "high", "baseline_amount"]:
                    v = (row.get(k) or "").strip()
                    if v and v.upper() != "TBD":
                        if re.fullmatch(r"[0-9,.\-]+", v):
                            if vs == "VERIFIED" and not (row.get("reviewer") or "").strip():
                                issues.append("verified_valuation_missing_reviewer")
                                break
                if "verified_valuation_missing_reviewer" in issues:
                    break
    # valuation worksheet canonical checks
    ws = repo/"00_Master_Knowledge_Base"/"VALUATION_WORKSHEET.csv"
    if ws.exists():
        with ws.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                for k in ["low_usd","base_usd","high_usd"]:
                    v=(row.get(k) or '').strip()
                    if v and v.upper() != 'TBD':
                        issues.append('valuation_not_tbd'); break
                if (row.get('valuation_status') or '').strip().upper() not in ('','TBD'):
                    issues.append('valuation_status_not_tbd')
                if issues: break
    # vector registry flags
    vr = repo/"99_Archives_and_Manifests"/"claim_vector_registry_3000.json"
    if vr.exists():
        try:
            obj=json.loads(vr.read_text(encoding='utf-8'))
            vecs=obj if isinstance(obj,list) else (obj.get('vectors') or obj.get('claims') or obj.get('items') or obj.get('registry') or [])
            for v in vecs:
                if not isinstance(v,dict): continue
                if v.get('valuation_status')!='TBD': issues.append('vector_valuation_not_tbd'); break
                if v.get('evidence_mapping_status') not in ('AUTO_CANDIDATE_PENDING_REVIEW','PENDING_EVIDENCE_MAPPING_REVIEW'):
                    issues.append('vector_mapping_status_bad'); break
                if v.get('review_status')!='PENDING_LEGAL_REVIEW': issues.append('vector_review_status_bad'); break
        except Exception as e:
            issues.append(f'vector_read_error:{e}')
    # dedupe
    dedup=[]; seen=set()
    for i in issues:
        if i not in seen: seen.add(i); dedup.append(i)
    return dedup


def main():
    repos = find_repos()
    bad = []
    for r in repos:
        try:
            iss = check(r)
            if iss:
                bad.append((r.name, iss))
        except Exception as e:
            bad.append((r.name, [f"error:{e}"]))
    print(f"CHECKED {len(repos)}")
    print(f"ISSUES {len(bad)}")
    for n, iss in bad[:50]:
        print(n, ";".join(iss))
    out = ROOT / ".opencode/batch5_qa_report.txt"
    with out.open("w", encoding="utf-8") as f:
        f.write(f"CHECKED {len(repos)}\nISSUES {len(bad)}\n")
        for n, iss in bad:
            f.write(f"{n}\t{';'.join(iss)}\n")
    print(f"REPORT {out}")


if __name__ == "__main__":
    main()
