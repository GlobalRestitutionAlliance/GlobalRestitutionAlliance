from pathlib import Path
import re

p = Path(r"W:\Legal\.opencode\bolster_latam_deep.py")
s = p.read_text(encoding="utf-8")

old1 = '''## Immediate Next Actions
1. Attach primary-source citations to each instrument.
2. Validate legal theories, fora, and procedural requirements.
3. Build forensic valuation and damages model per instrument.""")
    # core legal docs
    build_doc(cdir/'01_Pleadings_and_Complaints'/f"master_federal_court_complaint_{prof['iso'].lower()}_v1.md", f"Master Federal Court Complaint - {prof['country']} (Scaffold)", prof,
              """## Parties, Jurisdiction, Venue
To be completed with verified claimant classes, defendants, jurisdictional bases, and venue analysis.

## Factual Allegations
Populate with verified, source-cited historical and contemporary facts. Do not fabricate events, citations, or damages.

## Causes of Action
To be selected after legal verification (e.g., statutory, constitutional, tort, international law domestication pathways as applicable).

## Relief Requested
Declaratory relief, damages/restitution accounting, equitable remedies, and enforcement mechanisms - all subject to evidentiary and legal validation.""")
    build_doc(cdir/'02_Discovery_and_Evidentiary'/f"discovery_plan_{prof['iso'].lower()}_v1.md", f"Discovery & Evidentiary Plan - {prof['country']}", prof,
              """## Discovery Priorities
- Identify custodians, archives, agencies, and corporate records.
- Issue preservation notices/litigation holds where appropriate.
- Map each instrument to documentary, testimonial, and expert evidence.

## Evidence Classes
- Primary government records (declassified/public archives)
- Treaty/diplomatic records
- Financial/transactional records
- Expert reports (historical, economic, forensic)""")
    build_doc(cdir/'03_Motions_and_Briefs'/f"motions_and_briefs_index_{prof['iso'].lower']}.md" if False else cdir/'03_Motions_and_Briefs'/f"motions_and_briefs_index_{prof['iso'].lower()}_v1.md", f"Motions & Briefs Index - {prof['country']}", prof,
              """## Planned Motions/Briefs
- Motion for preservation / anti-spoliation
- Motion for judicial notice / treaty recognition (as applicable)
- Opposition templates for immunity, standing, limitations, political question defenses
- Summary judgment / evidentiary motions (post-discovery)""")
    build_doc(cdir/'04_International_Tribunals'/f"international_tribunal_strategy_{prof['iso'].lower()}_v1.md", f"International Tribunal Strategy - {prof['country']}", prof,
              """## Forum Assessment
Evaluate ICJ, IACHR, UN treaty bodies, UNCITRAL/PCA, and domestic exequatur pathways based on verified facts and standing.

## Filing Readiness Checklist
- Verified claimant/standing
- Exhaustion/admissibility analysis
- Evidence authentication
- Remedies/enforcement pathway""")
    build_doc(cdir/'05_Strategic_Doctrines_and_Red_Team'/f"red_team_doctrine_{prof['iso'].lower()}_v1.md", f"Strategic Doctrine & Red Team - {prof['country']}", prof,
              """## Adversarial Stress Tests
- Sovereign immunity and act-of-state defenses
- Statute of limitations / prescription
- Causation and damages attribution
- Political question / comity
- Evidence authenticity and chain-of-custody challenges""")
    build_doc(cdir/'06_Trial_and_Appellate_Prep'/f"trial_appellate_prep_{prof['iso'].lower()}_v1.md", f"Trial & Appellate Preparation - {prof['country']}", prof,
              """## Trial Prep
- Witness/expert matrix
- Exhibit authentication plan
- Verdict/ruling theory mapping

## Appellate Prep
- Preservation checklist
- Issue framing and standard-of-review matrix
- Record build plan""")
    build_doc(cdir/'07_Enforcement_and_Restitution'/f"enforcement_restitution_plan_{prof['iso'].lower()}_v1.md", f"Enforcement & Restitution Plan - {prof['country']}", prof,
              """## Enforcement Pathways
- Domestic judgment enforcement
- Foreign recognition/exequatur
- Asset tracing and recovery
- Qualified Settlement Fund / restitution trust administration (jurisdiction-specific, legally verified)""")'''
new1 = '''## Immediate Next Actions
1. Attach primary-source citations to each instrument.
2. Validate legal theories, fora, and procedural requirements.
3. Build forensic valuation and damages model per instrument.""", cdir)
    # core legal docs
    build_doc(cdir/'01_Pleadings_and_Complaints'/f"master_federal_court_complaint_{prof['iso'].lower()}_v1.md", f"Master Federal Court Complaint - {prof['country']} (Scaffold)", prof,
              """## Parties, Jurisdiction, Venue
To be completed with verified claimant classes, defendants, jurisdictional bases, and venue analysis.

## Factual Allegations
Populate with verified, source-cited historical and contemporary facts. Do not fabricate events, citations, or damages.

## Causes of Action
To be selected after legal verification (e.g., statutory, constitutional, tort, international law domestication pathways as applicable).

## Relief Requested
Declaratory relief, damages/restitution accounting, equitable remedies, and enforcement mechanisms - all subject to evidentiary and legal validation.""", cdir)
    build_doc(cdir/'02_Discovery_and_Evidentiary'/f"discovery_plan_{prof['iso'].lower()}_v1.md", f"Discovery & Evidentiary Plan - {prof['country']}", prof,
              """## Discovery Priorities
- Identify custodians, archives, agencies, and corporate records.
- Issue preservation notices/litigation holds where appropriate.
- Map each instrument to documentary, testimonial, and expert evidence.

## Evidence Classes
- Primary government records (declassified/public archives)
- Treaty/diplomatic records
- Financial/transactional records
- Expert reports (historical, economic, forensic)""", cdir)
    build_doc(cdir/'03_Motions_and_Briefs'/f"motions_and_briefs_index_{prof['iso'].lower()}_v1.md", f"Motions & Briefs Index - {prof['country']}", prof,
              """## Planned Motions/Briefs
- Motion for preservation / anti-spoliation
- Motion for judicial notice / treaty recognition (as applicable)
- Opposition templates for immunity, standing, limitations, political question defenses
- Summary judgment / evidentiary motions (post-discovery)""", cdir)
    build_doc(cdir/'04_International_Tribunals'/f"international_tribunal_strategy_{prof['iso'].lower()}_v1.md", f"International Tribunal Strategy - {prof['country']}", prof,
              """## Forum Assessment
Evaluate ICJ, IACHR, UN treaty bodies, UNCITRAL/PCA, and domestic exequatur pathways based on verified facts and standing.

## Filing Readiness Checklist
- Verified claimant/standing
- Exhaustion/admissibility analysis
- Evidence authentication
- Remedies/enforcement pathway""", cdir)
    build_doc(cdir/'05_Strategic_Doctrines_and_Red_Team'/f"red_team_doctrine_{prof['iso'].lower()}_v1.md", f"Strategic Doctrine & Red Team - {prof['country']}", prof,
              """## Adversarial Stress Tests
- Sovereign immunity and act-of-state defenses
- Statute of limitations / prescription
- Causation and damages attribution
- Political question / comity
- Evidence authenticity and chain-of-custody challenges""", cdir)
    build_doc(cdir/'06_Trial_and_Appellate_Prep'/f"trial_appellate_prep_{prof['iso'].lower()}_v1.md", f"Trial & Appellate Preparation - {prof['country']}", prof,
              """## Trial Prep
- Witness/expert matrix
- Exhibit authentication plan
- Verdict/ruling theory mapping

## Appellate Prep
- Preservation checklist
- Issue framing and standard-of-review matrix
- Record build plan""", cdir)
    build_doc(cdir/'07_Enforcement_and_Restitution'/f"enforcement_restitution_plan_{prof['iso'].lower()}_v1.md", f"Enforcement & Restitution Plan - {prof['country']}", prof,
              """## Enforcement Pathways
- Domestic judgment enforcement
- Foreign recognition/exequatur
- Asset tracing and recovery
- Qualified Settlement Fund / restitution trust administration (jurisdiction-specific, legally verified)""", cdir)'''
if old1 not in s:
    raise SystemExit("old1 not found")
s = s.replace(old1, new1)

# add module-level current country dir for build_antigravity write calls
s = s.replace(
    "def write(p: Path, content: str, country_dir: Path = None):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    if country_dir is not None:\n        backup_if_exists(p, country_dir)\n    p.write_text(content, encoding='utf-8', newline='\\n')",
    """_CURRENT_COUNTRY_DIR = None

def write(p: Path, content: str, country_dir: Path = None):
    global _CURRENT_COUNTRY_DIR
    if country_dir is None:
        country_dir = _CURRENT_COUNTRY_DIR
    p.parent.mkdir(parents=True, exist_ok=True)
    if country_dir is not None:
        backup_if_exists(p, country_dir)
    p.write_text(content, encoding='utf-8', newline='\\n')""",
    1,
)

s = s.replace(
    "def build_antigravity(country_dir: Path, name: str, prof: dict):\n    ag = country_dir / '.antigravity'",
    """def build_antigravity(country_dir: Path, name: str, prof: dict):
    global _CURRENT_COUNTRY_DIR
    _CURRENT_COUNTRY_DIR = country_dir
    ag = country_dir / '.antigravity\'""",
    1,
)

# reset at end of build_country
s = s.replace(
    "    build_antigravity(cdir, name, prof)\n\ndef main():",
    """    build_antigravity(cdir, name, prof)
    global _CURRENT_COUNTRY_DIR
    _CURRENT_COUNTRY_DIR = None

def main():""",
    1,
)

p.write_text(s, encoding="utf-8")
print("patched")
