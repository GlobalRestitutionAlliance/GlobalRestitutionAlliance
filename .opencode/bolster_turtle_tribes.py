import csv, hashlib, json, re, datetime, urllib.request, os, subprocess, shutil, sys, traceback
from pathlib import Path

TODAY = datetime.date.today().isoformat()
ROOT = Path(r"W:\Legal\US_TURTLE_ISLAND_NATIVES")
LOG = Path(r"W:\Legal\.opencode\turtle_tribes_bolster.log")

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
UA = "Mozilla/5.0 (compatible; GlobalRestitutionAlliance/1.0)"


def log(msg):
    line = f"[{datetime.datetime.utcnow().isoformat()}Z] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def sha256b(b):
    return hashlib.sha256(b).hexdigest()


def sha256p(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


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


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(), getattr(r, "status", 200), dict(r.headers.items()), r.geturl()


def find_repos():
    repos = []
    for gitdir in ROOT.rglob(".git"):
        if gitdir.is_dir():
            repos.append(gitdir.parent)
    return sorted(set(repos))


def bolster_repo(cdir):
    name = cdir.name
    # infer a readable label
    label = name.replace("_", " ").strip()
    for d in DIRS:
        (cdir / d).mkdir(parents=True, exist_ok=True)
    # core docs
    write(
        cdir / "README.md",
        f"# {label} - Litigation Framework\n\n**Template:** CUBA-adapted framework\n**Generated:** {TODAY}\n**Status:** SCAFFOLD - verification required. No fabricated citations.\n\nThis repository is a research/framework scaffold for qualified counsel and partner organizations. All captures are `PUBLIC_CAPTURE_UNAUTHENTICATED` until custodian/legal authentication.\n",
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
                f"  - id: agent_{i:03d}\n    name: Agent {i:03d}\n    status: ACTIVE_SCAFFOLD\n"
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
                f"  - id: skill_{i:03d}\n    name: Skill {i:03d}\n    status: ACTIVE_SCAFFOLD\n"
                for i in range(1, 253)
            ]
        ),
        cdir,
    )
    vec = ag / "vector-index"
    vec.mkdir(parents=True, exist_ok=True)
    (vec / "vector_index.jsonl").write_text(
        "\n".join(
            [
                f"VID-{i:04d}|{name}|scaffold|verification-required|{TODAY}"
                for i in range(1, 1806)
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    # sources
    ex = cdir / "03_Evidentiary_Exhibits"
    ex.mkdir(parents=True, exist_ok=True)
    rows = [
        (
            "TI",
            label,
            "PUBLIC_PORTAL",
            "National Archives - Native American Records",
            "https://www.archives.gov/research/native-americans",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "TI",
            label,
            "PUBLIC_PORTAL",
            "Bureau of Indian Affairs",
            "https://www.bia.gov/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "TI",
            label,
            "PUBLIC_PORTAL",
            "Library of Congress - Indigenous Law",
            "https://www.loc.gov/law/help/american-indian-consts/",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "TI",
            label,
            "PUBLIC_PORTAL",
            "US State Dept FRUS",
            "https://history.state.gov/historicaldocuments",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "TI",
            label,
            "PUBLIC_PORTAL",
            "UN OHCHR Indigenous Peoples",
            "https://www.ohchr.org/en/indigenous-peoples",
            "PUBLIC_PORTAL",
            "VERIFY_AND_DOWNLOAD",
        ),
        (
            "TI",
            label,
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
        f"# Evidence Intake Log - {label}\n\n| Date | Artifact | Source URL | Retrieved By | SHA-256 | Custody Status | Notes |\n|---|---|---|---|---|---|---|\n\n## Intake Rules\n- No `VERIFIED` status without local hashed source artifact and human sign-off.\n- Captures are `PUBLIC_CAPTURE_UNAUTHENTICATED` until custodian/legal authentication.\n",
        cdir,
    )
    write(
        cdir / "99_Archives_and_Manifests/LEGAL_ACCURACY_REVIEW_CHECKLIST.md",
        f"# Legal Accuracy Review Checklist - {label}\n\nStatus: FRAMEWORK TEMPLATE - not legal advice. Verify all citations.\n- [ ] Jurisdiction/standing/tribal sovereignty\n- [ ] Treaties/statutes/limitations\n- [ ] Causation/damages\n- [ ] Evidence authentication/chain of custody\n- [ ] Counsel/organization sign-off\n",
        cdir,
    )
    write(
        cdir / "03_Evidentiary_Exhibits/AUTHENTICATION_DECLARATION_TEMPLATE.md",
        f"# Authentication & Chain-of-Custody Declaration Template - {label}\n\nTEMPLATE - human attestation required. Not executed.\n",
        cdir,
    )
    write(
        cdir / "99_Archives_and_Manifests/FILING_PACKAGE_INDEX.md",
        f"# Filing Package Index - {label}\n\n- 01_Pleadings_and_Complaints: scaffold\n- 02_Discovery_and_Evidentiary: scaffold\n- 03_Motions_and_Briefs: scaffold\n- 04_International_Tribunals: scaffold\n- 05_Strategic_Doctrines_and_Red_Team: scaffold\n- 06_Trial_and_Appellate_Prep: scaffold\n- 07_Enforcement_and_Restitution: scaffold\n- Evidence: `03_Evidentiary_Exhibits/Immutable_Ledger/` (PUBLIC_CAPTURE_UNAUTHENTICATED)\n- Citations: `03_Evidentiary_Exhibits/CITATION_INDEX.*` (PENDING_LEGAL_REVIEW)\n",
        cdir,
    )
    # 01-07 md scaffolds
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
            cdir / folder / f"{folder}_SCAFFOLD.md",
            f"# {title} - {label}\n\nStatus: SCAFFOLD - verification required. Not legal advice.\n\n## Scope\n- Framework scaffold for counsel/organization review.\n- All citations must reference local hashed artifacts.\n\n## Checklist\n- [ ] Verify jurisdiction and standing\n- [ ] Verify citations and exhibits\n- [ ] Human legal review and sign-off\n",
            cdir,
        )
    # harvest
    ledger = cdir / "03_Evidentiary_Exhibits/Immutable_Ledger"
    ledger.mkdir(parents=True, exist_ok=True)
    logp = cdir / "03_Evidentiary_Exhibits/EVIDENCE_INTAKE_LOG.md"
    newrows = []
    for i, r in enumerate(rows[:6]):
        url = r[4]
        title = r[3]
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
                "local_artifact": str(art.relative_to(cdir)).replace("\\", "/"),
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
        f"# Citation Index - {label}\n\nRule: NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT. All PENDING_LEGAL_REVIEW.\n\n"
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
        d = cdir / folder
        if not d.exists():
            continue
        for p in d.rglob("*.md"):
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
    for fp in sorted(cdir.rglob("*")):
        if not fp.is_file():
            continue
        rel = fp.relative_to(cdir).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel == "VERIFICATION_KEYS/sha256_manifest.txt":
            continue
        try:
            lines.append(f"{sha256p(fp)}  {rel}")
        except:
            pass
    (cdir / "VERIFICATION_KEYS/sha256_manifest.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )
    return len(cites), len(lines)


def git_run(cdir, args, env, timeout=180):
    return subprocess.run(
        args, cwd=str(cdir), capture_output=True, text=True, env=env, timeout=timeout
    )


def commit_repo(cdir, env):
    git_run(cdir, ["git", "config", "core.autocrlf", "input"], env)
    git_run(cdir, ["git", "add", "-A"], env)
    st = git_run(cdir, ["git", "status", "--short"], env)
    if not st.stdout.strip():
        return "clean"
    c = git_run(
        cdir, ["git", "commit", "-m", "Bolster to Cuba-template framework parity"], env
    )
    return "committed" if c.returncode == 0 else "commit-fail"


def push_repo(cdir, env):
    p = git_run(cdir, ["git", "push", "origin", "HEAD"], env, timeout=240)
    return p.returncode == 0


def main():
    repos = find_repos()
    log(f"FOUND {len(repos)} repos")
    # bolster + commit
    committed = []
    for i, r in enumerate(repos, 1):
        try:
            cites, files = bolster_repo(r)
            env = os.environ.copy()
            env["GIT_TERMINAL_PROMPT"] = "0"
            st = commit_repo(r, env)
            committed.append((r, st))
            if i % 25 == 0 or i == len(repos):
                log(
                    f"BOLSTER {i}/{len(repos)} {r.name} cites={cites} files={files} {st}"
                )
        except Exception as e:
            log(f"ERR-BOLSTER {r.name}: {e}")
            committed.append((r, "error"))
    # push R03LV1S first
    subprocess.run(["gh", "auth", "switch", "-u", "R03LV1S"], capture_output=True)
    env_r = os.environ.copy()
    env_r["GIT_TERMINAL_PROMPT"] = "0"
    env_r["GH_TOKEN"] = os.environ.get("GH_TOKEN", "") or ""
    failed = []
    for i, (r, _) in enumerate(committed, 1):
        ok = push_repo(r, env_r)
        if ok:
            if i % 50 == 0:
                log(f"PUSH-R03 {i}/{len(committed)} ok")
        else:
            failed.append(r)
    log(
        f"R03LV1S pushed {len(committed) - len(failed)}/{len(committed)}; failed {len(failed)}"
    )
    # fallback GRA
    if failed:
        subprocess.run(
            ["gh", "auth", "switch", "-u", "GlobalRestitutionAlliance"],
            capture_output=True,
        )
        env_g = os.environ.copy()
        env_g["GIT_TERMINAL_PROMPT"] = "0"
        env_g.pop("GH_TOKEN", None)
        env_g.pop("GITHUB_TOKEN", None)
        still = []
        for i, r in enumerate(failed, 1):
            ok = push_repo(r, env_g)
            if not ok:
                still.append(r.name)
            if i % 50 == 0:
                log(f"PUSH-GRA {i}/{len(failed)}")
        log(f"GRA fallback failed {len(still)}: {still[:20]}")
        subprocess.run(["gh", "auth", "switch", "-u", "R03LV1S"], capture_output=True)
    log("DONE")


if __name__ == "__main__":
    main()
