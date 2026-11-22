import csv, hashlib, json, re, datetime, urllib.request, os, subprocess, shutil
from pathlib import Path

TODAY = datetime.date.today().isoformat()
ROOT = Path(r"W:\Legal\US_TURTLE_ISLAND_NATIVES")
REGIONS = sorted([d for d in ROOT.iterdir() if d.is_dir()])


def sha256b(b):
    return hashlib.sha256(b).hexdigest()


def sha256p(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


UA = "Mozilla/5.0"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(), getattr(r, "status", 200), dict(r.headers.items()), r.geturl()


def backup(path, cdir):
    if not path.exists():
        return
    b = cdir / "99_Archives_and_Manifests/pre_bolster_backup"
    b.mkdir(parents=True, exist_ok=True)
    d = b / path.name
    if not d.exists():
        try:
            shutil.copy2(path, d)
        except:
            pass


def write(path, content, cdir):
    path.parent.mkdir(parents=True, exist_ok=True)
    backup(path, cdir)
    path.write_text(content, encoding="utf-8", newline="\n")


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
for cdir in REGIONS:
    name = cdir.name
    iso = "TI"
    for d in DIRS:
        (cdir / d).mkdir(parents=True, exist_ok=True)
    write(
        cdir / "README.md",
        f"# {name} - Turtle Island Restitution Framework\n\n**Template:** GRA litigation framework\n**Generated:** {TODAY}\n**Status:** SCAFFOLD - verification required. No fabricated citations.\n",
        cdir,
    )
    write(
        cdir / ".github/workflows/integrity-verification.yml",
        'name: Evidentiary Integrity Verification\non:\n  push:\n  pull_request:\njobs:\n  verify-hashes:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Verify SHA-256 Manifest\n        run: |\n          cd "$GITHUB_WORKSPACE"\n          if [ -f VERIFICATION_KEYS/sha256_manifest.txt ]; then sha256sum -c VERIFICATION_KEYS/sha256_manifest.txt; else echo No manifest && exit 1; fi\n',
        cdir,
    )
    ag = cdir / ".antigravity"
    write(
        ag / "project.yaml",
        f"name: {name}\nstatus: SCAFFOLD_FRAMEWORK\ngenerated: {TODAY}\n",
        cdir,
    )
    write(
        ag / "agents/agent-registry.yaml",
        "agents:\n"
        + "".join(
            [
                f"  - id: agent_{name.lower()}_{i:03d}\n    name: {name} Agent {i:03d}\n    status: ACTIVE_SCAFFOLD\n"
                for i in range(1, 171)
            ]
        ),
        cdir,
    )
    write(
        ag / "skills/skill-registry.yaml",
        "skills:\n"
        + "".join(
            [
                f"  - id: skill_{name.lower()}_{i:03d}\n    name: {name} Skill {i:03d}\n    status: ACTIVE_SCAFFOLD\n"
                for i in range(1, 253)
            ]
        ),
        cdir,
    )
    vec = cdir / ".antigravity/vector-index"
    vec.mkdir(parents=True, exist_ok=True)
    (vec / "vector_index.jsonl").write_text(
        "\n".join(
            [
                f"VID-{name[:3].upper()}-{i:04d}|{name}|scaffold|verification-required|{TODAY}"
                for i in range(1, 1806)
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    ex = cdir / "03_Evidentiary_Exhibits"
    ex.mkdir(parents=True, exist_ok=True)
    rows = [
        (
            "TI",
            name,
            "PUBLIC_PORTAL",
            "National Archives - Native American Records",
            "https://www.archives.gov/research/native-americans",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "TI",
            name,
            "PUBLIC_PORTAL",
            "BIA",
            "https://www.bia.gov/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "TI",
            name,
            "PUBLIC_PORTAL",
            "Library of Congress - Indigenous Law",
            "https://www.loc.gov/law/help/american-indian-consts/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "TI",
            name,
            "PUBLIC_PORTAL",
            "US State Dept FRUS",
            "https://history.state.gov/historicaldocuments",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "TI",
            name,
            "PUBLIC_PORTAL",
            "UN OHCHR Indigenous Peoples",
            "https://www.ohchr.org/en/indigenous-peoples",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "TI",
            name,
            "PUBLIC_PORTAL",
            "CourtListener",
            "https://www.courtlistener.com/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
    ]
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
        cdir,
    )
    write(
        ex / "EVIDENCE_INTAKE_LOG.md",
        f"# Evidence Intake Log - {name}\n\n| Date | Artifact | Source URL | Retrieved By | SHA-256 | Custody Status | Notes |\n|---|---|---|---|---|---|---|\n",
        cdir,
    )
    write(
        cdir / "99_Archives_and_Manifests/LEGAL_ACCURACY_REVIEW_CHECKLIST.md",
        f"# Legal Accuracy Review Checklist - {name}\n\nStatus: FRAMEWORK TEMPLATE - not legal advice. Verify all citations.\n- [ ] Jurisdiction/standing/tribal sovereignty\n- [ ] Treaties/statutes/limitations\n- [ ] Causation/damages\n- [ ] Evidence authentication\n- [ ] Counsel/organization sign-off\n",
        cdir,
    )
    write(
        cdir / "03_Evidentiary_Exhibits/AUTHENTICATION_DECLARATION_TEMPLATE.md",
        f"# Authentication Declaration Template - {name}\n\nTEMPLATE - human attestation required.\n",
        cdir,
    )
    # quick harvest
    ledger = cdir / "03_Evidentiary_Exhibits/Immutable_Ledger"
    ledger.mkdir(parents=True, exist_ok=True)
    log = cdir / "03_Evidentiary_Exhibits/EVIDENCE_INTAKE_LOG.md"
    newrows = []
    for i, r in enumerate(rows[:6]):
        url = r[4]
        title = r[3]
        try:
            data, status, headers, final = fetch(url)
            ct = headers.get("Content-Type", "")
            ext = ".html"
            fn = re.sub(r"[^A-Za-z0-9._-]+", "_", title)[:70] + ext
            out = ledger / fn
            n = 1
            while out.exists():
                out = ledger / (fn.rsplit(".", 1)[0] + f"_{n}" + ext)
                n += 1
            out.write_bytes(data)
            meta = {
                "url": url,
                "final_url": final,
                "status": status,
                "content_type": ct,
                "bytes": len(data),
                "sha256": sha256b(data),
                "captured_at": datetime.datetime.utcnow().isoformat() + "Z",
                "custodian": "OpenCode/harvest",
            }
            out.with_suffix(out.suffix + ".meta.json").write_text(
                json.dumps(meta, indent=2), encoding="utf-8"
            )
            newrows.append(
                f"| {TODAY} | {out.name} | {url} | OpenCode/harvest | {meta['sha256']} | PUBLIC_CAPTURE_UNAUTHENTICATED | status={status} bytes={len(data)} |"
            )
        except Exception as e:
            newrows.append(
                f"| {TODAY} | {title} | {url} | OpenCode/harvest | N/A | CAPTURE_FAILED | {e} |"
            )
    if newrows and log.exists():
        txt = log.read_text(encoding="utf-8")
        m = "## Intake Rules"
        log.write_text(
            txt.replace(m, "\n".join(newrows) + "\n\n" + m, 1)
            if m in txt
            else txt + "\n" + "\n".join(newrows),
            encoding="utf-8",
            newline="\n",
        )
    # cite index
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
                "citation_id": f"TI-{len(cites) + 1:04d}",
                "url": meta.get("url", ""),
                "local_artifact": str(art.relative_to(cdir)).replace("\\", "/"),
                "sha256": meta.get("sha256", ""),
                "verification_status": "PENDING_LEGAL_REVIEW",
                "verification_rule": "NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT",
            }
        )
    ex2 = cdir / "03_Evidentiary_Exhibits"
    with (ex2 / "CITATION_INDEX.csv").open("w", newline="", encoding="utf-8") as f:
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
    (ex2 / "CITATION_INDEX.md").write_text(
        f"# Citation Index - {name}\n\nRule: NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT. All PENDING_LEGAL_REVIEW.\n\n"
        + "\n".join(
            [
                f"- {c['citation_id']}: {c['url']} | `{c['local_artifact']}` | `{c['sha256'][:16]}...`"
                for c in cites
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    # manifest
    lines = []
    for fp in sorted(cdir.rglob("*")):
        if not fp.is_file():
            continue
        rel = fp.relative_to(cdir).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel == "VERIFICATION_KEYS/sha256_manifest.txt":
            continue
        lines.append(f"{sha256p(fp)}  {rel}")
    (cdir / "VERIFICATION_KEYS/sha256_manifest.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )
    print("OK", name, "files", len(lines), "cites", len(cites))
print("DONE")
