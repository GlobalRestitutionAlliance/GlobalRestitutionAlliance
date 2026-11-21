import os
from pathlib import Path

ROOT = Path(r"W:\Legal\LATIN_AMERICA")
CUBA = ROOT / "US_CU_CUBA"

CANONICAL_DIRS = [
    ".antigravity",
    ".antigravity/agents",
    ".antigravity/datasets",
    ".antigravity/knowledge",
    ".antigravity/knowledge/vector-index",
    ".antigravity/rules",
    ".antigravity/skills",
    ".antigravity/templates",
    ".antigravity/tools",
    ".antigravity/workflows",
    ".github",
    ".github/ISSUE_TEMPLATE",
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

CODEOWNERS = """# Require approval from designated maintainers for core architecture
/.antigravity/                          @GlobalRestitutionAlliance/maintainer-council
/00_Master_Knowledge_Base/              @GlobalRestitutionAlliance/archival-sentinel @GlobalRestitutionAlliance/maintainer-council
/01_Pleadings_and_Complaints/           @GlobalRestitutionAlliance/procedural-blacksmith @GlobalRestitutionAlliance/maintainer-council
/02_Discovery_and_Evidentiary/          @GlobalRestitutionAlliance/agent-omega @GlobalRestitutionAlliance/maintainer-council
/03_Motions_and_Briefs/                 @GlobalRestitutionAlliance/procedural-blacksmith @GlobalRestitutionAlliance/maintainer-council
/04_International_Tribunals/            @GlobalRestitutionAlliance/global-tribunals-envoy @GlobalRestitutionAlliance/maintainer-council
/05_Strategic_Doctrines_and_Red_Team/   @GlobalRestitutionAlliance/sun-tzu-strategist @GlobalRestitutionAlliance/maintainer-council
/06_Trial_and_Appellate_Prep/           @GlobalRestitutionAlliance/procedural-blacksmith @GlobalRestitutionAlliance/maintainer-council
/07_Enforcement_and_Restitution/        @GlobalRestitutionAlliance/global-tribunals-envoy @GlobalRestitutionAlliance/maintainer-council
VERIFICATION_KEYS/                      @GlobalRestitutionAlliance/maintainer-council
GOVERNANCE.md                           @GlobalRestitutionAlliance/maintainer-council
"""

PR_TEMPLATE = """## Evidentiary & Strategic Pull Request

### 1. Vector / Module Reference
- Target Vector ID(s) or Strategic Module:
- Directory Modified:

### 2. Description of Contribution
Briefly explain the nature of this submission (e.g., primary archival record addition, procedural refinement, legal brief hardening, or algorithmic enhancement):

### 3. Primary Source Verification & Cryptographic Standards
- [ ] Primary source citations provided (NARA RG, Library of Congress, foreign archives, court dockets).
- [ ] All commits are GPG-signed by the contributor.
- [ ] `VERIFICATION_KEYS/sha256_manifest.txt` updated if files were added or modified.
- [ ] No unauthorized modifications to locked foundational records (`Master_Chain_of_Custody_Log.md`, `historical-timeline.yaml`, etc.).

### 4. Reviewer Checklist
- [ ] Automated CI integrity verification passed.
- [ ] Approved by designated module CODEOWNER.
- [ ] Secondary maintainer sign-off confirmed.
"""

ISSUE_ARCHIVAL = """---
name: Archival Discovery Alert
about: Report newly declassified, unsealed, or located historical archive records
title: "[ARCHIVAL-DISCOVERY]: <Archive / Record Group> - <Short Description>"
labels: [archival-discovery, research]
assignees: ''
---

### Archival Repository Details
- **Institution:**
- **Record Group / Collection:**
- **Physical / Digital Location:**

### Key Findings
Describe the newly located records and their material relevance to the restitution campaign:

### Chain of Custody & Authentication
- **Access Protocol:**
- **Certified Copy Availability (28 U.S.C. § 1733):**
- **Digitization Resolution (DPI):**
"""

ISSUE_SECURITY = """---
name: Security & Integrity Alert
about: Report repository tampering, compromised credentials, or pipeline anomalies
title: "[SECURITY-ALERT]: <Compromised Commit / Vulnerability / Anomaly>"
labels: [security, critical]
assignees: ''
---

### Incident Summary
Describe the observed anomaly, unauthorized commit attempt, or credential compromise:

### Affected Components
- **Commit SHA / Branch:**
- **Modified Files:**
- **Observed Integrity Failure:**

### Proposed Mitigation
- [ ] Hard reset to last verified signed release tag.
- [ ] Revoke compromised GPG key in `VERIFICATION_KEYS/maintainers.asc`.
- [ ] Trigger Reversion Protocol across all decentralized mirrors.
"""

ISSUE_VECTOR = """---
name: Evidentiary Vector Submission
about: Submit a new or enhanced historical/forensic vector for the Vector Index
title: "[VECTOR-SUBMISSION]: Vector XXXX - <Short Title>"
labels: [vector-submission, evidence]
assignees: ''
---

### Vector Metadata
- **Proposed Vector ID:**
- **Temporal Era:**
- **Primary Actors Involved:**

### Evidentiary Muniment & Citations
- **Archival Repository:** (NARA Record Group, LOC, foreign archives, etc.)
- **Container / Box / Entry Number:**
- **Document Description & Legal Significance:**

### Factual Proffer
Summary of factual assertions established by this document:

### Legal Nexus
How this vector establishes continuous liability, fiduciary breach, or an uncurable international taking:
"""


def repo_slug(country_dir_name: str) -> str:
    # US_AR_ARGENTINA -> latam-ar-argentina-master-litigation
    parts = country_dir_name.split("_")
    if len(parts) >= 3 and parts[0] == "US":
        iso = parts[1].lower()
        name = "-".join(p.lower() for p in parts[2:])
        return f"latam-{iso}-{name}-master-litigation"
    return country_dir_name.lower().replace("_", "-") + "-master-litigation"


def integrity_workflow() -> str:
    return """name: Evidentiary Integrity Verification

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  verify-hashes:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Verify SHA-256 Manifest
        run: |
          if [ -f VERIFICATION_KEYS/sha256_manifest.txt ]; then
            echo "Verifying evidentiary payload integrity..."
            sha256sum -c VERIFICATION_KEYS/sha256_manifest.txt --strict
            echo "All hashes verified. Chain of custody intact."
          else
            echo "No sha256 manifest found; skipping hash verification."
          fi

      - name: Verify Vector Index Count (if present)
        run: |
          if ls .antigravity/knowledge/vector-index/*.yaml >/dev/null 2>&1; then
            VECTOR_COUNT=$(grep -h "vector_id:" .antigravity/knowledge/vector-index/*.yaml | wc -l | tr -d ' ')
            echo "Vector entries found: $VECTOR_COUNT"
            if [ "$VECTOR_COUNT" -lt 1 ]; then
              echo "VECTOR COUNT INVALID."
              exit 1
            fi
          else
            echo "No vector index files found; skipping vector count check."
          fi

      - name: Check for Prohibited Alterations
        run: |
          if [ "$(git rev-parse --verify HEAD~1 2>/dev/null)" ]; then
            CHANGED=$(git diff --name-only HEAD~1 HEAD | grep -E "(historical-timeline|legal-precedents|Master_Chain_of_Custody_Log)" || true)
            if [ -n "$CHANGED" ]; then
              echo "ALERT: Attempted modification of locked foundational records:"
              echo "$CHANGED"
              exit 1
            fi
            echo "Foundational records untouched."
          else
            echo "Initial commit or single commit range; skipping diff check."
          fi
"""


def mirror_workflow(slug: str) -> str:
    return f"""name: Decentralized Mirror Synchronization

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
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Push to GitLab Mirror
        if: env.GITLAB_TOKEN != ''
        run: |
          git remote add gitlab https://oauth2:${{{{ secrets.GITLAB_MIRROR_TOKEN }}}}@gitlab.com/GlobalRestitutionAlliance/{slug}.git || true
          git push gitlab main --tags --force
        env:
          GITLAB_TOKEN: ${{{{ secrets.GITLAB_MIRROR_TOKEN }}}}

      - name: Push to Codeberg Mirror
        if: env.CODEBERG_TOKEN != ''
        run: |
          git remote add codeberg https://${{{{ secrets.CODEBERG_MIRROR_TOKEN }}}}@codeberg.org/GlobalRestitutionAlliance/{slug}.git || true
          git push codeberg main --tags --force
        env:
          CODEBERG_TOKEN: ${{{{ secrets.CODEBERG_MIRROR_TOKEN }}}}
"""


def ensure_file(path: Path, content: str, created, skipped):
    if path.exists():
        skipped.append(str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    created.append(str(path))


def main():
    created = []
    skipped = []
    for country in sorted([p for p in ROOT.iterdir() if p.is_dir()]):
        for d in CANONICAL_DIRS:
            (country / d).mkdir(parents=True, exist_ok=True)
        slug = repo_slug(country.name)
        ensure_file(country / ".github" / "CODEOWNERS", CODEOWNERS, created, skipped)
        ensure_file(
            country / ".github" / "PULL_REQUEST_TEMPLATE.md",
            PR_TEMPLATE,
            created,
            skipped,
        )
        ensure_file(
            country / ".github" / "ISSUE_TEMPLATE" / "archival-discovery.md",
            ISSUE_ARCHIVAL,
            created,
            skipped,
        )
        ensure_file(
            country / ".github" / "ISSUE_TEMPLATE" / "security-alert.md",
            ISSUE_SECURITY,
            created,
            skipped,
        )
        ensure_file(
            country / ".github" / "ISSUE_TEMPLATE" / "vector-submission.md",
            ISSUE_VECTOR,
            created,
            skipped,
        )
        ensure_file(
            country / ".github" / "workflows" / "integrity-verification.yml",
            integrity_workflow(),
            created,
            skipped,
        )
        ensure_file(
            country / ".github" / "workflows" / "mirror-sync.yml",
            mirror_workflow(slug),
            created,
            skipped,
        )

    print(f"CREATED={len(created)}")
    print(f"SKIPPED={len(skipped)}")
    for p in created[:60]:
        print("C", p)
    if len(created) > 60:
        print(f"... {len(created) - 60} more")


if __name__ == "__main__":
    main()
