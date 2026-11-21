import hashlib
from pathlib import Path
from bolster_africa_full import ROOT, PROFILES, backup_if_exists


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
