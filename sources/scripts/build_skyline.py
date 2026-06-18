import subprocess, datetime

def commits_per_day():
    counts = []
    for i in range(7):
        day = datetime.date.today() - datetime.timedelta(days=i)
        since = day.strftime("%Y-%m-%d 00:00")
        until = day.strftime("%Y-%m-%d 23:59")
        out = subprocess.run(
            ["git", "log", f"--since={since}", f"--until={until}", "--oneline"],
            capture_output=True, text=True
        )
        counts.append(len(out.stdout.strip().splitlines()))
    return list(reversed(counts))

def build_svg(counts):
    max_h = 180
    bars = ""
    for i, c in enumerate(counts):
        h = min(max_h, 20 + c * 25)
        x = 40 + i * 80
        y = 200 - h
        bars += f'<rect x="{x}" y="{y}" width="60" height="{h}" fill="#415a77"/>'
    return f'''<svg width="640" height="240" xmlns="http://www.w3.org/2000/svg">
        <rect width="640" height="200" fill="#0d1b2a"/>
        {bars}
    </svg>'''

if __name__ == "__main__":
    svg = build_svg(commits_per_day())
    with open("assets/skyline.svg", "w") as f:
        f.write(svg)
