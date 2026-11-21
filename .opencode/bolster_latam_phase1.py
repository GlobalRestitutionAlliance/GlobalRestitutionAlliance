from pathlib import Path
from bolster_latam_deep import ROOT, PROFILES, write, ensure, TODAY

AGENT_ROLES = [
    ("lead-counsel", "Lead Strategic Counsel & Campaign Coordination"),
    ("archival-sentinel", "Archival Retrieval & Evidence Authentication"),
    ("procedural-blacksmith", "Pleadings & Procedural Compliance"),
    ("tribunals-envoy", "International Tribunals & Exequatur"),
    ("red-team-adversary", "Adversarial Defense Simulation"),
    ("damages-economist", "Damages, Valuation & Forensic Economics"),
    ("discovery-specialist", "Discovery & Custodian Mapping"),
    ("immunity-strategist", "Sovereign Immunity & Jurisdiction Strategy"),
    ("human-rights-counsel", "Human Rights & International Law"),
    ("enforcement-marshal", "Asset Tracing & Enforcement"),
    ("sanctions-analyst", "Sanctions/OFAC Compliance Analysis"),
    ("corporate-forensics", "Corporate Veil & Forensic Accounting"),
    ("treaty-historian", "Treaty & Diplomatic History Analysis"),
    ("indigenous-rights", "Indigenous & Afrodescendant Rights"),
    ("environmental-harms", "Environmental & Climate Harms"),
    ("labor-migration", "Labor, Migration & Remittances"),
    ("public-health", "Public Health & Services Harms"),
    ("media-integrity", "Public Record Integrity & Communications"),
    ("appellate-strategist", "Appellate Preservation & Strategy"),
    ("qsf-trustee", "QSF/Trust Administration"),
]
# expand to 170 by sector/specialty variants
SECTORS = [
    "Debt",
    "Energy",
    "Mining",
    "Agriculture",
    "Infrastructure",
    "Telecom",
    "Banking",
    "Defense",
    "HumanRights",
    "Environment",
    "Labor",
    "Health",
    "Education",
    "Trade",
    "Maritime",
    "RealEstate",
    "Media",
    "Judicial",
    "Indigenous",
    "Disaster",
]
for s in SECTORS:
    for i in range(1, 9):  # 160 more
        AGENT_ROLES.append(
            (
                f"sector-{s.lower()}-{i:02d}",
                f"{s} Sector Specialist #{i} - Evidence & Liability Mapping",
            )
        )

SKILL_BASE = [
    "source-citation-verification",
    "damages-modeling",
    "discovery-protocol",
    "immunity-analysis",
    "tribunal-admissibility",
    "asset-tracing",
    "red-team-review",
    "timeline-construction",
    "document-authentication",
    "chain-of-custody-audit",
    "crosswalk-generation",
    "complaint-drafting",
    "motion-drafting",
    "brief-drafting",
    "discovery-drafting",
    "tribunal-petition-drafting",
    "settlement-trust-design",
    "expert-witness-coordination",
    "translation-verification",
    "public-record-corroboration",
]
SKILLS = []
for b in SKILL_BASE:
    SKILLS.append((b, b.replace("-", " ").title()))
for s in SECTORS:
    for i in range(1, 13):  # 240 more
        SKILLS.append((f"{s.lower()}-skill-{i:02d}", f"{s} Skill #{i} - Scaffold"))
# trim/pad to ~252
SKILLS = SKILLS[:252]
AGENTS = AGENT_ROLES[:170]


def write_agents(cdir, prof):
    ag = cdir / ".antigravity"
    agents_dir = ag / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    lines = ["registry: Agent Registry", "version: 2.0.0", "agents:"]
    for aid, role in AGENTS:
        fid = f"{aid}.yaml"
        lines += [
            f"  - id: {aid}",
            f"    file: {fid}",
            "    status: ACTIVE_SCAFFOLD",
            f"    role: {role}",
        ]
        ensure(
            agents_dir / fid,
            f"agent:\n  id: {aid}\n  jurisdiction: {prof['country']}\n  iso: {prof['iso']}\n  status: ACTIVE_SCAFFOLD\n  role: {role}\n  guardrails:\n    - no_fabricated_citations\n    - primary_source_verification_required\n    - legal_review_required_before_filing\n",
        )
    write(ag / "agents/agent-registry.yaml", "\n".join(lines) + "\n", cdir)


def write_skills(cdir, prof):
    ag = cdir / ".antigravity"
    skills_dir = ag / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    lines = ["registry: Skill Registry", "version: 2.0.0", "skills:"]
    for sid, desc in SKILLS:
        fid = f"{sid}.yaml"
        lines += [
            f"  - id: {sid}",
            f"    file: {fid}",
            "    status: ACTIVE_SCAFFOLD",
            f"    description: {desc}",
        ]
        ensure(
            skills_dir / fid,
            f"skill:\n  id: {sid}\n  jurisdiction: {prof['country']}\n  iso: {prof['iso']}\n  status: ACTIVE_SCAFFOLD\n  description: {desc}\n  guardrails:\n    - no_fabricated_citations\n    - primary_source_verification_required\n",
        )
    write(ag / "skills/skill-registry.yaml", "\n".join(lines) + "\n", cdir)


def write_vectors(cdir, prof):
    vdir = cdir / ".antigravity/knowledge/vector-index"
    vdir.mkdir(parents=True, exist_ok=True)
    anchors = prof["anchors"]
    # 1805 vectors across 19 blocks of 95? 19*95=1805
    total = 1805
    block_size = 95
    blocks = (total + block_size - 1) // block_size
    for b in range(blocks):
        start = b * block_size + 1
        end = min((b + 1) * block_size, total)
        p = vdir / f"vectors-{start:04d}-{end:04d}.yaml"
        if p.exists():
            continue
        lines = [
            f"vector_index_block:\n  jurisdiction: {prof['country']}\n  iso: {prof['iso']}\n  block: {b + 1}\n  range: [{start},{end}]\n  status: SCAFFOLDED_PENDING_VERIFICATION\n  vectors:"
        ]
        for i in range(start, end + 1):
            anchor = anchors[(i - 1) % len(anchors)]
            lines.append(
                f'    - vector_id: "{prof["iso"]}-V-{i:04d}"\n      anchor: "{anchor}"\n      claim_vector: "Pending evidentiary development"\n      evidence_status: PENDING_PRIMARY_SOURCE\n      verification_required: true'
            )
        p.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main():
    for name, prof in PROFILES.items():
        if name == "US_CU_CUBA":
            continue
        cdir = ROOT / name
        if not cdir.exists():
            continue
        write_agents(cdir, prof)
        write_skills(cdir, prof)
        write_vectors(cdir, prof)
        print("PHASE1", name)
    print("DONE", len(AGENTS), len(SKILLS), 1805)


if __name__ == "__main__":
    main()
