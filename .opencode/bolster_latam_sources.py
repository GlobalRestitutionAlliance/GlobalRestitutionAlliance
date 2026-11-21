import csv
from pathlib import Path
from bolster_latam_deep import ROOT, PROFILES, TODAY, backup_if_exists, write

# Real, publicly accessible source portals. Country-specific report links included where verified from public OAS/ICJ pages.
IACHR_REPORTS = {
    "AR": [
        (
            "IACHR - Report on the Situation of Human Rights in Argentina (1980)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
    "BO": [
        (
            "IACHR - Access to Justice and Social Inclusion: The Road towards Strengthening Democracy in Bolivia (2007)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        ),
        (
            "IACHR - Follow-up Report on Access to Justice and Social Inclusion in Bolivia (2009)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        ),
    ],
    "BR": [
        (
            "IACHR - Report on the Situation of Human Rights in Brazil (1997)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        ),
        (
            "IACHR - Situation of Human Rights in Brazil (2021)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        ),
    ],
    "CL": [
        (
            "IACHR - Report on the Situation of Human Rights in Chile (1974/1976/1977)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        ),
        (
            "IACHR - Situation of Human Rights in Chile (2022)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        ),
    ],
    "CO": [
        (
            "IACHR - Truth, Justice and Reparation - Colombia (2013)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        ),
        (
            "IACHR - Colombia country reports",
            "https://www.oas.org/en/iachr/reports/country.asp",
        ),
    ],
    "CU": [
        (
            "IACHR - Situation of Human Rights in Cuba (2020)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
    "DO": [
        (
            "IACHR - Situation of Human Rights in Dominican Republic (2015)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
    "EC": [
        (
            "IACHR - Report on the Situation of Human Rights in Ecuador (1997)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
    "SV": [
        (
            "IACHR - Situation of Human Rights in El Salvador (2021)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
    "GT": [
        (
            "IACHR - Justice and Social Inclusion: The Challenges of Democracy in Guatemala (2003)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        ),
        (
            "IACHR - Situation of Human Rights in Guatemala (2017)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        ),
    ],
    "HT": [
        (
            "IACHR - Situation of Human Rights in Haiti (2022)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
    "HN": [
        (
            "IACHR - Situation of Human Rights in Honduras (2024)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
    "JM": [
        (
            "IACHR - Report on the Situation of Human Rights in Jamaica (2012)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
    "MX": [
        (
            "IACHR - Situation of Human Rights in Mexico (2015)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
    "NI": [
        (
            "IACHR - Nicaragua: Concentration of Power and Weakened Rule of Law (2021)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
    "PA": [
        (
            "IACHR - Report on the Situation of Human Rights in Panama (1989)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
    "PY": [
        (
            "IACHR - Third Report on the Situation of Human Rights in Paraguay (2001)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
    "PE": [
        (
            "IACHR - Second Report on the Situation of Human Rights in Peru (2000)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
    "UY": [
        (
            "IACHR - Report on the Situation of Human Rights in Uruguay (1978)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
    "VE": [
        (
            "IACHR - Venezuela: Serious Human Rights Violations Following the Elections (2025)",
            "https://www.oas.org/en/iachr/reports/country.asp",
        )
    ],
}

ICJ_CASES = {
    "NI": [
        (
            "ICJ - Military and Paramilitary Activities in and against Nicaragua (Nicaragua v. United States of America)",
            "https://www.icj-cij.org/case/70",
        )
    ],
    "HN": [
        (
            "ICJ - Border and Transborder Armed Actions (Nicaragua v. Honduras) - related regional context",
            "https://www.icj-cij.org/cases",
        )
    ],
    "CO": [
        (
            "ICJ - Alleged Violations of Sovereign Rights and Maritime Spaces in the Caribbean Sea (Nicaragua v. Colombia)",
            "https://www.icj-cij.org/cases",
        )
    ],
    "BO": [
        (
            "ICJ - Obligation to Negotiate Access to the Pacific Ocean (Bolivia v. Chile)",
            "https://www.icj-cij.org/case/153",
        )
    ],
    "CL": [
        (
            "ICJ - Obligation to Negotiate Access to the Pacific Ocean (Bolivia v. Chile)",
            "https://www.icj-cij.org/case/153",
        )
    ],
    "GY": [
        (
            "ICJ - Arbitral Award of 3 October 1899 (Guyana v. Venezuela)",
            "https://www.icj-cij.org/case/171",
        )
    ],
    "VE": [
        (
            "ICJ - Arbitral Award of 3 October 1899 (Guyana v. Venezuela)",
            "https://www.icj-cij.org/case/171",
        )
    ],
    "GT": [
        (
            "ICJ - Nottebohm (Liechtenstein v. Guatemala)",
            "https://www.icj-cij.org/case/18",
        )
    ],
}

GENERIC_SOURCES = [
    ("UN Digital Library - Search", "https://digitallibrary.un.org/search"),
    ("UN OHCHR - Country Pages", "https://www.ohchr.org/en/countries"),
    (
        "UN Treaty Body Database",
        "https://tbinternet.ohchr.org/_layouts/15/TreatyBodyExternal/TBSearch.aspx",
    ),
    (
        "UN Human Rights Council - Universal Periodic Review",
        "https://www.ohchr.org/en/hr-bodies/upr/upr-home",
    ),
    ("IACHR - Country Reports", "https://www.oas.org/en/iachr/reports/country.asp"),
    ("IACHR - Annual Reports", "https://www.oas.org/en/iachr/reports/ia.asp"),
    (
        "US State Department - Country Reports on Human Rights Practices",
        "https://www.state.gov/reports-bureau-of-democracy-human-rights-and-labor/country-reports-on-human-rights-practices/",
    ),
    (
        "US State Department - Office of the Historian (FRUS)",
        "https://history.state.gov/historicaldocuments",
    ),
    (
        "NARA - Foreign Affairs Research",
        "https://www.archives.gov/research/foreign-policy",
    ),
    ("CIA FOIA Electronic Reading Room", "https://www.cia.gov/reading-room/"),
    (
        "Library of Congress - Research Guides / Country Studies",
        "https://guides.loc.gov/",
    ),
    ("World Bank - Country Data", "https://data.worldbank.org/country"),
    ("UNDP - Human Development Reports", "https://hdr.undp.org/"),
    ("ICJ - List of Cases", "https://www.icj-cij.org/cases"),
    ("UN Treaty Collection", "https://treaties.un.org/"),
]


def build_sources(name, prof):
    cdir = ROOT / name
    iso = prof["iso"]
    rows = []
    # country-specific
    for t, u in IACHR_REPORTS.get(iso, []):
        rows.append(
            (
                iso,
                prof["country"],
                "IACHR",
                t,
                u,
                "PUBLIC_PORTAL",
                "VERIFY_AND_DOWNLOAD",
            )
        )
    for t, u in ICJ_CASES.get(iso, []):
        rows.append(
            (iso, prof["country"], "ICJ", t, u, "PUBLIC_PORTAL", "VERIFY_AND_DOWNLOAD")
        )
    # generic
    for t, u in GENERIC_SOURCES:
        rows.append(
            (
                iso,
                prof["country"],
                "PUBLIC_SOURCE",
                t,
                u,
                "PUBLIC_PORTAL",
                "VERIFY_AND_DOWNLOAD",
            )
        )

    md = [
        f"# Verified Public Sources - {prof['country']} ({iso})",
        "",
        f"**Generated:** {TODAY}",
        "**Status:** Public-source registry. Links require verification/access review before evidentiary use.",
        "",
        "## Country-Specific Sources",
        "",
    ]
    seen = set()
    for _, _, typ, t, u, _, _ in rows:
        key = (t, u)
        if key in seen:
            continue
        seen.add(key)
        if typ in ("IACHR", "ICJ"):
            md.append(f"- **[{t}]({u})** ({typ})")
    md += ["", "## General Authoritative Portals", ""]
    for t, u in GENERIC_SOURCES:
        md.append(f"- [{t}]({u})")
    md += [
        "",
        "## Evidentiary Use Rules",
        "- Capture URL, access date, archive hash, and custodian for every downloaded artifact.",
        "- Prefer official PDFs/original scans over secondary summaries.",
        "- Do not treat links as authenticated evidence until chain-of-custody is recorded.",
    ]

    p_md = cdir / "03_Evidentiary_Exhibits" / "PRIMARY_PUBLIC_SOURCES.md"
    write(p_md, "\n".join(md) + "\n", cdir)

    p_csv = cdir / "03_Evidentiary_Exhibits" / "PRIMARY_PUBLIC_SOURCES.csv"
    backup_if_exists(p_csv, cdir)
    with p_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            ["iso", "country", "source_type", "title", "url", "access_class", "status"]
        )
        for r in rows:
            w.writerow(r)

    # also copy to knowledge base
    p2 = cdir / "00_Master_Knowledge_Base" / "PRIMARY_PUBLIC_SOURCES.md"
    write(p2, "\n".join(md) + "\n", cdir)


def main():
    for name, prof in PROFILES.items():
        if name == "US_CU_CUBA":
            continue
        cdir = ROOT / name
        if not cdir.exists():
            continue
        build_sources(name, prof)
        print("SOURCES", name)
    print("DONE")


if __name__ == "__main__":
    main()
