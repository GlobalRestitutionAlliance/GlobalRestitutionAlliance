#!/usr/bin/env python3
"""LATAM 8-repo full-enrichment wave: scaffold, harvest, enrich, manifests."""

from __future__ import annotations
import csv, json, hashlib, os, re, datetime, urllib.request, ssl
from pathlib import Path

BASE = Path(r"W:\Legal")
REGION = "LATIN_AMERICA"
REPOS = {
    "US_MX_MEXICO": [
        (
            "National Archives - Mexico",
            "https://www.archives.gov/research/foreign-policy/mexico",
        ),
        (
            "Library of Congress - Mexico",
            "https://www.loc.gov/search/?q=mexico+united+states+intervention",
        ),
        ("State Dept FRUS - Mexico", "https://history.state.gov/countries/mexico"),
        (
            "Yale Avalon - Treaty of Guadalupe Hidalgo 1848",
            "https://avalon.law.yale.edu/19th_century/guadhida.asp",
        ),
        (
            "UN Digital Library - Mexico",
            "https://digitallibrary.un.org/search?ln=en&p=mexico",
        ),
        ("World Bank - Mexico", "https://data.worldbank.org/country/mexico"),
        ("UNHCR - Mexico", "https://www.unhcr.org/countries/mexico"),
        ("HRW - Mexico", "https://www.hrw.org/americas/mexico"),
        (
            "Amnesty - Mexico",
            "https://www.amnesty.org/en/location/americas/north-america/mexico/",
        ),
        (
            "OAS - Mexico",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=MEX",
        ),
    ],
    "US_GT_GUATEMALA": [
        (
            "National Archives - Guatemala",
            "https://www.archives.gov/research/foreign-policy/guatemala",
        ),
        (
            "Library of Congress - Guatemala",
            "https://www.loc.gov/search/?q=guatemala+united+states+1954",
        ),
        (
            "State Dept FRUS - Guatemala 1952-54",
            "https://history.state.gov/historicaldocuments/frus1952-54Guat",
        ),
        (
            "UN Digital Library - Guatemala",
            "https://digitallibrary.un.org/search?ln=en&p=guatemala",
        ),
        (
            "National Security Archive - Guatemala",
            "https://nsarchive.gwu.edu/briefing-book/guatemala/2011-10-24/guatemala-1954-coup",
        ),
        ("World Bank - Guatemala", "https://data.worldbank.org/country/guatemala"),
        ("UNHCR - Guatemala", "https://www.unhcr.org/countries/guatemala"),
        ("HRW - Guatemala", "https://www.hrw.org/americas/guatemala"),
        (
            "Amnesty - Guatemala",
            "https://www.amnesty.org/en/location/americas/central-america-and-the-caribbean/guatemala/",
        ),
        (
            "OAS - Guatemala",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=GUA",
        ),
    ],
    "US_HN_HONDURAS": [
        (
            "National Archives - Honduras",
            "https://www.archives.gov/research/foreign-policy/honduras",
        ),
        (
            "Library of Congress - Honduras",
            "https://www.loc.gov/search/?q=honduras+united+states",
        ),
        ("State Dept - Honduras", "https://www.state.gov/countries-areas/honduras/"),
        (
            "UN Digital Library - Honduras",
            "https://digitallibrary.un.org/search?ln=en&p=honduras",
        ),
        ("World Bank - Honduras", "https://data.worldbank.org/country/honduras"),
        ("UNHCR - Honduras", "https://www.unhcr.org/countries/honduras"),
        ("HRW - Honduras", "https://www.hrw.org/americas/honduras"),
        (
            "Amnesty - Honduras",
            "https://www.amnesty.org/en/location/americas/central-america-and-the-caribbean/honduras/",
        ),
        (
            "OAS - Honduras",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=HON",
        ),
        ("IACHR - Honduras", "https://www.oas.org/en/iachr/reports/country.asp"),
    ],
    "US_SV_EL_SALVADOR": [
        (
            "National Archives - El Salvador",
            "https://www.archives.gov/research/foreign-policy/el-salvador",
        ),
        (
            "Library of Congress - El Salvador",
            "https://www.loc.gov/search/?q=el+salvador+united+states",
        ),
        (
            "State Dept - El Salvador",
            "https://www.state.gov/countries-areas/el-salvador/",
        ),
        (
            "UN Digital Library - El Salvador",
            "https://digitallibrary.un.org/search?ln=en&p=el+salvador",
        ),
        (
            "UN Truth Commission - El Salvador",
            "https://digitallibrary.un.org/record/183599?ln=en",
        ),
        ("World Bank - El Salvador", "https://data.worldbank.org/country/el-salvador"),
        ("UNHCR - El Salvador", "https://www.unhcr.org/countries/el-salvador"),
        ("HRW - El Salvador", "https://www.hrw.org/americas/el-salvador"),
        (
            "Amnesty - El Salvador",
            "https://www.amnesty.org/en/location/americas/central-america-and-the-caribbean/el-salvador/",
        ),
        (
            "OAS - El Salvador",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=ELS",
        ),
    ],
    "US_NI_NICARAGUA": [
        (
            "National Archives - Nicaragua",
            "https://www.archives.gov/research/foreign-policy/nicaragua",
        ),
        (
            "Library of Congress - Nicaragua",
            "https://www.loc.gov/search/?q=nicaragua+united+states+contra",
        ),
        ("State Dept - Nicaragua", "https://www.state.gov/countries-areas/nicaragua/"),
        (
            "ICJ - Military and Paramilitary Activities in and against Nicaragua",
            "https://www.icj-cij.org/case/70",
        ),
        (
            "UN Digital Library - Nicaragua",
            "https://digitallibrary.un.org/search?ln=en&p=nicaragua",
        ),
        ("World Bank - Nicaragua", "https://data.worldbank.org/country/nicaragua"),
        ("UNHCR - Nicaragua", "https://www.unhcr.org/countries/nicaragua"),
        ("HRW - Nicaragua", "https://www.hrw.org/americas/nicaragua"),
        (
            "Amnesty - Nicaragua",
            "https://www.amnesty.org/en/location/americas/central-america-and-the-caribbean/nicaragua/",
        ),
        (
            "OAS - Nicaragua",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=NIC",
        ),
    ],
    "US_PA_PANAMA": [
        (
            "National Archives - Panama",
            "https://www.archives.gov/research/foreign-policy/panama",
        ),
        (
            "Library of Congress - Panama",
            "https://www.loc.gov/search/?q=panama+united+states+invasion+1989",
        ),
        ("State Dept FRUS - Panama", "https://history.state.gov/countries/panama"),
        (
            "Yale Avalon - Panama Canal Treaty 1977",
            "https://avalon.law.yale.edu/20th_century/panama.asp",
        ),
        (
            "UN Digital Library - Panama",
            "https://digitallibrary.un.org/search?ln=en&p=panama",
        ),
        ("World Bank - Panama", "https://data.worldbank.org/country/panama"),
        ("UNHCR - Panama", "https://www.unhcr.org/countries/panama"),
        ("HRW - Panama", "https://www.hrw.org/americas/panama"),
        (
            "Amnesty - Panama",
            "https://www.amnesty.org/en/location/americas/central-america-and-the-caribbean/panama/",
        ),
        (
            "OAS - Panama",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=PAN",
        ),
    ],
    "US_HT_HAITI": [
        (
            "National Archives - Haiti",
            "https://www.archives.gov/research/foreign-policy/haiti",
        ),
        (
            "Library of Congress - Haiti",
            "https://www.loc.gov/search/?q=haiti+united+states+occupation",
        ),
        ("State Dept - Haiti", "https://www.state.gov/countries-areas/haiti/"),
        (
            "UN Digital Library - Haiti",
            "https://digitallibrary.un.org/search?ln=en&p=haiti",
        ),
        ("World Bank - Haiti", "https://data.worldbank.org/country/haiti"),
        ("UNHCR - Haiti", "https://www.unhcr.org/countries/haiti"),
        ("HRW - Haiti", "https://www.hrw.org/americas/haiti"),
        (
            "Amnesty - Haiti",
            "https://www.amnesty.org/en/location/americas/central-america-and-the-caribbean/haiti/",
        ),
        (
            "OAS - Haiti",
            "https://www.oas.org/en/member_states/member_state.asp?sCode=HAI",
        ),
        ("ICRC - Haiti", "https://www.icrc.org/en/where-we-work/americas/haiti"),
    ],
    "US_PR_PUERTO_RICO": [
        (
            "National Archives - Puerto Rico",
            "https://www.archives.gov/research/guide-fed-records/groups/186.html",
        ),
        (
            "Library of Congress - Puerto Rico",
            "https://www.loc.gov/search/?q=puerto+rico+united+states+colonial",
        ),
        (
            "Yale Avalon - Treaty of Paris 1898",
            "https://avalon.law.yale.edu/19th_century/sp1898.asp",
        ),
        (
            "UN Digital Library - Puerto Rico / Decolonization",
            "https://digitallibrary.un.org/search?ln=en&p=puerto+rico+decolonization",
        ),
        (
            "U.S. Congress - Puerto Rico Status",
            "https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22search%22%3A%22Puerto+Rico+status%22%7D",
        ),
        ("World Bank - Puerto Rico", "https://data.worldbank.org/country/puerto-rico"),
        ("HRW - United States / Puerto Rico", "https://www.hrw.org/united-states"),
        (
            "Amnesty - Puerto Rico",
            "https://www.amnesty.org/en/location/americas/north-america/united-states-of-america/",
        ),
        ("DOJ - Puerto Rico", "https://www.justice.gov/usao-pr"),
        ("GAO - Puerto Rico", "https://www.gao.gov/puerto-rico"),
    ],
}
import importlib.util

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
