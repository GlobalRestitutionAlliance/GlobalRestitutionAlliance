#!/usr/bin/env python3
"""LATAM 8-repo full-enrichment wave 3."""

from __future__ import annotations
import importlib.util
from pathlib import Path

BASE = Path(r"W:\Legal")
REGION = "LATIN_AMERICA"
REPOS = {
    "US_CO_COLOMBIA": [
        (
            "Library of Congress - Colombia",
            "https://www.loc.gov/search/?q=colombia+united+states",
        ),
        ("State Dept - Colombia", "https://www.state.gov/countries-areas/colombia/"),
        ("FRUS - Colombia", "https://history.state.gov/countries/colombia"),
        (
            "UN Digital Library - Colombia",
            "https://digitallibrary.un.org/search?ln=en&p=colombia",
        ),
        ("World Bank - Colombia", "https://data.worldbank.org/country/colombia"),
        ("UNHCR - Colombia", "https://www.unhcr.org/countries/colombia"),
        ("HRW - Colombia", "https://www.hrw.org/americas/colombia"),
        (
            "Amnesty - Colombia",
            "https://www.amnesty.org/en/location/americas/south-america/colombia/",
        ),
        ("NARA - Colombia", "https://catalog.archives.gov/search?q=colombia"),
        (
            "OAS - Colombia",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=COL",
        ),
    ],
    "US_CR_COSTA_RICA": [
        (
            "Library of Congress - Costa Rica",
            "https://www.loc.gov/search/?q=costa+rica+united+states",
        ),
        (
            "State Dept - Costa Rica",
            "https://www.state.gov/countries-areas/costa-rica/",
        ),
        (
            "UN Digital Library - Costa Rica",
            "https://digitallibrary.un.org/search?ln=en&p=costa+rica",
        ),
        ("World Bank - Costa Rica", "https://data.worldbank.org/country/costa-rica"),
        ("UNHCR - Costa Rica", "https://www.unhcr.org/countries/costa-rica"),
        ("HRW - Americas", "https://www.hrw.org/americas"),
        (
            "OAS - Costa Rica",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=COR",
        ),
        ("IACHR - Costa Rica", "https://www.oas.org/en/iachr/"),
        ("NARA - Costa Rica", "https://catalog.archives.gov/search?q=costa+rica"),
        ("ICRC - Americas", "https://www.icrc.org/en/where-we-work/americas"),
    ],
    "US_DM_DOMINICA": [
        (
            "Library of Congress - Dominica",
            "https://www.loc.gov/search/?q=dominica+united+states",
        ),
        ("State Dept - Dominica", "https://www.state.gov/countries-areas/dominica/"),
        (
            "UN Digital Library - Dominica",
            "https://digitallibrary.un.org/search?ln=en&p=dominica",
        ),
        ("World Bank - Dominica", "https://data.worldbank.org/country/dominica"),
        ("UNHCR - Dominica", "https://www.unhcr.org/countries/dominica"),
        ("HRW - Americas", "https://www.hrw.org/americas"),
        (
            "OAS - Dominica",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=DMI",
        ),
        ("CARICOM - Dominica", "https://caricom.org/country_profiles/dominica/"),
        ("NARA - Dominica", "https://catalog.archives.gov/search?q=dominica"),
        ("ICRC - Americas", "https://www.icrc.org/en/where-we-work/americas"),
    ],
    "US_DO_DOMINICAN_REPUBLIC": [
        (
            "Library of Congress - Dominican Republic",
            "https://www.loc.gov/search/?q=dominican+republic+united+states",
        ),
        (
            "State Dept - Dominican Republic",
            "https://www.state.gov/countries-areas/dominican-republic/",
        ),
        (
            "FRUS - Dominican Republic",
            "https://history.state.gov/countries/dominican-republic",
        ),
        (
            "UN Digital Library - Dominican Republic",
            "https://digitallibrary.un.org/search?ln=en&p=dominican+republic",
        ),
        (
            "World Bank - Dominican Republic",
            "https://data.worldbank.org/country/dominican-republic",
        ),
        (
            "UNHCR - Dominican Republic",
            "https://www.unhcr.org/countries/dominican-republic",
        ),
        ("HRW - Dominican Republic", "https://www.hrw.org/americas/dominican-republic"),
        (
            "Amnesty - Dominican Republic",
            "https://www.amnesty.org/en/location/americas/central-america-and-the-caribbean/dominican-republic/",
        ),
        (
            "NARA - Dominican Republic",
            "https://catalog.archives.gov/search?q=dominican+republic",
        ),
        (
            "OAS - Dominican Republic",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=DOR",
        ),
    ],
    "US_EC_ECUADOR": [
        (
            "Library of Congress - Ecuador",
            "https://www.loc.gov/search/?q=ecuador+united+states",
        ),
        ("State Dept - Ecuador", "https://www.state.gov/countries-areas/ecuador/"),
        ("FRUS - Ecuador", "https://history.state.gov/countries/ecuador"),
        (
            "UN Digital Library - Ecuador",
            "https://digitallibrary.un.org/search?ln=en&p=ecuador",
        ),
        ("World Bank - Ecuador", "https://data.worldbank.org/country/ecuador"),
        ("UNHCR - Ecuador", "https://www.unhcr.org/countries/ecuador"),
        ("HRW - Ecuador", "https://www.hrw.org/americas/ecuador"),
        (
            "Amnesty - Ecuador",
            "https://www.amnesty.org/en/location/americas/south-america/ecuador/",
        ),
        ("NARA - Ecuador", "https://catalog.archives.gov/search?q=ecuador"),
        (
            "OAS - Ecuador",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=ECU",
        ),
    ],
    "US_GD_GRENADA": [
        (
            "Library of Congress - Grenada",
            "https://www.loc.gov/search/?q=grenada+united+states",
        ),
        ("State Dept - Grenada", "https://www.state.gov/countries-areas/grenada/"),
        (
            "UN Digital Library - Grenada",
            "https://digitallibrary.un.org/search?ln=en&p=grenada",
        ),
        ("World Bank - Grenada", "https://data.worldbank.org/country/grenada"),
        ("UNHCR - Grenada", "https://www.unhcr.org/countries/grenada"),
        ("HRW - Americas", "https://www.hrw.org/americas"),
        (
            "OAS - Grenada",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=GRE",
        ),
        ("NARA - Grenada", "https://catalog.archives.gov/search?q=grenada+invasion"),
        (
            "National Security Archive - Grenada",
            "https://nsarchive2.gwu.edu/NSAEBB/NSAEBB323/index.htm",
        ),
        ("ICRC - Americas", "https://www.icrc.org/en/where-we-work/americas"),
    ],
    "US_GY_GUYANA": [
        (
            "Library of Congress - Guyana",
            "https://www.loc.gov/search/?q=guyana+united+states",
        ),
        ("State Dept - Guyana", "https://www.state.gov/countries-areas/guyana/"),
        (
            "UN Digital Library - Guyana",
            "https://digitallibrary.un.org/search?ln=en&p=guyana",
        ),
        ("World Bank - Guyana", "https://data.worldbank.org/country/guyana"),
        ("UNHCR - Guyana", "https://www.unhcr.org/countries/guyana"),
        ("HRW - Americas", "https://www.hrw.org/americas"),
        (
            "OAS - Guyana",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=GUY",
        ),
        ("CARICOM - Guyana", "https://caricom.org/country_profiles/guyana/"),
        ("NARA - Guyana", "https://catalog.archives.gov/search?q=guyana"),
        ("ICRC - Americas", "https://www.icrc.org/en/where-we-work/americas"),
    ],
    "US_JM_JAMAICA": [
        (
            "Library of Congress - Jamaica",
            "https://www.loc.gov/search/?q=jamaica+united+states",
        ),
        ("State Dept - Jamaica", "https://www.state.gov/countries-areas/jamaica/"),
        (
            "UN Digital Library - Jamaica",
            "https://digitallibrary.un.org/search?ln=en&p=jamaica",
        ),
        ("World Bank - Jamaica", "https://data.worldbank.org/country/jamaica"),
        ("UNHCR - Jamaica", "https://www.unhcr.org/countries/jamaica"),
        ("HRW - Jamaica", "https://www.hrw.org/americas/jamaica"),
        (
            "Amnesty - Jamaica",
            "https://www.amnesty.org/en/location/americas/central-america-and-the-caribbean/jamaica/",
        ),
        (
            "OAS - Jamaica",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=JAM",
        ),
        ("NARA - Jamaica", "https://catalog.archives.gov/search?q=jamaica"),
        ("CARICOM - Jamaica", "https://caricom.org/country_profiles/jamaica/"),
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
