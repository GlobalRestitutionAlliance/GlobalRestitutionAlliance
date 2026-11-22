from pathlib import Path

readme = Path(r"W:\Legal\README.md")
section = Path(r"W:\Legal\.opencode\turtle_section.md").read_text(encoding="utf-8")
txt = readme.read_text(encoding="utf-8")
start = "### Turtle Island (Indigenous Nations) — 597 Repositories (12 BIA Regions)"
end = "###  **Africa**  54 Sovereign Jurisdictions"
si = txt.index(start)
ei = txt.index(end)
# keep the --- separator before Africa; section should end with blank line
new = txt[:si] + section.rstrip() + "\n\n---\n\n" + txt[ei:]
readme.write_text(new, encoding="utf-8", newline="\n")
print("ok")
