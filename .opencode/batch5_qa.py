import csv, json, os, subprocess, re
from pathlib import Path

ROOT = Path(r"W:\Legal")


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
    seen = set()
    out = []
    for r in repos:
        k = str(r).lower()
        if k not in seen:
            seen.add(k)
            out.append(r)
    return sorted(out)


def check(repo):
    issues = []
    # manifest exists
    if not (repo / "VERIFICATION_KEYS/sha256_manifest.txt").exists():
        issues.append("missing_manifest")
    # citation index: no VERIFIED
    ci = repo / "03_Evidentiary_Exhibits/CITATION_INDEX.csv"
    if ci.exists():
        with ci.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                if (row.get("verification_status") or "").strip().upper() == "VERIFIED":
                    issues.append("verified_citation_without_gate")
                    break
    # valuation workbook: no numeric amounts marked VERIFIED without review fields - basic check
    wb = repo / "00_Master_Knowledge_Base/VALUATION_WORKBOOK.csv"
    if wb.exists():
        with wb.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                vs = (row.get("verification_status") or "").strip().upper()
                for k in ["low", "base", "high", "baseline_amount"]:
                    v = (row.get(k) or "").strip()
                    if v and v.upper() != "TBD":
                        # if numeric, must be PENDING_LEGAL_REVIEW or VERIFIED with reviewer
                        if re.fullmatch(r"[0-9,.\-]+", v):
                            if (
                                vs == "VERIFIED"
                                and not (row.get("reviewer") or "").strip()
                            ):
                                issues.append("verified_valuation_missing_reviewer")
                                break
                if "verified_valuation_missing_reviewer" in issues:
                    break
    return issues


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
    # write report
    out = ROOT / ".opencode/batch5_qa_report.txt"
    with out.open("w", encoding="utf-8") as f:
        f.write(f"CHECKED {len(repos)}\nISSUES {len(bad)}\n")
        for n, iss in bad:
            f.write(f"{n}\t{';'.join(iss)}\n")
    print(f"REPORT {out}")


if __name__ == "__main__":
    main()
