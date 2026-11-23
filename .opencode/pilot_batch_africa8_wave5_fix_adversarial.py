import json, csv, datetime, importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "w5", r"W:\Legal\.opencode\pilot_batch_africa8_wave5.py"
)
w5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w5)

BASE = Path(r"W:\Legal\AFRICA")


def ensure_sr_md(repo: Path):
    kb = repo / "00_Master_Knowledge_Base"
    csvp = kb / "SOURCE_REGISTRY.csv"
    mdp = kb / "SOURCE_REGISTRY.md"
    rows = []
    if csvp.exists():
        with csvp.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
    lines = [
        "# Source Registry",
        "",
        "Status: PENDING_LEGAL_REVIEW. Sources are public references for evidence capture; verify before legal reliance. No VERIFIED status without local hashed artifact + human sign-off.",
        "",
        "| source_id | title | url | source_type | access_method | verification_status | notes |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        vals = [
            str(r.get(k, "") or "").replace("|", "\\|").replace("\n", " ")
            for k in [
                "source_id",
                "title",
                "url",
                "source_type",
                "access_method",
                "verification_status",
                "notes",
            ]
        ]
        lines.append("| " + " | ".join(vals) + " |")
    mdp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return mdp.exists(), len(rows)


def fix_valuation(repo: Path):
    ws = repo / "00_Master_Knowledge_Base" / "VALUATION_WORKSHEET.csv"
    if not ws.exists():
        return False, 0
    with ws.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        fields = list(r.fieldnames or [])
        rows = list(r)
    changed = 0
    for row in rows:
        for k in ["low_usd", "base_usd", "high_usd"]:
            v = str(row.get(k, "") or "").strip()
            if v == "":
                row[k] = "TBD"
                changed += 1
        # keep review/valuation pending
        if not str(row.get("review_status", "") or "").strip():
            row["review_status"] = "PENDING_LEGAL_REVIEW"
        if not str(row.get("valuation_status", "") or "").strip():
            row["valuation_status"] = "TBD"
    with ws.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})
    return True, changed


def enhance_citation_index(repo: Path):
    ex = repo / "03_Evidentiary_Exhibits"
    cit_csv = ex / "CITATION_INDEX.csv"
    cit_md = ex / "CITATION_INDEX.md"
    ledger = ex / "Immutable_Ledger"
    if not cit_csv.exists():
        return False
    with cit_csv.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        fields = list(r.fieldnames or [])
        rows = list(r)
    extra = [
        "provenance",
        "http_status",
        "capture_access",
        "substantive",
        "quality_flag",
        "annotation_note",
    ]
    for e in extra:
        if e not in fields:
            fields.append(e)
    # build meta lookup by local_artifact
    meta_by_art = {}
    if ledger.exists():
        for mp in ledger.glob("*.meta.json"):
            try:
                meta = json.loads(mp.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                continue
            art = ledger / mp.name.removesuffix(".meta.json")
            if art.exists():
                rel = art.relative_to(repo).as_posix()
                meta_by_art[rel] = meta
    for row in rows:
        rel = str(row.get("local_artifact", "") or "").replace("\\", "/")
        meta = meta_by_art.get(rel, {})
        if not meta and rel:
            # try basename match
            for k, m in meta_by_art.items():
                if k.endswith("/" + rel.split("/")[-1]):
                    meta = m
                    break
        for e in extra:
            val = meta.get(e, row.get(e, ""))
            if e == "substantive" and isinstance(val, bool):
                val = "true" if val else "false"
            if val is None:
                val = ""
            if str(row.get(e, "") or "") == "" and str(val) != "":
                row[e] = val
            elif str(row.get(e, "") or "") != "":
                pass
            else:
                row[e] = val
    with cit_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})
    # rebuild md
    lines = [
        "# Citation Index",
        "",
        "Rule: NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT. All entries PENDING_LEGAL_REVIEW unless explicitly verified through local hashed artifact + human sign-off.",
        "",
    ]
    for row in rows:
        lines.append(
            f"- {row.get('citation_id', '')}: {row.get('url', '')} | `{row.get('local_artifact', '')}` | `{str(row.get('sha256', ''))[:16]}...` | {row.get('verification_status', '')} | substantive={row.get('substantive', '')} | quality={row.get('quality_flag', '')}"
        )
    cit_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def refresh_manifest(repo: Path):
    if hasattr(w5, "refresh_manifest"):
        try:
            w5.refresh_manifest(repo)
        except Exception as e:
            # fallback: touch manifest timestamp by regenerating if simple
            pass


def main():
    for rp, cfg in w5.REPOS.items():
        repo = Path(rp)
        sr_ok, sr_n = ensure_sr_md(repo)
        val_ok, val_changed = fix_valuation(repo)
        cit_ok = enhance_citation_index(repo)
        refresh_manifest(repo)
        print(
            {
                "repo": repo.name,
                "sr_md": sr_ok,
                "sr_rows": sr_n,
                "valuation_cells_set_tbd": val_changed,
                "citation_enhanced": cit_ok,
            }
        )


if __name__ == "__main__":
    main()
