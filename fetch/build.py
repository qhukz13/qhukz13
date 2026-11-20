"""Build the fastfetch-style profile card (fetch-dark.svg, fetch-light.svg).

Runs daily from .github/workflows/fetch.yml. Needs a token in GH_TOKEN;
a personal token counts private commits, the default Actions token does not.
"""
import base64
import datetime as dt
import json
import os
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

USER = "qhukz13"
BIRTH = dt.date(2009, 10, 28)
ROOT = Path(__file__).resolve().parent.parent
ART = (ROOT / "fetch" / "art.txt").read_text().rstrip("\n").split("\n")

ABOUT = [
    ("OS", "Void Linux"),
    ("Uptime", None),  # filled in below
    ("Editor", "Zed, Neovim"),
    ("Shell", "bash"),
    None,
    ("Languages", "Python, TypeScript, C, Rust"),
    ("Stack", "FastAPI, React, Tauri, Ollama"),
    ("Focus", "AI agents, systems programming"),
]
CONTACT = [("Email", "v.onashchuk@gmail.com"), ("GitHub", USER)]

THEMES = {
    "dark": dict(bg="#0d1117", border="#30363d", art="#e6edf3", key="#e6edf3", value="#8b949e", dots="#3d444d", head="#ffffff"),
    "light": dict(bg="#ffffff", border="#d0d7de", art="#1f2328", key="#1f2328", value="#59636e", dots="#c8d1da", head="#000000"),
}


def gql(query, variables=None):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GH_TOKEN']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(data["errors"])
    return data["data"]


def stats():
    base = gql(
        """query($u:String!){user(login:$u){
          followers{totalCount}
          repositories(ownerAffiliations:OWNER, privacy:PUBLIC, first:100){totalCount nodes{stargazerCount}}
          contributionsCollection{contributionYears contributionCalendar{totalContributions}}}}""",
        {"u": USER},
    )["user"]
    commits = total = 0
    for year in base["contributionsCollection"]["contributionYears"]:
        c = gql(
            """query($u:String!,$f:DateTime!,$t:DateTime!){user(login:$u){contributionsCollection(from:$f,to:$t){
              totalCommitContributions restrictedContributionsCount contributionCalendar{totalContributions}}}}""",
            {"u": USER, "f": f"{year}-01-01T00:00:00Z", "t": f"{year}-12-31T23:59:59Z"},
        )["user"]["contributionsCollection"]
        commits += c["totalCommitContributions"]
        total += c["contributionCalendar"]["totalContributions"]
    return {
        "Repos": str(base["repositories"]["totalCount"]),
        "Stars": str(sum(n["stargazerCount"] for n in base["repositories"]["nodes"])),
        "Followers": str(base["followers"]["totalCount"]),
        "Commits": f"{commits:,}",
        "Contributions": f"{base['contributionsCollection']['contributionCalendar']['totalContributions']:,} past year",
        "All time": f"{total:,}",
    }


def uptime(today):
    y, m, d = today.year - BIRTH.year, today.month - BIRTH.month, today.day - BIRTH.day
    if d < 0:
        m -= 1
        prev = today.replace(day=1) - dt.timedelta(days=1)
        d += prev.day
    if m < 0:
        y -= 1
        m += 12
    s = lambda n, w: f"{n} {w}{'' if n == 1 else 's'}"
    return f"{s(y, 'year')}, {s(m, 'month')}, {s(d, 'day')}"


# ---- layout -------------------------------------------------------------
W = 985
PAD = 40
ART_FS, ART_LH = 10, 11
ART_W = W - 2 * PAD - 40          # art drawn into a fixed width, any font
FS, LH = 14, 21
CW = FS * 0.6                     # nominal monospace advance
COLW = 420                        # width of one info column in px
COL_X = (PAD, W - PAD - COLW)     # columns line up with the art frame


def fixed(x, y, text, fill, anchor="start", weight=None):
    """Text forced to an exact monospace width, so any fallback font lines up."""
    w = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{x:.1f}" y="{y}" fill="{fill}" text-anchor="{anchor}"{w} textLength="{len(text) * CW:.1f}" '
            f'lengthAdjust="spacingAndGlyphs" xml:space="preserve">{escape(text)}</text>')


def leader(x1, x2, y, c, dotted=True):
    dash = ' stroke-dasharray="0.01 6" stroke-linecap="round" stroke-width="2"' if dotted else ' stroke-width="1"'
    return f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" stroke="{c["dots"]}"{dash}/>'


def row(x, y, key, value, c):
    k_end = x + (len(key) + 1) * CW
    v_start = x + COLW - len(value) * CW
    return "".join((
        fixed(x, y, key + ":", c["key"]),
        leader(k_end + CW, v_start - CW, y - 4, c),
        fixed(x + COLW, y, value, c["value"], anchor="end"),
    ))


def header(x, y, title, c):
    return fixed(x, y, title, c["head"], weight=700) + leader(x + (len(title) + 1) * CW, x + COLW, y - 5, c, dotted=False)


def render(theme, about, gh):
    c = THEMES[theme]
    out = []
    # banner art, framed like the original picture
    fx, fy = PAD, PAD
    fw, fh = W - 2 * PAD, len(ART) * ART_LH + 24
    out.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="{c["art"]}" stroke-width="1.5"/>')
    for i, line in enumerate(ART):
        if not line.strip():
            continue
        n = len(line)
        width = ART_W * n / max(len(l) for l in ART)
        out.append(
            f'<text x="{fx + 20}" y="{fy + 18 + (i + 1) * ART_LH - 3}" font-size="{ART_FS}" fill="{c["art"]}" '
            f'textLength="{width:.1f}" lengthAdjust="spacingAndGlyphs" xml:space="preserve">{escape(line)}</text>'
        )
    cy = fy + fh + 34
    cap = base64.b64encode((ROOT / "fetch" / f"caption-{theme}.png").read_bytes()).decode()
    out.append(f'<image x="{W / 2 - 122}" y="{cy - 22}" width="245" height="30" href="data:image/png;base64,{cap}"/>')

    # info columns
    y0 = cy + 46
    x = COL_X[0]
    out.append(header(x, y0, "qhukz@github", c))
    y = y0
    for item in about:
        y += LH
        if item:
            out.append(row(x, y, *item, c))
    x = COL_X[1]
    out.append(header(x, y0, "GitHub", c))
    y = y0
    for k, v in gh.items():
        y += LH
        out.append(row(x, y, k, v, c))
    y += LH * 2 - LH // 2
    out.append(header(x, y, "Contact", c))
    for k, v in CONTACT:
        y += LH
        out.append(row(x, y, k, v, c))
    height = max(y0 + LH * len(about), y) + PAD

    body = "\n".join(out)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}"
  font-family="ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace" font-size="{FS}">
<rect x="0.5" y="0.5" width="{W - 1}" height="{height - 1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>
{body}
</svg>
'''


def main():
    gh = stats()
    about = [None if i is None else (i[0], i[1] or uptime(dt.date.today())) for i in ABOUT]
    for theme in THEMES:
        (ROOT / f"fetch-{theme}.svg").write_text(render(theme, about, gh))


if __name__ == "__main__":
    main()
