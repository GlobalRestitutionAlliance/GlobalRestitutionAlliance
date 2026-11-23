#!/usr/bin/env python3
"""LATAM 8-repo full-enrichment wave 4."""

from __future__ import annotations
import importlib.util
from pathlib import Path

BASE = Path(r"W:\Legal")
REGION = "LATIN_AMERICA"
REPOS = {
    "US_KN_SAINT_KITTS_AND_NEVIS": [
        (
            "Library of Congress - Saint Kitts and Nevis",
            "https://www.loc.gov/search/?q=saint+kitts+nevis+united+states",
        ),
        (
            "State Dept - Saint Kitts and Nevis",
            "https://www.state.gov/countries-areas/saint-kitts-and-nevis/",
        ),
        (
            "UN Digital Library - Saint Kitts and Nevis",
            "https://digitallibrary.un.org/search?ln=en&p=saint+kitts+and+nevis",
        ),
        (
            "World Bank - St. Kitts and Nevis",
            "https://data.worldbank.org/country/st-kitts-and-nevis",
        ),
        (
            "OAS - Saint Kitts and Nevis",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=STK",
        ),
        (
            "CARICOM - Saint Kitts and Nevis",
            "https://caricom.org/country_profiles/st-kitts-and-nevis/",
        ),
        (
            "NARA - Saint Kitts and Nevis",
            "https://catalog.archives.gov/search?q=saint+kitts",
        ),
        ("HRW - Americas", "https://www.hrw.org/americas"),
        ("ICRC - Americas", "https://www.icrc.org/en/where-we-work/americas"),
        ("UNHCR - Americas", "https://www.unhcr.org/americas"),
    ],
    "US_LC_SAINT_LUCIA": [
        (
            "Library of Congress - Saint Lucia",
            "https://www.loc.gov/search/?q=saint+lucia+united+states",
        ),
        (
            "State Dept - Saint Lucia",
            "https://www.state.gov/countries-areas/saint-lucia/",
        ),
        (
            "UN Digital Library - Saint Lucia",
            "https://digitallibrary.un.org/search?ln=en&p=saint+lucia",
        ),
        ("World Bank - St. Lucia", "https://data.worldbank.org/country/st-lucia"),
        (
            "OAS - Saint Lucia",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=STL",
        ),
        ("CARICOM - Saint Lucia", "https://caricom.org/country_profiles/saint-lucia/"),
        ("NARA - Saint Lucia", "https://catalog.archives.gov/search?q=saint+lucia"),
        ("HRW - Americas", "https://www.hrw.org/americas"),
        ("ICRC - Americas", "https://www.icrc.org/en/where-we-work/americas"),
        ("UNHCR - Americas", "https://www.unhcr.org/americas"),
    ],
    "US_PE_PERU": [
        (
            "Library of Congress - Peru",
            "https://www.loc.gov/search/?q=peru+united+states",
        ),
        ("State Dept - Peru", "https://www.state.gov/countries-areas/peru/"),
        ("FRUS - Peru", "https://history.state.gov/countries/peru"),
        (
            "UN Digital Library - Peru",
            "https://digitallibrary.un.org/search?ln=en&p=peru",
        ),
        ("World Bank - Peru", "https://data.worldbank.org/country/peru"),
        ("UNHCR - Peru", "https://www.unhcr.org/countries/peru"),
        ("HRW - Peru", "https://www.hrw.org/americas/peru"),
        (
            "Amnesty - Peru",
            "https://www.amnesty.org/en/location/americas/south-america/peru/",
        ),
        ("NARA - Peru", "https://catalog.archives.gov/search?q=peru"),
        (
            "OAS - Peru",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=PER",
        ),
    ],
    "US_PY_PARAGUAY": [
        (
            "Library of Congress - Paraguay",
            "https://www.loc.gov/search/?q=paraguay+united+states",
        ),
        ("State Dept - Paraguay", "https://www.state.gov/countries-areas/paraguay/"),
        ("FRUS - Paraguay", "https://history.state.gov/countries/paraguay"),
        (
            "UN Digital Library - Paraguay",
            "https://digitallibrary.un.org/search?ln=en&p=paraguay",
        ),
        ("World Bank - Paraguay", "https://data.worldbank.org/country/paraguay"),
        ("UNHCR - Paraguay", "https://www.unhcr.org/countries/paraguay"),
        ("HRW - Paraguay", "https://www.hrw.org/americas/paraguay"),
        (
            "Amnesty - Paraguay",
            "https://www.amnesty.org/en/location/americas/south-america/paraguay/",
        ),
        ("NARA - Paraguay", "https://catalog.archives.gov/search?q=paraguay"),
        (
            "OAS - Paraguay",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=PAR",
        ),
    ],
    "US_SR_SURINAME": [
        (
            "Library of Congress - Suriname",
            "https://www.loc.gov/search/?q=suriname+united+states",
        ),
        ("State Dept - Suriname", "https://www.state.gov/countries-areas/suriname/"),
        (
            "UN Digital Library - Suriname",
            "https://digitallibrary.un.org/search?ln=en&p=suriname",
        ),
        ("World Bank - Suriname", "https://data.worldbank.org/country/suriname"),
        ("UNHCR - Suriname", "https://www.unhcr.org/countries/suriname"),
        ("HRW - Americas", "https://www.hrw.org/americas"),
        (
            "OAS - Suriname",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=SUR",
        ),
        ("CARICOM - Suriname", "https://caricom.org/country_profiles/suriname/"),
        ("NARA - Suriname", "https://catalog.archives.gov/search?q=suriname"),
        ("ICRC - Americas", "https://www.icrc.org/en/where-we-work/americas"),
    ],
    "US_TT_TRINIDAD_AND_TOBAGO": [
        (
            "Library of Congress - Trinidad and Tobago",
            "https://www.loc.gov/search/?q=trinidad+tobago+united+states",
        ),
        (
            "State Dept - Trinidad and Tobago",
            "https://www.state.gov/countries-areas/trinidad-and-tobago/",
        ),
        (
            "UN Digital Library - Trinidad and Tobago",
            "https://digitallibrary.un.org/search?ln=en&p=trinidad+and+tobago",
        ),
        (
            "World Bank - Trinidad and Tobago",
            "https://data.worldbank.org/country/trinidad-and-tobago",
        ),
        (
            "UNHCR - Trinidad and Tobago",
            "https://www.unhcr.org/countries/trinidad-and-tobago",
        ),
        ("HRW - Americas", "https://www.hrw.org/americas"),
        (
            "OAS - Trinidad and Tobago",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=TRI",
        ),
        (
            "CARICOM - Trinidad and Tobago",
            "https://caricom.org/country_profiles/trinidad-and-tobago/",
        ),
        (
            "NARA - Trinidad and Tobago",
            "https://catalog.archives.gov/search?q=trinidad+tobago",
        ),
        ("ICRC - Americas", "https://www.icrc.org/en/where-we-work/americas"),
    ],
    "US_UY_URUGUAY": [
        (
            "Library of Congress - Uruguay",
            "https://www.loc.gov/search/?q=uruguay+united+states",
        ),
        ("State Dept - Uruguay", "https://www.state.gov/countries-areas/uruguay/"),
        ("FRUS - Uruguay", "https://history.state.gov/countries/uruguay"),
        (
            "UN Digital Library - Uruguay",
            "https://digitallibrary.un.org/search?ln=en&p=uruguay",
        ),
        ("World Bank - Uruguay", "https://data.worldbank.org/country/uruguay"),
        ("UNHCR - Uruguay", "https://www.unhcr.org/countries/uruguay"),
        ("HRW - Uruguay", "https://www.hrw.org/americas/uruguay"),
        (
            "Amnesty - Uruguay",
            "https://www.amnesty.org/en/location/americas/south-america/uruguay/",
        ),
        ("NARA - Uruguay", "https://catalog.archives.gov/search?q=uruguay"),
        (
            "OAS - Uruguay",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=URU",
        ),
    ],
    "US_VC_SAINT_VINCENT_AND_THE_GRENADINES": [
        (
            "Library of Congress - Saint Vincent",
            "https://www.loc.gov/search/?q=saint+vincent+grenadines+united+states",
        ),
        (
            "State Dept - Saint Vincent and the Grenadines",
            "https://www.state.gov/countries-areas/saint-vincent-and-the-grenadines/",
        ),
        (
            "UN Digital Library - Saint Vincent",
            "https://digitallibrary.un.org/search?ln=en&p=saint+vincent+and+the+grenadines",
        ),
        (
            "World Bank - St. Vincent and the Grenadines",
            "https://data.worldbank.org/country/st-vincent-and-the-grenadines",
        ),
        (
            "OAS - Saint Vincent and the Grenadines",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=STV",
        ),
        (
            "CARICOM - Saint Vincent",
            "https://caricom.org/country_profiles/st-vincent-and-the-grenadines/",
        ),
        (
            "NARA - Saint Vincent",
            "https://catalog.archives.gov/search?q=saint+vincent+grenadines",
        ),
        ("HRW - Americas", "https://www.hrw.org/americas"),
        ("ICRC - Americas", "https://www.icrc.org/en/where-we-work/americas"),
        ("UNHCR - Americas", "https://www.unhcr.org/americas"),
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
