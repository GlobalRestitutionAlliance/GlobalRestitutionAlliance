from pathlib import Path
from bolster_latam_deep import ROOT, PROFILES, TODAY, backup_if_exists, write

PRECEDENT_FRAMEWORK = r"""
## Precedent & Framework Research Matrix (Template - For Counsel/Organization Tailoring)

> **Status:** FRAMEWORK TEMPLATE. Not legal advice. All case citations, statutes, and holdings must be independently verified by qualified counsel before reliance or filing. No docket numbers or archival IDs are fabricated.

### A. Jurisdiction & Standing (Research Starting Points)
| Issue | Framework / Precedent Starting Points | Verification Needed | Status |
|---|---|---|---|
| Subject-matter jurisdiction | 28 U.S.C. § 1331 (federal question), § 1332 (diversity), § 1350 (ATS - scope narrowed by *Sosa v. Alvarez-Machain*, *Kiobel v. Royal Dutch Petroleum*, *Jesner v. Arab Bank* - verify current applicability) | Confirm current statutory/case law; identify specific jurisdictional hook | PENDING_LEGAL_REVIEW |
| Personal jurisdiction | *International Shoe* minimum contacts; *Daimler AG v. Bauman* / *Goodyear* general jurisdiction limits; specific jurisdiction fact analysis | Defendant contacts, service, forum | PENDING_LEGAL_REVIEW |
| Standing | Article III injury-in-fact, causation, redressability (*Lujan v. Defenders of Wildlife* - verify); associational/organizational standing as applicable | Identify plaintiffs/claimants and traceable injury | PENDING_LEGAL_REVIEW |
| Sovereign immunity (FSIA) | 28 U.S.C. §§ 1604-1607; exceptions: commercial activity (§1605(a)(2)), expropriation (§1605(a)(3)), terrorism (§1605A - eligibility requirements), waiver (§1605(a)(1)) - verify applicability | Determine defendant status and applicable exception | PENDING_LEGAL_REVIEW |
| Act of state / political question | *Banco Nacional de Cuba v. Sabbatino* (act of state - verify scope/limitations); *Baker v. Carr* factors (political question) | Fact-specific analysis; separation of powers considerations | PENDING_LEGAL_REVIEW |

### B. Limitations / Prescription
| Issue | Framework / Precedent Starting Points | Verification Needed | Status |
|---|---|---|---|
| Statute of limitations | Federal/state SOL by cause of action; *TVPA* 10-year SOL (verify); equitable tolling, fraudulent concealment, continuing violation doctrines - case-specific | Identify accrual date, tolling facts, governing SOL | PENDING_LEGAL_REVIEW |

### C. Causation & Damages / Restitution
| Issue | Framework / Precedent Starting Points | Verification Needed | Status |
|---|---|---|---|
| Causation | Proximate cause, but-for causation, intervening causes; expert evidence requirements | Evidence chain, expert reports | PENDING_LEGAL_REVIEW |
| Damages / restitution | Compensatory, unjust enrichment/restitution, disgorgement, declaratory/injunctive relief; valuation methodology | Document damages model, evidentiary support | PENDING_LEGAL_REVIEW |

### D. Evidence & Authentication (Open-Source / Public Records)
| Issue | Framework | Verification Needed | Status |
|---|---|---|---|
| Public records | FRE 901/902 (authentication/self-authentication), 1002/1003 (best evidence), 803(8) public records exception - verify | Custodian declarations, certified copies, hash provenance | PENDING_LEGAL_REVIEW |
| Digital captures | Preserve URL, access date, SHA-256, HTTP metadata/WARC-like sidecar; maintain chain of custody | Independent re-capture verification; legal authentication | PUBLIC_CAPTURE_UNAUTHENTICATED |
"""

AFFIDAVIT_TEMPLATE = r"""
# Evidence Authentication & Chain-of-Custody Declaration (TEMPLATE)

> **TEMPLATE FOR COUNSEL/ORGANIZATION USE.** Not executed. Not notarized. Not legal advice. Complete only with true, verified information.

## 1. Declarant
- Name:
- Title/Role:
- Organization:
- Contact:
- Date of declaration:

## 2. Exhibit Identification
- Exhibit ID:
- File name:
- Local path (Immutable_Ledger):
- SHA-256:
- Bytes/MIME type:

## 3. Source & Capture Provenance
- Source URL:
- Final URL (if redirected):
- Access/capture date (UTC):
- Capture method (browser/HTTP/archive):
- Capturing tool/version:
- HTTP status/content-type (if available):
- WARC/provenance sidecar file:

## 4. Custody
- Storage location:
- Access controls:
- Hash verified on (date):
- Any alterations since capture: [ ] None known [ ] Describe:

## 5. Authentication Basis
- [ ] Official government/public body publication
- [ ] Certified copy obtained
- [ ] Witnessed capture
- [ ] Other (describe):

## 6. Declaration
I declare under penalty of perjury under the laws of the applicable jurisdiction that the foregoing is true and correct to the best of my knowledge, information, and belief.

Signature: ________________________
Date: ____________________________
Jurisdiction: _____________________
"""


def main():
    for name, prof in PROFILES.items():
        if name == "US_CU_CUBA":
            continue
        cdir = ROOT / name
        if not cdir.exists():
            continue
        iso = prof["iso"]
        country = prof["country"]
        # Legal accuracy review checklist - populate with precedent framework
        p = cdir / "99_Archives_and_Manifests" / "LEGAL_ACCURACY_REVIEW_CHECKLIST.md"
        backup_if_exists(p, cdir)
        content = f"""# Legal Accuracy Review Checklist - {country} ({iso})

**Generated:** {TODAY}
**Status:** FRAMEWORK TEMPLATE - FOR QUALIFIED COUNSEL/ORGANIZATION TAILORING
**Guardrail:** Not legal advice. No fabricated citations, docket numbers, or authenticated evidence claims. All precedents/holdings must be independently verified.

## Country Profile
- Country: {country} ({iso})
- Campaign: US_{iso}_{country.replace(" ", "_").upper()}
- Primary Issues: {prof.get("issue", "")}
- Core Treaty/Source Anchors (verify): {prof.get("instruments", "")}

{PRECEDENT_FRAMEWORK}

## E. Country-Specific Tailoring Checklist
- [ ] Identify specific defendants/entities and sovereign/status analysis
- [ ] Map claims to verified facts in `03_Evidentiary_Exhibits/Immutable_Ledger/`
- [ ] Confirm forum, venue, and service pathway
- [ ] Verify treaty/instrument citations from primary text
- [ ] Prepare damages/restitution valuation with expert support
- [ ] Complete authentication/chain-of-custody declarations for each exhibit
- [ ] Counsel sign-off before any filing or external reliance
"""
        p.write_text(content, encoding="utf-8", newline="\n")

        # Affidavit/declaration template
        a = cdir / "03_Evidentiary_Exhibits" / "AUTHENTICATION_DECLARATION_TEMPLATE.md"
        write(
            a,
            f"# Authentication & Chain-of-Custody Declaration Template - {country} ({iso})\n\nGenerated: {TODAY}\n"
            + AFFIDAVIT_TEMPLATE,
            cdir,
        )

        # Filing-grade package index
        idx = cdir / "99_Archives_and_Manifests" / "FILING_GRADE_PACKAGE_INDEX.md"
        write(
            idx,
            f"""# Filing-Grade Package Index - {country} ({iso})

**Generated:** {TODAY}
**Status:** FRAMEWORK/SCAFFOLD - FOR COUNSEL/ORGANIZATION TAILORING. Not filing-ready without verification.

## Package Components
| Component | Path | Status | Verification |
|---|---|---|---|
| Master Federal Complaint (DOCX scaffold) | `01_Pleadings_and_Complaints/master_federal_court_complaint_{iso.lower()}_v1.docx` | SCAFFOLD | Counsel review, verified facts/citations required |
| Discovery Plan (DOCX scaffold) | `02_Discovery_and_Evidentiary/discovery_plan_{iso.lower()}_v1.docx` | SCAFFOLD | Counsel review required |
| Motions Package (DOCX scaffold) | `03_Motions_and_Briefs/motion_package_{iso.lower()}_v1.docx` | SCAFFOLD | Counsel review required |
| Tribunal Submission (DOCX scaffold) | `04_International_Tribunals/tribunal_submission_{iso.lower()}_v1.docx` | SCAFFOLD | Counsel/forum review required |
| Enforcement & Restitution (DOCX scaffold) | `07_Enforcement_and_Restitution/enforcement_restitution_{iso.lower()}_v1.docx` | SCAFFOLD | Counsel review required |
| Evidence Index | `03_Evidentiary_Exhibits/CITATION_INDEX.csv` | PENDING_LEGAL_REVIEW | No verified without local hashed artifact + human sign-off |
| Authentication Declaration Template | `03_Evidentiary_Exhibits/AUTHENTICATION_DECLARATION_TEMPLATE.md` | TEMPLATE | Requires human custodian attestation |
| Legal Accuracy Checklist | `99_Archives_and_Manifests/LEGAL_ACCURACY_REVIEW_CHECKLIST.md` | FRAMEWORK TEMPLATE | Requires qualified counsel review |

## Pre-Filing Gate (must be completed by counsel/organization)
- [ ] All citations verified against primary sources
- [ ] All exhibits authenticated with custodian declarations
- [ ] Jurisdiction/standing/immunity/limitations/damages reviewed
- [ ] No fabricated citations, docket numbers, or archival IDs
- [ ] Forum-specific formatting and procedural rules satisfied
""",
            cdir,
        )
        print("OK", name)


if __name__ == "__main__":
    main()
