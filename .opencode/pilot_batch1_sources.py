import csv, hashlib, json, re, datetime, urllib.request, os, subprocess
from pathlib import Path

TODAY = datetime.date.today().isoformat()
ROOT = Path(r"W:\Legal")
UA = "Mozilla/5.0 (compatible; GlobalRestitutionAlliance/1.0; evidence-harvest)"

REPOS = {
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS": [
        (
            "Library of Congress - African American History",
            "https://www.loc.gov/classroom-materials/african-american-history/",
        ),
        (
            "National Archives - African American Records",
            "https://www.archives.gov/research/african-americans",
        ),
        (
            "Chronicling America - slavery search portal",
            "https://chroniclingamerica.loc.gov/",
        ),
        (
            "HathiTrust - public domain slavery narratives",
            "https://babel.hathitrust.org/cgi/mb?a=listis;c=729189149",
        ),
        ("Smithsonian NMAAHC", "https://nmaahc.si.edu/"),
        (
            "Congress.gov - HR40",
            "https://www.congress.gov/bill/117th-congress/house-bill/40",
        ),
        (
            "National Archives - Emancipation Proclamation",
            "https://www.archives.gov/exhibits/featured-documents/emancipation-proclamation",
        ),
        (
            "FOIA.gov - DOJ Civil Rights",
            "https://www.foia.gov/agency-search.html?id=9d4f7e74-7c93-4d5a-8d2a-9f7b8d0e2a2b",
        ),
    ],
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-gb-reparations-master-litigation": [
        (
            "UK National Archives - slavery research guide",
            "https://www.nationalarchives.gov.uk/help-with-your-research/research-guides/slavery-or-slave-owners/",
        ),
        (
            "UK Parliament - abolition",
            "https://www.parliament.uk/about/living-heritage/transformingsociety/tradeindustry/slavetrade/",
        ),
        ("Legacies of British Slavery - UCL", "https://www.ucl.ac.uk/lbs/"),
        (
            "The National Archives Discovery",
            "https://discovery.nationalarchives.gov.uk/",
        ),
        (
            "British Library - slavery and abolition",
            "https://www.bl.uk/collection-guides/abolition-of-the-slave-trade-and-slavery",
        ),
        ("Hansard UK Parliament", "https://hansard.parliament.uk/"),
    ],
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-pt-reparations-master-litigation": [
        (
            "Slave Voyages - Trans-Atlantic",
            "https://www.slavevoyages.org/voyage/database",
        ),
        ("Arquivo Nacional Torre do Tombo", "https://antt.dglab.gov.pt/"),
        ("Biblioteca Nacional de Portugal", "https://bndigital.bnportugal.gov.pt/"),
        (
            "UNESCO Routes of Enslaved Peoples",
            "https://www.unesco.org/en/routes-enslaved-peoples",
        ),
        ("Library of Congress - Portugal resources", "https://www.loc.gov/"),
    ],
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-nl-reparations-master-litigation": [
        (
            "Nationaal Archief - slavery past",
            "https://www.nationaalarchief.nl/en/research/search?searchTerm=slavery",
        ),
        (
            "Dutch National Archives slavery research",
            "https://www.nationaalarchief.nl/onderzoeken/zoekhulpen/slavernijverleden",
        ),
        ("Rijksmuseum - Slavery", "https://www.rijksmuseum.nl/en/stories/slavery"),
        ("Slave Voyages - Dutch", "https://www.slavevoyages.org/"),
        (
            "UNESCO Routes of Enslaved Peoples",
            "https://www.unesco.org/en/routes-enslaved-peoples",
        ),
    ],
    r"W:\Legal\US_DOMESTIC_VICTIMS\US_DW_NUCLEAR_DOWNWINDERS": [
        ("DOE OpenNet", "https://www.osti.gov/opennet/"),
        ("NNSA Nevada Field Office", "https://www.nnss.gov/"),
        ("RECA DOJ", "https://www.justice.gov/civil/common/reca"),
        (
            "NARA Atomic Energy Records",
            "https://www.archives.gov/research/military/atomic-energy",
        ),
        ("CDC NIOSH Radiation", "https://www.cdc.gov/niosh/ocas/ocascomp.html"),
        (
            "Congress.gov RECA amendments",
            "https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22search%22%3A%22Radiation+Exposure+Compensation+Act%22%7D",
        ),
    ],
    r"W:\Legal\PACIFIC\US_MH_MARSHALL_ISLANDS": [
        ("DOE OpenNet - Pacific tests", "https://www.osti.gov/opennet/"),
        (
            "US State Dept - Marshall Islands",
            "https://www.state.gov/countries-areas/marshall-islands/",
        ),
        (
            "NARA - Pacific nuclear testing",
            "https://www.archives.gov/research/military/atomic-energy",
        ),
        (
            "Marshall Islands Nuclear Claims Tribunal archive refs (public)",
            "https://www.rmiembassyus.org/",
        ),
        (
            "UN Digital Library - Marshall Islands",
            "https://digitallibrary.un.org/search?ln=en&cc=UN+Documents&p=Marshall+Islands+nuclear",
        ),
        (
            "Congress.gov - Compact of Free Association",
            "https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22search%22%3A%22Marshall+Islands+Compact%22%7D",
        ),
    ],
    r"W:\Legal\US_DOMESTIC_VICTIMS\US_JA_JAPANESE_AMERICAN_INTERNEES": [
        (
            "NARA - Japanese American Incarceration",
            "https://www.archives.gov/education/lessons/japanese-relocation",
        ),
        ("Densho Encyclopedia", "https://encyclopedia.densho.org/"),
        (
            "Library of Congress - Internment",
            "https://www.loc.gov/classroom-materials/japanese-american-internment/",
        ),
        (
            "National Archives - EO 9066",
            "https://www.archives.gov/milestone-documents/executive-order-9066",
        ),
        (
            "GovInfo - CWRIC report",
            "https://www.govinfo.gov/app/details/GPO-CRECB-1983-pt16/GPO-CRECB-1983-pt16-3-1",
        ),
        ("JACL History", "https://jacl.org/history"),
    ],
    r"W:\Legal\US_TURTLE_ISLAND_NATIVES\NAVAJO\US_AZ_NAVAJO_NATION_ARIZONA_NEW_MEXICO_UTAH": [
        (
            "NARA - Native American Records",
            "https://www.archives.gov/research/native-americans",
        ),
        ("BIA - Navajo Region", "https://www.bia.gov/regional-offices/navajo"),
        (
            "Library of Congress - American Indian Constitutions",
            "https://www.loc.gov/law/help/american-indian-consts/",
        ),
        (
            "US EPA - Navajo Nation uranium",
            "https://www.epa.gov/navajo-nation-uranium-cleanup",
        ),
        (
            "US Courts - Navajo Nation water rights (public)",
            "https://www.justice.gov/enrd/indian-resources-section",
        ),
        ("GovInfo - Navajo-Hopi settlement acts", "https://www.govinfo.gov/"),
    ],
}


def sha256b(b):
    return hashlib.sha256(b).hexdigest()


def sha256p(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read(), getattr(r, "status", 200), dict(r.headers.items()), r.geturl()


def git(cwd, args, env=None, timeout=180):
    return subprocess.run(
        args, cwd=str(cwd), capture_output=True, text=True, env=env, timeout=timeout
    )


for path, sources in REPOS.items():
    repo = Path(path)
    if not repo.exists():
        print("MISS", path)
        continue
    ex = repo / "03_Evidentiary_Exhibits"
    ex.mkdir(parents=True, exist_ok=True)
    csvp = ex / "PRIMARY_PUBLIC_SOURCES.csv"
    existing = set()
    rows = []
    if csvp.exists():
        with csvp.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                url = (row.get("url") or "").strip()
                if url:
                    existing.add(url)
                rows.append(row)
    added = 0
    for title, url in sources:
        if url in existing:
            continue
        rows.append(
            {
                "iso": "",
                "country": repo.name,
                "source_type": "PUBLIC_PORTAL",
                "title": title,
                "url": url,
                "access_class": "PUBLIC_PORTAL",
                "status": "VERIFY_AND_DOWNLOAD",
            }
        )
        existing.add(url)
        added += 1
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
    (ex / "PRIMARY_PUBLIC_SOURCES.md").write_text(
        "# Primary Public Sources\n\n"
        + "".join(
            [
                f"- [{r.get('title', '')}]({r.get('url', '')})\n"
                for r in rows
                if r.get("url")
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    # harvest
    ledger = ex / "Immutable_Ledger"
    ledger.mkdir(parents=True, exist_ok=True)
    logp = ex / "EVIDENCE_INTAKE_LOG.md"
    captured = set()
    for mp in ledger.glob("*.meta.json"):
        try:
            m = json.loads(mp.read_text(encoding="utf-8", errors="ignore"))
            captured.add((m.get("url") or "").strip())
        except:
            pass
    newrows = []
    ok = fail = skip = 0
    for title, url in [(r.get("title", ""), r.get("url", "")) for r in rows]:
        if not url or url in captured:
            skip += 1
            continue
        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", title)[:70] + ".html"
        out = ledger / safe
        n = 1
        while out.exists():
            out = ledger / (safe.rsplit(".", 1)[0] + f"_{n}.html")
            n += 1
        try:
            data, status, headers, final = fetch(url)
            out.write_bytes(data)
            meta = {
                "url": url,
                "final_url": final,
                "status": status,
                "content_type": headers.get("Content-Type", ""),
                "bytes": len(data),
                "sha256": sha256b(data),
                "captured_at": datetime.datetime.utcnow().isoformat() + "Z",
                "custodian": "OpenCode/harvest",
                "provenance": "direct-http-capture",
                "batch": "pilot-1",
            }
            out.with_suffix(out.suffix + ".meta.json").write_text(
                json.dumps(meta, indent=2), encoding="utf-8"
            )
            newrows.append(
                f"| {TODAY} | {out.name} | {url} | OpenCode/harvest | {meta['sha256']} | PUBLIC_CAPTURE_UNAUTHENTICATED | status={status} bytes={len(data)} |"
            )
            ok += 1
        except Exception as e:
            newrows.append(
                f"| {TODAY} | {title} | {url} | OpenCode/harvest | N/A | CAPTURE_FAILED | {str(e)[:160]} |"
            )
            fail += 1
    if newrows and logp.exists():
        txt = logp.read_text(encoding="utf-8", errors="ignore")
        m = "## Intake Rules"
        logp.write_text(
            txt.replace(m, "\n".join(newrows) + "\n\n" + m, 1)
            if m in txt
            else txt + "\n" + "\n".join(newrows),
            encoding="utf-8",
            newline="\n",
        )
    # citations
    cites = []
    for mp in sorted(ledger.glob("*.meta.json")):
        try:
            meta = json.loads(mp.read_text(encoding="utf-8", errors="ignore"))
        except:
            continue
        art = Path(str(mp).replace(".meta.json", ""))
        if not art.exists():
            continue
        cites.append(
            {
                "citation_id": f"CIT-{len(cites) + 1:04d}",
                "url": meta.get("url", ""),
                "local_artifact": str(art.relative_to(repo)).replace("\\", "/"),
                "sha256": meta.get("sha256", ""),
                "verification_status": "PENDING_LEGAL_REVIEW",
                "verification_rule": "NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT",
            }
        )
    with (ex / "CITATION_INDEX.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "citation_id",
                "url",
                "local_artifact",
                "sha256",
                "verification_status",
                "verification_rule",
            ],
        )
        w.writeheader()
        w.writerows(cites)
    (ex / "CITATION_INDEX.md").write_text(
        "# Citation Index\n\nRule: NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT. All PENDING_LEGAL_REVIEW.\n\n"
        + "\n".join(
            [
                f"- {c['citation_id']}: {c['url']} | `{c['local_artifact']}` | `{c['sha256'][:16]}...` | {c['verification_status']}"
                for c in cites
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
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
    print(
        f"{repo.name} added={added} ok={ok} fail={fail} skip={skip} cites={len(cites)}",
        flush=True,
    )

# commit/push
env = os.environ.copy()
env["GIT_TERMINAL_PROMPT"] = "0"
for path in REPOS:
    repo = Path(path)
    if not (repo / ".git").exists():
        continue
    git(repo, ["git", "add", "-A"], env=env)
    st = git(repo, ["git", "status", "--short"], env=env)
    if st.stdout.strip():
        git(
            repo,
            [
                "git",
                "commit",
                "-m",
                "Pilot Batch 1: targeted source expansion, harvest, citations",
            ],
            env=env,
        )
subprocess.run(
    ["gh", "auth", "switch", "-u", "GlobalRestitutionAlliance"], capture_output=True
)
envg = os.environ.copy()
envg["GIT_TERMINAL_PROMPT"] = "0"
envg.pop("GH_TOKEN", None)
envg.pop("GITHUB_TOKEN", None)
for path in REPOS:
    repo = Path(path)
    p = git(repo, ["git", "push", "origin", "HEAD"], envg, timeout=240)
    print(repo.name, "PUSH_OK" if p.returncode == 0 else "PUSH_FAIL", flush=True)
subprocess.run(["gh", "auth", "switch", "-u", "R03LV1S"], capture_output=True)
print("DONE", flush=True)
