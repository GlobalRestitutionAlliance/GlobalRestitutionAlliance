#!/usr/bin/env python3
"""ASIA 8-repo full-enrichment wave 2."""

from __future__ import annotations
import importlib.util
from pathlib import Path

BASE = Path(r"W:\Legal")
REGION = "ASIA"
REPOS = {
    "US_AE_UNITED_ARAB_EMIRATES": [
        (
            "Library of Congress - UAE",
            "https://www.loc.gov/search/?q=united+arab+emirates+united+states",
        ),
        (
            "State Dept - UAE",
            "https://www.state.gov/countries-areas/united-arab-emirates/",
        ),
        (
            "UN Digital Library - UAE",
            "https://digitallibrary.un.org/search?ln=en&p=united+arab+emirates",
        ),
        ("World Bank - UAE", "https://data.worldbank.org/country/united-arab-emirates"),
        ("UNHCR - UAE", "https://www.unhcr.org/countries/united-arab-emirates"),
        (
            "HRW - UAE",
            "https://www.hrw.org/middle-east/north-africa/united-arab-emirates",
        ),
        (
            "Amnesty - UAE",
            "https://www.amnesty.org/en/location/middle-east-and-north-africa/middle-east/united-arab-emirates/",
        ),
        (
            "ICRC - UAE",
            "https://www.icrc.org/en/where-we-work/middle-east/united-arab-emirates",
        ),
        ("UN Treaty Collection", "https://treaties.un.org/"),
        (
            "NARA - UAE",
            "https://catalog.archives.gov/search?q=united%20arab%20emirates",
        ),
    ],
    "US_AM_ARMENIA": [
        (
            "Library of Congress - Armenia",
            "https://www.loc.gov/search/?q=armenia+united+states",
        ),
        ("State Dept - Armenia", "https://www.state.gov/countries-areas/armenia/"),
        (
            "UN Digital Library - Armenia",
            "https://digitallibrary.un.org/search?ln=en&p=armenia",
        ),
        ("World Bank - Armenia", "https://data.worldbank.org/country/armenia"),
        ("UNHCR - Armenia", "https://www.unhcr.org/countries/armenia"),
        ("HRW - Armenia", "https://www.hrw.org/europe/central-asia/armenia"),
        (
            "Amnesty - Armenia",
            "https://www.amnesty.org/en/location/europe-and-central-asia/eastern-europe-and-central-asia/armenia/",
        ),
        (
            "ICRC - Armenia",
            "https://www.icrc.org/en/where-we-work/europe-central-asia/armenia",
        ),
        ("OSCE - Armenia", "https://www.osce.org/countries/armenia"),
        ("NARA - Armenia", "https://catalog.archives.gov/search?q=armenia"),
    ],
    "US_AZ_AZERBAIJAN": [
        (
            "Library of Congress - Azerbaijan",
            "https://www.loc.gov/search/?q=azerbaijan+united+states",
        ),
        (
            "State Dept - Azerbaijan",
            "https://www.state.gov/countries-areas/azerbaijan/",
        ),
        (
            "UN Digital Library - Azerbaijan",
            "https://digitallibrary.un.org/search?ln=en&p=azerbaijan",
        ),
        ("World Bank - Azerbaijan", "https://data.worldbank.org/country/azerbaijan"),
        ("UNHCR - Azerbaijan", "https://www.unhcr.org/countries/azerbaijan"),
        ("HRW - Azerbaijan", "https://www.hrw.org/europe/central-asia/azerbaijan"),
        (
            "Amnesty - Azerbaijan",
            "https://www.amnesty.org/en/location/europe-and-central-asia/eastern-europe-and-central-asia/azerbaijan/",
        ),
        (
            "ICRC - Azerbaijan",
            "https://www.icrc.org/en/where-we-work/europe-central-asia/azerbaijan",
        ),
        ("OSCE - Azerbaijan", "https://www.osce.org/countries/azerbaijan"),
        ("NARA - Azerbaijan", "https://catalog.archives.gov/search?q=azerbaijan"),
    ],
    "US_BD_BANGLADESH": [
        (
            "Library of Congress - Bangladesh",
            "https://www.loc.gov/search/?q=bangladesh+united+states",
        ),
        (
            "State Dept - Bangladesh",
            "https://www.state.gov/countries-areas/bangladesh/",
        ),
        (
            "UN Digital Library - Bangladesh",
            "https://digitallibrary.un.org/search?ln=en&p=bangladesh",
        ),
        ("World Bank - Bangladesh", "https://data.worldbank.org/country/bangladesh"),
        ("UNHCR - Bangladesh", "https://www.unhcr.org/countries/bangladesh"),
        ("HRW - Bangladesh", "https://www.hrw.org/asia/bangladesh"),
        (
            "Amnesty - Bangladesh",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-asia/bangladesh/",
        ),
        (
            "ICRC - Bangladesh",
            "https://www.icrc.org/en/where-we-work/asia-pacific/bangladesh",
        ),
        ("NARA - Bangladesh", "https://catalog.archives.gov/search?q=bangladesh"),
        ("UN OHCHR - Bangladesh", "https://www.ohchr.org/en/countries/bangladesh"),
    ],
    "US_BH_BAHRAIN": [
        (
            "Library of Congress - Bahrain",
            "https://www.loc.gov/search/?q=bahrain+united+states",
        ),
        ("State Dept - Bahrain", "https://www.state.gov/countries-areas/bahrain/"),
        (
            "UN Digital Library - Bahrain",
            "https://digitallibrary.un.org/search?ln=en&p=bahrain",
        ),
        ("World Bank - Bahrain", "https://data.worldbank.org/country/bahrain"),
        ("UNHCR - Bahrain", "https://www.unhcr.org/countries/bahrain"),
        ("HRW - Bahrain", "https://www.hrw.org/middle-east/north-africa/bahrain"),
        (
            "Amnesty - Bahrain",
            "https://www.amnesty.org/en/location/middle-east-and-north-africa/middle-east/bahrain/",
        ),
        ("ICRC - Bahrain", "https://www.icrc.org/en/where-we-work/middle-east/bahrain"),
        ("NARA - Bahrain", "https://catalog.archives.gov/search?q=bahrain"),
        ("US Navy 5th Fleet - Bahrain", "https://www.cusnc.navy.mil/"),
    ],
    "US_BN_BRUNEI": [
        (
            "Library of Congress - Brunei",
            "https://www.loc.gov/search/?q=brunei+united+states",
        ),
        (
            "State Dept - Brunei",
            "https://www.state.gov/countries-areas/brunei-darussalam/",
        ),
        (
            "UN Digital Library - Brunei",
            "https://digitallibrary.un.org/search?ln=en&p=brunei",
        ),
        ("World Bank - Brunei", "https://data.worldbank.org/country/brunei-darussalam"),
        ("UNHCR - Brunei", "https://www.unhcr.org/countries/brunei-darussalam"),
        ("HRW - Brunei", "https://www.hrw.org/asia/brunei"),
        (
            "Amnesty - Brunei",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-east-asia-and-the-pacific/brunei-darussalam/",
        ),
        ("ICRC - Brunei", "https://www.icrc.org/en/where-we-work/asia-pacific/brunei"),
        ("NARA - Brunei", "https://catalog.archives.gov/search?q=brunei"),
        ("ASEAN - Brunei", "https://asean.org/member-states/brunei-darussalam/"),
    ],
    "US_BT_BHUTAN": [
        (
            "Library of Congress - Bhutan",
            "https://www.loc.gov/search/?q=bhutan+united+states",
        ),
        ("State Dept - Bhutan", "https://www.state.gov/countries-areas/bhutan/"),
        (
            "UN Digital Library - Bhutan",
            "https://digitallibrary.un.org/search?ln=en&p=bhutan",
        ),
        ("World Bank - Bhutan", "https://data.worldbank.org/country/bhutan"),
        ("UNHCR - Bhutan", "https://www.unhcr.org/countries/bhutan"),
        ("HRW - Bhutan", "https://www.hrw.org/asia/bhutan"),
        (
            "Amnesty - Bhutan",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/south-asia/bhutan/",
        ),
        ("ICRC - Bhutan", "https://www.icrc.org/en/where-we-work/asia-pacific/bhutan"),
        ("NARA - Bhutan", "https://catalog.archives.gov/search?q=bhutan"),
        ("UN OHCHR - Bhutan", "https://www.ohchr.org/en/countries/bhutan"),
    ],
    "US_CN_CHINA": [
        (
            "Library of Congress - China",
            "https://www.loc.gov/search/?q=china+united+states+relations",
        ),
        ("State Dept - China", "https://www.state.gov/countries-areas/china/"),
        ("State Dept FRUS - China", "https://history.state.gov/countries/china"),
        (
            "UN Digital Library - China",
            "https://digitallibrary.un.org/search?ln=en&p=china",
        ),
        ("World Bank - China", "https://data.worldbank.org/country/china"),
        ("UNHCR - China", "https://www.unhcr.org/countries/china"),
        ("HRW - China", "https://www.hrw.org/asia/china-and-tibet"),
        (
            "Amnesty - China",
            "https://www.amnesty.org/en/location/asia-and-the-pacific/east-asia/china/",
        ),
        ("NARA - China", "https://catalog.archives.gov/search?q=china"),
        ("ICRC - China", "https://www.icrc.org/en/where-we-work/asia-pacific/china"),
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
