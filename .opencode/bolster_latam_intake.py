import hashlib
from pathlib import Path
from bolster_latam_deep import ROOT, PROFILES, TODAY, backup_if_exists, write


def sha256(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


for name, prof in PROFILES.items():
    if name == "US_CU_CUBA":
        continue
    cdir = ROOT / name
    if not cdir.exists():
        continue
    p = cdir / "03_Evidentiary_Exhibits" / "EVIDENCE_INTAKE_LOG.md"
    content = f"""# Evidence Intake Log - {prof["country"]}

| Date | Artifact | Source URL | Retrieved By | SHA-256 | Custody Status | Notes |
|---|---|---|---|---|---|---|
| {TODAY} | PRIMARY_PUBLIC_SOURCES.md | internal registry | OpenCode | pending | VERIFIED_PUBLIC_SOURCE_LINKS | Links require access verification and artifact download/authentication. |

## Intake Rules
- Record source URL, access date, downloader, file hash, and storage path.
- Store original files in `03_Evidentiary_Exhibits/Immutable_Ledger/` after verification.
- Do not mark as authenticated without provenance review.
"""
    write(p, content, cdir)
    manifest = cdir / "VERIFICATION_KEYS/sha256_manifest.txt"
    backup_if_exists(manifest, cdir)
    lines = []
    for fp in sorted(cdir.rglob("*")):
        if not fp.is_file():
            continue
        rel = fp.relative_to(cdir).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel == "VERIFICATION_KEYS/sha256_manifest.txt":
            continue
        lines.append(f"{sha256(fp)}  {rel}")
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("OK", name)
