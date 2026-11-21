from pathlib import Path

base = Path(r"W:\Legal\.opencode")
t = (base / "bolster_latam_docx.py").read_text(encoding="utf-8")
t = t.replace(
    "from bolster_latam_deep import ROOT, PROFILES, TODAY, write",
    "from bolster_africa_full import ROOT, PROFILES, TODAY, write",
)
t = t.replace("if name=='US_CU_CUBA': continue", "")
(base / "bolster_africa_docx.py").write_text(t, encoding="utf-8")
print("ok")
