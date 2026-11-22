import json, re, hashlib, datetime, sys, argparse
from pathlib import Path

WORKSPACE = Path(r"W:\Legal").resolve()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def safe_slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_")[:80] or "capture"


def sanitize_md(s: str) -> str:
    return (
        str(s or "").replace("|", "\\|").replace("\n", " ").replace("\r", " ").strip()
    )


def load_items(path: Path):
    txt = path.read_text(encoding="utf-8", errors="replace")
    try:
        data = json.loads(txt)
    except Exception:
        m = re.search(r"\[[\s\S]*\]", txt)
        if not m:
            raise ValueError(f"no JSON array found in {path}")
        data = json.loads(m.group(0))
    if not isinstance(data, list):
        raise ValueError("expected JSON array")
    return data


def resolve_repo(repo_str: str) -> Path:
    repo = Path(repo_str).resolve()
    try:
        repo.relative_to(WORKSPACE)
    except Exception as e:
        raise ValueError(f"repo outside workspace: {repo}") from e
    return repo


def main():
    ap = argparse.ArgumentParser(
        description="Save browser capture artifacts with provenance."
    )
    ap.add_argument("input", help="JSON file containing capture items")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    items = load_items(Path(args.input))
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    saved = 0
    for item in items:
        repo = resolve_repo(item["repo"])
        cap = item.get("captured")
        err = item.get("error")
        if not cap or err:
            print("skip", item.get("source_url"), err)
            continue
        if isinstance(cap, str):
            try:
                cap = json.loads(cap)
            except Exception:
                cap = {
                    "html": cap,
                    "title": item.get("source_title", ""),
                    "url": item.get("source_url", ""),
                }
        if not isinstance(cap, dict):
            print("skip", item.get("source_url"), "invalid capture")
            continue
        html = cap.get("html", "")
        if not isinstance(html, str) or not html.strip():
            print("skip", item.get("source_url"), "empty html")
            continue
        url = item.get("source_url") or cap.get("url") or ""
        title = item.get("source_title") or cap.get("title") or "capture"
        final_url = cap.get("url") or url
        http_status = cap.get(
            "http_status", cap.get("status", "unknown_browser_outerhtml_capture")
        )
        slug = safe_slug(title)[:60]
        existing = (
            sorted(
                (repo / "03_Evidentiary_Exhibits/Immutable_Ledger").glob(
                    f"*{slug}*_browser.html"
                )
            )
            if (repo / "03_Evidentiary_Exhibits/Immutable_Ledger").exists()
            else []
        )
        artifact = (
            existing[0]
            if existing
            else (
                repo
                / "03_Evidentiary_Exhibits/Immutable_Ledger"
                / f"{slug}_browser.html"
            )
        )
        meta_path = Path(str(artifact) + ".meta.json")
        html_bytes = html.encode("utf-8", errors="replace")
        sha = sha256_bytes(html_bytes)
        meta = {
            "url": url,
            "final_url": final_url,
            "title": title,
            "fetched_at": ts,
            "http_status": http_status,
            "status_note": "Browser outerHTML capture; HTTP status may be unknown unless explicitly provided by capture tooling. Do not treat as authenticated or verified.",
            "content_type": "text/html; browser-rendered",
            "bytes": len(html_bytes),
            "sha256": sha,
            "provenance": "browser-rendered-outerHTML",
            "custodian": "OpenCode/browser-fallback",
            "legal_review_status": "PENDING_LEGAL_REVIEW",
            "capture_method": "opencode-browse-extension+eval.outerHTML",
        }
        print(
            ("DRYRUN" if args.dry_run else "SAVE"),
            artifact.name,
            sha[:12],
            "http_status=" + str(http_status),
        )
        if args.dry_run:
            continue
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(html, encoding="utf-8", errors="replace")
        meta_path.write_text(
            json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        saved += 1
        # append intake log row if missing
        logp = repo / "03_Evidentiary_Exhibits/EVIDENCE_INTAKE_LOG.md"
        if logp.exists():
            logtxt = logp.read_text(encoding="utf-8", errors="ignore")
            if sha not in logtxt and artifact.name not in logtxt:
                row = f"| {datetime.date.today().isoformat()} | {sanitize_md(artifact.name)} | {sanitize_md(url)} | OpenCode/browser-fallback | {sha} | PUBLIC_CAPTURE_UNAUTHENTICATED | browser-fallback http_status={sanitize_md(http_status)} bytes={len(html_bytes)} final_url={sanitize_md(final_url)} |"
                marker = "## Intake Rules"
                if marker in logtxt:
                    logtxt = logtxt.replace(marker, row + "\n\n" + marker, 1)
                else:
                    logtxt = logtxt.rstrip() + "\n" + row + "\n"
                logp.write_text(logtxt, encoding="utf-8", newline="\n")
    print(f"saved={saved}")


if __name__ == "__main__":
    main()
