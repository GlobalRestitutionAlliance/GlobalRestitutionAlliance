import csv, json, re
from pathlib import Path
from bolster_asia_full import ROOT, PROFILES, TODAY, backup_if_exists, write

DOMAIN_BODY = {
    "ohchr.org": "UN OHCHR",
    "oas.org": "Organization of American States / IACHR",
    "iachr": "IACHR",
    "icj-cij.org": "International Court of Justice",
    "un.org": "United Nations",
    "digitallibrary.un.org": "UN Digital Library",
    "state.gov": "U.S. Department of State",
    "history.state.gov": "U.S. Department of State, Office of the Historian",
    "cia.gov": "U.S. Central Intelligence Agency",
    "archives.gov": "U.S. National Archives (NARA)",
    "loc.gov": "Library of Congress",
    "worldbank.org": "World Bank",
    "undp.org": "UNDP",
    "treaties.un.org": "United Nations Treaty Collection",
    "courtlistener.com": "CourtListener / Free Law Project",
}


def clean(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


def extract_html_metadata(data: bytes, url: str):
    try:
        txt = data.decode("utf-8", errors="ignore")
    except Exception:
        txt = str(data[:10000])
    title = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", txt, re.I | re.S)
    if m:
        title = clean(re.sub("<[^<]+?>", "", m.group(1)))
    # date heuristics
    date = ""
    for pat in [
        r'<meta[^>]+property=["\']article:published_time["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+name=["\'](?:citation_publication_date|DC\.date|dcterms\.date|date|pubdate)["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\'](?:citation_publication_date|DC\.date|dcterms\.date|date)["\']',
        r'<time[^>]+datetime=["\']([^"\']+)["\']',
    ]:
        mm = re.search(pat, txt, re.I)
        if mm:
            date = clean(mm.group(1))[:40]
            break
    # authoring body
    body = ""
    for pat in [
        r'<meta[^>]+name=["\'](?:citation_author|DC\.creator|author)["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\'](?:citation_author|DC\.creator|author)["\']',
    ]:
        mm = re.search(pat, txt, re.I)
        if mm:
            body = clean(mm.group(1))[:200]
            break
    if not body:
        ul = (url or "").lower()
        for k, v in DOMAIN_BODY.items():
            if k in ul:
                body = v
                break
    # excerpt and paragraph ref
    excerpt = ""
    pref = ""
    paras = re.findall(r"<p[^>]*>(.*?)</p>", txt, re.I | re.S)
    for i, p in enumerate(paras):
        t = clean(re.sub("<[^<]+?>", " ", p))
        if len(t) < 40:
            continue
        if re.search(r"cookie|javascript|subscribe|menu|navigation", t, re.I):
            continue
        excerpt = t[:500]
        pref = f"html/p[{i + 1}]"
        break
    return title, date, body, excerpt, pref


def main():
    for name, prof in PROFILES.items():
        if name == "US_CU_CUBA":
            continue
        cdir = ROOT / name
        ledger = cdir / "03_Evidentiary_Exhibits" / "Immutable_Ledger"
        out_csv = cdir / "03_Evidentiary_Exhibits" / "CITATION_INDEX.csv"
        out_md = cdir / "03_Evidentiary_Exhibits" / "CITATION_INDEX.md"
        rows = []
        if ledger.exists():
            for p in sorted(ledger.glob("*.meta.json")):
                try:
                    meta = json.loads(p.read_text(encoding="utf-8"))
                except Exception:
                    continue
                art = Path(p.name.replace(".meta.json", ""))
                artifact_path = None
                for cand in ledger.glob(art.stem + "*"):
                    if cand.name.endswith(".meta.json"):
                        continue
                    artifact_path = cand
                    break
                if not artifact_path or not artifact_path.exists():
                    continue
                sha = meta.get("sha256", "")
                status = "PENDING_LEGAL_REVIEW" if sha else "INVALID_NO_HASH"
                title = clean(meta.get("title", "")).strip('"')
                date = ""
                body = ""
                excerpt = ""
                pref = ""
                if artifact_path.suffix.lower() in [".html", ".htm"]:
                    t, d, b, e, pr = extract_html_metadata(
                        artifact_path.read_bytes(), meta.get("url", "")
                    )
                    title = title or t
                    date, body, excerpt, pref = d, b, e, pr
                if not body:
                    ul = (meta.get("url", "") or "").lower()
                    for k, v in DOMAIN_BODY.items():
                        if k in ul:
                            body = v
                            break
                rows.append(
                    {
                        "citation_id": f"{prof['iso']}-CIT-{len(rows) + 1:04d}",
                        "country": prof["country"],
                        "iso": prof["iso"],
                        "title": title,
                        "date": date,
                        "authoring_body": body,
                        "url": meta.get("url", ""),
                        "final_url": meta.get("final_url", ""),
                        "local_artifact": str(artifact_path.relative_to(cdir)).replace(
                            "\\", "/"
                        ),
                        "sha256": sha,
                        "bytes": meta.get("bytes", ""),
                        "content_type": meta.get("content_type", ""),
                        "captured_at": meta.get("captured_at", ""),
                        "excerpt": excerpt,
                        "page_paragraph_ref": pref,
                        "verification_status": status,
                        "verification_rule": "NO_VERIFIED_WITHOUT_LOCAL_HASHED_ARTIFACT",
                    }
                )
        backup_if_exists(out_csv, cdir)
        cols = [
            "citation_id",
            "country",
            "iso",
            "title",
            "date",
            "authoring_body",
            "url",
            "final_url",
            "local_artifact",
            "sha256",
            "bytes",
            "content_type",
            "captured_at",
            "excerpt",
            "page_paragraph_ref",
            "verification_status",
            "verification_rule",
        ]
        with out_csv.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in rows:
                w.writerow(r)
        md = [
            f"# Citation Index - {prof['country']} ({prof['iso']})",
            "",
            f"Generated: {TODAY}",
            "",
            "**Rule:** No citation marked VERIFIED without local hashed source artifact. All entries default `PENDING_LEGAL_REVIEW`.",
            "",
            "| Citation ID | Title | Date | Author | URL | Local Artifact | SHA-256 | Ref | Status |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
        for r in rows:
            md.append(
                f"| {r['citation_id']} | {clean(r['title'])[:60]} | {r['date']} | {clean(r['authoring_body'])[:30]} | {r['url']} | `{r['local_artifact']}` | `{r['sha256'][:16]}...` | {r['page_paragraph_ref']} | {r['verification_status']} |"
            )
        write(out_md, "\n".join(md) + "\n", cdir)
        print("CIT", name, len(rows))
    print("DONE")


if __name__ == "__main__":
    main()
