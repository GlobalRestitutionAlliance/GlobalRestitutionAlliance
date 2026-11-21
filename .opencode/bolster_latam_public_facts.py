import csv, json
from pathlib import Path
from bolster_latam_deep import ROOT, PROFILES, TODAY, backup_if_exists, write

# Well-known precedents - starting points for counsel verification. Citations are widely reported; verify before filing.
PRECEDENTS = [
    (
        "Filartiga v. Pena-Irala",
        "630 F.2d 876 (2d Cir. 1980)",
        "ATS/torture; human rights violations actionable - verify applicability/limits",
        "VERIFY_CITATION",
    ),
    (
        "Sosa v. Alvarez-Machain",
        "542 U.S. 692 (2004)",
        "ATS limited to norms of specific, universal, obligatory character",
        "VERIFY_CITATION",
    ),
    (
        "Kiobel v. Royal Dutch Petroleum Co.",
        "569 U.S. 108 (2013)",
        "ATS presumption against extraterritoriality; touch and concern test",
        "VERIFY_CITATION",
    ),
    (
        "Jesner v. Arab Bank, PLC",
        "584 U.S. 241 (2018)",
        "Foreign corporations not liable under ATS - verify scope",
        "VERIFY_CITATION",
    ),
    (
        "Argentine Republic v. Amerada Hess Shipping Corp.",
        "488 U.S. 428 (1989)",
        "FSIA is sole basis for jurisdiction over foreign sovereign; expropriation/commercial exceptions analyzed",
        "VERIFY_CITATION",
    ),
    (
        "Siderman de Blake v. Republic of Argentina",
        "965 F.2d 699 (9th Cir. 1992)",
        "FSIA/torture/jus cogens arguments - verify holdings and current status",
        "VERIFY_CITATION",
    ),
    (
        "Republic of Austria v. Altmann",
        "541 U.S. 677 (2004)",
        "FSIA expropriation exception; retroactivity considerations - verify",
        "VERIFY_CITATION",
    ),
    (
        "Bolivarian Republic of Venezuela v. Helmerich & Payne Int'l Drilling Co.",
        "581 U.S. 170 (2017)",
        "FSIA expropriation exception requires non-frivolous argument",
        "VERIFY_CITATION",
    ),
]


def load_citations(cdir):
    p = cdir / "03_Evidentiary_Exhibits" / "CITATION_INDEX.csv"
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    for name, prof in PROFILES.items():
        if name == "US_CU_CUBA":
            continue
        cdir = ROOT / name
        if not cdir.exists():
            continue
        cites = load_citations(cdir)
        iso = prof["iso"]
        country = prof["country"]
        lines = [
            f"# Public Facts, Precedents & Verifiable Sources - {country} ({iso})",
            "",
            f"**Generated:** {TODAY}",
            "**Status:** FRAMEWORK/RESEARCH STARTING POINTS. Not legal advice. Not counsel verification.",
            "**Guardrail:** No fabricated citations, docket numbers, archival IDs, or authenticated-evidence claims. All case citations/holdings must be independently verified before reliance.",
            "",
            "## 1. Campaign Profile (Repository-Verified)",
            f"- Country: {country} ({iso})",
            f"- Primary Issues: {prof.get('issue', '')}",
            f"- Treaty/Instrument Anchors (verify): {prof.get('instruments', '')}",
            "",
            "## 2. Precedent Research Starting Points (Verify Before Reliance)",
            "| Case | Citation | Relevance | Status |",
            "|---|---|---|---|",
        ]
        for case, cit, rel, st in PRECEDENTS:
            lines.append(f"| {case} | {cit} | {rel} | {st} |")
        lines += [
            "",
            "## 3. Harvested Public-Source Artifacts (Local Hashed, PENDING_LEGAL_REVIEW)",
            "| Citation ID | Title | Authoring Body | URL | Local Artifact | SHA-256 | Ref | Status |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
        for c in cites:
            lines.append(
                f"| {c.get('citation_id', '')} | {str(c.get('title', ''))[:60]} | {str(c.get('authoring_body', ''))[:30]} | {c.get('url', '')} | `{c.get('local_artifact', '')}` | `{str(c.get('sha256', ''))[:16]}...` | {c.get('page_paragraph_ref', '')} | {c.get('verification_status', 'PENDING_LEGAL_REVIEW')} |"
            )
        lines += [
            "",
            "## 4. Affidavit / Declaration Templates (For Human Attestation)",
            "- `03_Evidentiary_Exhibits/AUTHENTICATION_DECLARATION_TEMPLATE.md` - chain-of-custody/authentication declaration template (requires human custodian attestation).",
            "",
            "## 5. Verification Gates",
            "- [ ] Independently verify every case citation and holding before use.",
            "- [ ] Verify treaty/instrument text from official source.",
            "- [ ] Authenticate exhibits with custodian declarations and certified originals where required.",
            "- [ ] Counsel/organization review before any filing or external reliance.",
        ]
        out = cdir / "00_Master_Knowledge_Base" / "PUBLIC_FACTS_AND_PRECEDENTS.md"
        backup_if_exists(out, cdir)
        write(out, "\n".join(lines) + "\n", cdir)
        print("OK", name)


if __name__ == "__main__":
    main()
