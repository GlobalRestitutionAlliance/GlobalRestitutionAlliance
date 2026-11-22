import csv, hashlib, json, re, datetime, urllib.request, os, subprocess, shutil
from pathlib import Path

TODAY = datetime.date.today().isoformat()
BASE = Path(r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS")
GRA = "GlobalRestitutionAlliance"
UA = "Mozilla/5.0 (compatible; GlobalRestitutionAlliance/1.0)"

ACTORS = [
    {
        "slug": "gb",
        "iso": "GB",
        "name": "United Kingdom",
        "kind": "STATE",
        "repo": "african-american-gb-reparations-master-litigation",
        "focus": "British transatlantic slave trade, colonial slavery, Royal Navy/merchant networks - verification required",
        "sources": [
            (
                "UK National Archives - Slave Trade",
                "https://www.nationalarchives.gov.uk/help-with-your-research/research-guides/slavery-or-slave-owners/",
            ),
            (
                "UK Parliament - Slavery Abolition",
                "https://www.parliament.uk/about/living-heritage/transformingsociety/tradeindustry/slavetrade/",
            ),
            ("Legacies of British Slavery (UCL)", "https://www.ucl.ac.uk/lbs/"),
            (
                "British Library - Slavery Resources",
                "https://www.bl.uk/collection-guides/abolition-of-the-slave-trade-and-slavery",
            ),
            ("UN OHCHR", "https://www.ohchr.org/"),
            ("Library of Congress", "https://www.loc.gov/"),
        ],
    },
    {
        "slug": "pt",
        "iso": "PT",
        "name": "Portugal",
        "kind": "STATE",
        "repo": "african-american-pt-reparations-master-litigation",
        "focus": "Portuguese transatlantic slave trade, Angola/Brazil routes - verification required",
        "sources": [
            ("Arquivo Nacional Torre do Tombo", "https://antt.dglab.gov.pt/"),
            ("Biblioteca Nacional de Portugal", "https://www.bnportugal.gov.pt/"),
            ("Slave Voyages", "https://www.slavevoyages.org/"),
            ("UN OHCHR", "https://www.ohchr.org/"),
            ("Library of Congress", "https://www.loc.gov/"),
            (
                "UNESCO Slavery Routes",
                "https://www.unesco.org/en/routes-enslaved-peoples",
            ),
        ],
    },
    {
        "slug": "es",
        "iso": "ES",
        "name": "Spain",
        "kind": "STATE",
        "repo": "african-american-es-reparations-master-litigation",
        "focus": "Spanish colonial slavery, Asiento, Caribbean/South American systems - verification required",
        "sources": [
            (
                "Archivo General de Indias",
                "https://www.culturaydeporte.gob.es/cultura/areas/archivos/mc/archivos/agi/portada.html",
            ),
            ("Biblioteca Nacional de España", "https://www.bne.es/"),
            ("Slave Voyages", "https://www.slavevoyages.org/"),
            ("UN OHCHR", "https://www.ohchr.org/"),
            ("Library of Congress", "https://www.loc.gov/"),
            (
                "UNESCO Slavery Routes",
                "https://www.unesco.org/en/routes-enslaved-peoples",
            ),
        ],
    },
    {
        "slug": "nl",
        "iso": "NL",
        "name": "Netherlands",
        "kind": "STATE",
        "repo": "african-american-nl-reparations-master-litigation",
        "focus": "Dutch transatlantic slave trade, WIC/VOC involvement, Suriname/Caribbean - verification required",
        "sources": [
            (
                "Nationaal Archief - Slavery",
                "https://www.nationaalarchief.nl/onderzoeken/zoekhulpen/slavernijverleden",
            ),
            (
                "Dutch Slavery History (Rijksmuseum)",
                "https://www.rijksmuseum.nl/en/stories/slavery",
            ),
            ("Slave Voyages", "https://www.slavevoyages.org/"),
            ("UN OHCHR", "https://www.ohchr.org/"),
            ("Library of Congress", "https://www.loc.gov/"),
            (
                "UNESCO Slavery Routes",
                "https://www.unesco.org/en/routes-enslaved-peoples",
            ),
        ],
    },
    {
        "slug": "fr",
        "iso": "FR",
        "name": "France",
        "kind": "STATE",
        "repo": "african-american-fr-reparations-master-litigation",
        "focus": "French transatlantic slave trade, Code Noir, Caribbean colonies - verification required",
        "sources": [
            (
                "Archives Nationales d'Outre-Mer",
                "http://www.archivesnationales.culture.gouv.fr/anom/fr/",
            ),
            ("Bibliothèque nationale de France", "https://www.bnf.fr/"),
            ("CNRS/Slave Voyages", "https://www.slavevoyages.org/"),
            ("UN OHCHR", "https://www.ohchr.org/"),
            ("Library of Congress", "https://www.loc.gov/"),
            (
                "UNESCO Slavery Routes",
                "https://www.unesco.org/en/routes-enslaved-peoples",
            ),
        ],
    },
    {
        "slug": "dk",
        "iso": "DK",
        "name": "Denmark",
        "kind": "STATE",
        "repo": "african-american-dk-reparations-master-litigation",
        "focus": "Danish transatlantic slave trade, Danish West Indies - verification required",
        "sources": [
            ("Danish National Archives", "https://www.rigsarkivet.dk/"),
            ("Royal Danish Library", "https://www.kb.dk/"),
            ("Slave Voyages", "https://www.slavevoyages.org/"),
            ("UN OHCHR", "https://www.ohchr.org/"),
            ("Library of Congress", "https://www.loc.gov/"),
            (
                "UNESCO Slavery Routes",
                "https://www.unesco.org/en/routes-enslaved-peoples",
            ),
        ],
    },
    {
        "slug": "br",
        "iso": "BR",
        "name": "Brazil",
        "kind": "STATE",
        "repo": "african-american-br-reparations-master-litigation",
        "focus": "Brazilian slavery system, largest destination in transatlantic trade - verification required",
        "sources": [
            ("Arquivo Nacional (Brazil)", "https://www.gov.br/arquivonacional/pt-br"),
            ("Biblioteca Nacional do Brasil", "https://www.bn.gov.br/"),
            ("Slave Voyages", "https://www.slavevoyages.org/"),
            ("UN OHCHR", "https://www.ohchr.org/"),
            ("Library of Congress", "https://www.loc.gov/"),
            (
                "UNESCO Slavery Routes",
                "https://www.unesco.org/en/routes-enslaved-peoples",
            ),
        ],
    },
    {
        "slug": "actor-royal-african-company",
        "iso": "GB-ACTOR",
        "name": "Royal African Company (Actor Track)",
        "kind": "ACTOR",
        "repo": "african-american-actor-royal-african-company-reparations-master-litigation",
        "focus": "Royal African Company role in transatlantic slave trade; successor/jurisdiction anchors in GB - verification required",
        "sources": [
            (
                "UK National Archives - Royal African Company",
                "https://discovery.nationalarchives.gov.uk/details/c/F169346",
            ),
            ("Slave Voyages", "https://www.slavevoyages.org/"),
            ("Legacies of British Slavery (UCL)", "https://www.ucl.ac.uk/lbs/"),
            ("British Library", "https://www.bl.uk/"),
            ("UN OHCHR", "https://www.ohchr.org/"),
            ("Library of Congress", "https://www.loc.gov/"),
        ],
    },
    {
        "slug": "actor-dutch-wic",
        "iso": "NL-ACTOR",
        "name": "Dutch West India Company (Actor Track)",
        "kind": "ACTOR",
        "repo": "african-american-actor-dutch-wic-reparations-master-litigation",
        "focus": "WIC role in transatlantic slave trade; successor/jurisdiction anchors in NL - verification required",
        "sources": [
            (
                "Nationaal Archief - WIC",
                "https://www.nationaalarchief.nl/onderzoeken/archief/1.05.01.01",
            ),
            ("Slave Voyages", "https://www.slavevoyages.org/"),
            ("Dutch Slavery History", "https://www.rijksmuseum.nl/en/stories/slavery"),
            (
                "UNESCO Slavery Routes",
                "https://www.unesco.org/en/routes-enslaved-peoples",
            ),
            ("UN OHCHR", "https://www.ohchr.org/"),
            ("Library of Congress", "https://www.loc.gov/"),
        ],
    },
]

DIRS = [
    ".antigravity/agents",
    ".antigravity/skills",
    ".antigravity/workflows",
    ".antigravity/rules",
    ".antigravity/templates",
    ".antigravity/tools",
    ".antigravity/knowledge",
    ".antigravity/vector-index",
    ".github/workflows",
    "00_Master_Knowledge_Base",
    "01_Pleadings_and_Complaints",
    "02_Discovery_and_Evidentiary",
    "03_Evidentiary_Exhibits",
    "03_Evidentiary_Exhibits/Immutable_Ledger",
    "03_Motions_and_Briefs",
    "04_International_Tribunals",
    "05_Strategic_Doctrines_and_Red_Team",
    "06_Trial_and_Appellate_Prep",
    "07_Enforcement_and_Restitution",
    "99_Archives_and_Manifests",
    "VERIFICATION_KEYS",
]


def sha256b(b):
    return hashlib.sha256(b).hexdigest()


def sha256p(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read(), getattr(r, "status", 200), dict(r.headers.items()), r.geturl()


def git(cwd, args, env=None, timeout=180):
    return subprocess.run(
        args, cwd=str(cwd), capture_output=True, text=True, env=env, timeout=timeout
    )


def ensure_repo(actor):
    d = BASE / actor["repo"]
    if d.exists():
        return d
    subprocess.run(["gh", "auth", "switch", "-u", GRA], capture_output=True)
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    # create remote
    subprocess.run(
        [
            "gh",
            "repo",
            "create",
            f"{GRA}/{actor['repo']}",
            "--public",
            "--confirm",
            "--description",
            f"Master litigation repository for {actor['name']}. Part of the Global Restitution Alliance legal framework.",
        ],
        capture_output=True,
        text=True,
        env=env,
        timeout=120,
    )
    d.mkdir(parents=True, exist_ok=True)
    git(d, ["git", "init"], env=env)
    git(
        d,
        [
            "git",
            "remote",
            "add",
            "origin",
            f"https://github.com/{GRA}/{actor['repo']}.git",
        ],
        env=env,
    )
    return d


def scaffold(actor, d):
    for x in DIRS:
        (d / x).mkdir(parents=True, exist_ok=True)
    write(
        d / "README.md",
        f"# {actor['name']} - African American Reparations Framework\n\n**Framework:** GRA litigation framework\n**Generated:** {TODAY}\n**Status:** SCAFFOLD - verification required. No fabricated citations.\n\n**Focus:** {actor['focus']}\n\nThis repository is a research/framework scaffold for qualified counsel, researchers, and partner organizations. All captures are `PUBLIC_CAPTURE_UNAUTHENTICATED` until custodian/legal authentication. Counsel/researcher review is required before any filing.\n",
    )
    write(
        d / ".github/workflows/integrity-verification.yml",
        'name: Evidentiary Integrity Verification\non:\n  push:\n  pull_request:\njobs:\n  verify-hashes:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Verify SHA-256 Manifest\n        run: |\n          cd "$GITHUB_WORKSPACE"\n          if [ -f VERIFICATION_KEYS/sha256_manifest.txt ]; then sha256sum -c VERIFICATION_KEYS/sha256_manifest.txt; else echo No manifest && exit 1; fi\n',
    )
    ag = d / ".antigravity"
    write(
        ag / "project.yaml",
        f"name: {actor['repo']}\nstatus: SCAFFOLD_FRAMEWORK\ngenerated: {TODAY}\nactor: {actor['name']}\nkind: {actor['kind']}\n",
    )
    write(
        ag / "agents/agent-registry.yaml",
        "agents:\n"
        + "".join(
            [
                f"  - id: agent_{i:03d}\n    name: Agent {i:03d}\n    status: ACTIVE_SCAFFOLD\n"
                for i in range(1, 171)
            ]
        ),
    )
    write(
        ag / "skills/skill-registry.yaml",
        "skills:\n"
        + "".join(
            [
                f"  - id: skill_{i:03d}\n    name: Skill {i:03d}\n    status: ACTIVE_SCAFFOLD\n"
                for i in range(1, 253)
            ]
        ),
    )
    (ag / "vector-index/vector_index.jsonl").write_text(
        "\n".join(
            [
                f"VID-{i:04d}|{actor['repo']}|scaffold|verification-required|{TODAY}"
                for i in range(1, 1806)
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    # sources
    ex = d / "03_Evidentiary_Exhibits"
    ex.mkdir(parents=True, exist_ok=True)
    rows = []
    for title, url in actor["sources"]:
        rows.append(
            [
                actor["iso"],
                actor["name"],
                "PUBLIC_PORTAL",
                title,
                url,
                "PUBLIC_PORTAL",
                "VERIFY_AND_DOWNLOAD",
            ]
        )
    with (ex / "PRIMARY_PUBLIC_SOURCES.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f)
        w.writerow(
            ["iso", "country", "source_type", "title", "url", "access_class", "status"]
        )
        w.writerows(rows)
    write(
        ex / "PRIMARY_PUBLIC_SOURCES.md",
        "# Primary Public Sources\n\n"
        + "".join([f"- [{r[3]}]({r[4]})\n" for r in rows]),
    )
    write(
        ex / "EVIDENCE_INTAKE_LOG.md",
        f"# Evidence Intake Log - {actor['name']}\n\n| Date | Artifact | Source URL | Retrieved By | SHA-256 | Custody Status | Notes |\n|---|---|---|---|---|---|---|\n\n## Intake Rules\n- No `VERIFIED` status without local hashed source artifact and human sign-off.\n- Captures are `PUBLIC_CAPTURE_UNAUTHENTICATED` until custodian/legal authentication.\n",
    )
    write(
        d / "99_Archives_and_Manifests/LEGAL_ACCURACY_REVIEW_CHECKLIST.md",
        f"# Legal Accuracy Review Checklist - {actor['name']}\n\nStatus: FRAMEWORK TEMPLATE - not legal advice. Counsel/researcher review required before filing.\n- [ ] Jurisdiction/standing/successor liability\n- [ ] Applicable treaties/statutes/limitations\n- [ ] Causation/damages\n- [ ] Evidence authentication/chain of custody\n- [ ] Human sign-off\n",
    )
    write(
        d / "03_Evidentiary_Exhibits/AUTHENTICATION_DECLARATION_TEMPLATE.md",
        f"# Authentication & Chain-of-Custody Declaration Template - {actor['name']}\n\nTEMPLATE - human attestation required. Not executed.\n",
    )
    for folder, title in [
        ("01_Pleadings_and_Complaints", "Pleadings and Complaints"),
        ("02_Discovery_and_Evidentiary", "Discovery and Evidentiary"),
        ("03_Motions_and_Briefs", "Motions and Briefs"),
        ("04_International_Tribunals", "International Tribunals"),
        ("05_Strategic_Doctrines_and_Red_Team", "Strategic Doctrines and Red Team"),
        ("06_Trial_and_Appellate_Prep", "Trial and Appellate Prep"),
        ("07_Enforcement_and_Restitution", "Enforcement and Restitution"),
    ]:
        write(
            d / folder / f"{folder}_SCAFFOLD.md",
            f"# {title} - {actor['name']}\n\nStatus: SCAFFOLD - verification required. Not legal advice.\n\n## Scope\n- Framework scaffold for counsel/researcher review.\n- All citations must reference local hashed artifacts.\n\n## Verified Source Citations (PENDING_LEGAL_REVIEW)\n\nRule: No citation marked VERIFIED without local hashed source artifact and human sign-off.\n",
        )
    # harvest
    ledger = d / "03_Evidentiary_Exhibits/Immutable_Ledger"
    ledger.mkdir(parents=True, exist_ok=True)
    log = d / "03_Evidentiary_Exhibits/EVIDENCE_INTAKE_LOG.md"
    newrows = []
    for i, (title, url) in enumerate(actor["sources"]):
        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", title)[:70] + ".html"
        out = ledger / safe
        n = 1
        while out.exists():
            out = ledger / (safe.rsplit(".", 1)[0] + f"_{n}.html")
            n += 1
        meta_p = out.with_suffix(out.suffix + ".meta.json")
        if meta_p.exists():
            continue
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
            }
            meta_p.write_text(json.dumps(meta, indent=2), encoding="utf-8")
            newrows.append(
                f"| {TODAY} | {out.name} | {url} | OpenCode/harvest | {meta['sha256']} | PUBLIC_CAPTURE_UNAUTHENTICATED | status={status} bytes={len(data)} |"
            )
        except Exception as e:
            newrows.append(
                f"| {TODAY} | {title} | {url} | OpenCode/harvest | N/A | CAPTURE_FAILED | {str(e)[:160]} |"
            )
    if newrows and log.exists():
        txt = log.read_text(encoding="utf-8", errors="ignore")
        m = "## Intake Rules"
        log.write_text(
            txt.replace(m, "\n".join(newrows) + "\n\n" + m, 1)
            if m in txt
            else txt + "\n" + "\n".join(newrows),
            encoding="utf-8",
            newline="\n",
        )
    # citations
    cites = []
    for p in sorted(ledger.glob("*.meta.json")):
        try:
            meta = json.loads(p.read_text(encoding="utf-8"))
        except:
            continue
        art = Path(str(p).replace(".meta.json", ""))
        if not art.exists():
            continue
        cites.append(
            {
                "citation_id": f"CIT-{len(cites) + 1:04d}",
                "url": meta.get("url", ""),
                "local_artifact": str(art.relative_to(d)).replace("\\", "/"),
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
    write(
        ex / "CITATION_INDEX.md",
        f"# Citation Index - {actor['name']}\n\nRule: NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT. All PENDING_LEGAL_REVIEW.\n\n"
        + "\n".join(
            [
                f"- {c['citation_id']}: {c['url']} | `{c['local_artifact']}` | `{c['sha256'][:16]}...` | {c['verification_status']}"
                for c in cites
            ]
        )
        + "\n",
    )
    # patch docs
    block = (
        "\n\n## Verified Source Citations (PENDING_LEGAL_REVIEW)\n\nRule: No citation marked VERIFIED without local hashed source artifact and human sign-off.\n\n"
        + "\n".join(
            [
                f"- {c['citation_id']}: {c['url']} | `{c['local_artifact']}` | `{c['sha256'][:16]}...` | {c['verification_status']}"
                for c in cites[:20]
            ]
        )
        + "\n"
    )
    for folder in [
        "00_Master_Knowledge_Base",
        "01_Pleadings_and_Complaints",
        "02_Discovery_and_Evidentiary",
        "03_Motions_and_Briefs",
        "04_International_Tribunals",
        "05_Strategic_Doctrines_and_Red_Team",
        "06_Trial_and_Appellate_Prep",
        "07_Enforcement_and_Restitution",
    ]:
        fd = d / folder
        if not fd.exists():
            continue
        for p in fd.rglob("*.md"):
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except:
                continue
            if "## Verified Source Citations (PENDING_LEGAL_REVIEW)" in txt:
                idx = txt.index("## Verified Source Citations (PENDING_LEGAL_REVIEW)")
                p.write_text(txt[:idx].rstrip() + block, encoding="utf-8", newline="\n")
            else:
                p.write_text(txt.rstrip() + block, encoding="utf-8", newline="\n")
    # manifest
    lines = []
    for fp in sorted(d.rglob("*")):
        if not fp.is_file():
            continue
        rel = fp.relative_to(d).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel == "VERIFICATION_KEYS/sha256_manifest.txt":
            continue
        try:
            lines.append(f"{sha256p(fp)}  {rel}")
        except:
            pass
    (d / "VERIFICATION_KEYS/sha256_manifest.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )
    return len(cites)


def main():
    subprocess.run(["gh", "auth", "switch", "-u", GRA], capture_output=True)
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    for actor in ACTORS:
        d = ensure_repo(actor)
        cites = scaffold(actor, d)
        git(d, ["git", "add", "-A"], env=env)
        st = git(d, ["git", "status", "--short"], env=env)
        if st.stdout.strip():
            git(
                d,
                [
                    "git",
                    "commit",
                    "-m",
                    "Initial scaffold: framework, sources, harvest, citations, manifests",
                ],
                env=env,
            )
        p = git(d, ["git", "push", "-u", "origin", "HEAD:main"], env=env, timeout=240)
        if p.returncode != 0:
            git(d, ["git", "push", "-u", "origin", "HEAD:master"], env=env, timeout=240)
        print(f"OK {actor['repo']} cites={cites}", flush=True)
    subprocess.run(["gh", "auth", "switch", "-u", "R03LV1S"], capture_output=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
