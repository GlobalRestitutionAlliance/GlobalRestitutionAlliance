#!/usr/bin/env python3
"""ASIA 8-repo full-enrichment wave 5."""

from __future__ import annotations
import importlib.util
from pathlib import Path

BASE = Path(r"W:\Legal")
REGION = "ASIA"
REPOS = {
    "US_NP_NEPAL": [
        (
            "Library of Congress - Nepal",
            "https://www.loc.gov/search/?q=nepal+united+states",
        ),
        ("State Dept - Nepal", "https://www.state.gov/countries-areas/nepal/"),
        (
            "UN Digital Library - Nepal",
            "https://digitallibrary.un.org/search?ln=en&p=nepal",
        ),
        ("World Bank - Nepal", "https://data.worldbank.org/country/nepal"),
        ("UNHCR - Nepal", "https://www.unhcr.org/countries/nepal"),
        ("HRW - Nepal", "https://www.hrw.org/asia/nepal"),
        (
            "Amnesty - Nepal",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-asia/nepal/",
        ),
        ("ICRC - Nepal", "https://www.icrc.org/en/where-we-work/asia-pacific/nepal"),
        ("NARA - Nepal", "https://catalog.archives.gov/search?q=nepal"),
        ("UN OHCHR - Nepal", "https://www.ohchr.org/en/countries/nepal"),
    ],
    "US_OM_OMAN": [
        (
            "Library of Congress - Oman",
            "https://www.loc.gov/search/?q=oman+united+states",
        ),
        ("State Dept - Oman", "https://www.state.gov/countries-areas/oman/"),
        (
            "UN Digital Library - Oman",
            "https://digitallibrary.un.org/search?ln=en&p=oman",
        ),
        ("World Bank - Oman", "https://data.worldbank.org/country/oman"),
        ("UNHCR - Oman", "https://www.unhcr.org/countries/oman"),
        ("HRW - Oman", "https://www.hrw.org/middle-east/north-africa/oman"),
        (
            "Amnesty - Oman",
            "https://www.amnesty.org/en/location/middle-east-and-north-africa/middle-east/oman/",
        ),
        ("ICRC - Oman", "https://www.icrc.org/en/where-we-work/middle-east/oman"),
        ("NARA - Oman", "https://catalog.archives.gov/search?q=oman"),
        ("US Embassy Oman", "https://om.usembassy.gov/"),
    ],
    "US_PK_PAKISTAN": [
        (
            "Library of Congress - Pakistan",
            "https://www.loc.gov/search/?q=pakistan+united+states",
        ),
        ("State Dept - Pakistan", "https://www.state.gov/countries-areas/pakistan/"),
        ("FRUS - Pakistan", "https://history.state.gov/countries/pakistan"),
        (
            "UN Digital Library - Pakistan",
            "https://digitallibrary.un.org/search?ln=en&p=pakistan",
        ),
        ("World Bank - Pakistan", "https://data.worldbank.org/country/pakistan"),
        ("UNHCR - Pakistan", "https://www.unhcr.org/countries/pakistan"),
        ("HRW - Pakistan", "https://www.hrw.org/asia/pakistan"),
        (
            "Amnesty - Pakistan",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-asia/pakistan/",
        ),
        ("NARA - Pakistan", "https://catalog.archives.gov/search?q=pakistan"),
        (
            "ICRC - Pakistan",
            "https://www.icrc.org/en/where-we-work/asia-pacific/pakistan",
        ),
    ],
    "US_PS_PALESTINE": [
        (
            "Library of Congress - Palestine",
            "https://www.loc.gov/search/?q=palestine+united+states",
        ),
        (
            "State Dept - Palestinian Affairs",
            "https://www.state.gov/countries-areas/palestinian-territories/",
        ),
        (
            "UN Digital Library - Palestine",
            "https://digitallibrary.un.org/search?ln=en&p=palestine",
        ),
        (
            "World Bank - West Bank Gaza",
            "https://data.worldbank.org/country/west-bank-and-gaza",
        ),
        ("UNHCR - Palestine", "https://www.unhcr.org/countries/palestine"),
        (
            "HRW - Israel Palestine",
            "https://www.hrw.org/middle-east/north-africa/israel/palestine",
        ),
        (
            "Amnesty - Palestine",
            "https://www.amnesty.org/en/location/middle-east-and-north-africa/israel-and-occupied-palestinian-territories/",
        ),
        (
            "ICRC - Israel OT",
            "https://www.icrc.org/en/where-we-work/middle-east/israel-and-occupied-territories",
        ),
        ("UNRWA", "https://www.unrwa.org/"),
        ("NARA - Palestine", "https://catalog.archives.gov/search?q=palestine"),
    ],
    "US_QA_QATAR": [
        (
            "Library of Congress - Qatar",
            "https://www.loc.gov/search/?q=qatar+united+states",
        ),
        ("State Dept - Qatar", "https://www.state.gov/countries-areas/qatar/"),
        (
            "UN Digital Library - Qatar",
            "https://digitallibrary.un.org/search?ln=en&p=qatar",
        ),
        ("World Bank - Qatar", "https://data.worldbank.org/country/qatar"),
        ("UNHCR - Qatar", "https://www.unhcr.org/countries/qatar"),
        ("HRW - Qatar", "https://www.hrw.org/middle-east/north-africa/qatar"),
        (
            "Amnesty - Qatar",
            "https://www.amnesty.org/en/location/middle-east-and-north-africa/middle-east/qatar/",
        ),
        ("ICRC - Qatar", "https://www.icrc.org/en/where-we-work/middle-east/qatar"),
        ("NARA - Qatar", "https://catalog.archives.gov/search?q=qatar"),
        ("US CENTCOM - Qatar", "https://www.centcom.mil/"),
    ],
    "US_SA_SAUDI_ARABIA": [
        (
            "Library of Congress - Saudi Arabia",
            "https://www.loc.gov/search/?q=saudi+arabia+united+states",
        ),
        (
            "State Dept - Saudi Arabia",
            "https://www.state.gov/countries-areas/saudi-arabia/",
        ),
        (
            "UN Digital Library - Saudi Arabia",
            "https://digitallibrary.un.org/search?ln=en&p=saudi+arabia",
        ),
        (
            "World Bank - Saudi Arabia",
            "https://data.worldbank.org/country/saudi-arabia",
        ),
        ("UNHCR - Saudi Arabia", "https://www.unhcr.org/countries/saudi-arabia"),
        (
            "HRW - Saudi Arabia",
            "https://www.hrw.org/middle-east/north-africa/saudi-arabia",
        ),
        (
            "Amnesty - Saudi Arabia",
            "https://www.amnesty.org/en/location/middle-east-and-north-africa/middle-east/saudi-arabia/",
        ),
        (
            "ICRC - Saudi Arabia",
            "https://www.icrc.org/en/where-we-work/middle-east/saudi-arabia",
        ),
        ("NARA - Saudi Arabia", "https://catalog.archives.gov/search?q=saudi+arabia"),
        ("FRUS - Saudi Arabia", "https://history.state.gov/countries/saudi-arabia"),
    ],
    "US_SG_SINGAPORE": [
        (
            "Library of Congress - Singapore",
            "https://www.loc.gov/search/?q=singapore+united+states",
        ),
        ("State Dept - Singapore", "https://www.state.gov/countries-areas/singapore/"),
        (
            "UN Digital Library - Singapore",
            "https://digitallibrary.un.org/search?ln=en&p=singapore",
        ),
        ("World Bank - Singapore", "https://data.worldbank.org/country/singapore"),
        ("UNHCR - Singapore", "https://www.unhcr.org/countries/singapore"),
        ("HRW - Singapore", "https://www.hrw.org/asia/singapore"),
        (
            "Amnesty - Singapore",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-east-asia-and-the-pacific/singapore/",
        ),
        (
            "ICRC - Singapore",
            "https://www.icrc.org/en/where-we-work/asia-pacific/singapore",
        ),
        ("NARA - Singapore", "https://catalog.archives.gov/search?q=singapore"),
        ("ASEAN - Singapore", "https://asean.org/member-states/singapore/"),
    ],
    "US_SY_SYRIA": [
        (
            "Library of Congress - Syria",
            "https://www.loc.gov/search/?q=syria+united+states",
        ),
        ("State Dept - Syria", "https://www.state.gov/countries-areas/syria/"),
        (
            "UN Digital Library - Syria",
            "https://digitallibrary.un.org/search?ln=en&p=syrian+arab+republic",
        ),
        (
            "World Bank - Syria",
            "https://data.worldbank.org/country/syrian-arab-republic",
        ),
        ("UNHCR - Syria", "https://www.unhcr.org/countries/syria"),
        ("HRW - Syria", "https://www.hrw.org/middle-east/north-africa/syria"),
        (
            "Amnesty - Syria",
            "https://www.amnesty.org/en/location/middle-east-and-north-africa/middle-east/syria/",
        ),
        ("ICRC - Syria", "https://www.icrc.org/en/where-we-work/middle-east/syria"),
        ("NARA - Syria", "https://catalog.archives.gov/search?q=syria"),
        ("UN OHCHR - Syria", "https://www.ohchr.org/en/countries/syrian-arab-republic"),
    ],
}
spec = importlib.util.spec_from_file_location(
    "asiaw", str(BASE / ".opencode" / "pilot_batch_asia8_wave1.py")
)
asia = importlib.util.module_from_spec(spec)
spec.loader.exec_module(asia)


def main():
    for name, sources in REPOS.items():
        repo = BASE / REGION / name
        if not repo.exists():
            print("MISSING", repo)
            continue
        asia.ensure_source_registry(repo, sources)
        asia.ensure_valuation(repo)
        asia.ensure_vectors(repo)
        asia.harvest(repo, sources)
        asia.build_citation_indexes(repo)
        asia.refresh_manifest(repo)
        print("DONE", name)


if __name__ == "__main__":
    main()
