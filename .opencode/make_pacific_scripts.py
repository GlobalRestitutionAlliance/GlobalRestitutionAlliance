from pathlib import Path

base = Path(r"W:\Legal\.opencode")
src = (base / "bolster_africa_full.py").read_text(encoding="utf-8")
t = (
    src.replace(r"W:\Legal\AFRICA", r"W:\Legal\PACIFIC")
    .replace("AFRICA", "PACIFIC")
    .replace("africa", "pacific")
)
(base / "bolster_pacific_full.py").write_text(t, encoding="utf-8")
for src_name, out_name in [
    ("harvest_public_sources.py", "harvest_pacific.py"),
    ("populate_citations.py", "populate_citations_pacific.py"),
    ("apply_citations_to_docs.py", "apply_citations_pacific.py"),
    ("refresh_manifests.py", "refresh_manifests_pacific.py"),
    ("bolster_latam_docx.py", "bolster_pacific_docx.py"),
]:
    t = (base / src_name).read_text(encoding="utf-8")
    t = t.replace("from bolster_latam_deep import", "from bolster_pacific_full import")
    t = t.replace("if name=='US_CU_CUBA': continue", "")
    t = t.replace("if name == 'US_CU_CUBA':\n        continue", "")
    t = t.replace("if name == 'US_CU_CUBA':\n            continue", "")
    (base / out_name).write_text(t, encoding="utf-8")
print("ok")
