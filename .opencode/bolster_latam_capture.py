import urllib.request, hashlib, datetime
from pathlib import Path
from bolster_latam_deep import ROOT, PROFILES, TODAY, backup_if_exists

CAPTURES = {
    "US_NI_NICARAGUA": [
        ("ICJ_Case_70_Nicaragua_v_US.html", "https://www.icj-cij.org/case/70")
    ],
    "US_BO_BOLIVIA": [
        ("ICJ_Case_153_Bolivia_v_Chile.html", "https://www.icj-cij.org/case/153")
    ],
    "US_CL_CHILE": [
        ("ICJ_Case_153_Bolivia_v_Chile.html", "https://www.icj-cij.org/case/153")
    ],
    "US_GY_GUYANA": [
        ("ICJ_Case_171_Guyana_v_Venezuela.html", "https://www.icj-cij.org/case/171")
    ],
    "US_VE_VENEZUELA": [
        ("ICJ_Case_171_Guyana_v_Venezuela.html", "https://www.icj-cij.org/case/171")
    ],
    "US_GT_GUATEMALA": [
        ("ICJ_Case_18_Nottebohm.html", "https://www.icj-cij.org/case/18")
    ],
}


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def fetch(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read(), r.status, r.headers.get("Content-Type", "")


def main():
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    for name, prof in PROFILES.items():
        if name == "US_CU_CUBA":
            continue
        cdir = ROOT / name
        if not cdir.exists():
            continue
        capdir = cdir / "03_Evidentiary_Exhibits" / "Public_Source_Captures"
        capdir.mkdir(parents=True, exist_ok=True)
        log = cdir / "03_Evidentiary_Exhibits" / "EVIDENCE_INTAKE_LOG.md"
        rows = []
        for fn, url in CAPTURES.get(name, []):
            out = capdir / fn
            try:
                data, status, ctype = fetch(url)
                out.write_bytes(data)
                h = sha256(data)
                rows.append(
                    f"| {TODAY} | {fn} | {url} | OpenCode/urllib | {h} | PUBLIC_CAPTURE_UNAUTHENTICATED | HTTP {status}; {ctype}; bytes={len(data)}; captured={ts} |"
                )
                print("CAP", name, fn, len(data))
            except Exception as e:
                rows.append(
                    f"| {TODAY} | {fn} | {url} | OpenCode/urllib | N/A | CAPTURE_FAILED | {e} |"
                )
                print("ERR", name, fn, e)
        if rows and log.exists():
            txt = log.read_text(encoding="utf-8")
            # append rows before Intake Rules if present
            marker = "## Intake Rules"
            if marker in txt:
                txt = txt.replace(marker, "\n".join(rows) + "\n\n" + marker, 1)
            else:
                txt += "\n" + "\n".join(rows) + "\n"
            log.write_text(txt, encoding="utf-8", newline="\n")
    # refresh manifests for all
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
            h = hashlib.sha256(fp.read_bytes()).hexdigest()
            lines.append(f"{h}  {rel}")
        manifest.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("DONE")


if __name__ == "__main__":
    main()
