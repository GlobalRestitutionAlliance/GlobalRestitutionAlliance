import re
from pathlib import Path

ROOT = Path(r"W:\Legal\LATIN_AMERICA")

# Metadata from .github/profile/README.md (Latin America table)
PROFILE = {
    "US_AG_ANTIGUA_AND_BARBUDA": {
        "country": "Antigua & Barbuda",
        "iso": "AG",
        "pool": "$2B",
        "issues": "Climate, offshore",
    },
    "US_AR_ARGENTINA": {
        "country": "Argentina",
        "iso": "AR",
        "pool": "$100B",
        "issues": "Dirty War, debt",
    },
    "US_BB_BARBADOS": {
        "country": "Barbados",
        "iso": "BB",
        "pool": "$5B",
        "issues": "Climate, republic",
    },
    "US_BO_BOLIVIA": {
        "country": "Bolivia",
        "iso": "BO",
        "pool": "$20B",
        "issues": "Indigenous rights, gas",
    },
    "US_BR_BRAZIL": {
        "country": "Brazil",
        "iso": "BR",
        "pool": "$200B",
        "issues": "Amazon, dictatorship",
    },
    "US_BS_BAHAMAS": {
        "country": "Bahamas",
        "iso": "BS",
        "pool": "$15B",
        "issues": "Tourism, tax haven",
    },
    "US_BZ_BELIZE": {
        "country": "Belize",
        "iso": "BZ",
        "pool": "$3B",
        "issues": "Guatemala claim",
    },
    "US_CL_CHILE": {
        "country": "Chile",
        "iso": "CL",
        "pool": "$60B",
        "issues": "Pinochet, neoliberalism",
    },
    "US_CO_COLOMBIA": {
        "country": "Colombia",
        "iso": "CO",
        "pool": "$80B",
        "issues": "Conflict, coca",
    },
    "US_CR_COSTA_RICA": {
        "country": "Costa Rica",
        "iso": "CR",
        "pool": "$25B",
        "issues": "No military, environment",
    },
    "US_CU_CUBA": {
        "country": "Cuba",
        "iso": "CU",
        "pool": "$30B",
        "issues": "Embargo, sovereignty",
    },
    "US_DM_DOMINICA": {
        "country": "Dominica",
        "iso": "DM",
        "pool": "$2B",
        "issues": "Climate, hurricanes",
    },
    "US_DO_DOMINICAN_REPUBLIC": {
        "country": "Dominican Republic",
        "iso": "DO",
        "pool": "$30B",
        "issues": "Haiti border, sugar",
    },
    "US_EC_ECUADOR": {
        "country": "Ecuador",
        "iso": "EC",
        "pool": "$40B",
        "issues": "Oil, Rights of Nature",
    },
    "US_GD_GRENADA": {
        "country": "Grenada",
        "iso": "GD",
        "pool": "$2B",
        "issues": "US invasion 1983",
    },
    "US_GT_GUATEMALA": {
        "country": "Guatemala",
        "iso": "GT",
        "pool": "$30B",
        "issues": "Genocide, civil war",
    },
    "US_GY_GUYANA": {
        "country": "Guyana",
        "iso": "GY",
        "pool": "$20B",
        "issues": "Oil, Venezuela border",
    },
    "US_HN_HONDURAS": {
        "country": "Honduras",
        "iso": "HN",
        "pool": "$15B",
        "issues": "Coup, migration",
    },
    "US_HT_HAITI": {
        "country": "Haiti",
        "iso": "HT",
        "pool": "$15B",
        "issues": "First republic, occupation",
    },
    "US_JM_JAMAICA": {
        "country": "Jamaica",
        "iso": "JM",
        "pool": "$20B",
        "issues": "Reparations, debt",
    },
    "US_KN_SAINT_KITTS_AND_NEVIS": {
        "country": "Saint Kitts & Nevis",
        "iso": "KN",
        "pool": "$2B",
        "issues": "Citizenship by investment",
    },
    "US_LC_SAINT_LUCIA": {
        "country": "Saint Lucia",
        "iso": "LC",
        "pool": "$2B",
        "issues": "Tourism, climate",
    },
    "US_MX_MEXICO": {
        "country": "Mexico",
        "iso": "MX",
        "pool": "$150B",
        "issues": "Drug war, NAFTA",
    },
    "US_NI_NICARAGUA": {
        "country": "Nicaragua",
        "iso": "NI",
        "pool": "$15B",
        "issues": "Contra war, Ortega",
    },
    "US_PA_PANAMA": {
        "country": "Panama",
        "iso": "PA",
        "pool": "$25B",
        "issues": "Canal, invasion",
    },
    "US_PE_PERU": {
        "country": "Peru",
        "iso": "PE",
        "pool": "$50B",
        "issues": "Fujimori, Sendero",
    },
    "US_PR_PUERTO_RICO": {
        "country": "Puerto Rico",
        "iso": "PR",
        "pool": "$100B",
        "issues": "Territory, PROMESA, Maria",
    },
    "US_PY_PARAGUAY": {
        "country": "Paraguay",
        "iso": "PY",
        "pool": "$15B",
        "issues": "Hydro, Stroessner",
    },
    "US_SR_SURINAME": {
        "country": "Suriname",
        "iso": "SR",
        "pool": "$10B",
        "issues": "Bauxite, coups",
    },
    "US_SV_EL_SALVADOR": {
        "country": "El Salvador",
        "iso": "SV",
        "pool": "$15B",
        "issues": "Civil war, gangs",
    },
    "US_TT_TRINIDAD_AND_TOBAGO": {
        "country": "Trinidad & Tobago",
        "iso": "TT",
        "pool": "$30B",
        "issues": "Oil/gas, crime",
    },
    "US_UY_URUGUAY": {
        "country": "Uruguay",
        "iso": "UY",
        "pool": "$25B",
        "issues": "Stable democracy",
    },
    "US_VC_SAINT_VINCENT_AND_THE_GRENADINES": {
        "country": "Saint Vincent & the Grenadines",
        "iso": "VC",
        "pool": "$2B",
        "issues": "Volcano, climate",
    },
    "US_VE_VENEZUELA": {
        "country": "Venezuela",
        "iso": "VE",
        "pool": "$80B",
        "issues": "Oil, sanctions",
    },
}


def repo_slug(name: str) -> str:
    parts = name.split("_")
    iso = parts[1].lower()
    rest = "-".join(p.lower() for p in parts[2:])
    return f"latam-{iso}-{rest}-master-litigation"


def parse_manifest(country_dir: Path):
    p = country_dir / "Master_Armory_Manifest.md"
    if not p.exists():
        return {}
    txt = p.read_text(encoding="utf-8", errors="ignore")
    out = {}
    m = re.search(r"Total Actionable Instruments:\**\s*([^\n|]+)", txt, re.I)
    if m:
        out["instruments"] = m.group(1).strip().strip("*` ")
    m = re.search(r"Total Restitution Pool:\**\s*([^\n|]+)", txt, re.I)
    if m:
        out["pool"] = m.group(1).strip().strip("*` ")
    m = re.search(r"Autonomous Legal Agents:\**\s*([^\n|]+)", txt, re.I)
    if m:
        out["agents"] = m.group(1).strip().strip("*` ")
    m = re.search(r"Certified Procedural Skills:\**\s*([^\n|]+)", txt, re.I)
    if m:
        out["skills"] = m.group(1).strip().strip("*` ")
    return out


def has_rich_readme(txt: str) -> bool:
    # Cuba is the gold standard; skip only Cuba explicitly.
    return False


def build_readme(name: str, meta: dict) -> str:
    country = meta["country"]
    iso = meta["iso"]
    slug = repo_slug(name)
    cdir = ROOT / name
    m = parse_manifest(cdir)
    pool = m.get("pool") or meta["pool"]
    instruments = m.get("instruments") or "Scaffold in development"
    agents = m.get("agents") or "Scaffold in development"
    skills = m.get("skills") or "Scaffold in development"
    issues = meta["issues"]
    return f"""# US-{iso} {country.upper()} MASTER LITIGATION: INSTITUTIONAL RESTITUTION FRAMEWORK
[![Integrity Verification](https://github.com/GlobalRestitutionAlliance/{slug}/actions/workflows/integrity-verification.yml/badge.svg)](https://github.com/GlobalRestitutionAlliance/{slug}/actions/workflows/integrity-verification.yml)
[![Decentralized Mirror Sync](https://github.com/GlobalRestitutionAlliance/{slug}/actions/workflows/mirror-sync.yml/badge.svg)](https://github.com/GlobalRestitutionAlliance/{slug}/actions/workflows/mirror-sync.yml)
[![Jurisdiction](https://img.shields.io/badge/Jurisdiction-{country.replace(" ", "%20").replace("&", "%26")}-blue.svg)](README.md)
[![Restitution Pool](https://img.shields.io/badge/Restitution_Pool-{str(pool).replace(" ", "%20").replace("$", "%24").replace(",", "%2C")}-brightgreen.svg)](00_Master_Knowledge_Base/)
[![Status](https://img.shields.io/badge/Status-Active_Scaffold-orange.svg)](Master_Armory_Manifest.md)

A decentralized, cryptographically-verifiable legal and historical repository for the **United States–{country}** restitution campaign, maintained by the Global Restitution Alliance. This repository is structured to the Cuba campaign template standard and is being progressively bolstered with country-specific instruments, evidence, and enforcement workflows.

---

## 1. Project Overview & Legal Mission

The **US-{iso} {country} Master Litigation** repository is an institutional legal research, coordination, and enforcement scaffold designed to:

1. **Document Historical & Modern Liability:** Build an auditable evidentiary record of actionable harms, treaty breaches, fiduciary failures, and commercial expropriations relevant to US–{country} relations.
2. **Coordinate Multi-Jurisdictional Enforcement:** Prepare pleadings, discovery, and enforcement materials for domestic, foreign, and international fora as claims mature.
3. **Establish Accountability & Restitution Pathways:** Map claim vectors to legal instruments, evidentiary support, and restitution/disgorgement mechanisms.
4. **Preserve Integrity & Chain of Custody:** Maintain cryptographic manifests, signed commits, and immutable audit logs for all evidentiary artifacts.

**Key Issues (Profile Baseline):** {issues}

---

## 2. Current Operational Metrics

| Operational Metric | Current Status | Verification Reference |
|:---|:---:|:---|
| **Actionable Instruments** | **{instruments}** | [`Master_Armory_Manifest.md`](Master_Armory_Manifest.md) |
| **Target Restitution Pool** | **{pool}** | [`00_Master_Knowledge_Base/`](00_Master_Knowledge_Base/) |
| **Autonomous Legal Agents** | **{agents}** | [`.antigravity/agents/`](.antigravity/agents/) |
| **Certified Procedural Skills** | **{skills}** | [`.antigravity/skills/`](.antigravity/skills/) |
| **Integrity Hash Manifest** | **Tracked** | [`VERIFICATION_KEYS/sha256_manifest.txt`](VERIFICATION_KEYS/sha256_manifest.txt) |
| **Audit / Expansion Log** | **Active** | [`Expansion_and_Audit_Log.md`](Expansion_and_Audit_Log.md) |

> Metrics are synchronized from repository manifests where present. Values marked "Scaffold in development" indicate active bolstering in progress.

---

## 3. Repository Structure

```text
{slug}/
├── .antigravity/                      # Agents, skills, tools, workflows, rules, knowledge
├── .github/                           # CI integrity verification, templates, CODEOWNERS
├── 00_Master_Knowledge_Base/          # Crosswalk matrices, dashboards, dossiers
├── 01_Pleadings_and_Complaints/       # Complaints, petitions, filings
├── 02_Discovery_and_Evidentiary/      # Discovery, subpoenas, evidentiary records
├── 03_Evidentiary_Exhibits/           # Certified exhibits and source documents
├── 03_Motions_and_Briefs/             # Motions, briefs, oppositions
├── 04_International_Tribunals/        # ICJ/IACHR/UN/arbitral submissions
├── 05_Strategic_Doctrines_and_Red_Team/ # Risk analysis, doctrine, counter-arguments
├── 06_Trial_and_Appellate_Prep/       # Trial/appellate preparation materials
├── 07_Enforcement_and_Restitution/    # Enforcement, QSF, garnishment, distribution
├── 99_Archives_and_Manifests/         # Archives, manifests, audit artifacts
├── VERIFICATION_KEYS/                 # SHA-256 manifests and verification keys
├── Master_Armory_Manifest.md          # Instrument inventory
├── Expansion_and_Audit_Log.md         # Campaign audit history
├── Master_Chain_of_Custody_Log.md     # Custody/integrity log
├── GOVERNANCE.md                      # Maintainer council and protocol
└── MANIFESTO.md                       # Campaign principles and scope
```

---

## 4. Core Jurisprudential & Enforcement Pillars

1. **Evidentiary Rigor:** Every claim vector must map to primary sources, authenticated records, or adjudicated findings.
2. **Procedural Integrity:** Filings and research outputs must follow applicable procedural rules and tribunal standards.
3. **Sovereign & Commercial Accountability:** Apply applicable immunity exceptions, alter-ego/agency theories, and enforcement mechanisms where legally supported.
4. **Restitution Architecture:** Recovered assets should be administered through transparent, court-supervised or legally compliant restitution mechanisms.
5. **Cryptographic Verification:** All critical artifacts are tracked by SHA-256 manifests and auditable version control.

---

## 5. Verification & Integrity

```bash
# Verify SHA-256 integrity (when manifest is populated)
sha256sum -c VERIFICATION_KEYS/sha256_manifest.txt --strict

# Confirm repository status
git status
```

---

## 6. Governance & Participation

- Governance: [`GOVERNANCE.md`](GOVERNANCE.md)
- Contributions: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Security: [`SECURITY.md`](SECURITY.md)
- Manifesto: [`MANIFESTO.md`](MANIFESTO.md)

---

*Maintained under the authority of the Global Restitution Alliance Maintainer Council. This repository is a legal research and litigation scaffold; it does not constitute legal advice.*
"""


def main():
    updated = []
    skipped = []
    for name, meta in PROFILE.items():
        if name == "US_CU_CUBA":
            skipped.append(name)
            continue
        cdir = ROOT / name
        if not cdir.exists():
            skipped.append(name + " (missing)")
            continue
        readme = cdir / "README.md"
        content = build_readme(name, meta)
        readme.write_text(content, encoding="utf-8", newline="\n")
        updated.append(name)
    print(f"UPDATED={len(updated)}")
    print(f"SKIPPED={len(skipped)}")
    for n in updated:
        print(n)


if __name__ == "__main__":
    main()
