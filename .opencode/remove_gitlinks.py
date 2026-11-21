import subprocess, sys

# get gitlinks
r = subprocess.run(
    ["git", "ls-files", "--stage"], capture_output=True, text=True, cwd=r"W:\Legal"
)
links = []
for line in r.stdout.splitlines():
    if line.startswith("160000"):
        parts = line.split("\t", 1)
        if len(parts) == 2:
            links.append(parts[1])
print("FOUND", len(links))
# batch remove
for i in range(0, len(links), 50):
    batch = links[i : i + 50]
    subprocess.run(
        ["git", "rm", "--cached", "--"] + batch,
        cwd=r"W:\Legal",
        capture_output=True,
        text=True,
    )
r2 = subprocess.run(
    ["git", "ls-files", "--stage"], capture_output=True, text=True, cwd=r"W:\Legal"
)
left = sum(1 for l in r2.stdout.splitlines() if l.startswith("160000"))
print("LEFT", left)
