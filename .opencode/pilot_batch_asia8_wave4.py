#!/usr/bin/env python3
"""ASIA 8-repo full-enrichment wave 4."""

from __future__ import annotations
import importlib.util
from pathlib import Path

BASE = Path(r"W:\Legal")
REGION = "ASIA"
REPOS = {
    "US_KZ_KAZAKHSTAN": [
        (
            "Library of Congress - Kazakhstan",
            "https://www.loc.gov/search/?q=kazakhstan+united+states",
        ),
        (
            "State Dept - Kazakhstan",
            "https://www.state.gov/countries-areas/kazakhstan/",
        ),
        (
            "UN Digital Library - Kazakhstan",
            "https://digitallibrary.un.org/search?ln=en&p=kazakhstan",
        ),
        ("World Bank - Kazakhstan", "https://data.worldbank.org/country/kazakhstan"),
        ("UNHCR - Kazakhstan", "https://www.unhcr.org/countries/kazakhstan"),
        ("HRW - Kazakhstan", "https://www.hrw.org/europe/central-asia/kazakhstan"),
        (
            "Amnesty - Kazakhstan",
            "https://www.amnesty.org/en/location/europe-and-central-asia/eastern-europe-and-central-asia/kazakhstan/",
        ),
        (
            "ICRC - Kazakhstan",
            "https://www.icrc.org/en/where-we-work/europe-central-asia/kazakhstan",
        ),
        ("OSCE - Kazakhstan", "https://www.osce.org/countries/kazakhstan"),
        ("NARA - Kazakhstan", "https://catalog.archives.gov/search?q=kazakhstan"),
    ],
    "US_LA_LAOS": [
        (
            "Library of Congress - Laos",
            "https://www.loc.gov/search/?q=laos+united+states",
        ),
        ("State Dept - Laos", "https://www.state.gov/countries-areas/laos/"),
        ("FRUS - Laos", "https://history.state.gov/countries/laos"),
        (
            "UN Digital Library - Laos",
            "https://digitallibrary.un.org/search?ln=en&p=lao+people",
        ),
        ("World Bank - Laos", "https://data.worldbank.org/country/lao-pdr"),
        ("UNHCR - Laos", "https://www.unhcr.org/countries/laos"),
        ("HRW - Laos", "https://www.hrw.org/asia/laos"),
        (
            "Amnesty - Laos",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-east-asia-and-the-pacific/laos/",
        ),
        ("NARA - Laos", "https://catalog.archives.gov/search?q=laos"),
        ("Legacies of War", "https://legaciesofwar.org/"),
    ],
    "US_LB_LEBANON": [
        (
            "Library of Congress - Lebanon",
            "https://www.loc.gov/search/?q=lebanon+united+states",
        ),
        ("State Dept - Lebanon", "https://www.state.gov/countries-areas/lebanon/"),
        (
            "UN Digital Library - Lebanon",
            "https://digitallibrary.un.org/search?ln=en&p=lebanon",
        ),
        ("World Bank - Lebanon", "https://data.worldbank.org/country/lebanon"),
        ("UNHCR - Lebanon", "https://www.unhcr.org/countries/lebanon"),
        ("HRW - Lebanon", "https://www.hrw.org/middle-east/north-africa/lebanon"),
        (
            "Amnesty - Lebanon",
            "https://www.amnesty.org/en/location/middle-east-and-north-africa/middle-east/lebanon/",
        ),
        ("ICRC - Lebanon", "https://www.icrc.org/en/where-we-work/middle-east/lebanon"),
        ("NARA - Lebanon", "https://catalog.archives.gov/search?q=lebanon"),
        ("UNRWA - Lebanon", "https://www.unrwa.org/where-we-work/lebanon"),
    ],
    "US_LK_SRI_LANKA": [
        (
            "Library of Congress - Sri Lanka",
            "https://www.loc.gov/search/?q=sri+lanka+united+states",
        ),
        ("State Dept - Sri Lanka", "https://www.state.gov/countries-areas/sri-lanka/"),
        (
            "UN Digital Library - Sri Lanka",
            "https://digitallibrary.un.org/search?ln=en&p=sri+lanka",
        ),
        ("World Bank - Sri Lanka", "https://data.worldbank.org/country/sri-lanka"),
        ("UNHCR - Sri Lanka", "https://www.unhcr.org/countries/sri-lanka"),
        ("HRW - Sri Lanka", "https://www.hrw.org/asia/sri-lanka"),
        (
            "Amnesty - Sri Lanka",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-asia/sri-lanka/",
        ),
        (
            "ICRC - Sri Lanka",
            "https://www.icrc.org/en/where-we-work/asia-pacific/sri-lanka",
        ),
        ("NARA - Sri Lanka", "https://catalog.archives.gov/search?q=sri+lanka"),
        ("UN OHCHR - Sri Lanka", "https://www.ohchr.org/en/countries/sri-lanka"),
    ],
    "US_MM_MYANMAR": [
        (
            "Library of Congress - Myanmar",
            "https://www.loc.gov/search/?q=myanmar+burma+united+states",
        ),
        ("State Dept - Burma", "https://www.state.gov/countries-areas/burma/"),
        (
            "UN Digital Library - Myanmar",
            "https://digitallibrary.un.org/search?ln=en&p=myanmar",
        ),
        ("World Bank - Myanmar", "https://data.worldbank.org/country/myanmar"),
        ("UNHCR - Myanmar", "https://www.unhcr.org/countries/myanmar"),
        ("HRW - Myanmar", "https://www.hrw.org/asia/myanmar"),
        (
            "Amnesty - Myanmar",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-east-asia-and-the-pacific/myanmar/",
        ),
        (
            "ICRC - Myanmar",
            "https://www.icrc.org/en/where-we-work/asia-pacific/myanmar",
        ),
        ("NARA - Myanmar", "https://catalog.archives.gov/search?q=burma+myanmar"),
        ("UN OHCHR - Myanmar", "https://www.ohchr.org/en/countries/myanmar"),
    ],
    "US_MN_MONGOLIA": [
        (
            "Library of Congress - Mongolia",
            "https://www.loc.gov/search/?q=mongolia+united+states",
        ),
        ("State Dept - Mongolia", "https://www.state.gov/countries-areas/mongolia/"),
        (
            "UN Digital Library - Mongolia",
            "https://digitallibrary.un.org/search?ln=en&p=mongolia",
        ),
        ("World Bank - Mongolia", "https://data.worldbank.org/country/mongolia"),
        ("UNHCR - Mongolia", "https://www.unhcr.org/countries/mongolia"),
        ("HRW - Mongolia", "https://www.hrw.org/asia/mongolia"),
        (
            "Amnesty - Mongolia",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/east-asia/mongolia/",
        ),
        (
            "ICRC - Mongolia",
            "https://www.icrc.org/en/where-we-work/asia-pacific/mongolia",
        ),
        ("NARA - Mongolia", "https://catalog.archives.gov/search?q=mongolia"),
        ("OSCE - Mongolia", "https://www.osce.org/countries/mongolia"),
    ],
    "US_MV_MALDIVES": [
        (
            "Library of Congress - Maldives",
            "https://www.loc.gov/search/?q=maldives+united+states",
        ),
        ("State Dept - Maldives", "https://www.state.gov/countries-areas/maldives/"),
        (
            "UN Digital Library - Maldives",
            "https://digitallibrary.un.org/search?ln=en&p=maldives",
        ),
        ("World Bank - Maldives", "https://data.worldbank.org/country/maldives"),
        ("UNHCR - Maldives", "https://www.unhcr.org/countries/maldives"),
        ("HRW - Maldives", "https://www.hrw.org/asia/maldives"),
        (
            "Amnesty - Maldives",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-asia/maldives/",
        ),
        (
            "ICRC - Maldives",
            "https://www.icrc.org/en/where-we-work/asia-pacific/maldives",
        ),
        ("NARA - Maldives", "https://catalog.archives.gov/search?q=maldives"),
        ("UN OHCHR - Maldives", "https://www.ohchr.org/en/countries/maldives"),
    ],
    "US_MY_MALAYSIA": [
        (
            "Library of Congress - Malaysia",
            "https://www.loc.gov/search/?q=malaysia+united+states",
        ),
        ("State Dept - Malaysia", "https://www.state.gov/countries-areas/malaysia/"),
        (
            "UN Digital Library - Malaysia",
            "https://digitallibrary.un.org/search?ln=en&p=malaysia",
        ),
        ("World Bank - Malaysia", "https://data.worldbank.org/country/malaysia"),
        ("UNHCR - Malaysia", "https://www.unhcr.org/countries/malaysia"),
        ("HRW - Malaysia", "https://www.hrw.org/asia/malaysia"),
        (
            "Amnesty - Malaysia",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-east-asia-and-the-pacific/malaysia/",
        ),
        (
            "ICRC - Malaysia",
            "https://www.icrc.org/en/where-we-work/asia-pacific/malaysia",
        ),
        ("NARA - Malaysia", "https://catalog.archives.gov/search?q=malaysia"),
        ("ASEAN - Malaysia", "https://asean.org/member-states/malaysia/"),
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
