import subprocess, os, sys
from pathlib import Path

ROOT = Path(r"W:\Legal")
# collect repo names from git remotes under known dirs
dirs = []
# continental
for base in ["AFRICA", "ASIA", "PACIFIC", "US_DOMESTIC_VICTIMS"]:
    p = ROOT / base
    if p.exists():
        for d in p.iterdir():
            if d.is_dir() and (d / ".git").exists():
                dirs.append(d)
# turtle island tribal repos
ti = ROOT / "US_TURTLE_ISLAND_NATIVES"
if ti.exists():
    for gitdir in ti.rglob(".git"):
        if gitdir.is_dir():
            dirs.append(gitdir.parent)
# also top-level domestic-like
for n in ["US_AFRICAN_AMERICAN_REPARATIONS"]:
    p = ROOT / n
    if p.exists() and (p / ".git").exists():
        dirs.append(p)

repos = set()
for d in dirs:
    try:
        r = subprocess.run(
            ["git", "-C", str(d), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        url = r.stdout.strip()
        if "GlobalRestitutionAlliance/" in url:
            name = url.rstrip("/").split("/")[-1].replace(".git", "")
            repos.add(name)
    except:
        pass
repos = sorted(repos)
print(f"FOUND {len(repos)} repos", flush=True)

# switch to GRA
subprocess.run(
    ["gh", "auth", "switch", "-u", "GlobalRestitutionAlliance"], capture_output=True
)
env = os.environ.copy()
env["GIT_TERMINAL_PROMPT"] = "0"
env.pop("GH_TOKEN", None)
env.pop("GITHUB_TOKEN", None)
ok = 0
already = 0
fail = []
for i, name in enumerate(repos, 1):
    full = f"GlobalRestitutionAlliance/{name}"
    p = subprocess.run(
        [
            "gh",
            "repo",
            "edit",
            full,
            "--visibility",
            "public",
            "--accept-visibility-change-consequences",
        ],
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
    )
    if p.returncode == 0:
        ok += 1
    else:
        err = (p.stderr or p.stdout or "").lower()
        if "already public" in err or "visibility is already" in err:
            already += 1
        else:
            fail.append((name, (p.stderr or p.stdout)[:120]))
    if i % 50 == 0:
        print(
            f"PROGRESS {i}/{len(repos)} ok={ok} already={already} fail={len(fail)}",
            flush=True,
        )
print(f"DONE ok={ok} already={already} fail={len(fail)}", flush=True)
for n, e in fail[:30]:
    print(f"FAIL {n}: {e}", flush=True)
subprocess.run(["gh", "auth", "switch", "-u", "R03LV1S"], capture_output=True)
