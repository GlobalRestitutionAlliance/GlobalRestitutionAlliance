import csv, hashlib, json, re, datetime, urllib.request, os, subprocess, sys
from pathlib import Path

TODAY = datetime.date.today().isoformat()
ROOT = Path(r"W:\Legal")
LOG = Path(r"W:\Legal\.opencode\batch2b_harvest.log")
UA = "Mozilla/5.0 (compatible; GlobalRestitutionAlliance/1.0; evidence-harvest)"


def log(m):
    line = f"[{datetime.datetime.utcnow().isoformat()}Z] {m}"
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


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read(), getattr(r, "status", 200), dict(r.headers.items()), r.geturl()


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


def git(cwd, args, env=None, timeout=180):
    return subprocess.run(
        args, cwd=str(cwd), capture_output=True, text=True, env=env, timeout=timeout
    )


def harvest_repo(repo):
    src = repo / "03_Evidentiary_Exhibits/PRIMARY_PUBLIC_SOURCES.csv"
    if not src.exists():
        return 0, 0, 0
    ledger = repo / "03_Evidentiary_Exhibits/Immutable_Ledger"
    ledger.mkdir(parents=True, exist_ok=True)
    logp = repo / "03_Evidentiary_Exhibits/EVIDENCE_INTAKE_LOG.md"
    # existing captured urls
    captured = set()
    for mp in ledger.glob("*.meta.json"):
        try:
            m = json.loads(mp.read_text(encoding="utf-8", errors="ignore"))
            u = (m.get("url") or "").strip()
            if u:
                captured.add(u)
        except:
            pass
    rows = []
    with src.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            u = (row.get("url") or "").strip()
            if u:
                rows.append((row.get("title", "source"), u))
    ok = fail = skip = 0
    newrows = []
    for title, url in rows:
        if url in captured:
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
                "batch": "2b",
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
    # rebuild citations and patch docs if changed
    if ok > 0 or fail > 0:
        ex = repo / "03_Evidentiary_Exhibits"
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
        block = (
            "\n\n## Verified Source Citations (PENDING_LEGAL_REVIEW)\n\nRule: No citation marked VERIFIED without local hashed source artifact and human sign-off.\n\n"
            + "\n".join(
                [
                    f"- {c['citation_id']}: {c['url']} | `{c['local_artifact']}` | `{c['sha256'][:16]}...` | {c['verification_status']}"
                    for c in cites[:30]
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
            fd = repo / folder
            if not fd.exists():
                continue
            for p in fd.rglob("*.md"):
                try:
                    txt = p.read_text(encoding="utf-8", errors="ignore")
                except:
                    continue
                if "## Verified Source Citations (PENDING_LEGAL_REVIEW)" in txt:
                    idx = txt.index(
                        "## Verified Source Citations (PENDING_LEGAL_REVIEW)"
                    )
                    p.write_text(
                        txt[:idx].rstrip() + block, encoding="utf-8", newline="\n"
                    )
                else:
                    p.write_text(txt.rstrip() + block, encoding="utf-8", newline="\n")
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
    return ok, fail, skip


def main():
    repos = find_repos()
    log(f"FOUND {len(repos)}")
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    changed = []
    for i, r in enumerate(repos, 1):
        try:
            ok, fail, skip = harvest_repo(r)
            if ok > 0 or fail > 0:
                git(r, ["git", "add", "-A"], env=env)
                st = git(r, ["git", "status", "--short"], env=env)
                if st.stdout.strip():
                    git(
                        r,
                        [
                            "git",
                            "commit",
                            "-m",
                            "Batch 2b: harvest expanded sources, citations, manifests",
                        ],
                        env=env,
                    )
                    changed.append(r)
            if i % 50 == 0:
                log(
                    f"HARV {i}/{len(repos)} changed={len(changed)} last=ok{ok}/f{fail}/s{skip}"
                )
        except Exception as e:
            log(f"ERR {r.name}: {e}")
    log(f"HARV_DONE changed={len(changed)}")
    subprocess.run(
        ["gh", "auth", "switch", "-u", "GlobalRestitutionAlliance"], capture_output=True
    )
    envg = os.environ.copy()
    envg["GIT_TERMINAL_PROMPT"] = "0"
    envg.pop("GH_TOKEN", None)
    envg.pop("GITHUB_TOKEN", None)
    okp = failp = 0
    for i, r in enumerate(changed, 1):
        p = git(r, ["git", "push", "origin", "HEAD"], envg, timeout=240)
        if p.returncode == 0:
            okp += 1
        else:
            failp += 1
        if i % 50 == 0:
            log(f"PUSH {i}/{len(changed)} ok={okp} fail={failp}")
    log(f"PUSH_DONE ok={okp} fail={failp}")
    subprocess.run(["gh", "auth", "switch", "-u", "R03LV1S"], capture_output=True)
    log("DONE")


if __name__ == "__main__":
    main()
