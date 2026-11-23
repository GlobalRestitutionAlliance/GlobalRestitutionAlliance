#!/usr/bin/env python3
"""LATAM 2-repo full-enrichment wave 5 (final)."""

from __future__ import annotations
import importlib.util
from pathlib import Path

BASE = Path(r"W:\Legal")
REGION = "LATIN_AMERICA"
REPOS = {
    "US_VE_VENEZUELA": [
        (
            "Library of Congress - Venezuela",
            "https://www.loc.gov/search/?q=venezuela+united+states",
        ),
        ("State Dept - Venezuela", "https://www.state.gov/countries-areas/venezuela/"),
        ("FRUS - Venezuela", "https://history.state.gov/countries/venezuela"),
        (
            "UN Digital Library - Venezuela",
            "https://digitallibrary.un.org/search?ln=en&p=venezuela",
        ),
        ("World Bank - Venezuela", "https://data.worldbank.org/country/venezuela-rb"),
        ("UNHCR - Venezuela", "https://www.unhcr.org/countries/venezuela"),
        ("HRW - Venezuela", "https://www.hrw.org/americas/venezuela"),
        (
            "Amnesty - Venezuela",
            "https://www.amnesty.org/en/location/americas/south-america/venezuela/",
        ),
        ("NARA - Venezuela", "https://catalog.archives.gov/search?q=venezuela"),
        (
            "OAS - Venezuela",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=VEN",
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
