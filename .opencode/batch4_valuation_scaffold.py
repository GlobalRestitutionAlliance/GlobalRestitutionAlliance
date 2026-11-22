import csv, json, hashlib, os, subprocess
from pathlib import Path

ROOT = Path(r"W:\Legal")


def sha256p(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def git(cwd, args, env=None, timeout=180):
    return subprocess.run(
        args, cwd=str(cwd), capture_output=True, text=True, env=env, timeout=timeout
    )


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


def apply(repo):
    wb = repo / "00_Master_Knowledge_Base/VALUATION_WORKBOOK.csv"
    xw = repo / "00_Master_Knowledge_Base/MASTER_VECTOR_VALUATION_CROSSWALK.csv"
    vf = repo / ".antigravity/vector-index/vector_index.jsonl"
    if not wb.exists() or not vf.exists():
        return 0
    # read existing workbook vector_ids
    existing = set()
    with wb.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            vid = (row.get("vector_id") or "").strip()
            if vid:
                existing.add(vid)
    vectors = []
    for line in vf.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            continue
        vid = line.split("|")[0].strip()
        vectors.append(vid)
    # citations
    cites = []
    cp = repo / "03_Evidentiary_Exhibits/CITATION_INDEX.csv"
    if cp.exists():
        with cp.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                cites.append(row)
    added = 0
    # append rows for vectors not in workbook (scaffold only, no fabricated amounts)
    if vectors:
        with wb.open("a", encoding="utf-8", newline="") as f:
            cols = [
                "vector_id",
                "claim_category",
                "harm_period_start",
                "harm_period_end",
                "jurisdiction",
                "defendant_actor",
                "evidence_artifact",
                "citation_id",
                "sha256",
                "damages_theory",
                "baseline_amount",
                "baseline_currency",
                "baseline_year",
                "adjustment_method",
                "interest_or_multiplier",
                "offsets",
                "low",
                "base",
                "high",
                "confidence",
                "verification_status",
                "reviewer",
                "review_date",
                "notes",
            ]
            w = csv.DictWriter(f, fieldnames=cols)
            for vid in vectors:
                if vid in existing:
                    continue
                cit = cites[0] if cites else {}
                w.writerow(
                    {
                        "vector_id": vid,
                        "claim_category": "PENDING_CLASSIFICATION",
                        "harm_period_start": "",
                        "harm_period_end": "",
                        "jurisdiction": repo.name,
                        "defendant_actor": "PENDING_IDENTIFICATION",
                        "evidence_artifact": cit.get("local_artifact", ""),
                        "citation_id": cit.get("citation_id", ""),
                        "sha256": cit.get("sha256", ""),
                        "damages_theory": "PENDING_EVIDENCE",
                        "baseline_amount": "",
                        "baseline_currency": "",
                        "baseline_year": "",
                        "adjustment_method": "",
                        "interest_or_multiplier": "",
                        "offsets": "",
                        "low": "TBD",
                        "base": "TBD",
                        "high": "TBD",
                        "confidence": "UNVERIFIED",
                        "verification_status": "PENDING_LEGAL_REVIEW",
                        "reviewer": "",
                        "review_date": "",
                        "notes": "Scaffold row - no amount without verified evidence",
                    }
                )
                added += 1
    # update crosswalk similarly
    if xw.exists():
        existing_x = set()
        with xw.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                vid = (row.get("vector_id") or "").strip()
                if vid:
                    existing_x.add(vid)
        with xw.open("a", encoding="utf-8", newline="") as f:
            cols = [
                "vector_id",
                "vector_name",
                "era",
                "category",
                "primary_archive",
                "record_ref",
                "target_actor",
                "legal_hook",
                "pleading_target",
                "evidence_artifact",
                "citation_id",
                "verification_status",
                "valuation_row_id",
                "valuation_status",
                "low",
                "base",
                "high",
                "notes",
            ]
            w = csv.DictWriter(f, fieldnames=cols)
            for vid in vectors:
                if vid in existing_x:
                    continue
                cit = cites[0] if cites else {}
                w.writerow(
                    {
                        "vector_id": vid,
                        "vector_name": "PENDING",
                        "era": "PENDING",
                        "category": "PENDING",
                        "primary_archive": "",
                        "record_ref": "",
                        "target_actor": "PENDING",
                        "legal_hook": "PENDING",
                        "pleading_target": "",
                        "evidence_artifact": cit.get("local_artifact", ""),
                        "citation_id": cit.get("citation_id", ""),
                        "verification_status": "PENDING_LEGAL_REVIEW",
                        "valuation_row_id": vid,
                        "valuation_status": "TBD",
                        "low": "TBD",
                        "base": "TBD",
                        "high": "TBD",
                        "notes": "Scaffold crosswalk row - requires verified evidence",
                    }
                )
                added += 1
    if added:
        lines = []
        for fp in sorted(repo.rglob("*")):
            if not fp.is_file():
                continue
            rel = fp.relative_to(repo).as_posix()
            if rel.startswith(".git/"):
                continue
            if rel == "VERIFICATION_KEYS/sha256_manifest.txt":
                continue
            try:
                lines.append(f"{sha256p(fp)}  {rel}")
            except:
                pass
        (repo / "VERIFICATION_KEYS/sha256_manifest.txt").write_text(
            "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
        )
    return added


def main():
    repos = find_repos()
    print(f"FOUND {len(repos)}", flush=True)
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    changed = []
    for i, r in enumerate(repos, 1):
        try:
            a = apply(r)
            if a:
                git(r, ["git", "add", "-A"], env=env)
                st = git(r, ["git", "status", "--short"], env=env)
                if st.stdout.strip():
                    git(
                        r,
                        [
                            "git",
                            "commit",
                            "-m",
                            "Batch 4: scaffold valuation workbook/crosswalk rows (TBD pending evidence)",
                        ],
                        env=env,
                    )
                    changed.append(r)
            if i % 100 == 0:
                print(f"VAL {i}/{len(repos)} changed={len(changed)}", flush=True)
        except Exception as e:
            print(f"ERR {r.name}: {e}", flush=True)
    print(f"VAL_DONE changed={len(changed)}", flush=True)
    subprocess.run(
        ["gh", "auth", "switch", "-u", "GlobalRestitutionAlliance"], capture_output=True
    )
    envg = os.environ.copy()
    envg["GIT_TERMINAL_PROMPT"] = "0"
    envg.pop("GH_TOKEN", None)
    envg.pop("GITHUB_TOKEN", None)
    ok = fail = 0
    for i, r in enumerate(changed, 1):
        p = git(r, ["git", "push", "origin", "HEAD"], envg, timeout=240)
        if p.returncode == 0:
            ok += 1
        else:
            fail += 1
        if i % 100 == 0:
            print(f"PUSH {i}/{len(changed)} ok={ok} fail={fail}", flush=True)
    print(f"PUSH_DONE ok={ok} fail={fail}", flush=True)
    subprocess.run(["gh", "auth", "switch", "-u", "R03LV1S"], capture_output=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
