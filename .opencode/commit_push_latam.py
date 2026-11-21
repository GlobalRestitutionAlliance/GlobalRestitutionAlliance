import subprocess, os, sys
from pathlib import Path
from bolster_latam_deep import ROOT, PROFILES

results = []
for name, prof in PROFILES.items():
    if name == "US_CU_CUBA":
        continue
    cdir = ROOT / name
    if not (cdir / ".git").exists():
        results.append((name, "NO_GIT"))
        continue
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"

    def run(args, cwd=cdir):
        return subprocess.run(
            args, cwd=str(cwd), capture_output=True, text=True, env=env, timeout=120
        )

    r = run(["git", "add", "-A"])
    r2 = run(["git", "status", "--short"])
    if not r2.stdout.strip():
        # maybe nothing to commit, check if ahead
        r3 = run(["git", "status", "-sb"])
        results.append(
            (
                name,
                "CLEAN " + r3.stdout.strip().splitlines()[0] if r3.stdout else "CLEAN",
            )
        )
        continue
    r3 = run(
        [
            "git",
            "commit",
            "-m",
            "Bolster campaign to Cuba-template depth: evidence harvest, citations, legal framework, manifests",
        ]
    )
    if r3.returncode != 0:
        results.append((name, "COMMIT_FAIL " + r3.stderr.strip()[-200:]))
        continue
    r4 = run(["git", "push", "origin", "HEAD"])
    if r4.returncode != 0:
        results.append((name, "PUSH_FAIL " + r4.stderr.strip()[-200:]))
        continue
    results.append((name, "PUSHED"))
    print("OK", name)

for n, s in results:
    print(f"{n}: {s}")
print("DONE", len(results))
