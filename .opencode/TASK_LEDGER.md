# LATAM Bolstering Ledger

## Objective
Bolster all 33 non-Cuba LATAM campaigns to Cuba-template depth/coverage and document replicable workflow.

## Status: AUTOMATABLE PHASES EXECUTED (human/legal/auth/CI-secrets remain)

## Completed
- [x] B1-B6 structural/content scaffold passes
- [x] Phase 1 .antigravity depth (170 agents, 252 skills, 1805 vectors/country)
- [x] Phase 2 filing scaffold docs + DOCX scaffolds
- [x] Phase 3/Integrity sha256 manifests refreshed
- [x] Phase 4 legal/accuracy review checklists
- [x] Source registries (IACHR/ICJ/UN/OHCHR/FRUS/NARA/CIA/LOC/etc.) per country
- [x] Evidence intake logs with provenance rules
- [x] ICJ public web captures with hashes/provenance (NI/BO/CL/GY/VE/GT)
- [x] Phase F initial harvest: 211 ok, 181 failed/blocked, 23 skipped; artifacts+meta.json in Immutable_Ledger; intake logs updated
- [x] **Phase F browser-automation fallback**: 187/187 previously failed/blocked URLs retried via connected browser (Brave) with browser-rendered outerHTML capture, saved to `03_Evidentiary_Exhibits/Immutable_Ledger/*_browser.html` + `.meta.json` WARC-like provenance sidecars (url/final_url/status/title/bytes/sha256/captured_at/custodian/provenance). Intake logs updated. (`.opencode/capture_receiver.py`, `.opencode/process_browser_captures.py`, `.opencode/failed_harvest_worklist.json`)
- [x] Phase G citation index built/rebuilt: **12 citations/country, 396 total**; `NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT`; all `PENDING_LEGAL_REVIEW`. Enhanced extraction: title, date (when present), authoring body (meta/domain heuristic), excerpt, page/paragraph ref (`html/p[n]`), local hashed artifact, SHA-256.
- [x] **Citation references applied to crosswalks and 01-07 docs**: 2802 files patched/updated with "Verified Source Citations (PENDING_LEGAL_REVIEW)" sections/columns
- [x] Replication playbook: `W:\Legal\WORKFLOW_REPLICATION_PLAYBOOK.md`
- [x] Manifests refreshed after all updates

## Evidence snapshot
- Browser fallback batch: **187 ok / 0 fail** (from 187 deduped failed-harvest worklist)
- Citation indexes: 33 files, 12 entries each = 396 entries, all `PENDING_LEGAL_REVIEW`
- Sample artifact: `LATIN_AMERICA/US_NI_NICARAGUA/03_Evidentiary_Exhibits/Immutable_Ledger/NI_01_..._browser.html` + `.meta.json` (sha256 `57426f73...`, captured_at `2026-11-21T18:46:08Z`, custodian `OpenCode/browser-fallback`, provenance WARC-like sidecar)
- Docs patched: 2802 crosswalk/01-07 files

## Guardrails
- No fabricated citations, docket numbers, archival IDs, or authenticated-evidence claims.
- Captures `PUBLIC_CAPTURE_UNAUTHENTICATED`; citations `PENDING_LEGAL_REVIEW`.
- No `VERIFIED` without local hashed source artifact + human sign-off.

## Residual (human/legal/access/credentials)
- **Instrument-level citation extraction**: current pipeline extracts metadata/HTML title/excerpt; deeper instrument-level holdings (treaty article, judgment paragraph, case holding) require document-specific parsing/PDF text extraction and human verification.
- **Authenticated/certified originals**: obtain certified originals and chain-of-custody attestation; store in `Immutable_Ledger/` with custodian attestation.
- **Counsel validation**: qualified legal review per `LEGAL_ACCURACY_REVIEW_CHECKLIST.md` (jurisdiction/standing, immunity FSIA/act of state/comity, limitations/prescription, causation/damages, forum compliance). Prioritize NI, GT, CL, AR, SV, HN, CO, BR, VE, HT but complete all 33.
- **Filing-grade post-review packages**: court-formatted DOCX/PDF bundles with exhibit indexes and human-attested authentication affidavits only after counsel verification.
- **Remote CI/mirror**: commit/push in logical batches, configure GitHub secrets, make `integrity-verification` required on PRs.
