import csv, hashlib, json, datetime, argparse, shutil
from pathlib import Path

TODAY = datetime.date.today().isoformat()
DEFAULT_REPOS = [
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS",
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-gb-reparations-master-litigation",
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-pt-reparations-master-litigation",
    r"W:\Legal\US_AFRICAN_AMERICAN_REPARATIONS\african-american-nl-reparations-master-litigation",
    r"W:\Legal\US_DOMESTIC_VICTIMS\US_DW_NUCLEAR_DOWNWINDERS",
    r"W:\Legal\PACIFIC\US_MH_MARSHALL_ISLANDS",
    r"W:\Legal\US_DOMESTIC_VICTIMS\US_JA_JAPANESE_AMERICAN_INTERNEES",
    r"W:\Legal\US_TURTLE_ISLAND_NATIVES\NAVAJO\US_AZ_NAVAJO_NATION_ARIZONA_NEW_MEXICO_UTAH",
]

REQUIRED = [
    "citation_id",
    "url",
    "local_artifact",
    "sha256",
    "verification_status",
    "verification_rule",
]


def sha256p(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def sanitize_md(s: str) -> str:
    return (
        str(s or "").replace("|", "\\|").replace("\n", " ").replace("\r", " ").strip()
    )


def load_existing_index(csv_path: Path):
    if not csv_path.exists():
        return [], []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        fields = list(r.fieldnames or [])
        rows = list(r)
    return fields, rows


def next_cit_id(existing_ids):
    n = 0
    for cid in existing_ids:
        try:
            n = max(n, int(str(cid).split("-")[-1]))
        except Exception:
            pass
    return n + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repos", nargs="*")
    args = ap.parse_args()
    repos = args.repos or DEFAULT_REPOS

    for path in repos:
        repo = Path(path)
        ex = repo / "03_Evidentiary_Exhibits"
        ledger = ex / "Immutable_Ledger"
        if not ledger.exists():
            print("MISS", repo.name)
            continue

        # intake log: append only new browser-capture rows
        logp = ex / "EVIDENCE_INTAKE_LOG.md"
        logtxt = (
            logp.read_text(encoding="utf-8", errors="ignore")
            if logp.exists()
            else "# Evidence Intake Log\n\n| date | artifact | source_url | custodian | sha256 | status | notes |\n|---|---|---|---|---|---|---|\n\n## Intake Rules\n"
        )
        newrows = []
        for mp in sorted(ledger.glob("*.meta.json")):
            try:
                meta = json.loads(mp.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                continue
            art_name = mp.name.removesuffix(".meta.json")
            art = ledger / art_name
            if not art.exists():
                continue
            if meta.get("provenance") != "browser-rendered-outerHTML":
                continue
            sha = sha256p(art)
            meta_sha = meta.get("sha256", "")
            if meta_sha and meta_sha != sha:
                print(
                    f"WARN sha mismatch {repo.name} {art.name} meta={meta_sha[:12]} actual={sha[:12]}"
                )
            if sha in logtxt or art.name in logtxt:
                continue
            url = sanitize_md(meta.get("url", ""))
            cust = sanitize_md(meta.get("custodian", "OpenCode/browser-fallback"))
            http_status = meta.get("http_status", meta.get("status", "unknown"))
            notes = sanitize_md(
                f"browser-fallback http_status={http_status} bytes={meta.get('bytes', '')} final_url={meta.get('final_url', '')}"
            )
            newrows.append(
                f"| {TODAY} | {sanitize_md(art.name)} | {url} | {cust} | {sha} | PUBLIC_CAPTURE_UNAUTHENTICATED | {notes} |"
            )
        if newrows:
            marker = "## Intake Rules"
            block = "\n".join(newrows)
            if marker in logtxt:
                logtxt = logtxt.replace(marker, block + "\n\n" + marker, 1)
            else:
                logtxt = logtxt.rstrip() + "\n" + block + "\n"
            logp.write_text(logtxt, encoding="utf-8", newline="\n")

        # citations: merge/upsert, preserve existing fields/statuses
        cit_csv = ex / "CITATION_INDEX.csv"
        cit_md = ex / "CITATION_INDEX.md"
        old_fields, old_rows = load_existing_index(cit_csv)
        by_art = {}
        for r in old_rows:
            k = str(r.get("local_artifact", "")).replace("\\", "/")
            if k:
                by_art[k] = r
        fields = list(old_fields)
        for req in REQUIRED:
            if req not in fields:
                fields.append(req)
        existing_ids = [r.get("citation_id") for r in old_rows if r.get("citation_id")]
        nid = next_cit_id(existing_ids)
        merged = dict(by_art)  # keyed by local_artifact
        for mp in sorted(ledger.glob("*.meta.json")):
            try:
                meta = json.loads(mp.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                continue
            art_name = mp.name.removesuffix(".meta.json")
            art = ledger / art_name
            if not art.exists():
                continue
            rel = art.relative_to(repo).as_posix()
            sha = sha256p(art)
            meta_sha = meta.get("sha256", "")
            if meta_sha and meta_sha != sha:
                print(f"WARN sha mismatch {repo.name} {art.name}")
            prev = merged.get(rel, {})
            row = dict(prev)
            row["local_artifact"] = rel
            row["url"] = meta.get("url", prev.get("url", ""))
            row["sha256"] = sha
            row["verification_rule"] = (
                prev.get("verification_rule")
                or "NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT"
            )
            # preserve existing verification_status if present; default pending for new
            row["verification_status"] = (
                prev.get("verification_status") or "PENDING_LEGAL_REVIEW"
            )
            if not row.get("citation_id"):
                row["citation_id"] = f"CIT-{nid:04d}"
                nid += 1
            merged[rel] = row
        # stable sort by citation_id then local_artifact
        out_rows = sorted(
            merged.values(),
            key=lambda r: (
                str(r.get("citation_id", "")),
                str(r.get("local_artifact", "")),
            ),
        )
        # backup
        ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        if cit_csv.exists():
            shutil.copy2(cit_csv, cit_csv.with_name(f"CITATION_INDEX.backup-{ts}.csv"))
        if cit_md.exists():
            shutil.copy2(cit_md, cit_md.with_name(f"CITATION_INDEX.backup-{ts}.md"))
        with cit_csv.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            for r in out_rows:
                w.writerow({k: r.get(k, "") for k in fields})
        md_lines = [
            "# Citation Index",
            "",
            "Rule: NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT. All entries PENDING_LEGAL_REVIEW unless explicitly verified through local hashed artifact + human sign-off.",
            "",
        ]
        for r in out_rows:
            md_lines.append(
                f"- {sanitize_md(r.get('citation_id'))}: {sanitize_md(r.get('url'))} | `{sanitize_md(r.get('local_artifact'))}` | `{str(r.get('sha256', ''))[:16]}...` | {sanitize_md(r.get('verification_status'))}"
            )
        cit_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8", newline="\n")

        # manifest
        vk = repo / "VERIFICATION_KEYS"
        vk.mkdir(parents=True, exist_ok=True)
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
            except Exception:
                pass
        (vk / "sha256_manifest.txt").write_text(
            "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
        )
        print(
            f"{repo.name} browser_rows={len(newrows)} cites={len(out_rows)}", flush=True
        )


if __name__ == "__main__":
    main()
