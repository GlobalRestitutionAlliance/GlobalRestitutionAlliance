import json
from pathlib import Path
from bolster_latam_deep import ROOT, PROFILES

work = []
for name, prof in PROFILES.items():
    if name == "US_CU_CUBA":
        continue
    cdir = ROOT / name
    log = cdir / "03_Evidentiary_Exhibits" / "EVIDENCE_INTAKE_LOG.md"
    if not log.exists():
        continue
    txt = log.read_text(encoding="utf-8", errors="ignore")
    for line in txt.splitlines():
        if "CAPTURE_FAILED" not in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 7:
            continue
        url = parts[2]
        artifact = parts[1]
        if url.startswith("http"):
            work.append(
                {
                    "country": name,
                    "iso": prof["iso"],
                    "url": url,
                    "artifact": artifact,
                    "cdir": str(cdir),
                }
            )
seen = set()
dedup = []
for w in work:
    k = (w["country"], w["url"])
    if k in seen:
        continue
    seen.add(k)
    dedup.append(w)
Path(r"W:\Legal\.opencode\failed_harvest_worklist.json").write_text(
    json.dumps(dedup, indent=2), encoding="utf-8"
)
print(len(dedup))
