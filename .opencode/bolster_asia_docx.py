from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.style import WD_STYLE_TYPE
from bolster_asia_full import ROOT, PROFILES, TODAY, write


def set_base(doc):
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)


def add_header(doc, title, prof):
    doc.add_paragraph("GLOBAL RESTITUTION ALLIANCE").runs[0].bold = True
    doc.add_paragraph(
        f"UNITED STATES – {prof['country'].upper()} MASTER LITIGATION"
    ).runs[0].bold = True
    doc.add_paragraph(title).runs[0].bold = True
    doc.add_paragraph(
        f"Jurisdiction: US-{prof['iso']} {prof['country']} | Generated: {TODAY} | Status: SCAFFOLD - VERIFICATION REQUIRED"
    )
    doc.add_paragraph(
        "CONFIDENTIAL DRAFT - NOT FOR FILING WITHOUT LEGAL/EVIDENTIARY VERIFICATION"
    ).runs[0].bold = True
    doc.add_paragraph("_" * 78)


def add_footer_guard(doc):
    doc.add_page_break()
    doc.add_paragraph("VERIFICATION GUARDRAIL").runs[0].bold = True
    doc.add_paragraph(
        "This document is a scaffold. No fabricated citations, docket numbers, archival IDs, or authenticated evidence are included. All facts, citations, damages, and legal arguments require primary-source verification and qualified legal review before any external use or filing."
    )


def make_doc(path, title, prof, sections):
    doc = Document()
    set_base(doc)
    add_header(doc, title, prof)
    for h, body in sections:
        doc.add_heading(h, level=1)
        for para in body.split("\n"):
            if para.strip():
                doc.add_paragraph(para.strip())
    add_footer_guard(doc)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(path))


def main():
    for name, prof in PROFILES.items():
        if name == "US_CU_CUBA":
            continue
        cdir = ROOT / name
        iso = prof["iso"].lower()
        country = prof["country"]
        docs = [
            (
                cdir
                / "01_Pleadings_and_Complaints"
                / f"master_federal_court_complaint_{iso}_v1.docx",
                f"Master Federal Court Complaint - {country}",
                [
                    (
                        "I. INTRODUCTION",
                        "This scaffold complaint outlines potential claims arising from documented/public-record anchors. All allegations must be verified with primary sources before filing.",
                    ),
                    (
                        "II. PARTIES",
                        "Identify plaintiffs/claimants, defendants, and relevant agencies/entities after verification.",
                    ),
                    (
                        "III. JURISDICTION AND VENUE",
                        "To be completed with verified jurisdictional statutes, sovereign immunity exceptions, and venue analysis.",
                    ),
                    (
                        "IV. FACTUAL ALLEGATIONS",
                        "Populate with source-cited facts only. No fabricated events, citations, or damages.",
                    ),
                    (
                        "V. CAUSES OF ACTION",
                        "Select legally supported causes of action after counsel review.",
                    ),
                    (
                        "VI. PRAYER FOR RELIEF",
                        "Declaratory/injunctive relief, damages/restitution accounting, fees/costs as permitted, and other lawful relief.",
                    ),
                ],
            ),
            (
                cdir / "02_Discovery_and_Evidentiary" / f"discovery_plan_{iso}_v1.docx",
                f"Discovery Plan - {country}",
                [
                    (
                        "I. PRESERVATION",
                        "Issue litigation holds/preservation notices; identify custodians and ESI sources.",
                    ),
                    (
                        "II. DOCUMENT REQUESTS",
                        "Target policies, contracts, communications, financial records, and official archives.",
                    ),
                    (
                        "III. INTERROGATORIES / DEPOSITIONS",
                        "Identify responsible witnesses and Rule 30(b)(6) topics.",
                    ),
                    (
                        "IV. AUTHENTICATION",
                        "Chain of custody, hash manifests, certified records, translations.",
                    ),
                ],
            ),
            (
                cdir / "03_Motions_and_Briefs" / f"motion_package_{iso}_v1.docx",
                f"Motions Package Scaffold - {country}",
                [
                    (
                        "I. PRESERVATION / COMPEL",
                        "Motion to preserve/compel based on verified record.",
                    ),
                    (
                        "II. IMMUNITY / JUSTICIABILITY RESPONSES",
                        "Fact-specific responses to immunity, act of state, political question, limitations defenses.",
                    ),
                    (
                        "III. SUMMARY JUDGMENT FRAMEWORK",
                        "Undisputed facts, legal standards, evidentiary support.",
                    ),
                ],
            ),
            (
                cdir
                / "04_International_Tribunals"
                / f"tribunal_submission_{iso}_v1.docx",
                f"International Tribunal Submission Scaffold - {country}",
                [
                    (
                        "I. FORUM AND ADMISSIBILITY",
                        "Assess ICJ/IACHR/UN treaty bodies/arbitral fora and standing/admissibility.",
                    ),
                    (
                        "II. FACTS AND EVIDENCE",
                        "Source-cited facts and authenticated exhibits only.",
                    ),
                    (
                        "III. REMEDIES",
                        "Restitution, reparations, guarantees of non-repetition, enforcement pathways.",
                    ),
                ],
            ),
            (
                cdir
                / "07_Enforcement_and_Restitution"
                / f"enforcement_restitution_{iso}_v1.docx",
                f"Enforcement & Restitution Plan - {country}",
                [
                    (
                        "I. JUDGMENT/ORDER RECOGNITION",
                        "Domestic and foreign recognition/exequatur pathways.",
                    ),
                    (
                        "II. ASSET TRACING",
                        "Identify assets, intermediaries, and lawful enforcement mechanisms.",
                    ),
                    (
                        "III. DISTRIBUTION",
                        "Court-supervised/QSF/trust distribution with audit controls and claimant verification.",
                    ),
                ],
            ),
        ]
        for path, title, sections in docs:
            if not path.exists():
                make_doc(path, title, prof, sections)
        print("DOCX", name)
    print("DONE")


if __name__ == "__main__":
    main()
