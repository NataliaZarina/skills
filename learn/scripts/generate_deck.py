#!/usr/bin/env python3
"""
Generate a reveal.js HTML slide deck from JSON input.

Usage:
    echo '<json>' | python3 generate_deck.py --title "Title" --slug "slug" --repo-path /path/to/repo

Reads slide data JSON from stdin, writes a self-contained HTML file to:
    <repo-path>/decks/<slug>.html

Supports rich slide types including narrative text, embedded visuals,
comparison tables, images, and the standard constraint/tradeoff/insight types.
"""

import argparse
import json
import sys
import os
from html import escape


def render_slide(slide):
    """Render a single slide dict to reveal.js HTML."""
    t = slide.get("type", "content")

    if t == "section-title":
        return f"""<section data-background-color="#0d1117">
    <p style="color:#7c8cf5;font-size:0.7em;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.8em">{escape(slide.get('section_label', ''))}</p>
    <h2 style="font-size:1.8em;line-height:1.3">{escape(slide['title'])}</h2>
    <p style="color:#8b949e;font-size:0.85em;margin-top:1em;font-style:italic">"{escape(slide.get('subtitle', ''))}"</p>
</section>"""

    if t == "constraint":
        detail = ""
        if slide.get("detail"):
            detail = f'\n    <p class="fragment" style="color:#c9d1d9;font-size:0.8em;margin-top:1em;line-height:1.6">{escape(slide["detail"])}</p>'
        return f"""<section>
    <p style="color:#ff6b6b;font-size:0.7em;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.5em">The Constraint</p>
    <h2 style="font-size:1.4em;line-height:1.3">{escape(slide['title'])}</h2>
    <p style="font-size:0.95em;margin-top:1em;line-height:1.7;color:#e6edf3">{escape(slide['body'])}</p>{detail}
</section>"""

    if t == "tradeoff":
        return f"""<section>
    <h3 style="font-size:1.1em;margin-bottom:1.2em">{escape(slide['title'])}</h3>
    <div style="display:flex;gap:1.5em;text-align:center">
        <div style="flex:1;background:rgba(76,175,80,0.12);padding:1.2em;border-radius:12px;border:1px solid rgba(76,175,80,0.3)">
            <div style="color:#4caf50;font-size:0.7em;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.6em">Optimized For</div>
            <div style="font-size:0.95em;line-height:1.5;color:#e6edf3">{escape(slide['optimized'])}</div>
        </div>
        <div style="flex:1;background:rgba(255,107,107,0.12);padding:1.2em;border-radius:12px;border:1px solid rgba(255,107,107,0.3)">
            <div style="color:#ff6b6b;font-size:0.7em;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.6em">Sacrificed</div>
            <div style="font-size:0.95em;line-height:1.5;color:#e6edf3">{escape(slide['sacrificed'])}</div>
        </div>
    </div>
    <p class="fragment" style="color:#8b949e;font-size:0.8em;margin-top:1.2em;line-height:1.5">{escape(slide.get('why', ''))}</p>
</section>"""

    if t == "insight":
        impl = ""
        if slide.get("implication"):
            impl = f'\n    <p class="fragment" style="color:#8b949e;font-size:0.75em;margin-top:1.5em;line-height:1.5">{escape(slide["implication"])}</p>'
        return f"""<section data-background-color="#1a1a2e">
    <p style="color:#ffd93d;font-size:0.7em;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.8em">Key Insight</p>
    <p style="font-size:1.2em;font-weight:500;line-height:1.6;color:#e6edf3">{escape(slide['body'])}</p>{impl}
</section>"""

    if t == "narrative":
        # Longer prose slide for essay-style content
        text = slide.get("body", "")
        # Support multiple paragraphs separated by \n\n
        paragraphs = text.split("\\n\\n") if "\\n\\n" in text else [text]
        paras_html = "".join(f'<p style="font-size:0.82em;line-height:1.7;color:#c9d1d9;margin-bottom:0.8em;text-align:left">{escape(p.strip())}</p>' for p in paragraphs if p.strip())
        title_html = f'<h3 style="font-size:1.1em;margin-bottom:1em;text-align:left">{escape(slide["title"])}</h3>' if slide.get("title") else ""
        return f"""<section>
    {title_html}
    {paras_html}
</section>"""

    if t == "analogy":
        return f"""<section data-background-color="#161b22">
    <p style="color:#58a6ff;font-size:0.7em;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.8em">Analogy</p>
    <p style="font-size:1.05em;line-height:1.7;color:#e6edf3">{escape(slide['body'])}</p>
    <p class="fragment" style="color:#8b949e;font-size:0.8em;margin-top:1.2em;font-style:italic">{escape(slide.get('connection', ''))}</p>
</section>"""

    if t == "example":
        return f"""<section>
    <p style="color:#58a6ff;font-size:0.7em;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.5em">Real-World Example</p>
    <h3 style="font-size:1.1em;margin-bottom:0.8em">{escape(slide.get('title', ''))}</h3>
    <p style="font-size:0.9em;line-height:1.7;color:#c9d1d9">{escape(slide['body'])}</p>
</section>"""

    if t == "comparison":
        # Table comparison (e.g., CPU vs GPU vs TPU)
        headers = slide.get("headers", [])
        rows = slide.get("rows", [])
        header_html = "".join(f'<th style="padding:0.6em 0.8em;border-bottom:2px solid #30363d;color:#58a6ff;font-size:0.8em;text-transform:uppercase;letter-spacing:0.05em">{escape(h)}</th>' for h in headers)
        rows_html = ""
        for row in rows:
            cells = "".join(f'<td style="padding:0.5em 0.8em;border-bottom:1px solid #21262d;font-size:0.82em;color:#c9d1d9">{escape(str(c))}</td>' for c in row)
            rows_html += f"<tr>{cells}</tr>"
        return f"""<section>
    <h3 style="font-size:1.1em;margin-bottom:1em">{escape(slide.get('title', ''))}</h3>
    <table style="width:100%;border-collapse:collapse;margin:0 auto">
        <thead><tr>{header_html}</tr></thead>
        <tbody>{rows_html}</tbody>
    </table>
</section>"""

    if t == "image":
        # Image slide — either a URL or embedded SVG
        caption = f'<p style="color:#8b949e;font-size:0.75em;margin-top:0.8em">{escape(slide.get("caption", ""))}</p>' if slide.get("caption") else ""
        if slide.get("url"):
            return f"""<section>
    <h3 style="font-size:1em;margin-bottom:0.8em">{escape(slide.get('title', ''))}</h3>
    <img src="{escape(slide['url'])}" style="max-height:55vh;max-width:90%;border-radius:8px" alt="{escape(slide.get('alt', ''))}">
    {caption}
</section>"""
        elif slide.get("svg"):
            return f"""<section>
    <h3 style="font-size:1em;margin-bottom:0.8em">{escape(slide.get('title', ''))}</h3>
    <div style="display:flex;justify-content:center">{slide['svg']}</div>
    {caption}
</section>"""
        return ""

    if t == "html":
        # Custom HTML content — for complex visuals, custom layouts
        return f"""<section>
    {slide.get('html_content', '')}
</section>"""

    if t == "definition":
        # Term definition slide
        term = slide.get("term", "")
        definition = slide.get("definition", "")
        context = slide.get("context", "")
        ctx_html = f'<p class="fragment" style="color:#8b949e;font-size:0.8em;margin-top:1em;font-style:italic">{escape(context)}</p>' if context else ""
        return f"""<section>
    <p style="color:#c9a0dc;font-size:0.7em;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.5em">Definition</p>
    <h2 style="font-size:1.4em;color:#c9a0dc">{escape(term)}</h2>
    <p style="font-size:0.95em;margin-top:1em;line-height:1.7;color:#e6edf3">{escape(definition)}</p>
    {ctx_html}
</section>"""

    if t == "bigpicture":
        items = []
        for topic in slide.get("covered", []):
            items.append(f'<li style="color:#4caf50;margin-bottom:0.4em;font-size:0.9em">&#10003; {escape(topic)}</li>')
        if slide.get("current"):
            items.append(f'<li style="color:#ffd93d;margin-bottom:0.4em;font-size:0.9em">&#9654; {escape(slide["current"])}</li>')
        for topic in slide.get("upcoming", []):
            items.append(f'<li style="color:#484f58;margin-bottom:0.4em;font-size:0.9em">{escape(topic)}</li>')
        skipped = ""
        if slide.get("skipped"):
            skipped_items = "".join(f"<li style='font-size:0.8em;color:#484f58;margin-bottom:0.3em'>{escape(s)}</li>" for s in slide["skipped"])
            skipped = f'<div class="fragment" style="margin-top:1em;font-size:0.75em;color:#484f58"><p style="color:#6e7681;margin-bottom:0.3em">Consciously skipping:</p><ul style="list-style:none">{skipped_items}</ul></div>'
        return f"""<section data-background-color="#0d1117">
    <p style="color:#6e7681;font-size:0.7em;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.8em">Where We Are</p>
    <h3 style="font-size:1.1em;margin-bottom:1em">{escape(slide.get('title', 'Curriculum Map'))}</h3>
    <ul style="list-style:none;line-height:1.8">{''.join(items)}</ul>{skipped}
</section>"""

    if t == "summary":
        takeaways = slide.get("takeaways", [])
        items = "".join(f'<li class="fragment" style="margin-bottom:0.6em;font-size:0.9em;color:#e6edf3">{escape(tk)}</li>' for tk in takeaways)
        return f"""<section data-background-color="#1a1a2e">
    <h2 style="font-size:1.3em;margin-bottom:1em">{escape(slide.get('title', 'What You Can Now Reason About'))}</h2>
    <ul style="list-style:none;line-height:1.8">{items}</ul>
</section>"""

    if t == "quote":
        return f"""<section data-background-color="#161b22">
    <blockquote style="border-left:4px solid #ffd93d;padding:0.8em 1.2em;font-size:1.1em;line-height:1.6;color:#e6edf3;font-style:italic">
        {escape(slide['body'])}
    </blockquote>
    <p style="color:#8b949e;font-size:0.8em;margin-top:1em">— {escape(slide.get('attribution', ''))}</p>
</section>"""

    # Default: content slide with bullets
    bullets = slide.get("bullets", [])
    use_fragments = slide.get("fragments", False)
    frag = ' class="fragment"' if use_fragments else ""
    items = "".join(f"<li{frag} style='margin-bottom:0.5em;font-size:0.9em;color:#c9d1d9'>{escape(b)}</li>" for b in bullets)
    return f"""<section>
    <h3 style="font-size:1.1em;margin-bottom:1em">{escape(slide.get('title', ''))}</h3>
    <ul style="list-style:none;line-height:1.8;text-align:left">{items}</ul>
</section>"""


def generate_html(data):
    """Generate complete reveal.js HTML from slide data."""
    title = data.get("title", "Learning Deck")
    subtitle = data.get("subtitle", "")

    all_slides = []

    # Title slide
    all_slides.append(f"""<section data-background-color="#0d1117">
    <h1 style="font-size:2em;line-height:1.3">{escape(title)}</h1>
    <p style="color:#8b949e;font-size:0.9em;margin-top:0.8em">{escape(subtitle)}</p>
    <p style="color:#484f58;font-size:0.7em;margin-top:2em">Swipe to navigate &rarr;</p>
</section>""")

    for section in data.get("sections", []):
        section_slides = section.get("slides", [])
        for slide in section_slides:
            rendered = render_slide(slide)
            if rendered:
                all_slides.append(rendered)

    slides_html = "\n\n".join(all_slides)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/black.css">
    <style>
        :root {{
            --r-background-color: #0d1117;
            --r-main-font: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            --r-heading-font: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            --r-main-color: #e6edf3;
            --r-heading-color: #e6edf3;
            --r-link-color: #58a6ff;
        }}
        .reveal {{ font-family: var(--r-main-font); }}
        .reveal h1, .reveal h2, .reveal h3 {{
            text-transform: none;
            font-weight: 600;
            letter-spacing: -0.02em;
        }}
        .reveal ul {{ list-style: none; text-align: left; }}
        .reveal li::before {{ content: ''; }}
        .reveal p {{ line-height: 1.6; }}
        .reveal .progress {{ height: 3px; color: #7c8cf5; }}
        .reveal .controls {{ color: #484f58; }}
        .reveal blockquote {{ background: transparent; box-shadow: none; }}
        .reveal table {{ font-size: 0.85em; }}
        .reveal section {{ padding: 1.5em; }}

        /* Mobile-optimized */
        @media (max-width: 600px) {{
            .reveal h1 {{ font-size: 1.4em !important; }}
            .reveal h2 {{ font-size: 1.15em !important; }}
            .reveal h3 {{ font-size: 0.95em !important; }}
            .reveal p, .reveal li {{ font-size: 0.82em !important; }}
            .reveal section {{ padding: 1em; }}
        }}
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
{slides_html}
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
    <script>
        Reveal.initialize({{
            hash: true,
            touch: true,
            controls: true,
            controlsLayout: 'edges',
            progress: true,
            center: true,
            transition: 'slide',
            transitionSpeed: 'fast',
            width: '100%',
            height: '100%',
            margin: 0.08,
            embedded: false,
        }});
    </script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate reveal.js deck from JSON")
    parser.add_argument("--title", required=True, help="Deck title")
    parser.add_argument("--slug", required=True, help="URL slug for the deck")
    parser.add_argument("--repo-path", required=True, help="Path to learning-decks repo")
    args = parser.parse_args()

    data = json.load(sys.stdin)
    html = generate_html(data)

    decks_dir = os.path.join(args.repo_path, "decks")
    os.makedirs(decks_dir, exist_ok=True)

    output_path = os.path.join(decks_dir, f"{args.slug}.html")
    with open(output_path, "w") as f:
        f.write(html)

    print(f"Deck generated: {output_path}")
    print(f"Will be live at: https://nataliazarina.github.io/learning-decks/decks/{args.slug}.html")


if __name__ == "__main__":
    main()
