# Wave 7 Browser Capture Accounting

- Reported in-session capture count during fallback: 23 captures saved across batches + 2 no-captures recorded.
- Observed browser-rendered outerHTML metas across the 6 Wave 7 repos at reconciliation: 52.
- Reconciliation: all 52 observed browser metas were normalized/checked for required provenance fields (`http_status=unknown_browser_outerhtml_capture`, `provenance=browser-rendered-outerHTML`, `capture_access=PUBLIC_CAPTURE_UNAUTHENTICATED`, `legal_review_status=PENDING_LEGAL_REVIEW`) and quality/substantive flags. Non-substantive/challenge captures remain flagged `substantive=false` with `quality_flag`/`annotation_note`.
- Attribution: per-repo `99_Archives_and_Manifests/WAVE7_BROWSER_CAPTURE_MANIFEST.csv` and central `.opencode/wave7_browser_capture_manifest.csv` list every observed browser capture with repo/path/sha256/fetched_at/url/quality and `wave_attribution`. Current attribution marks captures as `WAVE7_SESSION_CAPTURED_OR_RECONCILED` when git-touched/fetched in Wave 7 reconciliation window; this is an accounting/audit manifest, not a claim of original capture time beyond recorded metadata.
- No-captures (honest): TN UNESCO Slave Route ERR_EMPTY_RESPONSE (-324); ZM UNESCO Slave Route navigation failure. Recorded in `tmp_w7_nocapture.json` and per-repo pending recapture registers.
