import csv, os, subprocess, hashlib
from pathlib import Path

ROOT = Path(r"W:\Legal")

BASE_SOURCES = [
    (
        "PUBLIC_PORTAL",
        "US National Archives",
        "https://www.archives.gov/",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
    (
        "PUBLIC_PORTAL",
        "Library of Congress",
        "https://www.loc.gov/",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
    (
        "PUBLIC_PORTAL",
        "Chronicling America (LOC Newspapers)",
        "https://chroniclingamerica.loc.gov/",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
    (
        "PUBLIC_PORTAL",
        "HathiTrust Digital Library",
        "https://www.hathitrust.org/",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
    (
        "PUBLIC_PORTAL",
        "Internet Archive",
        "https://archive.org/",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
    (
        "PUBLIC_PORTAL",
        "FOIA.gov",
        "https://www.foia.gov/",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
    (
        "PUBLIC_PORTAL",
        "NARA FOIA",
        "https://www.archives.gov/foia",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
    (
        "PUBLIC_PORTAL",
        "US State Dept FRUS",
        "https://history.state.gov/historicaldocuments",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
    (
        "PUBLIC_PORTAL",
        "UN Digital Library",
        "https://digitallibrary.un.org/",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
    (
        "PUBLIC_PORTAL",
        "UN OHCHR",
        "https://www.ohchr.org/",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
    (
        "PUBLIC_PORTAL",
        "CourtListener",
        "https://www.courtlistener.com/",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
    (
        "PUBLIC_PORTAL",
        "Justia",
        "https://www.justia.com/",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
    (
        "PUBLIC_PORTAL",
        "WorldCat",
        "https://search.worldcat.org/",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
    (
        "PUBLIC_PORTAL",
        "Wikisource",
        "https://en.wikisource.org/",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
    (
        "PUBLIC_PORTAL",
        "US Govt Publishing Office",
        "https://www.govinfo.gov/",
        "PUBLIC_PORTAL",
        "VERIFY_AND_DOWNLOAD",
    ),
]

DOMAIN = {
    "slavery": [
        (
            "PUBLIC_DATABASE",
            "SlaveVoyages",
            "https://www.slavevoyages.org/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "UCL Legacies of British Slavery",
            "https://www.ucl.ac.uk/lbs/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "UNESCO Routes of Enslaved Peoples",
            "https://www.unesco.org/en/routes-enslaved-peoples",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "UK National Archives - Slavery",
            "https://www.nationalarchives.gov.uk/help-with-your-research/research-guides/slavery-or-slave-owners/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "Library of Congress - Slavery Resources",
            "https://guides.loc.gov/slavery",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
    ],
    "nuclear": [
        (
            "PUBLIC_PORTAL",
            "DOE OpenNet / Declassified",
            "https://www.osti.gov/opennet/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "NNSA",
            "https://www.energy.gov/nnsa/national-nuclear-security-administration",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "RECA Program (DOJ)",
            "https://www.justice.gov/civil/common/reca",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "NARA - Nuclear Testing Records",
            "https://www.archives.gov/research/military/atomic-energy",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
    ],
    "indigenous": [
        (
            "PUBLIC_PORTAL",
            "NARA - Native American Records",
            "https://www.archives.gov/research/native-americans",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "Bureau of Indian Affairs",
            "https://www.bia.gov/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "Library of Congress - Indigenous Law",
            "https://www.loc.gov/law/help/american-indian-consts/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "UN OHCHR Indigenous Peoples",
            "https://www.ohchr.org/en/indigenous-peoples",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
    ],
    "japan_internment": [
        (
            "PUBLIC_PORTAL",
            "NARA - Japanese American Incarceration",
            "https://www.archives.gov/education/lessons/japanese-relocation",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "Densho Encyclopedia",
            "https://encyclopedia.densho.org/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "Library of Congress - Japanese American Internment",
            "https://www.loc.gov/classroom-materials/japanese-american-internment/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
    ],
    "guantanamo_rendition": [
        (
            "PUBLIC_PORTAL",
            "ACLU FOIA Torture Database",
            "https://www.aclu.org/issues/national-security/torture",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "National Security Archive",
            "https://nsarchive.gwu.edu/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "CIA FOIA Reading Room",
            "https://www.cia.gov/reading-room/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "PUBLIC_PORTAL",
            "ICRC Detention Resources",
            "https://www.icrc.org/en/war-and-law/detention",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
    ],
}


def classify(repo: Path):
    s = str(repo).lower()
    if (
        "african-american" in s
        or "reparations" in s
        or "actor-royal-african" in s
        or "actor-dutch-wic" in s
    ):
        return "slavery"
    if "downwinders" in s or "nuclear" in s:
        return "nuclear"
    if (
        "turtle_island_natives" in s
        or "tribe" in s
        or "nation" in s
        and "US_TURTLE_ISLAND" in str(repo)
    ):
        return "indigenous"
    if "japanese_american_internees" in s or "japanese-american-internees" in s:
        return "japan_internment"
    if "guantanamo" in s or "rendition" in s:
        return "guantanamo_rendition"
    return "general"


def find_repos():
    repos = []
    for base in ["AFRICA", "ASIA", "PACIFIC", "US_DOMESTIC_VICTIMS"]:
        p = ROOT / base
        if p.exists():
            for d in p.iterdir():
                if d.is_dir() and (d / ".git").exists():
                    repos.append(d)
    ti = ROOT / "US_TURTLE_ISLAND_NATIVES"
    if ti.exists():
        for gd in ti.rglob(".git"):
            if gd.is_dir():
                repos.append(gd.parent)
    for n in ["US_AFRICAN_AMERICAN_REPARATIONS"]:
        p = ROOT / n
        if p.exists() and (p / ".git").exists():
            repos.append(p)
        if p.exists():
            for d in p.iterdir():
                if d.is_dir() and (d / ".git").exists():
                    repos.append(d)
    seen = set()
    out = []
    for r in repos:
        k = str(r).lower()
        if k not in seen:
            seen.add(k)
            out.append(r)
    return sorted(out)


def sha256p(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def git(cwd, args, env=None, timeout=180):
    return subprocess.run(
        args, cwd=str(cwd), capture_output=True, text=True, env=env, timeout=timeout
    )


def apply(repo):
    ex = repo / "03_Evidentiary_Exhibits"
    ex.mkdir(parents=True, exist_ok=True)
    csvp = ex / "PRIMARY_PUBLIC_SOURCES.csv"
    existing = set()
    rows = []
    if csvp.exists():
        with csvp.open("r", encoding="utf-8", newline="") as f:
            r = csv.DictReader(f)
            for row in r:
                url = (row.get("url") or "").strip()
                if url:
                    existing.add(url)
                rows.append(row)
    dom = classify(repo)
    to_add = list(BASE_SOURCES) + list(DOMAIN.get(dom, []))
    added = 0
    for st, title, url, ac, status in to_add:
        if url in existing:
            continue
        rows.append(
            {
                "iso": "",
                "country": repo.name,
                "source_type": st,
                "title": title,
                "url": url,
                "access_class": ac,
                "status": status,
            }
        )
        existing.add(url)
        added += 1
    if added == 0:
        return 0
    with csvp.open("w", encoding="utf-8", newline="") as f:
        cols = [
            "iso",
            "country",
            "source_type",
            "title",
            "url",
            "access_class",
            "status",
        ]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for row in rows:
            w.writerow({c: row.get(c, "") for c in cols})
    # md
    md = ["# Primary Public Sources", "", ""] + [
        f"- [{r.get('title', '')}]({r.get('url', '')})" for r in rows if r.get("url")
    ]
    (ex / "PRIMARY_PUBLIC_SOURCES.md").write_text(
        "\n".join(md) + "\n", encoding="utf-8", newline="\n"
    )
    # manifest
    lines = []
    for fp in sorted(repo.rglob("*")):
        if not fp.is_file():
            continue
        rel = fp.relative_to(repo).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel == "VERIFICATION_KEYS/sha256_manifest.txt":
            continue
        try:
            lines.append(f"{sha256p(fp)}  {rel}")
        except:
            pass
    (repo / "VERIFICATION_KEYS/sha256_manifest.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )
    return added


def main():
    repos = find_repos()
    print(f"FOUND {len(repos)}", flush=True)
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    changed = []
    for i, r in enumerate(repos, 1):
        try:
            a = apply(r)
            if a:
                git(r, ["git", "add", "-A"], env=env)
                st = git(r, ["git", "status", "--short"], env=env)
                if st.stdout.strip():
                    git(
                        r,
                        [
                            "git",
                            "commit",
                            "-m",
                            "Expand primary public source registries (Batch 2)",
                        ],
                        env=env,
                    )
                    changed.append(r)
            if i % 100 == 0:
                print(f"REG {i}/{len(repos)} changed={len(changed)}", flush=True)
        except Exception as e:
            print(f"ERR {r.name}: {e}", flush=True)
    print(f"REG_DONE changed={len(changed)}", flush=True)
    subprocess.run(
        ["gh", "auth", "switch", "-u", "GlobalRestitutionAlliance"], capture_output=True
    )
    envg = os.environ.copy()
    envg["GIT_TERMINAL_PROMPT"] = "0"
    envg.pop("GH_TOKEN", None)
    envg.pop("GITHUB_TOKEN", None)
    ok = fail = 0
    for i, r in enumerate(changed, 1):
        p = git(r, ["git", "push", "origin", "HEAD"], envg, timeout=240)
        if p.returncode == 0:
            ok += 1
        else:
            fail += 1
        if i % 100 == 0:
            print(f"PUSH {i}/{len(changed)} ok={ok} fail={fail}", flush=True)
    print(f"PUSH_DONE ok={ok} fail={fail}", flush=True)
    subprocess.run(["gh", "auth", "switch", "-u", "R03LV1S"], capture_output=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
