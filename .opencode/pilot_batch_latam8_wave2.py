#!/usr/bin/env python3
"""LATAM 8-repo full-enrichment wave 2."""

from __future__ import annotations
import importlib.util
from pathlib import Path

BASE = Path(r"W:\Legal")
REGION = "LATIN_AMERICA"
REPOS = {
    "US_AG_ANTIGUA_AND_BARBUDA": [
        (
            "Library of Congress - Antigua and Barbuda",
            "https://www.loc.gov/search/?q=antigua+barbuda+united+states",
        ),
        (
            "State Dept - Antigua and Barbuda",
            "https://www.state.gov/countries-areas/antigua-and-barbuda/",
        ),
        (
            "UN Digital Library - Antigua and Barbuda",
            "https://digitallibrary.un.org/search?ln=en&p=antigua+and+barbuda",
        ),
        (
            "World Bank - Antigua and Barbuda",
            "https://data.worldbank.org/country/antigua-and-barbuda",
        ),
        (
            "UNHCR - Antigua and Barbuda",
            "https://www.unhcr.org/countries/antigua-and-barbuda",
        ),
        ("HRW - Americas", "https://www.hrw.org/americas"),
        (
            "OAS - Antigua and Barbuda",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=ANT",
        ),
        (
            "CARICOM - Antigua and Barbuda",
            "https://caricom.org/country_profiles/antigua-and-barbuda/",
        ),
        (
            "NARA - Antigua and Barbuda",
            "https://catalog.archives.gov/search?q=antigua+barbuda",
        ),
        ("ICRC - Americas", "https://www.icrc.org/en/where-we-work/americas"),
    ],
    "US_AR_ARGENTINA": [
        (
            "Library of Congress - Argentina",
            "https://www.loc.gov/search/?q=argentina+united+states",
        ),
        ("State Dept - Argentina", "https://www.state.gov/countries-areas/argentina/"),
        ("FRUS - Argentina", "https://history.state.gov/countries/argentina"),
        (
            "UN Digital Library - Argentina",
            "https://digitallibrary.un.org/search?ln=en&p=argentina",
        ),
        ("World Bank - Argentina", "https://data.worldbank.org/country/argentina"),
        ("UNHCR - Argentina", "https://www.unhcr.org/countries/argentina"),
        ("HRW - Argentina", "https://www.hrw.org/americas/argentina"),
        (
            "Amnesty - Argentina",
            "https://www.amnesty.org/en/location/americas/south-america/argentina/",
        ),
        ("NARA - Argentina", "https://catalog.archives.gov/search?q=argentina"),
        (
            "OAS - Argentina",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=ARG",
        ),
    ],
    "US_BB_BARBADOS": [
        (
            "Library of Congress - Barbados",
            "https://www.loc.gov/search/?q=barbados+united+states",
        ),
        ("State Dept - Barbados", "https://www.state.gov/countries-areas/barbados/"),
        (
            "UN Digital Library - Barbados",
            "https://digitallibrary.un.org/search?ln=en&p=barbados",
        ),
        ("World Bank - Barbados", "https://data.worldbank.org/country/barbados"),
        ("UNHCR - Barbados", "https://www.unhcr.org/countries/barbados"),
        ("HRW - Americas", "https://www.hrw.org/americas"),
        (
            "OAS - Barbados",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=BAR",
        ),
        ("CARICOM - Barbados", "https://caricom.org/country_profiles/barbados/"),
        ("NARA - Barbados", "https://catalog.archives.gov/search?q=barbados"),
        ("ICRC - Americas", "https://www.icrc.org/en/where-we-work/americas"),
    ],
    "US_BO_BOLIVIA": [
        (
            "Library of Congress - Bolivia",
            "https://www.loc.gov/search/?q=bolivia+united+states",
        ),
        ("State Dept - Bolivia", "https://www.state.gov/countries-areas/bolivia/"),
        ("FRUS - Bolivia", "https://history.state.gov/countries/bolivia"),
        (
            "UN Digital Library - Bolivia",
            "https://digitallibrary.un.org/search?ln=en&p=bolivia",
        ),
        ("World Bank - Bolivia", "https://data.worldbank.org/country/bolivia"),
        ("UNHCR - Bolivia", "https://www.unhcr.org/countries/bolivia"),
        ("HRW - Bolivia", "https://www.hrw.org/americas/bolivia"),
        (
            "Amnesty - Bolivia",
            "https://www.amnesty.org/en/location/americas/south-america/bolivia/",
        ),
        ("NARA - Bolivia", "https://catalog.archives.gov/search?q=bolivia"),
        (
            "OAS - Bolivia",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=BOL",
        ),
    ],
    "US_BR_BRAZIL": [
        (
            "Library of Congress - Brazil",
            "https://www.loc.gov/search/?q=brazil+united+states",
        ),
        ("State Dept - Brazil", "https://www.state.gov/countries-areas/brazil/"),
        ("FRUS - Brazil", "https://history.state.gov/countries/brazil"),
        (
            "UN Digital Library - Brazil",
            "https://digitallibrary.un.org/search?ln=en&p=brazil",
        ),
        ("World Bank - Brazil", "https://data.worldbank.org/country/brazil"),
        ("UNHCR - Brazil", "https://www.unhcr.org/countries/brazil"),
        ("HRW - Brazil", "https://www.hrw.org/americas/brazil"),
        (
            "Amnesty - Brazil",
            "https://www.amnesty.org/en/location/americas/south-america/brazil/",
        ),
        ("NARA - Brazil", "https://catalog.archives.gov/search?q=brazil"),
        (
            "OAS - Brazil",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=BRA",
        ),
    ],
    "US_BS_BAHAMAS": [
        (
            "Library of Congress - Bahamas",
            "https://www.loc.gov/search/?q=bahamas+united+states",
        ),
        ("State Dept - Bahamas", "https://www.state.gov/countries-areas/bahamas/"),
        (
            "UN Digital Library - Bahamas",
            "https://digitallibrary.un.org/search?ln=en&p=bahamas",
        ),
        ("World Bank - Bahamas", "https://data.worldbank.org/country/bahamas-the"),
        ("UNHCR - Bahamas", "https://www.unhcr.org/countries/bahamas"),
        ("HRW - Americas", "https://www.hrw.org/americas"),
        (
            "OAS - Bahamas",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=BAH",
        ),
        ("CARICOM - Bahamas", "https://caricom.org/country_profiles/bahamas/"),
        ("NARA - Bahamas", "https://catalog.archives.gov/search?q=bahamas"),
        ("ICRC - Americas", "https://www.icrc.org/en/where-we-work/americas"),
    ],
    "US_BZ_BELIZE": [
        (
            "Library of Congress - Belize",
            "https://www.loc.gov/search/?q=belize+united+states",
        ),
        ("State Dept - Belize", "https://www.state.gov/countries-areas/belize/"),
        (
            "UN Digital Library - Belize",
            "https://digitallibrary.un.org/search?ln=en&p=belize",
        ),
        ("World Bank - Belize", "https://data.worldbank.org/country/belize"),
        ("UNHCR - Belize", "https://www.unhcr.org/countries/belize"),
        ("HRW - Americas", "https://www.hrw.org/americas"),
        (
            "OAS - Belize",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=BZE",
        ),
        ("CARICOM - Belize", "https://caricom.org/country_profiles/belize/"),
        ("NARA - Belize", "https://catalog.archives.gov/search?q=belize"),
        ("ICRC - Americas", "https://www.icrc.org/en/where-we-work/americas"),
    ],
    "US_CL_CHILE": [
        (
            "Library of Congress - Chile",
            "https://www.loc.gov/search/?q=chile+united+states",
        ),
        ("State Dept - Chile", "https://www.state.gov/countries-areas/chile/"),
        ("FRUS - Chile", "https://history.state.gov/countries/chile"),
        (
            "UN Digital Library - Chile",
            "https://digitallibrary.un.org/search?ln=en&p=chile",
        ),
        ("World Bank - Chile", "https://data.worldbank.org/country/chile"),
        ("UNHCR - Chile", "https://www.unhcr.org/countries/chile"),
        ("HRW - Chile", "https://www.hrw.org/americas/chile"),
        (
            "Amnesty - Chile",
            "https://www.amnesty.org/en/location/americas/south-america/chile/",
        ),
        ("NARA - Chile", "https://catalog.archives.gov/search?q=chile"),
        (
            "National Security Archive - Chile",
            "https://nsarchive.gwu.edu/project/chile-documentation-project",
        ),
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
