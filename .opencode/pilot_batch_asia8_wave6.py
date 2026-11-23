#!/usr/bin/env python3
"""ASIA 8-repo full-enrichment wave 6."""

from __future__ import annotations
import importlib.util
from pathlib import Path

BASE = Path(r"W:\Legal")
REGION = "ASIA"
REPOS = {
    "US_TH_THAILAND": [
        (
            "Library of Congress - Thailand",
            "https://www.loc.gov/search/?q=thailand+united+states",
        ),
        ("State Dept - Thailand", "https://www.state.gov/countries-areas/thailand/"),
        (
            "UN Digital Library - Thailand",
            "https://digitallibrary.un.org/search?ln=en&p=thailand",
        ),
        ("World Bank - Thailand", "https://data.worldbank.org/country/thailand"),
        ("UNHCR - Thailand", "https://www.unhcr.org/countries/thailand"),
        ("HRW - Thailand", "https://www.hrw.org/asia/thailand"),
        (
            "Amnesty - Thailand",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-east-asia-and-the-pacific/thailand/",
        ),
        (
            "ICRC - Thailand",
            "https://www.icrc.org/en/where-we-work/asia-pacific/thailand",
        ),
        ("NARA - Thailand", "https://catalog.archives.gov/search?q=thailand"),
        ("ASEAN - Thailand", "https://asean.org/member-states/thailand/"),
    ],
    "US_TJ_TAJIKISTAN": [
        (
            "Library of Congress - Tajikistan",
            "https://www.loc.gov/search/?q=tajikistan+united+states",
        ),
        (
            "State Dept - Tajikistan",
            "https://www.state.gov/countries-areas/tajikistan/",
        ),
        (
            "UN Digital Library - Tajikistan",
            "https://digitallibrary.un.org/search?ln=en&p=tajikistan",
        ),
        ("World Bank - Tajikistan", "https://data.worldbank.org/country/tajikistan"),
        ("UNHCR - Tajikistan", "https://www.unhcr.org/countries/tajikistan"),
        ("HRW - Tajikistan", "https://www.hrw.org/europe/central-asia/tajikistan"),
        (
            "Amnesty - Tajikistan",
            "https://www.amnesty.org/en/location/europe-and-central-asia/eastern-europe-and-central-asia/tajikistan/",
        ),
        (
            "ICRC - Tajikistan",
            "https://www.icrc.org/en/where-we-work/europe-central-asia/tajikistan",
        ),
        ("OSCE - Tajikistan", "https://www.osce.org/countries/tajikistan"),
        ("NARA - Tajikistan", "https://catalog.archives.gov/search?q=tajikistan"),
    ],
    "US_TL_TIMOR_LESTE": [
        (
            "Library of Congress - Timor-Leste",
            "https://www.loc.gov/search/?q=timor+leste+united+states",
        ),
        (
            "State Dept - Timor-Leste",
            "https://www.state.gov/countries-areas/timor-leste/",
        ),
        (
            "UN Digital Library - Timor-Leste",
            "https://digitallibrary.un.org/search?ln=en&p=timor-leste",
        ),
        ("World Bank - Timor-Leste", "https://data.worldbank.org/country/timor-leste"),
        ("UNHCR - Timor-Leste", "https://www.unhcr.org/countries/timor-leste"),
        ("HRW - Timor-Leste", "https://www.hrw.org/asia/timor-leste"),
        (
            "Amnesty - Timor-Leste",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-east-asia-and-the-pacific/timor-leste/",
        ),
        (
            "ICRC - Timor-Leste",
            "https://www.icrc.org/en/where-we-work/asia-pacific/timor-leste",
        ),
        ("NARA - Timor-Leste", "https://catalog.archives.gov/search?q=east+timor"),
        ("UN OHCHR - Timor-Leste", "https://www.ohchr.org/en/countries/timor-leste"),
    ],
    "US_TM_TURKMENISTAN": [
        (
            "Library of Congress - Turkmenistan",
            "https://www.loc.gov/search/?q=turkmenistan+united+states",
        ),
        (
            "State Dept - Turkmenistan",
            "https://www.state.gov/countries-areas/turkmenistan/",
        ),
        (
            "UN Digital Library - Turkmenistan",
            "https://digitallibrary.un.org/search?ln=en&p=turkmenistan",
        ),
        (
            "World Bank - Turkmenistan",
            "https://data.worldbank.org/country/turkmenistan",
        ),
        ("UNHCR - Turkmenistan", "https://www.unhcr.org/countries/turkmenistan"),
        ("HRW - Turkmenistan", "https://www.hrw.org/europe/central-asia/turkmenistan"),
        (
            "Amnesty - Turkmenistan",
            "https://www.amnesty.org/en/location/europe-and-central-asia/eastern-europe-and-central-asia/turkmenistan/",
        ),
        (
            "ICRC - Turkmenistan",
            "https://www.icrc.org/en/where-we-work/europe-central-asia/turkmenistan",
        ),
        ("OSCE - Turkmenistan", "https://www.osce.org/countries/turkmenistan"),
        ("NARA - Turkmenistan", "https://catalog.archives.gov/search?q=turkmenistan"),
    ],
    "US_TR_TURKEY": [
        (
            "Library of Congress - Turkey",
            "https://www.loc.gov/search/?q=turkey+united+states+relations",
        ),
        ("State Dept - Turkey", "https://www.state.gov/countries-areas/turkiye/"),
        ("FRUS - Turkey", "https://history.state.gov/countries/turkey"),
        (
            "UN Digital Library - Turkey",
            "https://digitallibrary.un.org/search?ln=en&p=turkey",
        ),
        ("World Bank - Turkey", "https://data.worldbank.org/country/turkiye"),
        ("UNHCR - Turkey", "https://www.unhcr.org/countries/turkiye"),
        ("HRW - Turkey", "https://www.hrw.org/europe/central-asia/turkey"),
        (
            "Amnesty - Turkey",
            "https://www.amnesty.org/en/location/europe-and-central-asia/turkiye/",
        ),
        (
            "ICRC - Turkey",
            "https://www.icrc.org/en/where-we-work/europe-central-asia/turkey",
        ),
        ("NARA - Turkey", "https://catalog.archives.gov/search?q=turkey"),
    ],
    "US_TW_TAIWAN": [
        (
            "Library of Congress - Taiwan",
            "https://www.loc.gov/search/?q=taiwan+united+states",
        ),
        ("State Dept - Taiwan", "https://www.state.gov/countries-areas/taiwan/"),
        ("AIT - Taiwan", "https://www.ait.org.tw/"),
        (
            "UN Digital Library - Taiwan",
            "https://digitallibrary.un.org/search?ln=en&p=taiwan",
        ),
        ("World Bank - Taiwan", "https://data.worldbank.org/country/taiwan-china"),
        ("HRW - Taiwan", "https://www.hrw.org/asia/taiwan"),
        (
            "Amnesty - Taiwan",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/east-asia/taiwan/",
        ),
        ("NARA - Taiwan", "https://catalog.archives.gov/search?q=taiwan"),
        ("FRUS - China/Taiwan", "https://history.state.gov/countries/china"),
        ("ICRC - Taiwan", "https://www.icrc.org/en/where-we-work/asia-pacific/taiwan"),
    ],
    "US_UZ_UZBEKISTAN": [
        (
            "Library of Congress - Uzbekistan",
            "https://www.loc.gov/search/?q=uzbekistan+united+states",
        ),
        (
            "State Dept - Uzbekistan",
            "https://www.state.gov/countries-areas/uzbekistan/",
        ),
        (
            "UN Digital Library - Uzbekistan",
            "https://digitallibrary.un.org/search?ln=en&p=uzbekistan",
        ),
        ("World Bank - Uzbekistan", "https://data.worldbank.org/country/uzbekistan"),
        ("UNHCR - Uzbekistan", "https://www.unhcr.org/countries/uzbekistan"),
        ("HRW - Uzbekistan", "https://www.hrw.org/europe/central-asia/uzbekistan"),
        (
            "Amnesty - Uzbekistan",
            "https://www.amnesty.org/en/location/europe-and-central-asia/eastern-europe-and-central-asia/uzbekistan/",
        ),
        (
            "ICRC - Uzbekistan",
            "https://www.icrc.org/en/where-we-work/europe-central-asia/uzbekistan",
        ),
        ("OSCE - Uzbekistan", "https://www.osce.org/countries/uzbekistan"),
        ("NARA - Uzbekistan", "https://catalog.archives.gov/search?q=uzbekistan"),
    ],
    "US_YE_YEMEN": [
        (
            "Library of Congress - Yemen",
            "https://www.loc.gov/search/?q=yemen+united+states",
        ),
        ("State Dept - Yemen", "https://www.state.gov/countries-areas/yemen/"),
        (
            "UN Digital Library - Yemen",
            "https://digitallibrary.un.org/search?ln=en&p=yemen",
        ),
        ("World Bank - Yemen", "https://data.worldbank.org/country/yemen-rep"),
        ("UNHCR - Yemen", "https://www.unhcr.org/countries/yemen"),
        ("HRW - Yemen", "https://www.hrw.org/middle-east/north-africa/yemen"),
        (
            "Amnesty - Yemen",
            "https://www.amnesty.org/en/location/middle-east-and-north-africa/middle-east/yemen/",
        ),
        ("ICRC - Yemen", "https://www.icrc.org/en/where-we-work/middle-east/yemen"),
        ("NARA - Yemen", "https://catalog.archives.gov/search?q=yemen"),
        ("UN OHCHR - Yemen", "https://www.ohchr.org/en/countries/yemen"),
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
