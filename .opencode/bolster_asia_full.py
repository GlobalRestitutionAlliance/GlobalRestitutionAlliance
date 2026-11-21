import csv, datetime, hashlib, json, os, re, shutil
from pathlib import Path

TODAY = datetime.date.today().isoformat()
ROOT = Path(r"W:\Legal\ASIA")
BACKUP = "99_Archives_and_Manifests/pre_bolster_backup"


# Generic safe anchors - verification required. No fabricated citations.
def make_profile(name):
    m = re.match(r"US_([A-Z]{2})_(.+)", name)
    iso = m.group(1) if m else "XX"
    country = m.group(2).replace("_", " ").title() if m else name
    return {
        "iso": iso,
        "country": country,
        "issue": "Historical intervention, resource extraction, economic coercion, governance impacts - verification required",
        "instruments": "UN Charter; African Charter on Human and Peoples' Rights; relevant bilateral treaties (verify)",
        "anchors": [
            f"UN/OHCHR country documentation for {country} (verify)",
            f"US State Department human rights/reporting for {country} (verify)",
            f"African Union / regional records (verify)",
        ],
    }


PROFILES = {d.name: make_profile(d.name) for d in sorted(ROOT.iterdir()) if d.is_dir()}

DIRS = [
    ".antigravity/agents",
    ".antigravity/skills",
    ".antigravity/workflows",
    ".antigravity/rules",
    ".antigravity/templates",
    ".antigravity/tools",
    ".antigravity/knowledge",
    ".antigravity/datasets",
    ".antigravity/vector-index",
    ".antigravity/knowledge/vector-index",
    ".github/workflows",
    ".github/ISSUE_TEMPLATE",
    "00_Master_Knowledge_Base",
    "01_Pleadings_and_Complaints",
    "02_Discovery_and_Evidentiary",
    "03_Evidentiary_Exhibits",
    "03_Evidentiary_Exhibits/Immutable_Ledger",
    "03_Motions_and_Briefs",
    "04_International_Tribunals",
    "05_Strategic_Doctrines_and_Red_Team",
    "06_Trial_and_Appellate_Prep",
    "07_Enforcement_and_Restitution",
    "99_Archives_and_Manifests",
    "VERIFICATION_KEYS",
]


def backup_if_exists(path, cdir):
    if not path.exists():
        return
    b = cdir / BACKUP
    b.mkdir(parents=True, exist_ok=True)
    dest = b / path.name
    if not dest.exists():
        shutil.copy2(path, dest)


def write(path, content, cdir):
    path.parent.mkdir(parents=True, exist_ok=True)
    backup_if_exists(path, cdir)
    path.write_text(content, encoding="utf-8", newline="\n")


def sha256(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def ci_workflows(cdir, iso, country):
    wf = cdir / ".github/workflows/integrity-verification.yml"
    write(
        wf,
        f"""name: Evidentiary Integrity Verification
on:
  push:
  pull_request:
jobs:
  verify-hashes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Verify SHA-256 Manifest
        run: |
          cd "$GITHUB_WORKSPACE"
          if [ -f VERIFICATION_KEYS/sha256_manifest.txt ]; then
            sha256sum -c VERIFICATION_KEYS/sha256_manifest.txt
          else
            echo "No manifest found" && exit 1
          fi
""",
        cdir,
    )
    wf2 = cdir / ".github/workflows/mirror-sync.yml"
    write(
        wf2,
        f"""name: Decentralized Mirror Synchronization
on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:
jobs:
  mirror:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Push to GitLab Mirror
        if: env.GITLAB_TOKEN != ''
        run: |
          git remote add gitlab https://oauth2:${{{{ secrets.GITLAB_MIRROR_TOKEN }}}}@gitlab.com/GlobalRestitutionAlliance/asia-{iso.lower()}-{country.lower().replace(" ", "-")}.git || true
          git push gitlab main --tags --force
        env:
          GITLAB_TOKEN: ${{{{ secrets.GITLAB_MIRROR_TOKEN }}}}
      - name: Push to Codeberg Mirror
        if: env.CODEBERG_TOKEN != ''
        run: |
          git remote add codeberg https://${{{{ secrets.CODEBERG_MIRROR_TOKEN }}}}@codeberg.org/GlobalRestitutionAlliance/asia-{iso.lower()}-{country.lower().replace(" ", "-")}.git || true
          git push codeberg main --tags --force
        env:
          CODEBERG_TOKEN: ${{{{ secrets.CODEBERG_MIRROR_TOKEN }}}}
""",
        cdir,
    )


def antigravity(cdir, name, prof):
    iso = prof["iso"]
    country = prof["country"]
    ag = cdir / ".antigravity"
    # simple but substantial registries
    agents = []
    for i in range(1, 171):
        agents.append(
            {
                "id": f"agent_{iso.lower()}_{i:03d}",
                "name": f"{country} Agent {i:03d}",
                "status": "ACTIVE_SCAFFOLD",
                "role": "verification-required scaffold agent",
                "scope": name,
            }
        )
    skills = []
    for i in range(1, 253):
        skills.append(
            {
                "id": f"skill_{iso.lower()}_{i:03d}",
                "name": f"{country} Skill {i:03d}",
                "status": "ACTIVE_SCAFFOLD",
                "scope": name,
            }
        )
    write(
        ag / "project.yaml",
        f"name: {name}\ncountry: {country}\niso: {iso}\nstatus: SCAFFOLD_FRAMEWORK\ntemplate: LATIN_AMERICA/US_CU_CUBA\ngenerated: {TODAY}\n",
        cdir,
    )
    write(
        ag / "agents/agent-registry.yaml",
        "agents:\n"
        + "".join(
            [
                f"  - id: {a['id']}\n    name: {a['name']}\n    status: {a['status']}\n"
                for a in agents
            ]
        ),
        cdir,
    )
    write(
        ag / "skills/skill-registry.yaml",
        "skills:\n"
        + "".join(
            [
                f"  - id: {s['id']}\n    name: {s['name']}\n    status: {s['status']}\n"
                for s in skills
            ]
        ),
        cdir,
    )
    # vector index
    vec = cdir / ".antigravity/vector-index"
    vec.mkdir(parents=True, exist_ok=True)
    lines = [
        f"VID-{iso}-{i:04d}|{name}|scaffold|verification-required|{TODAY}"
        for i in range(1, 1806)
    ]
    (vec / "asia_vector_index.jsonl").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )


def sources(cdir, prof):
    iso = prof["iso"]
    country = prof["country"]
    rows = [
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "UN Digital Library - Search",
            "https://digitallibrary.un.org/search",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "UN OHCHR - Country Page",
            "https://www.ohchr.org/en/countries",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "UN Human Rights Council - UPR",
            "https://www.ohchr.org/en/hr-bodies/upr/upr-home",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "African Union",
            "https://au.int/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "US State Dept Human Rights Reports",
            "https://www.state.gov/reports-bureau-of-democracy-human-rights-and-labor/country-reports-on-human-rights-practices/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "US State Dept Office of the Historian (FRUS)",
            "https://history.state.gov/historicaldocuments",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "NARA Foreign Affairs Research",
            "https://www.archives.gov/research/foreign-policy",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "CIA FOIA Reading Room",
            "https://www.cia.gov/reading-room/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "World Bank Country Data",
            "https://data.worldbank.org/country",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "UN Treaty Collection",
            "https://treaties.un.org/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "ICJ Cases",
            "https://www.icj-cij.org/cases",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "African Commission on Human and Peoples Rights",
            "https://achpr.au.int/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
    ]
    ex = cdir / "03_Evidentiary_Exhibits"
    ex.mkdir(parents=True, exist_ok=True)
    with (ex / "PRIMARY_PUBLIC_SOURCES.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f)
        w.writerow(
            ["iso", "country", "source_type", "title", "url", "access_class", "status"]
        )
        w.writerows(rows)
    md = [
        f"# Primary Public Sources - {country} ({iso})",
        "",
        f"Generated: {TODAY}",
        "Status: Public-source registry. Links require verification before evidentiary use.",
        "",
    ]
    for _, _, _, t, u, _, _ in rows:
        md.append(f"- [{t}]({u})")
    md.append(
        "\n## Rule\nNo fabricated citations. No authenticated evidence claims without provenance review."
    )
    write(ex / "PRIMARY_PUBLIC_SOURCES.md", "\n".join(md) + "\n", cdir)
    write(
        cdir / "00_Master_Knowledge_Base/PRIMARY_PUBLIC_SOURCES.md",
        "\n".join(md) + "\n",
        cdir,
    )
    write(
        ex / "EVIDENCE_INTAKE_LOG.md",
        f"# Evidence Intake Log - {country}\n\n| Date | Artifact | Source URL | Retrieved By | SHA-256 | Custody Status | Notes |\n|---|---|---|---|---|---|---|\n\n## Intake Rules\n- Record source URL, access date, downloader, file hash, and storage path.\n- No authenticated claim without custodian/legal review.\n",
        cdir,
    )


def legal_framework(cdir, prof):
    iso = prof["iso"]
    country = prof["country"]
    write(
        cdir / "99_Archives_and_Manifests/LEGAL_ACCURACY_REVIEW_CHECKLIST.md",
        f"""# Legal Accuracy Review Checklist - {country} ({iso})

**Generated:** {TODAY}
**Status:** FRAMEWORK TEMPLATE - FOR QUALIFIED COUNSEL/ORGANIZATION TAILORING. Not legal advice.

## Precedent/Framework Starting Points (VERIFY)
- FSIA: 28 U.S.C. §§ 1604-1607 (verify exceptions/applicability)
- ATS scope: *Sosa v. Alvarez-Machain*, 542 U.S. 692 (2004); *Kiobel*, 569 U.S. 108 (2013); *Jesner*, 584 U.S. 241 (2018) - verify current applicability
- FSIA/expropriation: *Republic of Austria v. Altmann*, 541 U.S. 677 (2004); *Bolivarian Republic of Venezuela v. Helmerich & Payne*, 581 U.S. 170 (2017) - verify
- Standing/jurisdiction: *Lujan*, *Daimler*, *International Shoe* - verify
- African Charter / AU instruments / UN treaties - verify primary texts

## Checklist
- [ ] Jurisdiction/standing
- [ ] Immunity (FSIA/sovereign)
- [ ] Limitations/prescription
- [ ] Causation/damages
- [ ] Forum compliance
- [ ] Evidence authentication/chain of custody
- [ ] Counsel/organization sign-off before filing
""",
        cdir,
    )
    write(
        cdir / "03_Evidentiary_Exhibits/AUTHENTICATION_DECLARATION_TEMPLATE.md",
        f"""# Authentication & Chain-of-Custody Declaration Template - {country} ({iso})

**TEMPLATE FOR COUNSEL/ORGANIZATION USE.** Not executed. Not notarized. Not legal advice.

- Declarant / role / organization / date
- Exhibit ID / file / SHA-256 / bytes
- Source URL / final URL / capture date / method
- Custody history / access controls / hash verification
- Authentication basis (certified copy, official publication, witnessed capture, etc.)
- Signature / jurisdiction / date
""",
        cdir,
    )
    write(
        cdir / "99_Archives_and_Manifests/FILING_GRADE_PACKAGE_INDEX.md",
        f"""# Filing-Grade Package Index - {country} ({iso})

**Generated:** {TODAY}
**Status:** FRAMEWORK/SCAFFOLD - for counsel/organization tailoring. Not filing-ready without verification.

| Component | Path | Status |
|---|---|---|
| Complaint scaffold | `01_Pleadings_and_Complaints/master_federal_court_complaint_{iso.lower()}_v1.docx` | SCAFFOLD |
| Discovery scaffold | `02_Discovery_and_Evidentiary/discovery_plan_{iso.lower()}_v1.docx` | SCAFFOLD |
| Motions scaffold | `03_Motions_and_Briefs/motion_package_{iso.lower()}_v1.docx` | SCAFFOLD |
| Tribunal scaffold | `04_International_Tribunals/tribunal_submission_{iso.lower()}_v1.docx` | SCAFFOLD |
| Enforcement scaffold | `07_Enforcement_and_Restitution/enforcement_restitution_{iso.lower()}_v1.docx` | SCAFFOLD |
| Evidence index | `03_Evidentiary_Exhibits/CITATION_INDEX.csv` | PENDING_LEGAL_REVIEW |
""",
        cdir,
    )


def docs(cdir, prof):
    iso = prof["iso"]
    country = prof["country"]
    write(
        cdir / "README.md",
        f"""# {country} ({iso}) - US-{iso} Restitution & Reparations Framework

**Template baseline:** LATIN_AMERICA/US_CU_CUBA (adapted for ASIA)  
**Status:** Framework/Scaffold - for counsel/organization tailoring  
**Generated:** {TODAY}

## Scope
- Campaign: `US_{iso}_{country.replace(" ", "_").upper()}`
- Primary issues (verification required): {prof["issue"]}
- Instrument anchors (verification required): {prof["instruments"]}

## Guardrails
- No fabricated citations, docket numbers, archival IDs, or authenticated-evidence claims.
- Public captures are `PUBLIC_CAPTURE_UNAUTHENTICATED` until custodian/legal authentication.
- No citation marked `VERIFIED` without local hashed source artifact + human sign-off.

## Key Paths
- `00_Master_Knowledge_Base/` - crosswalks, dossiers, source registries
- `01`-`07` - pleadings, discovery, motions, tribunals, strategy, trial/appellate, enforcement
- `03_Evidentiary_Exhibits/` - source registries, intake logs, immutable ledger, citation index
- `99_Archives_and_Manifests/` - review checklists, filing package index
- `VERIFICATION_KEYS/sha256_manifest.txt` - integrity manifest
""",
        cdir,
    )
    write(
        cdir / "Master_Armory_Manifest.md",
        f"""# Master Armory Manifest - {country} ({iso})

**Generated:** {TODAY}
**Status:** SCAFFOLD - verification required. No fabricated citations.

## Campaign
- Country: {country}
- ISO: {iso}
- Primary issues (verify): {prof["issue"]}
- Instrument anchors (verify): {prof["instruments"]}

## Verification Gates
- All claims require primary-source verification.
- All citations require local hashed artifacts and human sign-off before VERIFIED status.
""",
        cdir,
    )
    # basic crosswalk
    kb = cdir / "00_Master_Knowledge_Base"
    kb.mkdir(parents=True, exist_ok=True)
    with (
        kb
        / f"Master_US_{iso}_{country.replace(' ', '_')}_Restitution_Crosswalk_Matrix.csv"
    ).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "instrument_id",
                "issue",
                "anchor",
                "source_type",
                "verification_status",
                "notes",
            ]
        )
        for i, a in enumerate(prof["anchors"], 1):
            w.writerow(
                [
                    f"{iso}-A-{i:03d}",
                    prof["issue"],
                    a,
                    "PUBLIC_RECORD",
                    "PENDING_PRIMARY_SOURCE",
                    "Verify with primary source and counsel review",
                ]
            )
    # 01-07 minimal scaffolds
    for folder, fn, title in [
        (
            "01_Pleadings_and_Complaints",
            f"master_federal_court_complaint_{iso.lower()}_v1.md",
            f"Master Federal Court Complaint - {country}",
        ),
        (
            "02_Discovery_and_Evidentiary",
            f"discovery_plan_{iso.lower()}_v1.md",
            f"Discovery Plan - {country}",
        ),
        (
            "03_Motions_and_Briefs",
            f"motion_package_{iso.lower()}_v1.md",
            f"Motions Package - {country}",
        ),
        (
            "04_International_Tribunals",
            f"tribunal_submission_{iso.lower()}_v1.md",
            f"Tribunal Submission - {country}",
        ),
        (
            "05_Strategic_Doctrines_and_Red_Team",
            f"red_team_doctrine_{iso.lower()}_v1.md",
            f"Red Team Doctrine - {country}",
        ),
        (
            "06_Trial_and_Appellate_Prep",
            f"trial_appellate_prep_{iso.lower()}_v1.md",
            f"Trial & Appellate Prep - {country}",
        ),
        (
            "07_Enforcement_and_Restitution",
            f"enforcement_restitution_{iso.lower()}_v1.md",
            f"Enforcement & Restitution - {country}",
        ),
    ]:
        write(
            cdir / folder / fn,
            f"# {title}\n\n**Generated:** {TODAY}\n**Status:** SCAFFOLD - verification required. Not legal advice. No fabricated citations.\n\n## Framework\n- Identify verified facts from local hashed artifacts in `03_Evidentiary_Exhibits/Immutable_Ledger/`.\n- Populate jurisdiction/standing/immunity/limitations/damages with counsel review.\n- Keep all citations `PENDING_LEGAL_REVIEW` until human sign-off.\n",
            cdir,
        )


def refresh_manifest(cdir):
    manifest = cdir / "VERIFICATION_KEYS/sha256_manifest.txt"
    manifest.parent.mkdir(parents=True, exist_ok=True)
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


def main():
    for name, prof in PROFILES.items():
        cdir = ROOT / name
        for d in DIRS:
            (cdir / d).mkdir(parents=True, exist_ok=True)
        ci_workflows(cdir, prof["iso"], prof["country"])
        antigravity(cdir, name, prof)
        sources(cdir, prof)
        legal_framework(cdir, prof)
        docs(cdir, prof)
        refresh_manifest(cdir)
        print("OK", name)
    print("DONE", len(PROFILES))


if __name__ == "__main__":
    main()
