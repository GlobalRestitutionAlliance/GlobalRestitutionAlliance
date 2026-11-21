# Global Restitution Campaign Bolstering Workflow (Replication Playbook)

**Template baseline:** `LATIN_AMERICA/US_CU_CUBA`  
**First full rollout:** `LATIN_AMERICA/*` (33 non-Cuba countries)  
**Status date:** 2026-11-21

## 1) Objective
Replicate Cuba-template campaign depth across all regional/country repositories while preserving evidentiary integrity:
- No fabricated citations, docket numbers, archival IDs, or authenticated-evidence claims.
- Every "verified" citation must map to a locally hashed source artifact.
- Legal conclusions require qualified counsel sign-off.

## 2) Prerequisites
- Python 3.x; `python-docx` for DOCX scaffolds (`pip install python-docx`).
- Git repo access; GitHub Actions secrets for mirrors if used.
- Optional: browser automation for 403-blocked sources; CourtListener token for higher-rate API use.
- Disk space for source captures and manifests.

## 3) Phase Model

### Phase A - Structural Baseline (idempotent)
**Goal:** Ensure every country has canonical dirs and governance baseline.
- Dirs: `.antigravity/{agents,datasets,knowledge/vector-index,rules,skills,templates,tools,workflows}`, `.github/{ISSUE_TEMPLATE,workflows}`, `00_Master_Knowledge_Base`, `01_Pleadings_and_Complaints`, `02_Discovery_and_Evidentiary`, `03_Evidentiary_Exhibits`, `03_Motions_and_Briefs`, `04_International_Tribunals`, `05_Strategic_Doctrines_and_Red_Team`, `06_Trial_and_Appellate_Prep`, `07_Enforcement_and_Restitution`, `99_Archives_and_Manifests`, `VERIFICATION_KEYS`.
- Root docs: README, MANIFESTO, GOVERNANCE, CONTRIBUTING, SECURITY, LICENSE, Master_Armory_Manifest, Expansion_and_Audit_Log, Master_Chain_of_Custody_Log.
- CI: `integrity-verification.yml` (manifest check + vector count if present), `mirror-sync.yml`.
- **Script:** `.opencode/bolster_latam_scaffold.py` (adapt paths/naming for region).

### Phase B - README/Manifest Uplift
**Goal:** Cuba-aligned, country-specific README with manifest metrics.
- Parse `Master_Armory_Manifest.md` for instruments/pool/agents/skills.
- Preserve existing facts; back up overwritten files to `99_Archives_and_Manifests/pre_bolster_backup/`.
- **Script:** `.opencode/bolster_latam_readmes.py`.

### Phase C - Deep Content Scaffold
**Goal:** Populate core campaign categories with non-fabricated scaffolds.
- Generate: crosswalk CSV/MD, executive dossier, 01-07 core docs, .antigravity project/registries/agents/skills/templates/workflows/rules/knowledge/vector index.
- Use high-level public anchors only; mark `PENDING_PRIMARY_SOURCE` / `SCAFFOLDED`.
- **Scripts:** `.opencode/bolster_latam_deep.py`, `.opencode/bolster_latam_deep2.py`.

### Phase D - .antigravity Depth Expansion
**Goal:** Approach Cuba-scale agent/skill/vector counts.
- 170 agents, 252 skills, 1805 vector entries per country (or region-appropriate scale), all `ACTIVE_SCAFFOLD`/verification-required.
- **Script:** `.opencode/bolster_latam_phase1.py`.

### Phase E - Filing-Grade Scaffolds & Review Gates
**Goal:** Add filing-formatted MD/DOCX scaffolds and review checklists.
- DOCX: complaint, discovery, motions, tribunal, enforcement packages with verification guardrail.
- Add `LEGAL_ACCURACY_REVIEW_CHECKLIST.md` per country.
- **Scripts:** `.opencode/bolster_latam_phase234.py`, `.opencode/bolster_latam_docx.py`.

### Phase F - Evidence Harvest (Automatable)
**Goal:** Download public primary docs with provenance.
- Read `03_Evidentiary_Exhibits/PRIMARY_PUBLIC_SOURCES.csv` per country.
- Download to `03_Evidentiary_Exhibits/Immutable_Ledger/`; save `.meta.json` sidecar (URL, final URL, status, content-type, bytes, sha256, captured_at, custodian, headers).
- Append to `EVIDENCE_INTAKE_LOG.md` with `PUBLIC_CAPTURE_UNAUTHENTICATED` or `CAPTURE_FAILED`.
- Retry with browser automation for 403 blocks; preserve HTTP metadata/WARC-like provenance where possible.
- **Scripts:** `.opencode/harvest_public_sources.py`, `.opencode/bolster_latam_capture.py`, `.opencode/make_failed_worklist.py`.
- **Current LATAM status:** harvest run complete (211 ok / 181 failed-blocked / 23 skipped). Failed URL worklist: `.opencode/failed_harvest_worklist.json` (187 deduped). Browser relay was connected at check time, but bulk browser capture requires a scripted batch runner that saves content+metadata outside execute context; run when browser session is stable.

### Phase G - Citation Population (Automatable, Review-Gated)
**Goal:** Replace scaffold anchors with verified citations tied to local hashed artifacts.
- Extract metadata from downloaded docs: title, date, authoring body, URL, excerpt, page/paragraph ref.
- Update crosswalks and 01-07 docs with citation entries.
- **Hard rule:** no citation marked `VERIFIED` without local hashed source artifact. Default `PENDING_LEGAL_REVIEW`.
- **Script:** `.opencode/populate_citations.py` (to be built/extended per source type).

### Phase H - Legal Validation (Human-Required)
**Goal:** Counsel sign-off per country.
- Complete `99_Archives_and_Manifests/LEGAL_ACCURACY_REVIEW_CHECKLIST.md`.
- Review jurisdiction/standing, immunity, limitations, causation/damages, forum compliance, defamation/accuracy.
- Only after sign-off: mark citations verified, produce filing-ready packages.

### Phase I - Filing Packages & CI (Semi-Automatable)
**Goal:** Court-formatted bundles and remote integrity.
- Generate DOCX/PDF bundles with exhibit indexes and chain-of-custody declarations (human custodian attestation required for authentication).
- Regenerate `VERIFICATION_KEYS/sha256_manifest.txt` on every artifact update.
- Run CI locally where possible; push in logical batches; enable required integrity checks on PRs.

## 4) Guardrails (Non-Negotiable)
- **No fabrication:** no invented citations, docket numbers, archival IDs, quotes, or evidence.
- **No false authentication:** web captures/downloads are `PUBLIC_CAPTURE_UNAUTHENTICATED` until human custodial/legal authentication.
- **No false legal verification:** counsel review required before filing/external legal reliance.
- **Backup before overwrite:** `99_Archives_and_Manifests/pre_bolster_backup/`.
- **Hash everything:** SHA-256 manifest refreshed after content changes.

## 5) Replication Checklist for New Continent/Region
1. Copy/adapt profile map (`PROFILES`) with country ISO, name, pool, issues, high-level public anchors.
2. Set `ROOT` to region dir (e.g., `W:\Legal\AFRICA`).
3. Run Phase A-E scripts in order; verify `ALL_OK` structure check.
4. Seed `PRIMARY_PUBLIC_SOURCES.csv` per country with authoritative portals + country-specific reports.
5. Run Phase F harvest; review capture failures; add browser fallback for blocked sources.
6. Run Phase G citation population; keep review-gated.
7. Assign counsel review (Phase H) in parallel batches.
8. Generate filing packages and CI (Phase I).
9. Update regional ledger and this playbook with lessons learned.

## 6) Artifacts Produced (LATAM rollout)
- Ledger: `.opencode/TASK_LEDGER.md`
- Scripts: `.opencode/bolster_latam_scaffold.py`, `bolster_latam_readmes.py`, `bolster_latam_deep.py`, `bolster_latam_deep2.py`, `bolster_latam_phase1.py`, `bolster_latam_phase234.py`, `bolster_latam_docx.py`, `bolster_latam_sources.py`, `bolster_latam_intake.py`, `bolster_latam_capture.py`, `harvest_public_sources.py`
- Per-country outputs: canonical dirs, .github, README, manifests/logs, crosswalks, 01-07 scaffolds, .antigravity depth, source registries, intake logs, DOCX scaffolds, public captures, sha256 manifests.

## 7) Known Limits
- Some official sources block automated download (403/bot protection); browser automation or manual download required.
- Authentication of evidence and legal conclusions require human professionals.
- Remote CI/mirror sync requires repo secrets/credentials.
