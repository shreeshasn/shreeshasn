import os
import re

base = "assets"

dark_palette = [
    "#f5f5f5",  # 1. JavaScript (28.55%) - Brightest White
    "#888888",  # 2. HTML (26.87%) - Mid Slate Grey
    "#e0e0e0",  # 3. TypeScript (18.91%) - Light Silver
    "#707070",  # 4. Python (15.49%) - Muted Dark Grey
    "#cccccc",  # 5. CSS (4.99%) - Soft Silver
    "#585858",  # 6. Java (2.84%) - Medium Charcoal
    "#b4b4b4",  # 7. Rust (1.09%) - Ash Grey
    "#444444",  # 8. Astro (0.52%) - Dark Slate
    "#9c9c9c",  # 9. Jupyter Notebook (0.38%) - Medium Grey
    "#333333",  # 10. PLpgSQL (0.37%) - Deep Grey
]

light_palette = [
    "#0a0a0a",  # 1. JavaScript (28.55%) - Deep Jet Black
    "#606060",  # 2. HTML (26.87%) - Mid Grey (huge contrast with JS)
    "#202020",  # 3. TypeScript (18.91%) - Very Dark Charcoal (huge contrast with HTML)
    "#808080",  # 4. Python (15.49%) - Medium Silver Grey (huge contrast with TS)
    "#383838",  # 5. CSS (4.99%) - Dark Grey
    "#9a9a9a",  # 6. Java (2.84%) - Light Silver
    "#4d4d4d",  # 7. Rust (1.09%) - Medium Slate
    "#b4b4b4",  # 8. Astro (0.52%) - Soft Grey
    "#303030",  # 9. Jupyter Notebook (0.38%) - Charcoal Grey
    "#c8c8c8",  # 10. PLpgSQL (0.37%) - Platinum Silver
]

def update_top_langs(path, palette, bg_fill, border_stroke, header_fill, text_fill, slice_stroke):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        svg = f.read()

    # Update card bg
    svg = re.sub(r'(<rect\s+data-testid="card-bg"[^>]*?fill=")[^"]*(")', rf'\g<1>{bg_fill}\2', svg)
    svg = re.sub(r'(<rect\s+data-testid="card-bg"[^>]*?stroke=")[^"]*(")', rf'\g<1>{border_stroke}\2', svg)

    # Update header fill in style
    svg = re.sub(r'(\.header\s*\{[^}]*?fill:\s*)[^;]+(;)', rf'\g<1>{header_fill}\2', svg)

    # Update stat & lang-name fill in style
    svg = re.sub(r'(\.stat\s*\{[^}]*?fill:\s*)[^;]+(;)', rf'\g<1>{text_fill}\2', svg)
    svg = re.sub(r'(\.lang-name\s*\{[^}]*?fill:\s*)[^;]+(;)', rf'\g<1>{text_fill}\2', svg)

    # Update pie paths with fill and distinct slice boundary stroke
    pie_idx = [0]
    def replace_pie(m):
        idx = pie_idx[0]
        pie_idx[0] += 1
        color = palette[idx] if idx < len(palette) else palette[-1]
        size_attr = m.group(1)
        d_attr = m.group(2)
        return f'<path\n          data-testid="lang-pie"\n          {size_attr}\n          {d_attr}\n          fill="{color}"\n          stroke="{slice_stroke}"\n          stroke-width="2"\n          stroke-linejoin="round"\n        />'

    svg = re.sub(
        r'<path\s+data-testid="lang-pie"\s+(size="[^"]*")\s+(d="[^"]*")\s+fill="[^"]*"(?:\s+stroke="[^"]*"\s+stroke-width="[^"]*"\s+stroke-linejoin="[^"]*")?\s*/>',
        replace_pie,
        svg
    )

    # Update legend circles
    circle_idx = [0]
    def replace_circle(m):
        idx = circle_idx[0]
        circle_idx[0] += 1
        color = palette[idx] if idx < len(palette) else palette[-1]
        return f'<circle cx="5" cy="6" r="5" fill="{color}" />'

    svg = re.sub(r'<circle\s+cx="5"\s+cy="6"\s+r="5"\s+fill="[^"]*"\s*/>', replace_circle, svg)

    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Post-processed top-langs: {path}")

def update_streak_stats(path, bg_fill, border_stroke, num_fill, label_fill, ring_stroke, fire_fill):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        svg = f.read()

    # Ensure 150px height
    svg = re.sub(r'height="\d+"', 'height="150"', svg, count=1)
    svg = re.sub(r'viewBox="0 0 495 \d+"', 'viewBox="0 0 495 150"', svg)
    svg = re.sub(r'<rect x="0.5" y="0.5" rx="4.5" width="494" height="\d+"', '<rect x="0.5" y="0.5" rx="4.5" width="494" height="149"', svg)

    # Styling fills
    svg = re.sub(r'(<rect x="0.5" y="0.5" rx="4.5" width="494" height="149"\s+fill=")[^"]*("\s+stroke=")[^"]*(")', rf'\g<1>{bg_fill}\2{border_stroke}\3', svg)
    svg = re.sub(r'(\.fire\s*\{\s*fill:\s*)[^;]+(;)', rf'\g<1>{fire_fill}\2', svg)

    # Adjust vertical translation
    svg = re.sub(r'<g transform="translate\(50,\s*\d+\)">', '<g transform="translate(50, 38)">', svg)
    svg = re.sub(r'<g transform="translate\(197,\s*\d+\)">', '<g transform="translate(197, 12)">', svg)
    svg = re.sub(r'<g transform="translate\(340,\s*\d+\)">', '<g transform="translate(340, 38)">', svg)

    # Adjust streak circle
    svg = re.sub(r'<circle\s+cx="50"\s+cy="\d+"\s+r="\d+"\s+fill="none"\s+stroke="[^"]*"\s+stroke-width="\d+"', f'<circle cx="50" cy="48" r="32" fill="none" stroke="{ring_stroke}" stroke-width="5"', svg)

    # Adjust text positioning inside middle circle
    svg = re.sub(r'(<text class="stat-number"[^>]*?x="50"\s+y=")\d+(")', r'\g<1>56\2', svg)
    svg = re.sub(r'(<text class="stat-label"[^>]*?x="50"\s+y=")\d+(")', r'\g<1>100\2', svg)
    svg = re.sub(r'(<text class="date-range"[^>]*?x="50"\s+y=")\d+(")', r'\g<1>118\2', svg)

    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Post-processed streak stats: {path}")

# Run postprocessors
update_top_langs(os.path.join(base, "github-top-langs-dark.svg"), dark_palette, "#0a0a0a", "#3a3a3a", "#d4d4d4", "#a0a0a0", "#0a0a0a")
update_top_langs(os.path.join(base, "github-top-langs.svg"), light_palette, "#ffffff", "#d4d4d4", "#0a0a0a", "#2a2a2a", "#ffffff")

update_streak_stats(os.path.join(base, "github-streak-stats-dark.svg"), "#0a0a0a", "#3a3a3a", "#d4d4d4", "#a0a0a0", "#a0a0a0", "#d4d4d4")
update_streak_stats(os.path.join(base, "github-streak-stats.svg"), "#ffffff", "#d4d4d4", "#0a0a0a", "#2a2a2a", "#2a2a2a", "#0a0a0a")
