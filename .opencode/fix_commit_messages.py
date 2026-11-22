import subprocess, os, sys
from pathlib import Path

ROOT = Path(r"W:\Legal")
DRY = "--dry" in sys.argv
BAD = ["Cuba-template", "Nicaragua template", "cuba-template", "Nicaragua Template"]


def git(cwd, args, env=None, timeout=120):
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
    seen = set()
    out = []
    for r in repos:
        s = str(r).lower()
        if s not in seen:
            seen.add(s)
            out.append(r)
    return sorted(out)


repos = find_repos()
targets = []
for r in repos:
    msg = git(r, ["git", "log", "-1", "--pretty=%B"]).stdout.strip()
    if any(b.lower() in msg.lower() for b in BAD):
        targets.append((r, msg.splitlines()[0]))
print(f"FOUND {len(targets)} repos with bad last commit msg")
for r, m in targets[:15]:
    print(f" - {r.name}: {m}")

if DRY:
    sys.exit(0)

subprocess.run(
    ["gh", "auth", "switch", "-u", "GlobalRestitutionAlliance"], capture_output=True
)
env = os.environ.copy()
env["GIT_TERMINAL_PROMPT"] = "0"
env.pop("GH_TOKEN", None)
env.pop("GITHUB_TOKEN", None)
ok = fail = 0
for i, (r, old) in enumerate(targets, 1):
    new = "Update campaign framework, evidence, and documentation"
    a = git(r, ["git", "commit", "--amend", "-m", new], env=env)
    if a.returncode != 0:
        fail += 1
        continue
    p = git(
        r, ["git", "push", "--force-with-lease", "origin", "HEAD"], env=env, timeout=240
    )
    if p.returncode == 0:
        ok += 1
    else:
        fail += 1
    if i % 50 == 0:
        print(f"PROGRESS {i}/{len(targets)} ok={ok} fail={fail}", flush=True)
print(f"DONE ok={ok} fail={fail}", flush=True)
subprocess.run(["gh", "auth", "switch", "-u", "R03LV1S"], capture_output=True)
