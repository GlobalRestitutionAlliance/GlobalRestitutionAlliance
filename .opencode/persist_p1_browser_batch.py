import json, re, os, hashlib, datetime, sys
from pathlib import Path


def main():
    tool_out = Path(r"C:\Users\User\.local\share\opencode\tool-output")
    files = sorted(tool_out.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)[
        :30
    ]
    needle = sys.argv[1] if len(sys.argv) > 1 else None
    data = None
    src_file = None
    for f in files:
        txt = f.read_text(encoding="utf-8", errors="replace").lstrip()
        if not txt.startswith("["):
            continue
        if needle and needle not in txt:
            continue
        try:
            obj = json.loads(txt)
        except Exception:
            continue
        if (
            isinstance(obj, list)
            and obj
            and isinstance(obj[0], dict)
            and "repo_key" in obj[0]
        ):
            # if needle given, ensure it matches
            if needle and not any(needle in json.dumps(x) for x in obj):
                continue
            data = obj
            src_file = f.name
            break
    if not data:
        print("NO_DATA")
        sys.exit(1)
    base = Path(r"W:\Legal\PACIFIC")
    nc_path = Path(r"W:\Legal\.opencode\tmp_p1_nocapture.json")
    ncs = json.loads(nc_path.read_text(encoding="utf-8")) if nc_path.exists() else []
    saved = 0
    for it in data:
        rk = it.get("repo_key")
        title = it.get("title")
        url = it.get("url")
        cap = it.get("captured")
        err = it.get("error")
        repo = base / rk
        if not repo.exists():
            # try case-insensitive
            dirs = [x for x in os.listdir(base) if x.upper() == rk.upper()]
            repo = base / dirs[0] if dirs else None
        if not repo or not repo.exists():
            print("NO_REPO", rk)
            continue
        led = repo / "03_Evidentiary_Exhibits" / "Immutable_Ledger"
        led.mkdir(parents=True, exist_ok=True)
        # skip if already captured for this url
        exists = False
        for mp in led.glob("*.meta.json"):
            try:
                m = json.loads(mp.read_text(encoding="utf-8", errors="ignore"))
                if m.get("url") == url:
                    exists = True
                    break
            except:
                pass
        if exists:
            print("SKIP_EXISTS", rk, title)
            continue
        if err or not cap or not cap.get("html"):
            if not any(x["url"] == url and x["repo_key"] == rk for x in ncs):
                ncs.append(
                    {
                        "repo_key": rk,
                        "title": title,
                        "url": url,
                        "error": (err or "no html")[:300],
                        "recorded_at": datetime.datetime.utcnow().isoformat() + "Z",
                    }
                )
            print("FAIL", rk, title, (err or "no html")[:120])
            continue
        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", title).strip("_")[:80] or "capture"
        html = cap["html"]
        art = led / f"{safe}_browser.html"
        if art.exists():
            art = (
                led
                / f"{safe}_{hashlib.sha256(url.encode()).hexdigest()[:8]}_browser.html"
            )
        art.write_text(html, encoding="utf-8")
        sha = hashlib.sha256(html.encode("utf-8")).hexdigest()
        lower = html.lower()
        is_challenge = (
            ("just a moment" in lower and "cloudflare" in lower)
            or ("cf-challenge" in lower)
            or (
                "challenge-platform" in lower
                and "enable javascript and cookies" in lower
            )
            or ("awswaf" in lower)
            or (
                "javascript is disabled" in lower
                and "verify that you're not a robot" in lower
            )
            or ("max challenge attempts exceeded" in lower)
        )
        tiny = len(html.encode("utf-8")) < 800
        meta = {
            "url": url,
            "final_url": cap.get("url") or url,
            "title": title,
            "fetched_at": datetime.datetime.utcnow().isoformat() + "Z",
            "http_status": "unknown_browser_outerhtml_capture",
            "content_type": "text/html; browser-rendered-outerHTML",
            "bytes": len(html.encode("utf-8")),
            "sha256": sha,
            "provenance": "browser-rendered-outerHTML",
            "custodian": "OpenCode/browser-fallback",
            "capture_access": "PUBLIC_CAPTURE_UNAUTHENTICATED",
            "legal_review_status": "PENDING_LEGAL_REVIEW",
            "note": "Captured via browser fallback; not authenticated; pending legal review.",
        }
        if is_challenge or tiny:
            meta["substantive"] = False
            meta["quality_flag"] = (
                "NOT_SUBSTANTIVE_CHALLENGE_PENDING_RECAPTURE"
                if is_challenge
                else "NOT_SUBSTANTIVE_EMPTY_PENDING_RECAPTURE"
            )
            meta["annotation_note"] = (
                "Browser capture landed on bot-challenge/AWS WAF/CF interstitial; not substantive evidence. Pending recapture."
                if is_challenge
                else "Capture too small/empty; not substantive evidence. Pending recapture."
            )
        art.with_name(art.name + ".meta.json").write_text(
            json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        saved += 1
        flag = meta.get("quality_flag", "OK")
        print(
            ("CHALLENGE" if is_challenge else ("TINY" if tiny else "OK")),
            rk,
            title,
            len(html),
            flag,
        )
    nc_path.write_text(json.dumps(ncs, ensure_ascii=False, indent=2), encoding="utf-8")
    print("SRC", src_file, "SAVED", saved, "NOCAP", len(ncs))


if __name__ == "__main__":
    main()
