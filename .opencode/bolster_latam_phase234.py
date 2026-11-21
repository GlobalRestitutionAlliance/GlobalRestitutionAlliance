import hashlib, os
from pathlib import Path
from bolster_latam_deep import ROOT, PROFILES, write, build_doc, TODAY, backup_if_exists


def sha256(p: Path):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def add_phase2_docs(cdir, prof):
    iso = prof["iso"].lower()
    c = prof["country"]
    # more filing-grade scaffolds (MD) - verification required
    docs = [
        (
            "01_Pleadings_and_Complaints",
            f"complaint_exhibit_index_{iso}.md",
            "Complaint Exhibit Index (Scaffold)",
            "## Exhibit Index\nMap each allegation to exhibit, source, authentication method, and custodian. No exhibits listed without verification.",
        ),
        (
            "01_Pleadings_and_Complaints",
            f"damages_methodology_{iso}.md",
            "Damages Methodology (Scaffold)",
            "## Methodology\nEconomic loss, restitution, disgorgement, interest, and equitable adjustments - all require expert/forensic support.",
        ),
        (
            "02_Discovery_and_Evidentiary",
            f"esi_protocol_{iso}.md",
            "ESI Protocol (Scaffold)",
            "## ESI Protocol\nPreservation, collection, processing, review, production formats, privilege log, and clawback terms.",
        ),
        (
            "02_Discovery_and_Evidentiary",
            f"subpoena_schedule_{iso}.md",
            "Subpoena Schedule (Scaffold)",
            "## Subpoena Targets\nIdentify agencies, custodians, banks, and third parties after legal/factual verification.",
        ),
        (
            "03_Motions_and_Briefs",
            f"motion_summary_judgment_{iso}.md",
            "Summary Judgment Motion Scaffold",
            "## Standard\nIdentify undisputed material facts supported by verified evidence; address defenses and remedies.",
        ),
        (
            "03_Motions_and_Briefs",
            f"daubert_frye_expert_motion_{iso}.md",
            "Expert Admissibility Motion Scaffold",
            "## Expert Reliability\nMethodology, qualifications, fit, and evidentiary reliability - pending expert retention/verification.",
        ),
        (
            "04_International_Tribunals",
            f"icj_iachr_memorial_outline_{iso}.md",
            "International Memorial Outline (Scaffold)",
            "## Memorial Outline\nJurisdiction/admissibility, facts, legal claims, remedies, annexes - verify all sources.",
        ),
        (
            "04_International_Tribunals",
            f"exequatur_enforcement_package_{iso}.md",
            "Exequatur & Enforcement Package (Scaffold)",
            "## Recognition/Enforcement\nDomestic recognition, treaty basis, service, defenses, asset attachment - jurisdiction-specific verification required.",
        ),
        (
            "05_Strategic_Doctrines_and_Red_Team",
            f"attrition_countermeasures_{iso}.md",
            "Attrition & Countermeasure Doctrine (Scaffold)",
            "## Countermeasures\nTimeline control, preservation, sanctions for spoliation, burden-shifting, and procedural resilience.",
        ),
        (
            "05_Strategic_Doctrines_and_Red_Team",
            f"narrative_integrity_policy_{iso}.md",
            "Narrative Integrity & Non-Fabrication Policy",
            "## Policy\nNo fabricated citations, no unverified quotes, no synthetic evidence presented as authentic. All public statements must be source-backed.",
        ),
        (
            "06_Trial_and_Appellate_Prep",
            f"jury_instructions_outline_{iso}.md",
            "Jury/Findings Instructions Outline (Scaffold)",
            "## Instructions/Findings\nElements, burden of proof, causation, damages, defenses - jurisdiction and claim specific.",
        ),
        (
            "06_Trial_and_Appellate_Prep",
            f"appellate_preservation_checklist_{iso}.md",
            "Appellate Preservation Checklist",
            "## Preservation\nObjections, offers of proof, post-trial motions, record citations, standards of review.",
        ),
        (
            "07_Enforcement_and_Restitution",
            f"judgment_enforcement_checklist_{iso}.md",
            "Judgment Enforcement Checklist (Scaffold)",
            "## Enforcement\nDomestic registration, foreign recognition, asset discovery, garnishment/attachment, receivership, compliance monitoring.",
        ),
        (
            "07_Enforcement_and_Restitution",
            f"claimant_distribution_protocol_{iso}.md",
            "Claimant Distribution Protocol (Scaffold)",
            "## Distribution\nEligibility, verification, anti-fraud controls, audit trail, appeals, privacy, tax compliance.",
        ),
    ]
    for folder, fn, title, body in docs:
        build_doc(cdir / folder / fn, f"{title} - {c}", prof, body, cdir)


def add_phase4_review(cdir, prof):
    p = cdir / "99_Archives_and_Manifests" / "LEGAL_ACCURACY_REVIEW_CHECKLIST.md"
    content = f"""# Legal Accuracy & Verification Review Checklist - {prof["country"]}

**Generated:** {TODAY}  
**Status:** REQUIRED BEFORE EXTERNAL USE/FILING

## 1. Evidence Verification
- [ ] Every factual assertion has a primary-source citation.
- [ ] No fabricated citations, docket numbers, archival IDs, or quotes.
- [ ] Documents/translations authenticated; chain of custody recorded.
- [ ] `03_Evidentiary_Exhibits` contains only verified, lawfully obtained materials.

## 2. Legal Review
- [ ] Jurisdiction, standing, and venue verified.
- [ ] Sovereign immunity / FSIA / act-of-state / comity analyzed.
- [ ] Statutes of limitation/prescription and tolling analyzed.
- [ ] Causation, damages, and remedies supported by admissible evidence.
- [ ] Forum-specific procedural rules complied with.

## 3. Integrity & Compliance
- [ ] `VERIFICATION_KEYS/sha256_manifest.txt` regenerated.
- [ ] CI integrity workflow passes.
- [ ] Sensitive personal data redacted/minimized as required.
- [ ] Public communications reviewed for accuracy and non-defamation.

## 4. Sign-off
- [ ] Legal counsel review completed.
- [ ] Fact/evidence review completed.
- [ ] Security/integrity review completed.
"""
    write(p, content, cdir)


def refresh_sha256(cdir):
    manifest = cdir / "VERIFICATION_KEYS/sha256_manifest.txt"
    backup_if_exists(manifest, cdir)
    lines = []
    for p in sorted(cdir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(cdir).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel == "VERIFICATION_KEYS/sha256_manifest.txt":
            continue
        lines.append(f"{sha256(p)}  {rel}")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main():
    for name, prof in PROFILES.items():
        if name == "US_CU_CUBA":
            continue
        cdir = ROOT / name
        if not cdir.exists():
            continue
        add_phase2_docs(cdir, prof)
        add_phase4_review(cdir, prof)
        refresh_sha256(cdir)
        print("PHASE234", name)
    print("DONE")


if __name__ == "__main__":
    main()
