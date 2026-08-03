import base64
import os
import requests


def get_image_data_uri(source):
  """Converte uma URL ou um arquivo local em Data URI Base64 seguro para o GitHub."""
  try:
    if os.path.exists(source):
      mime = "image/png" if source.endswith(".png") else "image/svg+xml"
      with open(source, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64,{b64}"

    elif source.startswith("http"):
      res = requests.get(source, timeout=5)
      if res.status_code == 200:
        content_type = res.headers.get("Content-Type", "")
        mime = (
            "image/svg+xml"
            if "svg" in content_type or source.endswith(".svg")
            else "image/png"
        )
        b64 = base64.b64encode(res.content).decode("utf-8")
        return f"data:{mime};base64,{b64}"
  except Exception as e:
    print(f"Aviso: Não foi possível carregar a imagem '{source}': {e}")

  return None


def generate_inventory_svg():
  width = 750
  height = 420

  LOGOS_SOURCES = {
      "Laravel": (
          "https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Laravel-Dark.svg"
      ),
      "PHP": (
          "https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/PHP-Dark.svg"
      ),
      "React": (
          "https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/React-Dark.svg"
      ),
      "Tailwind": (
          "https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/TailwindCSS-Dark.svg"
      ),
      "Python": (
          "https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Python-Dark.svg"
      ),
      "Steam": (
          "https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Steam-Dark.svg"
      ),
      "YOLO": "assets/yolo.png",
      "RPG": "assets/rpg.png",
  }

  LOGOS_DATA = {}
  for name, source in LOGOS_SOURCES.items():
    data_uri = get_image_data_uri(source)
    if data_uri:
      LOGOS_DATA[name] = data_uri

  items = [
      {
          "slot": "⚔️ MAIN HAND",
          "name": "Laravel & PHP",
          "logos": ["Laravel", "PHP"],
          "rarity": "LENDÁRIO",
          "rarity_color": "#ff79c6",
          "stats": "+100 Back-end, +85 Vel. Dev",
      },
      {
          "slot": "🛡️ OFF HAND",
          "name": "React & Tailwind",
          "logos": ["React", "Tailwind"],
          "rarity": "RARO",
          "rarity_color": "#8be9fd",
          "stats": "+90 Estilização, +80 Reatividade",
      },
      {
          "slot": "🔮 SPELLBOOK",
          "name": "YOLO & Visão Computacional",
          "logos": ["Python", "YOLO"],
          "rarity": "ÉPICO",
          "rarity_color": "#bd93f9",
          "stats": "Detecção de Objetos & CNNs em vídeo",
      },
      {
          "slot": "🧪 POTION",
          "name": "Elixir do Desenvolvedor",
          "logos": ["PHP", "Python"],
          "rarity": "CONSUMÍVEL",
          "rarity_color": "#50fa7b",
          "stats": "Transforma Café em Código Funcional",
      },
      {
          "slot": "📜 MAIN QUEST",
          "name": "TCC & Inovação",
          "logos": ["Laravel", "Python"],
          "rarity": "EM ANDAMENTO",
          "rarity_color": "#ffb86c",
          "stats": "IA Aplicada & Sistemas Full-Stack",
      },
  ]

  svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <style>
        .header-title {{ font-family: 'Courier New', monospace; font-weight: bold; fill: #ff79c6; font-size: 16px; letter-spacing: 1px; }}
        .slot-title {{ font-family: 'Courier New', monospace; font-weight: bold; fill: #f8f8f2; font-size: 12px; }}
        .item-name {{ font-family: 'Courier New', monospace; font-weight: bold; fill: #f1fa8c; font-size: 13px; }}
        .item-stats {{ font-family: 'Courier New', monospace; fill: #6272a4; font-size: 11px; }}
        .rarity-tag {{ font-family: 'Courier New', monospace; font-weight: bold; font-size: 10px; }}
        .card-bg {{ fill: #161b22; stroke: #30363d; stroke-width: 2; rx: 6px; }}
    </style>

    <rect width="{width}" height="{height}" fill="#0d1117" rx="10" stroke="#44475a" stroke-width="2"/>
    
    <text x="25" y="35" class="header-title">🎒 INVENTÁRIO DO AVENTUREIRO (EQUIPAMENTOS & SKILLS)</text>
    <line x1="25" y1="48" x2="725" y2="48" stroke="#44475a" stroke-width="1" stroke-dasharray="4 4"/>
    """

  for i, item in enumerate(items):
    col = i % 2
    row = i // 2

    x = 25 + (col * 355)
    y = 65 + (row * 110)

    svg += f"""
        <g transform="translate({x}, {y})">
            <rect x="0" y="0" width="345" height="98" class="card-bg"/>
            
            <rect x="0" y="0" width="5" height="98" fill="{item['rarity_color']}" rx="2"/>

            <text x="18" y="24" class="slot-title">{item['slot']}</text>
            <rect x="235" y="12" width="95" height="16" fill="#21262d" rx="4"/>
            <text x="282" y="24" class="rarity-tag" fill="{item['rarity_color']}" text-anchor="middle">{item['rarity']}</text>

            <text x="18" y="48" class="item-name">{item['name']}</text>

            <text x="18" y="70" class="item-stats">⚡ {item['stats']}</text>

            """

    logo_x = 315
    logo_y = 65
    logo_size = 22
    logo_spacing = 6

    for logo_name in item["logos"]:
      if logo_name in LOGOS_DATA:
        img_data_uri = LOGOS_DATA[logo_name]
        svg += f"""
            <image href="{img_data_uri}" x="{logo_x - logo_size}" y="{logo_y - logo_size/2}" width="{logo_size}" height="{logo_size}" preserveAspectRatio="xMidYMid meet" />
                """
        logo_x -= logo_size + logo_spacing

    svg += """
        </g>
        """

  svg += "</svg>"

  with open("inventory.svg", "w", encoding="utf-8") as f:
    f.write(svg)


if __name__ == "__main__":
  generate_inventory_svg()
