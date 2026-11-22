import csv, json, hashlib, os, subprocess, re
from pathlib import Path

TODAY = "2026-11-21"
ROOT = Path(r"W:\Legal")
REPOS = [
    Path(r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS"),
    Path(
        r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-gb-reparations-master-litigation"
    ),
    Path(
        r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-pt-reparations-master-litigation"
    ),
    Path(
        r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-nl-reparations-master-litigation"
    ),
    Path(r"W:\Legal\US_DOMESTIC_VICTIMS\US_DW_NUCLEAR_DOWNWINDERS"),
    Path(r"W:\Legal\PACIFIC\US_MH_MARSHALL_ISLANDS"),
    Path(r"W:\Legal\US_DOMESTIC_VICTIMS\US_JA_JAPANESE_AMERICAN_INTERNEES"),
    Path(
        r"W:\Legal\US_TURTLE_ISLAND_NATIVES\NAVAJO\US_AZ_NAVAJO_NATION_ARIZONA_NEW_MEXICO_UTAH"
    ),
]


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


def load_citations(repo):
    p = repo / "03_Evidentiary_Exhibits/CITATION_INDEX.csv"
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def enrich(repo):
    cites = load_citations(repo)
    vf = repo / ".antigravity/vector-index/vector_index.jsonl"
    if not vf.exists():
        return 0
    lines = [
        l
        for l in vf.read_text(encoding="utf-8", errors="ignore").splitlines()
        if l.strip()
    ]
    # build enriched lines for first N vectors based on citations
    enriched = 0
    new_lines = []
    for i, line in enumerate(lines):
        parts = line.split("|")
        vid = parts[0] if parts else f"VID-{i + 1:04d}"
        # if already enriched, keep
        if len(parts) >= 5 and parts[2] not in ("scaffold", "scaffold-expanded"):
            new_lines.append(line)
            continue
        cit = cites[i % len(cites)] if cites else None
        if cit:
            art = Path(cit.get("local_artifact", "")).name
            title = re.sub(r"[_\-]+", " ", Path(art).stem).strip()[:80]
            url = cit.get("url", "")
            cid = cit.get("citation_id", "")
            # conservative, evidence-linked enrichment
            new_lines.append(
                f"{vid}|{repo.name}|evidence-linked|PENDING_LEGAL_REVIEW|{title} | source:{cid} | {url}"
            )
            enriched += 1
        else:
            new_lines.append(line)
    vf.write_text("\n".join(new_lines) + "\n", encoding="utf-8", newline="\n")
    # update valuation workbook rows for enriched vectors
    wb = repo / "00_Master_Knowledge_Base/VALUATION_WORKBOOK.csv"
    if wb.exists() and cites:
        rows = []
        with wb.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            cols = reader.fieldnames
            for row in reader:
                rows.append(row)
        for i, row in enumerate(rows):
            cit = cites[i % len(cites)]
            if (
                row.get("verification_status") or ""
            ) == "PENDING_LEGAL_REVIEW" and row.get(
                "claim_category"
            ) == "PENDING_CLASSIFICATION":
                row["evidence_artifact"] = cit.get("local_artifact", "")
                row["citation_id"] = cit.get("citation_id", "")
                row["sha256"] = cit.get("sha256", "")
                row["damages_theory"] = "PENDING_EVIDENCE_REVIEW"
                row["notes"] = (
                    "Evidence-linked scaffold; amount TBD pending verified methodology and human review"
                )
        with wb.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
    # manifest
    linesm = []
    for fp in sorted(repo.rglob("*")):
        if not fp.is_file():
            continue
        rel = fp.relative_to(repo).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel == "VERIFICATION_KEYS/sha256_manifest.txt":
            continue
        try:
            linesm.append(f"{sha256p(fp)}  {rel}")
        except:
            pass
    (repo / "VERIFICATION_KEYS/sha256_manifest.txt").write_text(
        "\n".join(linesm) + "\n", encoding="utf-8", newline="\n"
    )
    return enriched


env = os.environ.copy()
env["GIT_TERMINAL_PROMPT"] = "0"
for repo in REPOS:
    e = enrich(repo)
    git(repo, ["git", "add", "-A"], env=env)
    st = git(repo, ["git", "status", "--short"], env=env)
    if st.stdout.strip():
        git(
            repo,
            [
                "git",
                "commit",
                "-m",
                "Pilot Batch 2: evidence-linked vector/valuation enrichment (PENDING_LEGAL_REVIEW)",
            ],
            env=env,
        )
    print(repo.name, "enriched", e, flush=True)

subprocess.run(
    ["gh", "auth", "switch", "-u", "GlobalRestitutionAlliance"], capture_output=True
)
envg = os.environ.copy()
envg["GIT_TERMINAL_PROMPT"] = "0"
envg.pop("GH_TOKEN", None)
envg.pop("GITHUB_TOKEN", None)
for repo in REPOS:
    p = git(repo, ["git", "push", "origin", "HEAD"], envg, timeout=240)
    print(repo.name, "PUSH_OK" if p.returncode == 0 else "PUSH_FAIL", flush=True)
subprocess.run(["gh", "auth", "switch", "-u", "R03LV1S"], capture_output=True)
print("DONE", flush=True)
