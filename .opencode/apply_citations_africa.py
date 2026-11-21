import csv, json, re
from pathlib import Path
from bolster_africa_full import ROOT, PROFILES, TODAY, backup_if_exists, write


def load_citations(cdir):
    p = cdir / "03_Evidentiary_Exhibits" / "CITATION_INDEX.csv"
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def citation_block(cites):
    lines = [
        "## Verified Source Citations (PENDING_LEGAL_REVIEW)",
        "",
        "Rule: No citation marked VERIFIED without local hashed source artifact and counsel sign-off.",
        "",
    ]
    for c in cites[:20]:
        lines.append(
            f"- {c['citation_id']}: {c.get('title', '')} | {c.get('url', '')} | local=`{c.get('local_artifact', '')}` | sha256=`{(c.get('sha256') or '')[:16]}...` | status={c.get('verification_status', 'PENDING_LEGAL_REVIEW')}"
        )
    if len(cites) > 20:
        lines.append(
            f"- ... {len(cites) - 20} additional citations in `03_Evidentiary_Exhibits/CITATION_INDEX.csv`"
        )
    return "\n".join(lines) + "\n"


def patch_md(path, cites, cdir):
    if not path.exists() or not cites:
        return False
    txt = path.read_text(encoding="utf-8", errors="ignore")
    marker = "## Verified Source Citations (PENDING_LEGAL_REVIEW)"
    block = citation_block(cites)
    if marker in txt:
        idx = txt.index(marker)
        new_txt = txt[:idx].rstrip() + "\n\n" + block
        if new_txt == txt:
            return False
        backup_if_exists(path, cdir)
        path.write_text(new_txt, encoding="utf-8", newline="\n")
        return True
    backup_if_exists(path, cdir)
    path.write_text(txt.rstrip() + "\n\n" + block, encoding="utf-8", newline="\n")
    return True


def patch_crosswalk_csv(path, cites, cdir):
    if not path.exists() or not cites:
        return False
    backup_if_exists(path, cdir)
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        cols = reader.fieldnames or []
    for extra in [
        "citation_id",
        "citation_url",
        "citation_local_artifact",
        "citation_sha256",
        "citation_status",
    ]:
        if extra not in cols:
            cols.append(extra)
    for i, r in enumerate(rows):
        c = cites[i % len(cites)]
        r["citation_id"] = c["citation_id"]
        r["citation_url"] = c.get("url", "")
        r["citation_local_artifact"] = c.get("local_artifact", "")
        r["citation_sha256"] = c.get("sha256", "")
        r["citation_status"] = c.get("verification_status", "PENDING_LEGAL_REVIEW")
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    return True


def main():
    patched = 0
    for name, prof in PROFILES.items():
        if name == "US_CU_CUBA":
            continue
        cdir = ROOT / name
        cites = load_citations(cdir)
        if not cites:
            continue
        # patch 01-07 md docs
        for folder in [
            "01_Pleadings_and_Complaints",
            "02_Discovery_and_Evidentiary",
            "03_Motions_and_Briefs",
            "04_International_Tribunals",
            "05_Strategic_Doctrines_and_Red_Team",
            "06_Trial_and_Appellate_Prep",
            "07_Enforcement_and_Restitution",
            "00_Master_Knowledge_Base",
        ]:
            d = cdir / folder
            if not d.exists():
                continue
            for p in d.rglob("*.md"):
                if patch_md(p, cites, cdir):
                    patched += 1
            for p in d.rglob("*Crosswalk*.csv"):
                if patch_crosswalk_csv(p, cites, cdir):
                    patched += 1
        print("APPLY", name, "cites", len(cites))
    print("PATCHED", patched)


if __name__ == "__main__":
    main()
