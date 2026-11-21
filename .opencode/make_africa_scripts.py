from pathlib import Path

base = Path(r"W:\Legal\.opencode")
t = (base / "harvest_public_sources.py").read_text(encoding="utf-8")
t = t.replace(
    "from bolster_latam_deep import ROOT, PROFILES, TODAY, backup_if_exists",
    "from bolster_africa_full import ROOT, PROFILES, TODAY, backup_if_exists",
)
t = t.replace("if name=='US_CU_CUBA': continue", "")
t = t.replace("if name == 'US_CU_CUBA':\n        continue", "")
(base / "harvest_africa.py").write_text(t, encoding="utf-8")
t = (base / "populate_citations.py").read_text(encoding="utf-8")
t = t.replace(
    "from bolster_latam_deep import ROOT, PROFILES, TODAY, backup_if_exists, write",
    "from bolster_africa_full import ROOT, PROFILES, TODAY, backup_if_exists, write",
)
t = t.replace("if name == 'US_CU_CUBA':\n            continue", "")
(base / "populate_citations_africa.py").write_text(t, encoding="utf-8")
t = (base / "apply_citations_to_docs.py").read_text(encoding="utf-8")
t = t.replace(
    "from bolster_latam_deep import ROOT, PROFILES, TODAY, backup_if_exists, write",
    "from bolster_africa_full import ROOT, PROFILES, TODAY, backup_if_exists, write",
)
t = t.replace("if name=='US_CU_CUBA': continue", "")
(base / "apply_citations_africa.py").write_text(t, encoding="utf-8")
t = (base / "refresh_manifests.py").read_text(encoding="utf-8")
t = t.replace(
    "from bolster_latam_deep import ROOT, PROFILES, backup_if_exists",
    "from bolster_africa_full import ROOT, PROFILES, backup_if_exists",
)
t = t.replace("if name=='US_CU_CUBA': continue", "")
(base / "refresh_manifests_africa.py").write_text(t, encoding="utf-8")
print("ok")
