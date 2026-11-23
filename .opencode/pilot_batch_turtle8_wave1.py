#!/usr/bin/env python3
"""TURTLE_ISLAND 8-repo full-enrichment wave: scaffold, harvest, enrich, manifests."""

from __future__ import annotations
import importlib.util
from pathlib import Path

BASE = Path(r"W:\Legal")
REPOS = {
    str(
        BASE / "US_TURTLE_ISLAND_NATIVES" / "EASTERN_OKLAHOMA" / "US_OK_CHEROKEE_NATION"
    ): [
        (
            "National Archives - American Indians",
            "https://www.archives.gov/research/native-americans",
        ),
        (
            "Library of Congress - Cherokee",
            "https://www.loc.gov/search/?q=cherokee+nation+treaty",
        ),
        (
            "Yale Avalon - Treaty with the Cherokee 1835",
            "https://avalon.law.yale.edu/19th_century/cherokee.asp",
        ),
        (
            "BIA - Cherokee Nation",
            "https://www.bia.gov/bia/ois/dhs/icwa/agents-locations/cherokee-nation",
        ),
        ("Oklahoma Historical Society - Cherokee", "https://www.okhistory.org/"),
        (
            "Supreme Court - Cherokee Nation v. Georgia",
            "https://supreme.justia.com/cases/federal/us/30/1/",
        ),
        ("HRW - Indigenous Rights US", "https://www.hrw.org/united-states"),
        (
            "UN - Indigenous Peoples",
            "https://www.un.org/development/desa/indigenouspeoples/",
        ),
        ("NARF - Native American Rights Fund", "https://narf.org/"),
        (
            "GPO - Federal Register Cherokee",
            "https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=cherokee+nation",
        ),
    ],
    str(
        BASE / "US_TURTLE_ISLAND_NATIVES" / "GREAT_PLAINS" / "US_SD_OGLALA_SIOUX_TRIBE"
    ): [
        (
            "National Archives - American Indians",
            "https://www.archives.gov/research/native-americans",
        ),
        (
            "Library of Congress - Oglala Sioux",
            "https://www.loc.gov/search/?q=oglala+sioux+treaty",
        ),
        (
            "Yale Avalon - Fort Laramie Treaty 1868",
            "https://avalon.law.yale.edu/19th_century/nt001.asp",
        ),
        (
            "BIA - Pine Ridge Agency",
            "https://www.bia.gov/regional-offices/great-plains/south-dakota/pine-ridge-agency",
        ),
        (
            "Supreme Court - United States v. Sioux Nation",
            "https://supreme.justia.com/cases/federal/us/448/371/",
        ),
        ("NPS - Wounded Knee", "https://www.nps.gov/articles/000/wounded-knee.htm"),
        ("HRW - Indigenous Rights US", "https://www.hrw.org/united-states"),
        (
            "UN - Indigenous Peoples",
            "https://www.un.org/development/desa/indigenouspeoples/",
        ),
        ("NARF - Native American Rights Fund", "https://narf.org/"),
        (
            "GPO - Federal Register Oglala Sioux",
            "https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=oglala+sioux",
        ),
    ],
    str(
        BASE
        / "US_TURTLE_ISLAND_NATIVES"
        / "EASTERN_OKLAHOMA"
        / "US_OK_THE_CHOCTAW_NATION_OF_OKLAHOMA"
    ): [
        (
            "National Archives - American Indians",
            "https://www.archives.gov/research/native-americans",
        ),
        (
            "Library of Congress - Choctaw Nation",
            "https://www.loc.gov/search/?q=choctaw+nation+treaty",
        ),
        (
            "Yale Avalon - Treaty of Dancing Rabbit Creek 1830",
            "https://avalon.law.yale.edu/19th_century/choctaw.asp",
        ),
        (
            "BIA - Choctaw Nation",
            "https://www.bia.gov/bia/ois/dhs/icwa/agents-locations/choctaw-nation-oklahoma",
        ),
        (
            "Supreme Court - McGirt v. Oklahoma",
            "https://supreme.justia.com/cases/federal/us/591/18-9526/",
        ),
        ("Oklahoma Historical Society - Choctaw", "https://www.okhistory.org/"),
        ("HRW - Indigenous Rights US", "https://www.hrw.org/united-states"),
        (
            "UN - Indigenous Peoples",
            "https://www.un.org/development/desa/indigenouspeoples/",
        ),
        ("NARF - Native American Rights Fund", "https://narf.org/"),
        (
            "GPO - Federal Register Choctaw",
            "https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=choctaw+nation",
        ),
    ],
    str(
        BASE
        / "US_TURTLE_ISLAND_NATIVES"
        / "EASTERN_OKLAHOMA"
        / "US_OK_THE_SEMINOLE_NATION_OF_OKLAHOMA"
    ): [
        (
            "National Archives - American Indians",
            "https://www.archives.gov/research/native-americans",
        ),
        (
            "Library of Congress - Seminole Nation",
            "https://www.loc.gov/search/?q=seminole+nation+oklahoma",
        ),
        (
            "Yale Avalon - Treaty with the Seminole 1832",
            "https://avalon.law.yale.edu/19th_century/seminole.asp",
        ),
        (
            "BIA - Seminole Nation of Oklahoma",
            "https://www.bia.gov/bia/ois/dhs/icwa/agents-locations/seminole-nation-oklahoma",
        ),
        ("Oklahoma Historical Society - Seminole", "https://www.okhistory.org/"),
        (
            "Supreme Court - Seminole Tribe v. Florida",
            "https://supreme.justia.com/cases/federal/us/517/44/",
        ),
        ("HRW - Indigenous Rights US", "https://www.hrw.org/united-states"),
        (
            "UN - Indigenous Peoples",
            "https://www.un.org/development/desa/indigenouspeoples/",
        ),
        ("NARF - Native American Rights Fund", "https://narf.org/"),
        (
            "GPO - Federal Register Seminole Nation",
            "https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=seminole+nation+oklahoma",
        ),
    ],
    str(
        BASE / "US_TURTLE_ISLAND_NATIVES" / "WESTERN" / "US_AZ_HOPI_TRIBE_OF_ARIZONA"
    ): [
        (
            "National Archives - American Indians",
            "https://www.archives.gov/research/native-americans",
        ),
        (
            "Library of Congress - Hopi",
            "https://www.loc.gov/search/?q=hopi+tribe+arizona",
        ),
        (
            "BIA - Hopi Agency",
            "https://www.bia.gov/regional-offices/western/hopi-agency",
        ),
        ("NPS - Hopi", "https://www.nps.gov/subjects/nagpra/index.htm"),
        (
            "Supreme Court - Masayesva v. Zah",
            "https://supreme.justia.com/cases/federal/us/prec/516-1002/",
        ),
        ("Arizona State Museum - Hopi", "https://statemuseum.arizona.edu/"),
        ("HRW - Indigenous Rights US", "https://www.hrw.org/united-states"),
        (
            "UN - Indigenous Peoples",
            "https://www.un.org/development/desa/indigenouspeoples/",
        ),
        ("NARF - Native American Rights Fund", "https://narf.org/"),
        (
            "GPO - Federal Register Hopi Tribe",
            "https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=hopi+tribe",
        ),
    ],
    str(
        BASE
        / "US_TURTLE_ISLAND_NATIVES"
        / "GREAT_PLAINS"
        / "US_SD_ROSEBUD_SIOUX_TRIBE_OF_THE_ROSEBUD_INDIA"
    ): [
        (
            "National Archives - American Indians",
            "https://www.archives.gov/research/native-americans",
        ),
        (
            "Library of Congress - Rosebud Sioux",
            "https://www.loc.gov/search/?q=rosebud+sioux+tribe",
        ),
        (
            "Yale Avalon - Fort Laramie Treaty 1868",
            "https://avalon.law.yale.edu/19th_century/nt001.asp",
        ),
        (
            "BIA - Rosebud Agency",
            "https://www.bia.gov/regional-offices/great-plains/south-dakota/rosebud-agency",
        ),
        (
            "Supreme Court - Rosebud Sioux Tribe v. Kneip",
            "https://supreme.justia.com/cases/federal/us/430/584/",
        ),
        ("NARF - Native American Rights Fund", "https://narf.org/"),
        ("HRW - Indigenous Rights US", "https://www.hrw.org/united-states"),
        (
            "UN - Indigenous Peoples",
            "https://www.un.org/development/desa/indigenouspeoples/",
        ),
        (
            "GPO - Federal Register Rosebud Sioux",
            "https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=rosebud+sioux",
        ),
        ("DOI - Indian Affairs", "https://www.bia.gov/"),
    ],
    str(
        BASE
        / "US_TURTLE_ISLAND_NATIVES"
        / "GREAT_PLAINS"
        / "US_ND_STANDING_ROCK_SIOUX_TRIBE_OF_NORTH_SOUTH"
    ): [
        (
            "National Archives - American Indians",
            "https://www.archives.gov/research/native-americans",
        ),
        (
            "Library of Congress - Standing Rock Sioux",
            "https://www.loc.gov/search/?q=standing+rock+sioux+tribe",
        ),
        (
            "Yale Avalon - Fort Laramie Treaty 1868",
            "https://avalon.law.yale.edu/19th_century/nt001.asp",
        ),
        (
            "BIA - Standing Rock Agency",
            "https://www.bia.gov/regional-offices/great-plains/north-dakota/standing-rock-agency",
        ),
        (
            "Army Corps - Dakota Access Pipeline",
            "https://www.nwo.usace.army.mil/Missions/Dam-and-Lake-Projects/Oil-and-Gas-Development/Dakota-Access-Pipeline/",
        ),
        ("NARF - Native American Rights Fund", "https://narf.org/"),
        ("HRW - Indigenous Rights US", "https://www.hrw.org/united-states"),
        (
            "UN - Indigenous Peoples",
            "https://www.un.org/development/desa/indigenouspeoples/",
        ),
        (
            "GPO - Federal Register Standing Rock",
            "https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=standing+rock+sioux",
        ),
        ("DOI - Indian Affairs", "https://www.bia.gov/"),
    ],
    str(
        BASE
        / "US_TURTLE_ISLAND_NATIVES"
        / "ROCKY_MOUNTAIN"
        / "US_MT_BLACKFEET_TRIBE_OF_THE_BLACKFEET_INDIAN_"
    ): [
        (
            "National Archives - American Indians",
            "https://www.archives.gov/research/native-americans",
        ),
        (
            "Library of Congress - Blackfeet",
            "https://www.loc.gov/search/?q=blackfeet+tribe+montana+treaty",
        ),
        (
            "Yale Avalon - Treaty with the Blackfeet 1855",
            "https://avalon.law.yale.edu/19th_century/blackfeet.asp",
        ),
        (
            "BIA - Blackfeet Agency",
            "https://www.bia.gov/regional-offices/rocky-mountain/blackfeet-agency",
        ),
        (
            "Supreme Court - Montana v. United States",
            "https://supreme.justia.com/cases/federal/us/450/544/",
        ),
        ("NARF - Native American Rights Fund", "https://narf.org/"),
        ("HRW - Indigenous Rights US", "https://www.hrw.org/united-states"),
        (
            "UN - Indigenous Peoples",
            "https://www.un.org/development/desa/indigenouspeoples/",
        ),
        (
            "GPO - Federal Register Blackfeet",
            "https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=blackfeet+tribe",
        ),
        ("DOI - Indian Affairs", "https://www.bia.gov/"),
    ],
}

spec = importlib.util.spec_from_file_location(
    "asiaw", str(BASE / ".opencode" / "pilot_batch_asia8_wave1.py")
)
asia = importlib.util.module_from_spec(spec)
spec.loader.exec_module(asia)


def main():
    for repo_path, sources in REPOS.items():
        repo = Path(repo_path)
        if not repo.exists():
            print("MISSING", repo)
            continue
        asia.ensure_source_registry(repo, sources)
        asia.ensure_valuation(repo)
        asia.ensure_vectors(repo)
        asia.harvest(repo, sources)
        asia.build_citation_indexes(repo)
        asia.refresh_manifest(repo)
        print("DONE", repo.name)


if __name__ == "__main__":
    main()
