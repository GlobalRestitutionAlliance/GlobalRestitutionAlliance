import os, subprocess, hashlib
from pathlib import Path

ROOT = Path(r"W:\Legal")
REPOS = {
    Path(r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS"): {
        "domain": "African American reparations (US)",
        "theories": [
            "Unjust enrichment from enslaved labor",
            "Property takings/dispossession",
            "Civil rights harms and discriminatory policy damages (where legally cognizable)",
            "Contract/wage theft and exclusion harms (evidence-backed)",
        ],
        "evidence": [
            "Census/slave schedules, probate/manumission records",
            "Freedmen's Bureau records, land/title records",
            "Congressional records, agency reports, FOIA responses",
            "Oral histories/testimonies with authentication",
            "News archives, diaries, church records",
        ],
        "foia": [
            "DOJ Civil Rights Division",
            "NARA RG29/RG105 related holdings",
            "State/local archives FOIA/public records requests",
        ],
    },
    Path(
        r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-gb-reparations-master-litigation"
    ): {
        "domain": "UK transatlantic slavery actor track",
        "theories": [
            "Unjust enrichment/corporate successor tracing",
            "State complicity and restitution claims (jurisdiction-specific)",
            "Property/labor expropriation harms",
        ],
        "evidence": [
            "UK National Archives slavery/colonial records",
            "UCL Legacies of British Slavery database exports/citations",
            "Parliamentary Hansard, abolition compensation records",
            "Port/shipping manifests, insurance records",
        ],
        "foia": [
            "UK National Archives discovery requests",
            "UK public records / FOI requests where applicable",
        ],
    },
    Path(
        r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-pt-reparations-master-litigation"
    ): {
        "domain": "Portugal transatlantic slavery actor track",
        "theories": [
            "Unjust enrichment",
            "Forced labor/property harms",
            "Colonial trade liability (jurisdiction-specific)",
        ],
        "evidence": [
            "Arquivo Nacional Torre do Tombo records",
            "SlaveVoyages voyage records",
            "Portuguese colonial administration records",
            "Church/parish records, testimonies",
        ],
        "foia": ["Portuguese public archives requests", "EU/UN historical records"],
    },
    Path(
        r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-nl-reparations-master-litigation"
    ): {
        "domain": "Netherlands/WIC slavery actor track",
        "theories": [
            "Unjust enrichment/corporate successor tracing",
            "State/corporate complicity",
            "Forced labor/property harms",
        ],
        "evidence": [
            "Nationaal Archief WIC/slavery records",
            "SlaveVoyages records",
            "Notarial/probate/shipping records",
            "Oral histories/testimonies",
        ],
        "foia": [
            "Nationaal Archief requests",
            "Dutch government public records requests",
        ],
    },
    Path(r"W:\Legal\US_DOMESTIC_VICTIMS\US_DW_NUCLEAR_DOWNWINDERS"): {
        "domain": "Nuclear downwinders",
        "theories": [
            "Personal injury/wrongful death (statutory/FTCA where applicable)",
            "Property contamination/diminution",
            "Medical monitoring/health costs",
            "Statutory compensation gaps (RECA)",
        ],
        "evidence": [
            "DOE/NNSA declassified test records",
            "RECA claims/program records",
            "CDC/NIOSH/NCI exposure studies",
            "Congressional hearings, GAO reports",
            "Eyewitness testimony/medical records (authenticated)",
        ],
        "foia": ["DOE/NNSA FOIA", "DoD/agency FOIA", "State health/public records"],
    },
    Path(r"W:\Legal\PACIFIC\US_MH_MARSHALL_ISLANDS"): {
        "domain": "Marshall Islands nuclear testing",
        "theories": [
            "Property/environmental takings and contamination",
            "Personal injury/health harms",
            "Unjust enrichment/failed remediation duties (jurisdiction-specific)",
            "Treaty/compact obligations (evidence-backed)",
        ],
        "evidence": [
            "DOE OpenNet declassified documents",
            "UN Trusteeship records",
            "Congressional/GAO reports",
            "Nuclear Claims Tribunal records (public)",
            "Eyewitness testimonies/oral histories",
        ],
        "foia": [
            "DOE/NNSA FOIA",
            "State Dept/DOI FOIA",
            "NARA classified/declassified requests",
        ],
    },
    Path(r"W:\Legal\US_DOMESTIC_VICTIMS\US_JA_JAPANESE_AMERICAN_INTERNEES"): {
        "domain": "Japanese American internment",
        "theories": [
            "Property loss/takings",
            "Unjust enrichment/lost wages",
            "Civil liberties/personal injury harms (jurisdiction-specific)",
            "Statutory redress gaps",
        ],
        "evidence": [
            "NARA WRA/DOJ records, EO 9066 records",
            "CWRIC report and hearings",
            "Densho oral histories (with authentication)",
            "Property claims records, camp records",
            "News archives, diaries, letters",
        ],
        "foia": ["NARA FOIA", "DOJ/FBI FOIA", "Agency records requests"],
    },
    Path(
        r"W:\Legal\US_TURTLE_ISLAND_NATIVES\NAVAJO\US_AZ_NAVAJO_NATION_ARIZONA_NEW_MEXICO_UTAH"
    ): {
        "domain": "Navajo Nation claims",
        "theories": [
            "Treaty breach/trust responsibility",
            "Land/resource takings and water rights harms",
            "Uranium mining contamination/personal injury",
            "Unjust enrichment/resource extraction",
        ],
        "evidence": [
            "NARA RG75/BIA records",
            "Treaties and federal statutes",
            "EPA/DOE/USGS contamination records",
            "Court decisions/dockets",
            "Oral histories/testimonies (authenticated)",
        ],
        "foia": ["BIA/DOI FOIA", "DOE/EPA FOIA", "Tribal/federal records requests"],
    },
}


def sha256p(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def git(cwd, args, env=None, timeout=180):
    return subprocess.run(
        args, cwd=str(cwd), capture_output=True, text=True, env=env, timeout=timeout
    )


for repo, meta in REPOS.items():
    d = repo / "00_Master_Knowledge_Base"
    d.mkdir(parents=True, exist_ok=True)
    p = d / "VALUATION_METHODOLOGY_PILOT.md"
    lines = [
        f"# Valuation Methodology - Pilot ({meta['domain']})",
        "",
        "**Status:** TEMPLATE - verification required. Not legal advice. No fabricated amounts.",
        "**Rule:** No published pool without versioned cited workbook and human sign-off.",
        "",
        "## Damages theories (candidate, verify applicability)",
    ]
    lines += [f"- {t}" for t in meta["theories"]]
    lines += ["", "## Evidence types to prioritize"]
    lines += [f"- {t}" for t in meta["evidence"]]
    lines += ["", "## FOIA / records request targets"]
    lines += [f"- {t}" for t in meta["foia"]]
    lines += [
        "",
        "## Workbook rule",
        "- All `low/base/high` remain `TBD` until supported by cited, hashed evidence and reviewed methodology.",
        "- Each quantified row requires: baseline source, currency/year, adjustment method, interest/multiplier authority, offsets, confidence, reviewer.",
    ]
    p.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    # manifest
    linesm = []
    for fp in sorted(repo.rglob("*")):
        if not fp.is_file():
            continue
        rel = fp.relative_to(repo).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel == "VERIFICATION_KEYS/sha256_manifest.txt":
            continue
        try:
            linesm.append(f"{sha256p(fp)}  {rel}")
        except:
            pass
    (repo / "VERIFICATION_KEYS/sha256_manifest.txt").write_text(
        "\n".join(linesm) + "\n", encoding="utf-8", newline="\n"
    )

env = os.environ.copy()
env["GIT_TERMINAL_PROMPT"] = "0"
for repo in REPOS:
    git(repo, ["git", "add", "-A"], env=env)
    st = git(repo, ["git", "status", "--short"], env=env)
    if st.stdout.strip():
        git(
            repo,
            [
                "git",
                "commit",
                "-m",
                "Pilot Batch 3: domain valuation methodology and FOIA/research queue",
            ],
            env=env,
        )
        print(repo.name, "COMMIT")
    else:
        print(repo.name, "CLEAN")

subprocess.run(
    ["gh", "auth", "switch", "-u", "GlobalRestitutionAlliance"], capture_output=True
)
envg = os.environ.copy()
envg["GIT_TERMINAL_PROMPT"] = "0"
envg.pop("GH_TOKEN", None)
envg.pop("GITHUB_TOKEN", None)
for repo in REPOS:
    p = git(repo, ["git", "push", "origin", "HEAD"], envg, timeout=240)
    print(repo.name, "PUSH_OK" if p.returncode == 0 else "PUSH_FAIL")
subprocess.run(["gh", "auth", "switch", "-u", "R03LV1S"], capture_output=True)
print("DONE")
