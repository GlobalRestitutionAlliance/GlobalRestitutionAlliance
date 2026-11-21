import subprocess, os, json
from bolster_latam_deep import ROOT, PROFILES

env = os.environ.copy()
env["GIT_TERMINAL_PROMPT"] = "0"


def gh(args, timeout=60):
    return subprocess.run(
        ["gh"] + args, capture_output=True, text=True, env=env, timeout=timeout
    )


for name in PROFILES.items() if False else []:
    pass

for name, prof in PROFILES.items():
    if name == "US_CU_CUBA":
        continue
    cdir = ROOT / name
    r = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=str(cdir),
        capture_output=True,
        text=True,
    )
    url = r.stdout.strip()
    repo = (
        url.split("github.com/")[-1].replace(".git", "")
        if "github.com/" in url
        else None
    )
    if not repo:
        print(name, "NO_REPO")
        continue
    # make public
    p = gh(
        [
            "repo",
            "edit",
            repo,
            "--visibility",
            "public",
            "--accept-visibility-change-consequences",
        ]
    )
    vis = "OK" if p.returncode == 0 else "ERR"
    # set branch protection on main
    prot = {
        "required_status_checks": {
            "strict": True,
            "contexts": ["integrity-verification"],
        },
        "enforce_admins": False,
        "required_pull_request_reviews": None,
        "restrictions": None,
    }
    p2 = gh(
        [
            "api",
            "-X",
            "PUT",
            f"repos/{repo}/branches/main/protection",
            "-H",
            "Accept: application/vnd.github+json",
            "--input",
            "-",
        ],
        timeout=60,
    )
    # --input - needs stdin; easier use json
    import tempfile, pathlib

    tf = pathlib.Path(os.environ.get("TEMP", "/tmp")) / "prot.json"
    tf.write_text(json.dumps(prot), encoding="utf-8")
    p2 = subprocess.run(
        [
            "gh",
            "api",
            "-X",
            "PUT",
            f"repos/{repo}/branches/main/protection",
            "-H",
            "Accept: application/vnd.github+json",
            "--input",
            str(tf),
        ],
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
    )
    bp = "OK" if p2.returncode == 0 else p2.stderr.strip()[:120]
    print(f"{name}: vis={vis} protect={bp}")
