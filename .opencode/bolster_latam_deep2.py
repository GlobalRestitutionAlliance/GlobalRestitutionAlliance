import csv
from pathlib import Path
from bolster_latam_deep import (
    ROOT,
    PROFILES,
    write,
    ensure,
    build_doc,
    TODAY,
    slug,
    backup_if_exists,
)

SECTORS = [
    "Sovereign_Debt_and_Financial_Coercion",
    "Natural_Resources_and_Extractivism",
    "Agriculture_Land_and_Food_Systems",
    "Infrastructure_and_Public_Utilities",
    "Telecom_and_Digital_Infrastructure",
    "Banking_and_Sanctions_Compliance",
    "Defense_Security_and_Law_Enforcement",
    "Human_Rights_and_Civil_Liberties",
    "Environmental_and_Climate_Harms",
    "Labor_Migration_and_Remittances",
    "Health_Pharma_and_Public_Services",
    "Education_Culture_and_Heritage",
    "Trade_Tariffs_and_Market_Access",
    "Maritime_Ports_and_Logistics",
    "Energy_Oil_Gas_and_Mining",
    "Real_Estate_Tourism_and_Development",
    "Media_Information_and_Surveillance",
    "Judicial_Cooperation_and_Extradition",
    "Indigenous_and_Afrodescendant_Rights",
    "Emergency_Response_and_Disaster_Recovery",
]


def add_sector_crosswalks(cdir, name, prof):
    base = cdir / "00_Master_Knowledge_Base"
    for sec in SECTORS:
        csvp = base / f"Master_{sec}_{prof['iso']}_Crosswalk_Matrix.csv"
        mdp = base / f"Master_{sec}_{prof['iso']}_Crosswalk_Dashboard.md"
        backup_if_exists(csvp, cdir)
        backup_if_exists(mdp, cdir)
        with csvp.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    "instrument_id",
                    "sector",
                    "anchor",
                    "claim_vector",
                    "evidence_status",
                    "status",
                ]
            )
            for i in range(1, 6):
                anchor = prof["anchors"][(i - 1) % len(prof["anchors"])]
                w.writerow(
                    [
                        f"{prof['iso']}-{sec[:3].upper()}-{i:02d}",
                        sec.replace("_", " "),
                        anchor,
                        "Pending evidentiary development",
                        "PENDING_PRIMARY_SOURCE",
                        "SCAFFOLDED",
                    ]
                )
        lines = [
            f"# {prof['country']} - {sec.replace('_', ' ')} Crosswalk Dashboard",
            "",
            f"**Jurisdiction:** US-{prof['iso']} {prof['country']}  ",
            f"**Sector:** {sec.replace('_', ' ')}  ",
            f"**Generated:** {TODAY}",
            "",
            "## Anchors",
            *[f"- {a}" for a in prof["anchors"]],
            "",
            "## Matrix",
            "| ID | Anchor | Evidence | Status |",
            "|---|---|---|---|",
        ]
        for i in range(1, 6):
            anchor = prof["anchors"][(i - 1) % len(prof["anchors"])]
            lines.append(
                f"| {prof['iso']}-{sec[:3].upper()}-{i:02d} | {anchor} | PENDING_PRIMARY_SOURCE | SCAFFOLDED |"
            )
        lines.append(
            "\n## Guardrail\nNo fabricated citations or docket numbers. Primary-source verification required before filing use."
        )
        mdp.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def add_more_docs(cdir, name, prof):
    iso = prof["iso"].lower()
    country = prof["country"]
    # pleadings
    for i, title, body in [
        (
            2,
            "Class Action Certification Motion (Scaffold)",
            "## Rule 23 / Class Basis\nDefine proposed classes, commonality, typicality, adequacy, and superiority after evidentiary verification.\n\n## Evidence\nMap class-wide evidence and damages methodology.",
        ),
        (
            3,
            "Motion for Preliminary Injunction (Scaffold)",
            "## Standard\nLikelihood of success, irreparable harm, balance of equities, public interest - to be supported by verified evidence.\n\n## Requested Relief\nPreservation, notice, non-dissipation, or other equitable relief as appropriate.",
        ),
        (
            4,
            "Motion for Judicial Notice (Scaffold)",
            "## Records for Notice\nPublic treaties, declassified records, official reports, and authenticated government documents - only after verification.",
        ),
    ]:
        build_doc(
            cdir / "01_Pleadings_and_Complaints" / f"pleading_{i:02d}_{iso}.md",
            f"{title} - {country}",
            prof,
            body,
            cdir,
        )
    # discovery
    for i, title, body in [
        (
            2,
            "Requests for Production (Scaffold)",
            "## RFP Categories\n- Policy and decision records\n- Financial flows and contracts\n- Communications and meeting records\n- Sanctions/export-control/compliance records",
        ),
        (
            3,
            "Interrogatories (Scaffold)",
            "## Interrogatory Topics\nIdentify persons with knowledge, decision chains, document custodians, and factual bases for defenses.",
        ),
        (
            4,
            "Rule 30(b)(6) Deposition Notice (Scaffold)",
            "## Deposition Topics\nCorporate/government representative topics tied to verified claim vectors and defenses.",
        ),
    ]:
        build_doc(
            cdir / "02_Discovery_and_Evidentiary" / f"discovery_{i:02d}_{iso}.md",
            f"{title} - {country}",
            prof,
            body,
            cdir,
        )
    # motions
    for i, title, body in [
        (
            2,
            "Opposition to Sovereign Immunity Defense (Scaffold)",
            "## Argument Framework\nAnalyze applicable FSIA/treaty/statutory exceptions only after verified fact development.\n\n## Evidence Needed\nCommercial activity, expropriation exception facts, waiver/contract nexus as applicable.",
        ),
        (
            3,
            "Opposition to Act of State / Political Question (Scaffold)",
            "## Argument Framework\nDevelop justiciable legal standards and evidentiary record; avoid conclusory political assertions.",
        ),
        (
            4,
            "Motion to Compel / Preserve (Scaffold)",
            "## Preservation & Compulsion\nSeek preservation orders, compel production, and address spoliation where supported by record.",
        ),
    ]:
        build_doc(
            cdir / "03_Motions_and_Briefs" / f"motion_{i:02d}_{iso}.md",
            f"{title} - {country}",
            prof,
            body,
            cdir,
        )
    # tribunals
    for i, title, body in [
        (
            2,
            "IACHR / Human Rights Petition Scaffold",
            "## Petition Elements\nStanding/admissibility, exhaustion analysis, rights claims, remedies - all fact-verified.",
        ),
        (
            3,
            "UN Treaty Body Submission Scaffold",
            "## Submission Elements\nState obligations, documented harms, recommended remedies, evidentiary annex plan.",
        ),
    ]:
        build_doc(
            cdir / "04_International_Tribunals" / f"tribunal_{i:02d}_{iso}.md",
            f"{title} - {country}",
            prof,
            body,
            cdir,
        )
    # doctrine
    for i, title, body in [
        (
            2,
            "Evidentiary Authentication Doctrine",
            "## Authentication\nChain of custody, hash manifests, certified records, translations, and expert validation.",
        ),
        (
            3,
            "Damages & Valuation Doctrine",
            "## Valuation\nForensic accounting, economic loss modeling, restitution/disgorgement, prejudgment interest - evidence-backed only.",
        ),
    ]:
        build_doc(
            cdir / "05_Strategic_Doctrines_and_Red_Team" / f"doctrine_{i:02d}_{iso}.md",
            f"{title} - {country}",
            prof,
            body,
            cdir,
        )
    # trial/appellate
    for i, title, body in [
        (
            2,
            "Exhibit and Witness Matrix",
            "## Matrix\nMap each claim element to exhibits, witnesses, custodians, and authentication method.",
        ),
    ]:
        build_doc(
            cdir / "06_Trial_and_Appellate_Prep" / f"trial_{i:02d}_{iso}.md",
            f"{title} - {country}",
            prof,
            body,
            cdir,
        )
    # enforcement
    for i, title, body in [
        (
            2,
            "Asset Tracing & Recovery Playbook",
            "## Tracing\nIdentify assets, intermediaries, jurisdictions, and enforcement instruments; comply with all legal process.",
        ),
        (
            3,
            "QSF / Trust Administration Scaffold",
            "## Administration\nCourt-supervised distribution, claimant verification, audit controls, tax/compliance review.",
        ),
    ]:
        build_doc(
            cdir / "07_Enforcement_and_Restitution" / f"enforcement_{i:02d}_{iso}.md",
            f"{title} - {country}",
            prof,
            body,
            cdir,
        )


def add_agents_skills(cdir, name, prof):
    ag = cdir / ".antigravity"
    agents = [
        ("agent-historical-analyst", "Historical Record & Timeline Analysis"),
        ("agent-damages-economist", "Damages, Valuation & Forensic Economics"),
        ("agent-discovery-specialist", "Discovery, Subpoenas & Custodian Mapping"),
        ("agent-immunity-strategist", "Sovereign Immunity & Jurisdiction Strategy"),
        ("agent-human-rights-counsel", "Human Rights & International Law"),
        ("agent-enforcement-marshal", "Asset Tracing & Enforcement"),
        ("agent-comms-integrity", "Public Record Integrity & Non-Fabrication Guard"),
    ]
    skills = [
        (
            "source-citation-verification",
            "Verify primary-source citations before filing",
        ),
        ("damages-modeling", "Build evidence-backed damages models"),
        ("discovery-protocol", "Plan and execute discovery workflows"),
        ("immunity-analysis", "Analyze immunity and jurisdiction defenses"),
        ("tribunal-admissibility", "Assess tribunal admissibility and standing"),
        ("asset-tracing", "Trace assets and enforcement pathways"),
        ("red-team-review", "Adversarial review for legal/factual weaknesses"),
    ]
    reg_agents = ag / "agents/agent-registry.yaml"
    reg_skills = ag / "skills/skill-registry.yaml"
    # append if not present
    if reg_agents.exists():
        txt = reg_agents.read_text(encoding="utf-8")
        for aid, role in agents:
            if aid not in txt:
                txt += f"  - id: {aid}\n    file: {aid}.yaml\n    status: ACTIVE\n    role: {role}\n"
        write(reg_agents, txt, cdir)
    if reg_skills.exists():
        txt = reg_skills.read_text(encoding="utf-8")
        for sid, desc in skills:
            if sid not in txt:
                txt += f"  - id: {sid}\n    file: {sid}.yaml\n    status: ACTIVE\n    description: {desc}\n"
        write(reg_skills, txt, cdir)
    for aid, role in agents:
        ensure(
            ag / f"agents/{aid}.yaml",
            f"agent:\n  id: {aid}\n  jurisdiction: {prof['country']}\n  status: ACTIVE\n  role: {role}\n  guardrails:\n    - no_fabricated_citations\n    - primary_source_verification_required\n",
        )
    for sid, desc in skills:
        ensure(
            ag / f"skills/{sid}.yaml",
            f"skill:\n  id: {sid}\n  jurisdiction: {prof['country']}\n  status: ACTIVE\n  description: {desc}\n  guardrails:\n    - no_fabricated_citations\n",
        )


def main():
    for name, prof in PROFILES.items():
        if name == "US_CU_CUBA":
            continue
        cdir = ROOT / name
        if not cdir.exists():
            continue
        add_sector_crosswalks(cdir, name, prof)
        add_more_docs(cdir, name, prof)
        add_agents_skills(cdir, name, prof)
        print("DEEP2", name)
    print("DONE")


if __name__ == "__main__":
    main()
