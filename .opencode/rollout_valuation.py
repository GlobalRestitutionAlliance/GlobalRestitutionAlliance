import os, subprocess, hashlib, shutil
from pathlib import Path

ROOT = Path(r"W:\Legal")
TPL = Path(r"W:\Legal\.opencode\templates\valuation")
METH = (TPL / "VALUATION_METHODOLOGY.md").read_text(encoding="utf-8")
WB = (TPL / "VALUATION_WORKBOOK.csv").read_text(encoding="utf-8")
XW = (TPL / "MASTER_VECTOR_VALUATION_CROSSWALK.csv").read_text(encoding="utf-8")
DQM = (TPL / "damages-quantum-modeling.yaml").read_text(encoding="utf-8")


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
    # also perpetrator repos under US_AFRICAN_AMERICAN_REPARATIONS
    aa = ROOT / "US_AFRICAN_AMERICAN_REPARATIONS"
    if aa.exists():
        for d in aa.iterdir():
            if d.is_dir() and (d / ".git").exists():
                repos.append(d)
    seen = set()
    out = []
    for r in repos:
        s = str(r).lower()
        if s not in seen:
            seen.add(s)
            out.append(r)
    return sorted(out)


def apply(repo):
    changed = False
    kb = repo / "00_Master_Knowledge_Base"
    kb.mkdir(parents=True, exist_ok=True)
    for name, content in [
        ("VALUATION_METHODOLOGY.md", METH),
        ("VALUATION_WORKBOOK.csv", WB),
        ("MASTER_VECTOR_VALUATION_CROSSWALK.csv", XW),
    ]:
        p = kb / name
        if not p.exists():
            p.write_text(content, encoding="utf-8", newline="\n")
            changed = True
    skill = repo / ".antigravity/skills/damages-quantum-modeling.yaml"
    skill.parent.mkdir(parents=True, exist_ok=True)
    if not skill.exists():
        skill.write_text(DQM, encoding="utf-8", newline="\n")
        changed = True
    else:
        # update policy key if missing
        txt = skill.read_text(encoding="utf-8", errors="ignore")
        if "1805 minimum baseline and goal" not in txt:
            # append policy note minimally
            if "policy:" not in txt:
                txt = txt.replace(
                    "skill:\n",
                    'skill:\n  policy:\n    vector_baseline: "1805 vectors minimum baseline and goal; expand with verified evidence"\n    valuation_status_default: "TBD (valuation pending)"\n',
                    1,
                )
            else:
                txt = txt.replace(
                    "policy:\n",
                    'policy:\n    vector_baseline: "1805 vectors minimum baseline and goal; expand with verified evidence"\n',
                    1,
                )
            skill.write_text(txt, encoding="utf-8", newline="\n")
            changed = True
    if changed:
        # refresh manifest
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
        (repo / "VERIFICATION_KEYS/sha256_manifest.txt").parent.mkdir(
            parents=True, exist_ok=True
        )
        (repo / "VERIFICATION_KEYS/sha256_manifest.txt").write_text(
            "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
        )
    return changed


def main():
    repos = find_repos()
    print(f"FOUND {len(repos)}", flush=True)
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    changed = []
    for i, r in enumerate(repos, 1):
        try:
            if apply(r):
                git(r, ["git", "add", "-A"], env=env)
                st = git(r, ["git", "status", "--short"], env=env)
                if st.stdout.strip():
                    git(
                        r,
                        [
                            "git",
                            "commit",
                            "-m",
                            "Add evidence-backed valuation methodology scaffolding",
                        ],
                        env=env,
                    )
                    changed.append(r)
            if i % 100 == 0:
                print(f"APPLY {i}/{len(repos)} changed={len(changed)}", flush=True)
        except Exception as e:
            print(f"ERR {r.name}: {e}", flush=True)
    print(f"APPLY_DONE changed={len(changed)}", flush=True)
    # push GRA
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
