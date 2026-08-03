import os
import requests

USERNAME = os.environ.get("GH_USERNAME")
TOKEN = os.environ.get("GH_TOKEN")

COLOR_MAP = {
    "PHP": "#777BB4",
    "Laravel": "#FF2D20",
    "JavaScript": "#F7DF1E",
    "TypeScript": "#3178C6",
    "Python": "#3776AB",
    "C++": "#00599C",
    "HTML": "#E34F26",
    "CSS": "#1572B6",
    "Blade": "#F7523F"
}
DEFAULT_COLOR = "#6E7681"

def fetch_top_languages():
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    query = """
    query {
      user(login: "%s") {
        repositories(first: 100, isFork: false, ownerAffiliations: OWNER) {
          nodes {
            languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
              edges {
                size
                node { name }
              }
            }
          }
        }
      }
    }
    """ % USERNAME

    res = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)
    data = res.json()
    
    lang_sizes = {}
    repos = data.get("data", {}).get("user", {}).get("repositories", {}).get("nodes", [])
    for repo in repos:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            size = edge["size"]
            lang_sizes[name] = lang_sizes.get(name, 0) + size
            
    sorted_langs = sorted(lang_sizes.items(), key=lambda x: x[1], reverse=True)[:5]
    return [lang[0] for lang in sorted_langs]

def build_vhs_svg(languages):
    width = 600
    height = 200
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
    <style>
        .title {{ font-family: 'Courier New', monospace; font-weight: bold; fill: #f0f6fc; font-size: 14px; }}
        .vhs-label {{ font-family: 'Courier New', monospace; font-weight: bold; font-size: 11px; fill: #111; }}
        .shelf-wood {{ fill: #3d2314; stroke: #24140a; stroke-width: 3; }}
    </style>
    
    <rect width="{width}" height="{height}" fill="#0d1117" rx="8"/>
    
    <text x="20" y="30" class="title" fill="#ff79c6">📼 LOCADORA DEV - SELEÇÃO DO MÊS</text>
    
    <rect x="20" y="150" width="560" height="15" rx="2" class="shelf-wood"/>
    <rect x="20" y="165" width="560" height="8" fill="#1b0f08"/>
    '''

    start_x = 40
    for i, lang in enumerate(languages):
        x = start_x + (i * 100)
        y = 65
        color = COLOR_MAP.get(lang, DEFAULT_COLOR)
        
        svg += f'''
        <g transform="translate({x}, {y})">
            <rect x="0" y="0" width="80" height="85" rx="3" fill="#161b22" stroke="#30363d" stroke-width="2"/>
            <rect x="5" y="5" width="70" height="75" rx="2" fill="{color}"/>
            
            <rect x="10" y="15" width="60" height="55" rx="1" fill="#f0f6fc"/>
            <line x1="10" y1="25" x2="70" y2="25" stroke="{color}" stroke-width="2"/>
            
            <text x="40" y="45" text-anchor="middle" class="vhs-label">{lang[:8]}</text>
            <text x="40" y="60" text-anchor="middle" font-family="monospace" font-size="8" fill="#555">VHS-NTSC</text>
            
            <rect x="15" y="72" width="50" height="4" fill="#0d1117"/>
        </g>
        '''

    svg += "</svg>"
    
    with open("shelf.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    langs = fetch_top_languages()
    if not langs:
        langs = ["PHP", "JavaScript", "Python", "HTML", "CSS"] 
    build_vhs_svg(langs)