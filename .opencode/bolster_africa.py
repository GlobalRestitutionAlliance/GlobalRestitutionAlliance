import csv, datetime, hashlib, re, shutil
from pathlib import Path

TODAY = datetime.date.today().isoformat()
ROOT = Path(r"W:\Legal\AFRICA")

# High-level, publicly known anchors only. All require verification before legal reliance.
PROFILES = {
    "US_AO_ANGOLA": {
        "iso": "AO",
        "country": "Angola",
        "pool": "250000000000",
        "issue": "Cold War proxy intervention, covert support to armed factions, resource extraction legacies",
        "instruments": "UN Charter; ICJ principles; AU human rights instruments; IACHR/African Charter (verify)",
        "anchors": [
            "Portuguese colonial legacy and independence war (public record)",
            "Cold War-era external intervention and covert operations (public record - verify specifics)",
            "Oil/diamond/resource concession and conflict-economy harms (verify)",
        ],
    },
    "US_ZA_SOUTH_AFRICA": {
        "iso": "ZA",
        "country": "South Africa",
        "pool": "250000000000",
        "issue": "Apartheid-era sanctions, corporate complicity, transitional justice restitution gaps",
        "instruments": "UN apartheid conventions; TRC records; constitutional restitution framework (verify)",
        "anchors": [
            "UN apartheid-era measures (public record)",
            "Truth and Reconciliation Commission findings (public record - verify)",
            "Corporate/state complicity claims (verify)",
        ],
    },
    "US_CD_CONGO_DEMOCRATIC_REPUBLIC_OF_THE": {
        "iso": "CD",
        "country": "Democratic Republic of the Congo",
        "pool": "300000000000",
        "issue": "Colonial extraction, Cold War intervention, conflict minerals and stabilization harms",
        "instruments": "UN Charter; ICJ Armed Activities on the Territory of the Congo (DRC v. Uganda) - verify; African Charter",
        "anchors": [
            "Colonial extraction legacy (public record)",
            "ICJ Armed Activities (DRC v. Uganda) - verify",
            "Conflict minerals/resource governance harms (verify)",
        ],
    },
    "US_ET_ETHIOPIA": {
        "iso": "ET",
        "country": "Ethiopia",
        "pool": "150000000000",
        "issue": "Cold War alignment shifts, security assistance, humanitarian and conflict impacts",
        "instruments": "UN Charter; AU Constitutive Act; Geneva Conventions (verify)",
        "anchors": [
            "Cold War-era security alignments (public record)",
            "Humanitarian/security assistance impacts (verify)",
        ],
    },
    "US_NG_NIGERIA": {
        "iso": "NG",
        "country": "Nigeria",
        "pool": "250000000000",
        "issue": "Oil extraction, environmental harms, security partnerships, governance impacts",
        "instruments": "African Charter on Human and Peoples' Rights; UN Guiding Principles on Business and Human Rights (verify)",
        "anchors": [
            "Niger Delta environmental harm/public record litigation (verify specifics)",
            "Oil/resource governance and security partnerships (verify)",
        ],
    },
}

GENERIC_ISSUE = "Historical intervention, economic coercion, resource extraction, and governance impacts requiring verification"
GENERIC_INSTRUMENTS = "UN Charter; African Charter on Human and Peoples' Rights; relevant bilateral treaties (verify)"
GENERIC_ANCHORS = [
    "Publicly documented bilateral/regional history (verify)",
    "UN/OAU/AU records where applicable (verify)",
    "National archives and treaty texts (verify)",
]


def ensure_profile(name):
    if name in PROFILES:
        return PROFILES[name]
    m = re.match(r"US_([A-Z]{2})_(.+)", name)
    iso = m.group(1) if m else "XX"
    country = m.group(2).replace("_", " ").title() if m else name
    return {
        "iso": iso,
        "country": country,
        "pool": "150000000000",
        "issue": GENERIC_ISSUE,
        "instruments": GENERIC_INSTRUMENTS,
        "anchors": GENERIC_ANCHORS[:],
    }


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
    ".github/workflows",
    "00_Master_Knowledge_Base",
    "01_Pleadings_and_Complaints",
    "02_Discovery_and_Evidentiary",
    "03_Evidentiary_Exhibits",
    "03_Motions_and_Briefs",
    "04_International_Tribunals",
    "05_Strategic_Doctrines_and_Red_Team",
    "06_Trial_and_Appellate_Prep",
    "07_Enforcement_and_Restitution",
    "99_Archives_and_Manifests",
    "VERIFICATION_KEYS",
]


def backup_if_exists(path: Path, cdir: Path):
    if not path.exists():
        return
    bdir = cdir / "99_Archives_and_Manifests/pre_bolster_backup"
    bdir.mkdir(parents=True, exist_ok=True)
    dest = bdir / path.name
    if not dest.exists():
        shutil.copy2(path, dest)


def write(path: Path, content: str, cdir: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    backup_if_exists(path, cdir)
    path.write_text(content, encoding="utf-8", newline="\n")


def sha256(p: Path):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def make_readme(name, prof):
    iso = prof["iso"]
    country = prof["country"]
    return f"""# {country} ({iso}) - US-{iso} Restitution & Reparations Framework

**Template baseline:** LATIN_AMERICA/US_CU_CUBA (adapted)  
**Status:** Framework/Scaffold - for counsel/organization tailoring  
**Generated:** {TODAY}

## Scope
- Campaign: `{name}`
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
"""


def scaffold_country(name):
    cdir = ROOT / name
    prof = ensure_profile(name)
    for d in DIRS:
        (cdir / d).mkdir(parents=True, exist_ok=True)
    # clean contaminated core docs with safe scaffold
    write(cdir / "README.md", make_readme(name, prof), cdir)
    # basic manifests/logs
    write(
        cdir / "Master_Armory_Manifest.md",
        f"# Master Armory Manifest - {prof['country']}\n\nStatus: SCAFFOLD - verification required. No fabricated citations.\n",
        cdir,
    )
    write(
        cdir / "Expansion_and_Audit_Log.md",
        f"# Expansion and Audit Log - {prof['country']}\n\n- {TODAY}: Scaffolded/bolstered to GRA litigation framework.\n",
        cdir,
    )
    write(
        cdir / "Master_Chain_of_Custody_Log.md",
        f"# Master Chain of Custody Log - {prof['country']}\n\n| Date | Artifact | Hash | Custodian | Status | Notes |\n|---|---|---|---|---|---|\n",
        cdir,
    )
    # source registry placeholders
    kb = cdir / "00_Master_Knowledge_Base"
    write(
        kb / "PRIMARY_PUBLIC_SOURCES.md",
        f"# Primary Public Sources - {prof['country']}\n\nStatus: SCAFFOLD - verify all sources.\n\n- UN Digital Library: https://digitallibrary.un.org/search\n- UN OHCHR: https://www.ohchr.org/en/countries\n- AU: https://au.int/\n- World Bank: https://data.worldbank.org/country\n- US State Dept Human Rights Reports: https://www.state.gov/reports-bureau-of-democracy-human-rights-and-labor/country-reports-on-human-rights-practices/\n",
        cdir,
    )
    # evidence intake
    ex = cdir / "03_Evidentiary_Exhibits"
    write(
        ex / "EVIDENCE_INTAKE_LOG.md",
        f"# Evidence Intake Log - {prof['country']}\n\n| Date | Artifact | Source URL | Retrieved By | SHA-256 | Custody Status | Notes |\n|---|---|---|---|---|---|---|\n\n## Intake Rules\n- Record source URL, access date, downloader, file hash, and storage path.\n- No authenticated claim without custodian/legal review.\n",
        cdir,
    )
    # review checklist
    write(
        cdir / "99_Archives_and_Manifests/LEGAL_ACCURACY_REVIEW_CHECKLIST.md",
        f"# Legal Accuracy Review Checklist - {prof['country']} ({prof['iso']})\n\nStatus: FRAMEWORK TEMPLATE - not legal advice. Verify all citations/holdings.\n\n- [ ] Jurisdiction/standing\n- [ ] Immunity (FSIA/sovereign)\n- [ ] Limitations/prescription\n- [ ] Causation/damages\n- [ ] Forum compliance\n- [ ] Evidence authentication/chain of custody\n",
        cdir,
    )


def main():
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir():
            continue
        scaffold_country(d.name)
        print("OK", d.name)
    print("DONE")


if __name__ == "__main__":
    main()
