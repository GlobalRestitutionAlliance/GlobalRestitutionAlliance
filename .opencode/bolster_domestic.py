import csv, datetime, hashlib, json, os, re, shutil
from pathlib import Path

TODAY = datetime.date.today().isoformat()
BASE = Path(r"W:\Legal")
TARGETS = {
    "US_AFRICAN_AMERICAN_REPARATIONS": {
        "iso": "AA",
        "country": "African American Reparations",
        "issue": "Slavery, Jim Crow, systemic discrimination, economic exclusion - verification required",
        "instruments": "US Constitution amendments; Civil Rights Act; UN human rights instruments (verify)",
        "anchors": [
            "Public historical records (verify)",
            "Congressional reports/legislation (verify)",
            "Federal/state archives (verify)",
        ],
    },
    "US_DW_NUCLEAR_DOWNWINDERS": {
        "iso": "DW",
        "country": "Nuclear Downwinders",
        "issue": "Nuclear testing fallout exposure, health harms, compensation gaps - verification required",
        "instruments": "RECA; federal statutes; public health records (verify)",
        "anchors": [
            "DOE/NNSA records (verify)",
            "RECA program records (verify)",
            "Public health studies (verify)",
        ],
    },
    "US_ER_EXTRAORDINARY_RENDITION_VICTIMS": {
        "iso": "ER",
        "country": "Extraordinary Rendition Victims",
        "issue": "Extraordinary rendition, detention, torture allegations - verification required",
        "instruments": "UN CAT; ICCPR; US statutes/treaties (verify)",
        "anchors": [
            "Senate/official reports (verify)",
            "Court records (verify)",
            "International investigations (verify)",
        ],
    },
    "US_GT_GUANTANAMO_DETAINEES": {
        "iso": "GT",
        "country": "Guantanamo Detainees",
        "issue": "Indefinite detention, due process, treatment - verification required",
        "instruments": "Geneva Conventions; US Constitution; international law (verify)",
        "anchors": [
            "Court filings/opinions (verify)",
            "DoD/official records (verify)",
            "UN reports (verify)",
        ],
    },
    "US_JA_JAPANESE_AMERICAN_INTERNEES": {
        "iso": "JA",
        "country": "Japanese American Internees",
        "issue": "WWII internment, property loss, civil liberties violations - verification required",
        "instruments": "Civil Liberties Act of 1988; court records (verify)",
        "anchors": [
            "National Archives records (verify)",
            "CWRIC reports (verify)",
            "Court decisions (verify)",
        ],
    },
}


def find_dir(name):
    for p in [BASE / name, BASE / "US_DOMESTIC_VICTIMS" / name]:
        if p.exists():
            return p
    return None


DIRS = [
    ".antigravity/agents",
    ".antigravity/skills",
    ".antigravity/workflows",
    ".antigravity/rules",
    ".antigravity/templates",
    ".antigravity/tools",
    ".antigravity/knowledge",
    ".antigravity/vector-index",
    ".github/workflows",
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


def backup(path, cdir):
    if not path.exists():
        return
    b = cdir / "99_Archives_and_Manifests/pre_bolster_backup"
    b.mkdir(parents=True, exist_ok=True)
    d = b / path.name
    if not d.exists():
        shutil.copy2(path, d)


def write(path, content, cdir):
    path.parent.mkdir(parents=True, exist_ok=True)
    backup(path, cdir)
    path.write_text(content, encoding="utf-8", newline="\n")


def sha256(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


for name, prof in TARGETS.items():
    cdir = find_dir(name)
    if not cdir:
        print("MISS", name)
        continue
    iso = prof["iso"]
    country = prof["country"]
    for d in DIRS:
        (cdir / d).mkdir(parents=True, exist_ok=True)
    write(
        cdir / "README.md",
        f"# {country} - Framework\n\n**Template:** CUBA-adapted framework\n**Generated:** {TODAY}\n**Status:** SCAFFOLD - verification required. No fabricated citations.\n\nIssues (verify): {prof['issue']}\nInstruments (verify): {prof['instruments']}\n",
        cdir,
    )
    # CI
    write(
        cdir / ".github/workflows/integrity-verification.yml",
        'name: Evidentiary Integrity Verification\non:\n  push:\n  pull_request:\njobs:\n  verify-hashes:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Verify SHA-256 Manifest\n        run: |\n          cd "$GITHUB_WORKSPACE"\n          if [ -f VERIFICATION_KEYS/sha256_manifest.txt ]; then sha256sum -c VERIFICATION_KEYS/sha256_manifest.txt; else echo No manifest && exit 1; fi\n',
        cdir,
    )
    # antigravity
    ag = cdir / ".antigravity"
    agents = "agents:\n" + "".join(
        [
            f"  - id: agent_{iso.lower()}_{i:03d}\n    name: {country} Agent {i:03d}\n    status: ACTIVE_SCAFFOLD\n"
            for i in range(1, 171)
        ]
    )
    skills = "skills:\n" + "".join(
        [
            f"  - id: skill_{iso.lower()}_{i:03d}\n    name: {country} Skill {i:03d}\n    status: ACTIVE_SCAFFOLD\n"
            for i in range(1, 253)
        ]
    )
    write(
        ag / "project.yaml",
        f"name: {name}\nstatus: SCAFFOLD_FRAMEWORK\ngenerated: {TODAY}\n",
        cdir,
    )
    write(ag / "agents/agent-registry.yaml", agents, cdir)
    write(ag / "skills/skill-registry.yaml", skills, cdir)
    vec = cdir / ".antigravity/vector-index"
    vec.mkdir(parents=True, exist_ok=True)
    (vec / "vector_index.jsonl").write_text(
        "\n".join(
            [
                f"VID-{iso}-{i:04d}|{name}|scaffold|verification-required|{TODAY}"
                for i in range(1, 1806)
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    # sources
    ex = cdir / "03_Evidentiary_Exhibits"
    rows = [
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "US National Archives",
            "https://www.archives.gov/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "Library of Congress",
            "https://www.loc.gov/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "US State Dept FRUS",
            "https://history.state.gov/historicaldocuments",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "DOJ Civil Rights Division",
            "https://www.justice.gov/crt",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "UN OHCHR",
            "https://www.ohchr.org/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            iso,
            country,
            "PUBLIC_PORTAL",
            "CourtListener",
            "https://www.courtlistener.com/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
    ]
    with (ex / "PRIMARY_PUBLIC_SOURCES.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f)
        w.writerow(
            ["iso", "country", "source_type", "title", "url", "access_class", "status"]
        )
        w.writerows(rows)
    write(
        ex / "PRIMARY_PUBLIC_SOURCES.md",
        "# Primary Public Sources\n\n"
        + "".join([f"- [{r[3]}]({r[4]})\n" for r in rows]),
        cdir,
    )
    write(
        ex / "EVIDENCE_INTAKE_LOG.md",
        f"# Evidence Intake Log - {country}\n\n| Date | Artifact | Source URL | Retrieved By | SHA-256 | Custody Status | Notes |\n|---|---|---|---|---|---|---|\n",
        cdir,
    )
    write(
        cdir / "99_Archives_and_Manifests/LEGAL_ACCURACY_REVIEW_CHECKLIST.md",
        f"# Legal Accuracy Review Checklist - {country}\n\nStatus: FRAMEWORK TEMPLATE - not legal advice. Verify all citations.\n- [ ] Jurisdiction/standing\n- [ ] Immunity/limitations\n- [ ] Causation/damages\n- [ ] Evidence authentication\n- [ ] Counsel/organization sign-off\n",
        cdir,
    )
    write(
        cdir / "03_Evidentiary_Exhibits/AUTHENTICATION_DECLARATION_TEMPLATE.md",
        f"# Authentication & Chain-of-Custody Declaration Template - {country}\n\nTEMPLATE - human attestation required. Not executed.\n",
        cdir,
    )
    # manifest
    manifest = cdir / "VERIFICATION_KEYS/sha256_manifest.txt"
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
    print("OK", name)
print("DONE")
