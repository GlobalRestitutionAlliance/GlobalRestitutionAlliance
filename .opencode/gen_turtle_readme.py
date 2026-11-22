from pathlib import Path
import subprocess, re

root = Path(r"W:\Legal\US_TURTLE_ISLAND_NATIVES")
regions = sorted([d for d in root.iterdir() if d.is_dir()])
region_map = {
    "ALASKA": ("Alaska", "AK"),
    "EASTERN": ("Eastern", "Various"),
    "EASTERN_OKLAHOMA": ("Eastern Oklahoma", "OK"),
    "GREAT_PLAINS": ("Great Plains", "Various"),
    "MIDWEST": ("Midwest", "Various"),
    "NAVAJO": ("Navajo", "AZ/NM/UT"),
    "NORTHWEST": ("Northwest", "Various"),
    "PACIFIC": ("Pacific", "Various"),
    "ROCKY_MOUNTAIN": ("Rocky Mountain", "Various"),
    "SOUTHERN_PLAINS": ("Southern Plains", "Various"),
    "SOUTHWEST": ("Southwest", "Various"),
    "WESTERN": ("Western", "Various"),
}


def nice_name(dir_name):
    n = dir_name
    n = re.sub(r"^US_[A-Z]{2}_", "", n)
    n = n.replace("_", " ").strip()
    n = n.title()
    for a, b in [
        (" Of ", " of "),
        (" And ", " and "),
        (" The ", " the "),
        (" At ", " at "),
        (" In ", " in "),
    ]:
        n = n.replace(a, b)
    return n


lines = []
lines.append(
    "### Turtle Island (Indigenous Nations) — 597 Repositories (12 BIA Regions)"
)
lines.append("")
total = 0
for region in regions:
    repos = sorted(
        [d for d in region.iterdir() if d.is_dir() and (d / ".git").exists()]
    )
    total += len(repos)
    title, default_state = region_map.get(
        region.name, (region.name.replace("_", " ").title(), "Various")
    )
    lines.append(f"#### {title} ({len(repos)})")
    lines.append("<details>")
    lines.append(
        f"<summary><strong>View All {len(repos)} {title} Repositories</strong></summary>"
    )
    lines.append("")
    lines.append("| Tribe | Region | Repository | Pool | Key Issues |")
    lines.append("|-------|--------|------------|------|------------|")
    for r in repos:
        try:
            res = subprocess.run(
                ["git", "-C", str(r), "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            url = res.stdout.strip()
            repo_name = url.rstrip("/").split("/")[-1].replace(".git", "")
        except Exception:
            repo_name = r.name
        tribe = nice_name(r.name)
        lines.append(
            f"| {tribe} | {title} | `{repo_name}` | TBD (valuation pending) | Pending verified research; treaty/land/resource claims (verification required) |"
        )
    lines.append("")
    lines.append("</details>")
    lines.append("")
print(f"TOTAL={total}")
Path(r"W:\Legal\.opencode\turtle_section.md").write_text(
    "\n".join(lines), encoding="utf-8", newline="\n"
)
print("wrote")
