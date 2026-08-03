import base64
import os
import requests


def get_image_data_uri(source):
  """Converte imagem remota ou local para Data URI Base64 seguro."""
  try:
    if source.startswith("http"):
      res = requests.get(
          source, headers={"User-Agent": "Mozilla/5.0"}, timeout=5
      )
      if res.status_code == 200:
        content_type = res.headers.get("Content-Type", "")
        mime = (
            "image/svg+xml"
            if "svg" in content_type or source.endswith(".svg")
            else "image/png"
        )
        b64 = base64.b64encode(res.content).decode("utf-8")
        return f"data:{mime};base64,{b64}"
    else:
      possible_paths = [
          source,
          os.path.join(os.getcwd(), source),
          os.path.join(os.path.dirname(__file__), source),
      ]
      for p in possible_paths:
        if os.path.exists(p) and os.path.isfile(p):
          mime = "image/png" if p.endswith(".png") else "image/svg+xml"
          with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            return f"data:{mime};base64,{b64}"
  except Exception as e:
    print(f"⚠️ Erro ao carregar imagem {source}: {e}")
  return None


def generate_about_svg():
  width = 750
  height = 380

  topics = [
      {
          "icon": "🎓",
          "title": "Formação",
          "lines": [
              "Análise e Desenvolvimento de Sistemas - FEMA (3º ano / 3)",
              "Bacharelado emPublicidade e Propaganda - FEMA 2019 - 2022",
              "Técnico Administração - ETEC 2015 - 2016",
          ],
      },
      {
          "icon": "🚀",
          "title": "Experiência",
          "lines": [
              "Estagiário no Hub de Inovação FEMA (Sistemas & Mídias)",
              "Roteirista e Editor de Vídeo Freelancer (2022 - 2024)",
              "Estagiário TV FEMA (2019-2022)",
          ],
      },
      {
          "icon": "🔮",
          "title": "Foco Atual (TCC)",
          "lines": ["Treinamento de modelos YOLO e Visão Computacional"],
      },
      {
          "icon": "📋",
          "title": "Metodologias",
          "lines": [
              "Vivência prática com Kanban, Scrum e Engenharia de Requisitos"
          ],
      },
      {
          "icon": "💡",
          "title": "Mindset",
          "lines": [
              "Sempre buscando aprender e explorar novas linguagens e frameworks"
          ],
      },
  ]

SOCIAL_LINKS = {
        "LinkedIn": "https://www.linkedin.com/in/joaovitorfurlancosta/",
        "GitHub": "https://github.com/JoaoFurlanCosta",
        "Gmail": "mailto:joaovitorfurlandacosta@gmail.com",
    }

SOCIAL_SOURCES = {
      "LinkedIn": (
          "https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/LinkedIn.svg"
      ),
      "GitHub": (
          "https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Github-Dark.svg"
      ),
      "Gmail": (
          "https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Gmail-Dark.svg"
      ),
  }

SOCIAL_DATA = {}
for name, src in SOCIAL_SOURCES.items():
    uri = get_image_data_uri(src)
    if uri:
      SOCIAL_DATA[name] = uri

svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <style>
        .title {{ font-family: 'Courier New', monospace; font-weight: bold; fill: #8be9fd; font-size: 16px; letter-spacing: 1px; }}
        .section-sub {{ font-family: 'Courier New', monospace; font-weight: bold; fill: #bd93f9; font-size: 12px; }}
        .topic-title {{ font-family: 'Courier New', monospace; font-weight: bold; fill: #ff79c6; font-size: 13px; }}
        .topic-desc {{ font-family: 'Courier New', monospace; fill: #f8f8f2; font-size: 12px; }}
        .bullet-icon {{ font-size: 14px; }}
    </style>

    <rect width="{width}" height="{height}" fill="#0d1117" rx="10" stroke="#44475a" stroke-width="2"/>
    
    <text x="25" y="35" class="title">👤 SOBRE MIM (CHARACTER PROFILE)</text>
    <line x1="25" y1="48" x2="725" y2="48" stroke="#44475a" stroke-width="1" stroke-dasharray="4 4"/>
    """

current_y = 75

for topic in topics:
    clean_title = topic["title"].replace("&", "&amp;")

    svg += f"""
        <g transform="translate(25, {current_y})">
            <text x="0" y="0" class="bullet-icon">{topic['icon']}</text>
            <text x="28" y="-1" class="topic-title">{clean_title}:</text>
        </g>
        """

    title_width = 35 + (len(clean_title) * 8.5)

    for idx, line in enumerate(topic["lines"]):
      clean_line = line.replace("&", "&amp;")

      if idx == 0:
        svg += f"""
                <text x="{title_width + 25}" y="{current_y - 1}" class="topic-desc">{clean_line}</text>
                """
      else:
        current_y += 22
        svg += f"""
                <text x="60" y="{current_y - 1}" class="topic-desc">▸ {clean_line}</text>
                """

    current_y += 30

footer_y = height - 40
svg += f"""
    <line x1="25" y1="{footer_y - 20}" x2="725" y2="{footer_y - 20}" stroke="#44475a" stroke-width="1" stroke-dasharray="2 2"/>
    <text x="25" y="{footer_y + 12}" class="section-sub">🌐 ONDE ME ENCONTRAR:</text>
  """

social_x = 240
social_y = footer_y - 6
icon_size = 26
spacing = 15

for name, data_uri in SOCIAL_DATA.items():
      url = SOCIAL_LINKS.get(name, "#")
      svg += f"""
        <a href="{url}" target="_blank">
            <image href="{data_uri}" xlink:href="{data_uri}" x="{social_x}" y="{social_y}" width="{icon_size}" height="{icon_size}" />
        </a>
    """
      social_x += icon_size + spacing

svg += "</svg>"

with open("about.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("--- About SVG gerado com sucesso! ---")


if __name__ == "__main__":
  generate_about_svg()