#!/usr/bin/env python3
"""
Script para generar HTML estático independiente de presentaciones
Convierte una presentación del sistema a un archivo HTML completo con Reveal.js
"""

import re
import yaml
import base64
import os
import sys
import json
from pathlib import Path

def parse_yaml_metadata(content):
    """Extrae y parsea los metadatos YAML del contenido markdown"""
    if content.startswith('---'):
        try:
            end_index = content.find('---', 3)
            if end_index != -1:
                yaml_content = content[3:end_index].strip()
                metadata = yaml.safe_load(yaml_content)
                markdown_content = content[end_index + 3:].strip()
                return metadata, markdown_content
        except yaml.YAMLError as e:
            print(f"Error parsing YAML metadata: {e}")
    return {}, content

def extract_slides(content):
    """Extrae las slides individuales del contenido markdown"""
    slides = []
    # Dividir por comentarios SLIDE
    slide_parts = re.split(r'<!-- SLIDE -->', content)

    for part in slide_parts:
        if part.strip():
            slides.append(part.strip())

    return slides

def extract_slide_components(slide_content):
    """Extrae componentes de una slide: contenido, notas, fondo, iframe"""
    # Buscar imagen de fondo
    background_match = re.search(r'<!-- BACKGROUND: ([^\s]+) -->', slide_content)
    background_image = background_match.group(1) if background_match else None

    # Buscar iframe
    iframe_match = re.search(r'<!-- IFRAME: (.+?) -->', slide_content)
    iframe_url = iframe_match.group(1).strip() if iframe_match else None

    # Buscar notas
    notes_match = re.search(r'<!-- NOTES -->([\s\S]*?)(?=<!-- SLIDE -->|$)', slide_content)
    notes = notes_match.group(1).strip() if notes_match else ""

    # Limpiar contenido principal
    main_content = slide_content
    if background_match:
        main_content = main_content.replace(background_match.group(0), "")
    if iframe_match:
        main_content = main_content.replace(iframe_match.group(0), "")
    if notes_match:
        main_content = main_content.split("<!-- NOTES -->")[0]

    main_content = main_content.strip()

    return {
        'content': main_content,
        'notes': notes,
        'background': background_image,
        'iframe': iframe_url
    }

def process_markdown_content(content, presentation_path, embed_images=True):
    """Procesa el contenido markdown a HTML"""
    # Procesar columnas
    content = re.sub(
        r'\$COLUMNS\$(.*?)\$END\$',
        lambda m: process_columns(m.group(1)),
        content,
        flags=re.DOTALL
    )

    # Procesar grids
    content = re.sub(
        r'\$GRID\$(.*?)\$END\$',
        lambda m: process_grid(m.group(1)),
        content,
        flags=re.DOTALL
    )

    # Convertir markdown básico a HTML
    content = convert_basic_markdown(content)

    # Procesar imágenes
    content = process_images(content, presentation_path, embed_images)

    return content

def process_columns(columns_content):
    """Convierte $COL$ en estructura de columnas HTML"""
    cols = re.split(r'\$COL\$', columns_content)
    cols = [col.strip() for col in cols if col.strip()]

    html = '<div class="columns">'
    for col in cols:
        col_html = convert_basic_markdown(col)
        html += f'<div class="column">{col_html}</div>'
    html += '</div>'

    return html

def process_grid(grid_content):
    """Convierte $ROW$ y $CELL$ en estructura de grid HTML"""
    rows = re.split(r'\$ROW\$', grid_content)
    rows = [row.strip() for row in rows if row.strip()]

    html = '<div class="grid">'
    for row in rows:
        cells = re.split(r'\$CELL\$', row)
        cells = [cell.strip() for cell in cells if cell.strip()]

        html += '<div class="grid-row">'
        for cell in cells:
            cell_html = convert_basic_markdown(cell)
            html += f'<div class="grid-cell">{cell_html}</div>'
        html += '</div>'

    html += '</div>'
    return html

def convert_basic_markdown(content):
    """Convierte markdown básico a HTML"""
    # Títulos
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)

    # Negritas
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)

    # Cursivas
    content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)

    # Enlaces
    content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', content)

    # Listas
    content = re.sub(r'^- (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
    content = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', content, flags=re.DOTALL)
    content = re.sub(r'</ul>\s*<ul>', '', content)

    # Párrafos
    lines = content.split('\n')
    processed_lines = []
    in_list = False

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('<h') or line.startswith('<div') or line.startswith('<ul') or line.startswith('</'):
            processed_lines.append(line)
        elif line.startswith('<li>'):
            if not in_list:
                processed_lines.append('<ul>')
                in_list = True
            processed_lines.append(line)
        else:
            if in_list:
                processed_lines.append('</ul>')
                in_list = False
            if line:
                processed_lines.append(f'<p>{line}</p>')

    if in_list:
        processed_lines.append('</ul>')

    return '\n'.join(processed_lines)

def process_images(content, presentation_path, embed_images=True):
    """Procesa las imágenes, convirtiéndolas a base64 o usando enlaces relativos"""
    def replace_image(match):
        alt_text = match.group(1)
        img_path = match.group(2)

        # Construir ruta completa para verificar que existe
        full_path = os.path.join(presentation_path, img_path)

        if os.path.exists(full_path):
            if embed_images:
                # Convertir a base64
                try:
                    with open(full_path, 'rb') as img_file:
                        img_data = img_file.read()
                        img_base64 = base64.b64encode(img_data).decode('utf-8')

                        # Detectar tipo de imagen
                        ext = os.path.splitext(img_path)[1].lower()
                        mime_types = {
                            '.png': 'image/png',
                            '.jpg': 'image/jpeg',
                            '.jpeg': 'image/jpeg',
                            '.webp': 'image/webp',
                            '.gif': 'image/gif'
                        }
                        mime_type = mime_types.get(ext, 'image/png')

                        return f'<img src="data:{mime_type};base64,{img_base64}" alt="{alt_text}">'
                except Exception as e:
                    print(f"Error processing image {img_path}: {e}")
                    return f'<img src="{img_path}" alt="{alt_text}">'
            else:
                # Usar enlace relativo
                return f'<img src="{img_path}" alt="{alt_text}">'
        else:
            print(f"Image not found: {full_path}")
            return f'<img src="{img_path}" alt="{alt_text}">'

    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, content)

def get_background_image_path(img_path, presentation_path, embed_images=True):
    """Obtiene la ruta de imagen de fondo (base64 o relativa)"""
    full_path = os.path.join(presentation_path, img_path)

    if os.path.exists(full_path):
        if embed_images:
            try:
                with open(full_path, 'rb') as img_file:
                    img_data = img_file.read()
                    img_base64 = base64.b64encode(img_data).decode('utf-8')

                    ext = os.path.splitext(img_path)[1].lower()
                    mime_types = {
                        '.png': 'image/png',
                        '.jpg': 'image/jpeg',
                        '.jpeg': 'image/jpeg',
                        '.webp': 'image/webp'
                    }
                    mime_type = mime_types.get(ext, 'image/png')

                    return f'data:{mime_type};base64,{img_base64}'
            except Exception as e:
                print(f"Error processing background image {img_path}: {e}")
                return img_path
        else:
            # Usar enlace relativo
            return img_path
    else:
        print(f"Background image not found: {full_path}")

    return img_path

def generate_css_variables(metadata):
    """Genera variables CSS a partir de los metadatos"""
    css_vars = []

    if 'colors' in metadata:
        colors = metadata['colors']
        css_vars.append(':root {')

        color_mappings = {
            'color': '--color',
            'main-color': '--heading1-color',
            'background': '--background-color',
            'heading-color': '--heading1-color',
            'heading2-color': '--heading2-color',
            'heading3-color': '--heading3-color',
            'accent-color': '--accent-color',
            'text-color': '--text-color',
            'light-gray': '--light-gray',
            'dark-gray': '--dark-gray'
        }

        for color_key, css_var in color_mappings.items():
            if color_key in colors:
                css_vars.append(f'  {css_var}: {colors[color_key]};')

        css_vars.append('}')

    if 'fonts' in metadata:
        fonts = metadata['fonts']
        if 'heading-fontsize' in fonts:
            css_vars.append(f':root {{ --heading-fontsize: {fonts["heading-fontsize"]}; }}')

    if 'fontSize' in metadata:
        css_vars.append(f':root {{ --font-size: {metadata["fontSize"]}; }}')

    return '\n'.join(css_vars)

def generate_standalone_html(presentation_name, output_file=None, embed_images=None):
    """Genera HTML estático independiente de una presentación"""

    # Buscar la carpeta de la presentación
    presentation_path = Path(presentation_name)
    if not presentation_path.exists():
        print(f"Error: Presentation folder '{presentation_name}' not found")
        return False

    # Buscar archivo markdown
    md_files = list(presentation_path.glob("*.md"))
    if not md_files:
        print(f"Error: No markdown files found in '{presentation_name}'")
        return False

    md_file = md_files[0]  # Usar el primer archivo .md encontrado

    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading markdown file: {e}")
        return False

    # Parsear metadatos y contenido
    metadata, markdown_content = parse_yaml_metadata(content)

    # Decidir sobre embebido de imágenes
    if embed_images is None:
        print("\n¿Cómo quieres manejar las imágenes?")
        print("1. Embebidas en HTML (base64) - Archivo 100% autónomo, más pesado")
        print("2. Enlaces relativos - Archivo más liviano, requiere carpeta completa")

        while True:
            choice = input("Elige opción (1 o 2): ").strip()
            if choice == "1":
                embed_images = True
                break
            elif choice == "2":
                embed_images = False
                break
            else:
                print("Por favor, elige 1 o 2")

    # Extraer slides
    slides = extract_slides(markdown_content)

    # Procesar cada slide
    processed_slides = []
    for slide_content in slides:
        slide_data = extract_slide_components(slide_content)

        # Procesar contenido de la slide
        if slide_data['iframe']:
            # Slide con iframe
            slide_html = f'<section class="iframe-slide">'
            slide_html += f'<iframe src="{slide_data["iframe"]}" class="fullscreen-iframe" allowfullscreen></iframe>'
            slide_html += '</section>'
        else:
            # Slide normal
            slide_html = '<section'

            # Añadir imagen de fondo si existe
            if slide_data['background']:
                bg_data = get_background_image_path(slide_data['background'], presentation_path, embed_images)
                slide_html += f' data-background-image="{bg_data}" data-background-size="cover" data-background-position="center"'

            slide_html += '>'

            # Procesar contenido
            content_html = process_markdown_content(slide_data['content'], presentation_path, embed_images)
            slide_html += content_html

            # Añadir notas si existen
            if slide_data['notes']:
                notes_html = convert_basic_markdown(slide_data['notes'])
                slide_html += f'<aside class="notes">{notes_html}</aside>'

            slide_html += '</section>'

        processed_slides.append(slide_html)

    # Generar CSS personalizado
    custom_css = generate_css_variables(metadata)

    # Obtener configuración de Reveal.js
    reveal_config = {
        'hash': True,
        'controls': True,
        'progress': True,
        'center': True,
        'transition': metadata.get('transition', 'slide'),
        'transitionSpeed': metadata.get('transitionSpeed', 'default'),
        'theme': metadata.get('theme', 'white')
    }

    # Mostrar información sobre el tipo de archivo generado
    if embed_images:
        print(f"📦 Generando HTML con imágenes embebidas (archivo autónomo)")
    else:
        print(f"🔗 Generando HTML con enlaces relativos (requiere carpeta completa)")

    # Generar HTML completo
    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{presentation_name}</title>

    <!-- Reveal.js CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/theme/{reveal_config['theme']}.css">

    <!-- Highlight.js para código -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/highlight/monokai.css">

    <style>
        /* Estilos personalizados */
        {custom_css}

        /* Reset y estilos básicos */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: var(--font-size, 32px);
        }}

        .reveal h1 {{
            color: var(--heading1-color, #333) !important;
            font-size: var(--heading-fontsize, 2.5em) !important;
        }}

        .reveal h2 {{
            color: var(--heading2-color, #333) !important;
            font-size: calc(var(--heading-fontsize, 2.5em) * 0.9) !important;
        }}

        .reveal h3 {{
            color: var(--heading3-color, #333) !important;
            font-size: calc(var(--heading-fontsize, 2.5em) * 0.8) !important;
        }}

        /* Columnas */
        .columns {{
            display: flex;
            gap: 2rem;
            margin: 1.5rem 0;
        }}

        .column {{
            flex: 1;
        }}

        /* Grid */
        .grid {{
            display: grid;
            gap: 1rem;
            margin: 1.5rem 0;
        }}

        .grid-row {{
            display: flex;
            gap: 1rem;
        }}

        .grid-cell {{
            flex: 1;
            padding: 1rem;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}

        /* Iframes */
        .reveal iframe.fullscreen-iframe {{
            max-width: 80vw;
            max-height: 83vh;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            display: block !important;
            padding: 0;
            margin: 0;
        }}

        .reveal .slides section.iframe-slide {{
            top: 0px !important;
            display: flex !important;
            margin: 0 !important;
            font-size: 32px !important;
            padding: 0 !important;
            text-align: left !important;
            justify-content: flex-start !important;
            align-items: flex-start !important;
        }}

        .reveal .slides,
        .reveal .slides section {{
            background: transparent !important;
        }}
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
            {''.join(processed_slides)}
        </div>
    </div>

    <!-- Reveal.js JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/notes/notes.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/markdown/markdown.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/highlight/highlight.js"></script>

    <script>
        Reveal.initialize({{
            hash: {json.dumps(reveal_config['hash'])},
            controls: {json.dumps(reveal_config['controls'])},
            progress: {json.dumps(reveal_config['progress'])},
            center: {json.dumps(reveal_config['center'])},
            transition: {json.dumps(reveal_config['transition'])},
            transitionSpeed: {json.dumps(reveal_config['transitionSpeed'])},
            plugins: [ RevealMarkdown, RevealHighlight, RevealNotes ]
        }});
    </script>
</body>
</html>"""

    # Determinar archivo de salida
    if not output_file:
        output_file = os.path.join(presentation_path, "index.html")

    # Escribir archivo
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_template)

        print(f"✅ Standalone HTML generated: {output_file}")
        return True

    except Exception as e:
        print(f"Error writing output file: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_standalone.py <presentation_name> [output_file] [--embed|--link]")
        print("Example: python export_standalone.py refactoring-cultural")
        print("Example: python export_standalone.py refactoring-cultural myfile.html --embed")
        print("By default, generates 'index.html' in the presentation folder")
        print("Options:")
        print("  --embed  Embed images as base64 (autonomous file)")
        print("  --link   Use relative links to images (smaller file)")
        sys.exit(1)

    presentation_name = sys.argv[1]
    output_file = None
    embed_images = None

    # Procesar argumentos
    for arg in sys.argv[2:]:
        if arg == "--embed":
            embed_images = True
        elif arg == "--link":
            embed_images = False
        elif not arg.startswith("--"):
            output_file = arg

    success = generate_standalone_html(presentation_name, output_file, embed_images)
    sys.exit(0 if success else 1)