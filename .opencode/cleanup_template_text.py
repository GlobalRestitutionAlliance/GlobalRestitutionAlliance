import os, subprocess, hashlib, sys
from pathlib import Path

ROOT = Path(r"W:\Legal")
LOG = Path(r"W:\Legal\.opencode\cleanup_template_text.log")

REPLACEMENTS = [
    ("GRA litigation framework", "GRA litigation framework"),
    ("GRA litigation framework", "GRA litigation framework"),
    ("GRA litigation framework", "GRA litigation framework"),
    ("CUBA template framework", "GRA litigation framework"),
]

SKIP_DIRS = {".git", "Immutable_Ledger"}
TEXT_EXTS = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".py",
    ".csv",
    ".html",
    ".xml",
    ".rst",
}


def log(m):
    line = str(m)
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def sha256p(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


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
        for gitdir in ti.rglob(".git"):
            if gitdir.is_dir():
                repos.append(gitdir.parent)
    for n in ["US_AFRICAN_AMERICAN_REPARATIONS"]:
        p = ROOT / n
        if p.exists() and (p / ".git").exists():
            repos.append(p)
    # dedupe
    seen = set()
    out = []
    for r in repos:
        s = str(r).lower()
        if s not in seen:
            seen.add(s)
            out.append(r)
    return sorted(out)


def clean_repo(repo):
    changed = 0
    for p in repo.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(repo).as_posix()
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() not in TEXT_EXTS:
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except:
            continue
        orig = txt
        for a, b in REPLACEMENTS:
            if a in txt:
                txt = txt.replace(a, b)
        if txt != orig:
            p.write_text(txt, encoding="utf-8", newline="\n")
            changed += 1
    # refresh manifest
    manifest = repo / "VERIFICATION_KEYS/sha256_manifest.txt"
    if manifest.parent.exists():
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
        manifest.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return changed


def git_run(repo, args, env, timeout=180):
    return subprocess.run(
        args, cwd=str(repo), capture_output=True, text=True, env=env, timeout=timeout
    )


def main():
    repos = find_repos()
    log(f"FOUND {len(repos)} repos")
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    changed_repos = []
    for i, r in enumerate(repos, 1):
        try:
            c = clean_repo(r)
            if c > 0:
                git_run(r, ["git", "config", "core.autocrlf", "input"], env)
                git_run(r, ["git", "add", "-A"], env)
                st = git_run(r, ["git", "status", "--short"], env)
                if st.stdout.strip():
                    git_run(
                        r,
                        ["git", "commit", "-m", "Clean template boilerplate text"],
                        env,
                    )
                    changed_repos.append(r)
            if i % 50 == 0:
                log(f"CLEAN {i}/{len(repos)} changed_repos={len(changed_repos)}")
        except Exception as e:
            log(f"ERR {r.name}: {e}")
    log(f"CLEAN_DONE changed_repos={len(changed_repos)}")
    # push with GRA (org repos) - GRA owns them
    subprocess.run(
        ["gh", "auth", "switch", "-u", "GlobalRestitutionAlliance"], capture_output=True
    )
    envg = os.environ.copy()
    envg["GIT_TERMINAL_PROMPT"] = "0"
    envg.pop("GH_TOKEN", None)
    envg.pop("GITHUB_TOKEN", None)
    ok = fail = 0
    for i, r in enumerate(changed_repos, 1):
        p = git_run(r, ["git", "push", "origin", "HEAD"], envg, timeout=240)
        if p.returncode == 0:
            ok += 1
        else:
            fail += 1
        if i % 50 == 0:
            log(f"PUSH {i}/{len(changed_repos)} ok={ok} fail={fail}")
    log(f"PUSH_DONE ok={ok} fail={fail}")
    subprocess.run(["gh", "auth", "switch", "-u", "R03LV1S"], capture_output=True)
    log("DONE")


if __name__ == "__main__":
    main()
