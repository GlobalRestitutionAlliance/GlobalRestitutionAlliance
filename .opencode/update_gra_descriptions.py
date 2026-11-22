import subprocess, os, re
from pathlib import Path

ROOT = Path(r"W:\Legal")


def nice_name(dir_name):
    n = dir_name
    n = re.sub(r"^US_([A-Z]{2})_", r"\1 ", n)
    n = n.replace("_", " ").strip()
    # Title case with small-word fixes
    n = n.title()
    for a, b in [
        (" Of ", " of "),
        (" And ", " and "),
        (" The ", " the "),
        (" De ", " de "),
        (" Da ", " da "),
        (" Do ", " do "),
        (" La ", " la "),
        (" Le ", " le "),
        (" Du ", " du "),
        (" D'", " d'"),
    ]:
        n = n.replace(a, b)
    # fix leading
    if n.startswith("d'"):
        n = "D'" + n[2:]
    return n


dirs = []
for base in ["AFRICA", "ASIA", "PACIFIC", "US_DOMESTIC_VICTIMS"]:
    p = ROOT / base
    if p.exists():
        for d in p.iterdir():
            if d.is_dir() and (d / ".git").exists():
                dirs.append((d, base))
ti = ROOT / "US_TURTLE_ISLAND_NATIVES"
if ti.exists():
    for gitdir in ti.rglob(".git"):
        if gitdir.is_dir():
            dirs.append((gitdir.parent, "TURTLE_ISLAND"))
p = ROOT / "US_AFRICAN_AMERICAN_REPARATIONS"
if p.exists() and (p / ".git").exists():
    dirs.append((p, "DOMESTIC"))

repos = {}
for d, base in dirs:
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
            label = nice_name(d.name)
            desc = f"Master litigation repository for {label}. Part of the Global Restitution Alliance legal framework."
            repos[name] = desc
    except:
        pass

print(f"FOUND {len(repos)} repos", flush=True)
subprocess.run(
    ["gh", "auth", "switch", "-u", "GlobalRestitutionAlliance"], capture_output=True
)
env = os.environ.copy()
env["GIT_TERMINAL_PROMPT"] = "0"
env.pop("GH_TOKEN", None)
env.pop("GITHUB_TOKEN", None)
ok = fail = 0
for i, (name, desc) in enumerate(sorted(repos.items()), 1):
    full = f"GlobalRestitutionAlliance/{name}"
    p = subprocess.run(
        ["gh", "repo", "edit", full, "--description", desc],
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
    )
    if p.returncode == 0:
        ok += 1
    else:
        fail += 1
    if i % 100 == 0:
        print(f"PROGRESS {i}/{len(repos)} ok={ok} fail={fail}", flush=True)
print(f"DONE ok={ok} fail={fail}", flush=True)
subprocess.run(["gh", "auth", "switch", "-u", "R03LV1S"], capture_output=True)
