#!/usr/bin/env python3
"""ASIA 8-repo full-enrichment wave 3."""

from __future__ import annotations
import importlib.util
from pathlib import Path

BASE = Path(r"W:\Legal")
REGION = "ASIA"
REPOS = {
    "US_CY_CYPRUS": [
        (
            "Library of Congress - Cyprus",
            "https://www.loc.gov/search/?q=cyprus+united+states",
        ),
        ("State Dept - Cyprus", "https://www.state.gov/countries-areas/cyprus/"),
        (
            "UN Digital Library - Cyprus",
            "https://digitallibrary.un.org/search?ln=en&p=cyprus",
        ),
        ("World Bank - Cyprus", "https://data.worldbank.org/country/cyprus"),
        ("UNHCR - Cyprus", "https://www.unhcr.org/countries/cyprus"),
        ("HRW - Cyprus", "https://www.hrw.org/europe/central-asia/cyprus"),
        (
            "Amnesty - Cyprus",
            "https://www.amnesty.org/en/location/europe-and-central-asia/europe/cyprus/",
        ),
        (
            "ICRC - Cyprus",
            "https://www.icrc.org/en/where-we-work/europe-central-asia/cyprus",
        ),
        ("NARA - Cyprus", "https://catalog.archives.gov/search?q=cyprus"),
        ("UN Peacekeeping - UNFICYP", "https://peacekeeping.un.org/en/mission/unficyp"),
    ],
    "US_GE_GEORGIA": [
        (
            "Library of Congress - Georgia",
            "https://www.loc.gov/search/?q=georgia+country+united+states",
        ),
        ("State Dept - Georgia", "https://www.state.gov/countries-areas/georgia/"),
        (
            "UN Digital Library - Georgia",
            "https://digitallibrary.un.org/search?ln=en&p=georgia",
        ),
        ("World Bank - Georgia", "https://data.worldbank.org/country/georgia"),
        ("UNHCR - Georgia", "https://www.unhcr.org/countries/georgia"),
        ("HRW - Georgia", "https://www.hrw.org/europe/central-asia/georgia"),
        (
            "Amnesty - Georgia",
            "https://www.amnesty.org/en/location/europe-and-central-asia/eastern-europe-and-central-asia/georgia/",
        ),
        (
            "ICRC - Georgia",
            "https://www.icrc.org/en/where-we-work/europe-central-asia/georgia",
        ),
        ("OSCE - Georgia", "https://www.osce.org/countries/georgia"),
        ("NARA - Georgia", "https://catalog.archives.gov/search?q=georgia+soviet"),
    ],
    "US_IN_INDIA": [
        (
            "Library of Congress - India",
            "https://www.loc.gov/search/?q=india+united+states+relations",
        ),
        ("State Dept - India", "https://www.state.gov/countries-areas/india/"),
        ("FRUS - India", "https://history.state.gov/countries/india"),
        (
            "UN Digital Library - India",
            "https://digitallibrary.un.org/search?ln=en&p=india",
        ),
        ("World Bank - India", "https://data.worldbank.org/country/india"),
        ("UNHCR - India", "https://www.unhcr.org/countries/india"),
        ("HRW - India", "https://www.hrw.org/asia/india"),
        (
            "Amnesty - India",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-asia/india/",
        ),
        ("NARA - India", "https://catalog.archives.gov/search?q=india"),
        ("ICRC - India", "https://www.icrc.org/en/where-we-work/asia-pacific/india"),
    ],
    "US_JO_JORDAN": [
        (
            "Library of Congress - Jordan",
            "https://www.loc.gov/search/?q=jordan+united+states",
        ),
        ("State Dept - Jordan", "https://www.state.gov/countries-areas/jordan/"),
        (
            "UN Digital Library - Jordan",
            "https://digitallibrary.un.org/search?ln=en&p=jordan",
        ),
        ("World Bank - Jordan", "https://data.worldbank.org/country/jordan"),
        ("UNHCR - Jordan", "https://www.unhcr.org/countries/jordan"),
        ("HRW - Jordan", "https://www.hrw.org/middle-east/north-africa/jordan"),
        (
            "Amnesty - Jordan",
            "https://www.amnesty.org/en/location/middle-east-and-north-africa/middle-east/jordan/",
        ),
        ("ICRC - Jordan", "https://www.icrc.org/en/where-we-work/middle-east/jordan"),
        ("NARA - Jordan", "https://catalog.archives.gov/search?q=jordan"),
        ("UNRWA - Jordan", "https://www.unrwa.org/where-we-work/jordan"),
    ],
    "US_JP_JAPAN": [
        (
            "Library of Congress - Japan",
            "https://www.loc.gov/search/?q=japan+united+states+relations",
        ),
        ("State Dept - Japan", "https://www.state.gov/countries-areas/japan/"),
        ("FRUS - Japan", "https://history.state.gov/countries/japan"),
        (
            "UN Digital Library - Japan",
            "https://digitallibrary.un.org/search?ln=en&p=japan",
        ),
        ("World Bank - Japan", "https://data.worldbank.org/country/japan"),
        ("HRW - Japan", "https://www.hrw.org/asia/japan"),
        (
            "Amnesty - Japan",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/east-asia/japan/",
        ),
        ("NARA - Japan", "https://catalog.archives.gov/search?q=japan"),
        (
            "National Archives Japan - US relations",
            "https://www.archives.gov/research/military/ww2",
        ),
        ("ICRC - Japan", "https://www.icrc.org/en/where-we-work/asia-pacific/japan"),
    ],
    "US_KG_KYRGYZSTAN": [
        (
            "Library of Congress - Kyrgyzstan",
            "https://www.loc.gov/search/?q=kyrgyzstan+united+states",
        ),
        (
            "State Dept - Kyrgyzstan",
            "https://www.state.gov/countries-areas/kyrgyzstan/",
        ),
        (
            "UN Digital Library - Kyrgyzstan",
            "https://digitallibrary.un.org/search?ln=en&p=kyrgyzstan",
        ),
        (
            "World Bank - Kyrgyzstan",
            "https://data.worldbank.org/country/kyrgyz-republic",
        ),
        ("UNHCR - Kyrgyzstan", "https://www.unhcr.org/countries/kyrgyzstan"),
        ("HRW - Kyrgyzstan", "https://www.hrw.org/europe/central-asia/kyrgyzstan"),
        (
            "Amnesty - Kyrgyzstan",
            "https://www.amnesty.org/en/location/europe-and-central-asia/eastern-europe-and-central-asia/kyrgyzstan/",
        ),
        (
            "ICRC - Kyrgyzstan",
            "https://www.icrc.org/en/where-we-work/europe-central-asia/kyrgyzstan",
        ),
        ("OSCE - Kyrgyzstan", "https://www.osce.org/countries/kyrgyzstan"),
        ("NARA - Kyrgyzstan", "https://catalog.archives.gov/search?q=kyrgyzstan"),
    ],
    "US_KP_NORTH_KOREA": [
        (
            "Library of Congress - North Korea",
            "https://www.loc.gov/search/?q=north+korea+united+states",
        ),
        (
            "State Dept - North Korea",
            "https://www.state.gov/countries-areas/north-korea/",
        ),
        ("FRUS - Korea", "https://history.state.gov/countries/korea"),
        (
            "UN Digital Library - North Korea",
            "https://digitallibrary.un.org/search?ln=en&p=democratic+people%27s+republic+of+korea",
        ),
        ("HRW - North Korea", "https://www.hrw.org/asia/north-korea"),
        (
            "Amnesty - North Korea",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/east-asia/north-korea/",
        ),
        (
            "UN OHCHR - North Korea",
            "https://www.ohchr.org/en/countries/democratic-peoples-republic-korea",
        ),
        ("NARA - Korea War", "https://catalog.archives.gov/search?q=korean+war"),
        ("ICRC - Korea", "https://www.icrc.org/en/where-we-work/asia-pacific/korea"),
        (
            "UN Security Council - DPRK",
            "https://www.un.org/securitycouncil/sanctions/1718",
        ),
    ],
    "US_KW_KUWAIT": [
        (
            "Library of Congress - Kuwait",
            "https://www.loc.gov/search/?q=kuwait+united+states",
        ),
        ("State Dept - Kuwait", "https://www.state.gov/countries-areas/kuwait/"),
        (
            "UN Digital Library - Kuwait",
            "https://digitallibrary.un.org/search?ln=en&p=kuwait",
        ),
        ("World Bank - Kuwait", "https://data.worldbank.org/country/kuwait"),
        ("UNHCR - Kuwait", "https://www.unhcr.org/countries/kuwait"),
        ("HRW - Kuwait", "https://www.hrw.org/middle-east/north-africa/kuwait"),
        (
            "Amnesty - Kuwait",
            "https://www.amnesty.org/en/location/middle-east-and-north-africa/middle-east/kuwait/",
        ),
        ("ICRC - Kuwait", "https://www.icrc.org/en/where-we-work/middle-east/kuwait"),
        ("NARA - Kuwait", "https://catalog.archives.gov/search?q=kuwait"),
        ("Gulf War - AWM", "https://www.awm.gov.au/collection/CN500019"),
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
