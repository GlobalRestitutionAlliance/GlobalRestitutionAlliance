from pathlib import Path

base = Path(r"W:\Legal\.opencode")
src = (base / "bolster_africa_full.py").read_text(encoding="utf-8")
t = (
    src.replace(r"W:\Legal\AFRICA", r"W:\Legal\ASIA")
    .replace("AFRICA", "ASIA")
    .replace("africa", "asia")
)
(base / "bolster_asia_full.py").write_text(t, encoding="utf-8")
# derived scripts
for src_name, out_name, old, news in [
    (
        "harvest_public_sources.py",
        "harvest_asia.py",
        "bolster_latam_deep",
        "bolster_asia_full",
    ),
    (
        "populate_citations.py",
        "populate_citations_asia.py",
        "bolster_latam_deep",
        "bolster_asia_full",
    ),
    (
        "apply_citations_to_docs.py",
        "apply_citations_asia.py",
        "bolster_latam_deep",
        "bolster_asia_full",
    ),
    (
        "refresh_manifests.py",
        "refresh_manifests_asia.py",
        "bolster_latam_deep",
        "bolster_asia_full",
    ),
    (
        "bolster_latam_docx.py",
        "bolster_asia_docx.py",
        "bolster_latam_deep",
        "bolster_asia_full",
    ),
]:
    t = (base / src_name).read_text(encoding="utf-8")
    t = t.replace(f"from {old} import", f"from {news} import")
    t = t.replace("if name=='US_CU_CUBA': continue", "")
    t = t.replace("if name == 'US_CU_CUBA':\n        continue", "")
    t = t.replace("if name == 'US_CU_CUBA':\n            continue", "")
    (base / out_name).write_text(t, encoding="utf-8")
print("ok")
