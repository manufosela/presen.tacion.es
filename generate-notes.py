#!/usr/bin/env python3
"""
Generador de notas para presentaciones
Genera un documento HTML optimizado para imprimir en formato tarjeta postal
con el título, número y notas de cada slide
"""

import os
import sys
import yaml
import re
from pathlib import Path


def parse_yaml_frontmatter(content):
    """Extrae y parsea el frontmatter YAML del markdown"""
    if not content.startswith('---'):
        return {}, content

    # Buscar el segundo ---
    end_index = content.find('---', 3)
    if end_index == -1:
        return {}, content

    yaml_content = content[3:end_index].strip()
    markdown_content = content[end_index + 3:].strip()

    try:
        metadata = yaml.safe_load(yaml_content)
        return metadata or {}, markdown_content
    except yaml.YAMLError as e:
        print(f"⚠️  Error parsing YAML: {e}")
        return {}, markdown_content


def extract_title_from_content(content):
    """Extrae el primer título del contenido markdown"""
    # Buscar títulos de nivel 1, 2 o 3
    title_match = re.search(r'^#{1,3}\s+(.+?)$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()

    # Si no hay título, buscar texto destacado
    bold_match = re.search(r'\*\*(.+?)\*\*', content)
    if bold_match:
        return bold_match.group(1).strip()

    # Si no hay nada, retornar las primeras palabras
    first_line = content.split('\n')[0].strip()
    words = first_line.split()[:8]
    return ' '.join(words) + ('...' if len(words) >= 8 else '')


def process_markdown_to_notes(markdown_content):
    """Convierte el markdown en estructura de notas para imprimir"""
    slides_data = []
    slide_blocks = re.split(r'<!--\s*SLIDE\s*-->', markdown_content)

    slide_number = 0

    for block in slide_blocks:
        block = block.strip()
        if not block:
            continue

        # Dividir por <!-- SUBSLIDE -->
        subslides = re.split(r'<!--\s*SUBSLIDE\s*-->', block)
        subslide_number = 0

        for subslide in subslides:
            subslide = subslide.strip()
            if not subslide:
                continue

            # Limpiar marcadores especiales
            subslide = subslide.replace('<!-- INVERTED -->', '').strip()
            subslide = re.sub(r'<!--\s*BACKGROUND:\s*[^\s]+\s*-->', '', subslide).strip()

            # Separar contenido y notas
            parts = re.split(r'<!--\s*NOTES\s*-->', subslide, 1)
            content = parts[0].strip()
            notes = parts[1].strip() if len(parts) > 1 else ''

            # Solo agregar si hay notas
            if notes:
                # Extraer título del contenido
                title = extract_title_from_content(content)

                # Calcular número de slide
                if subslide_number == 0:
                    slide_number += 1
                    slide_num_str = str(slide_number)
                else:
                    slide_num_str = f"{slide_number}.{subslide_number}"

                slides_data.append({
                    'number': slide_num_str,
                    'title': title,
                    'notes': notes
                })

            subslide_number += 1

    return slides_data


def generate_notes_html(presentation_name, metadata, slides_data):
    """Genera el HTML para imprimir las notas"""

    # Colores desde metadata
    colors = metadata.get('colors', {})
    main_color = colors.get('main-color', colors.get('heading-color', '#DF006E'))
    bg_color = colors.get('background', '#FFFFFF')
    text_color = colors.get('text-color', '#000000')

    # Generar tarjetas de notas
    cards_html = []
    for slide in slides_data:
        # Procesar notas: convertir markdown básico
        notes_html = slide['notes']
        notes_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', notes_html)
        notes_html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', notes_html)
        notes_html = notes_html.replace('\n', '<br>')

        card = f'''
        <div class="note-card">
            <div class="note-header">
                <div class="note-number">#{slide['number']}</div>
                <div class="note-title">{slide['title']}</div>
            </div>
            <div class="note-content">
                {notes_html}
            </div>
        </div>
        '''
        cards_html.append(card)

    cards_content = '\n'.join(cards_html)

    # Template HTML
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notas: {presentation_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Lato', sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        h1 {{
            text-align: center;
            color: {main_color};
            margin-bottom: 30px;
            font-size: 2rem;
        }}

        .notes-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .note-card {{
            background: white;
            border: 2px solid {main_color};
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            break-inside: avoid;
            page-break-inside: avoid;
            height: 280px; /* Tamaño tarjeta postal ~A6 */
            display: flex;
            flex-direction: column;
        }}

        .note-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 2px solid {main_color};
        }}

        .note-number {{
            background: {main_color};
            color: white;
            font-weight: bold;
            font-size: 1.1rem;
            padding: 6px 12px;
            border-radius: 4px;
            min-width: 50px;
            text-align: center;
        }}

        .note-title {{
            flex: 1;
            font-weight: bold;
            font-size: 1.1rem;
            color: {text_color};
            line-height: 1.3;
        }}

        .note-content {{
            flex: 1;
            color: {text_color};
            font-size: 0.95rem;
            line-height: 1.5;
            overflow: auto;
        }}

        .note-content strong {{
            color: {main_color};
        }}

        /* Estilos de impresión - Tamaño A6 (una tarjeta por página) */
        @page {{
            size: A6;
            margin: 10mm;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
                margin: 0;
            }}

            .container {{
                max-width: 100%;
                margin: 0;
            }}

            h1 {{
                display: none; /* Ocultar título en impresión */
            }}

            .notes-grid {{
                display: block;
                margin: 0;
                padding: 0;
            }}

            .note-card {{
                width: 128mm; /* A6 width - margins */
                height: 85mm; /* A6 height - margins */
                page-break-after: always;
                page-break-inside: avoid;
                break-inside: avoid;
                box-shadow: none;
                border: none;
                margin: 0;
                padding: 8mm;
                border-radius: 0;
                display: flex;
                flex-direction: column;
            }}

            .note-card:last-child {{
                page-break-after: auto;
            }}

            .note-header {{
                gap: 8px;
                margin-bottom: 8px;
                padding-bottom: 8px;
                flex-shrink: 0;
            }}

            .note-number {{
                font-size: 0.9rem;
                padding: 4px 8px;
                min-width: 40px;
            }}

            .note-title {{
                font-size: 1rem;
                line-height: 1.2;
            }}

            .note-content {{
                font-size: 0.85rem;
                line-height: 1.4;
                overflow: hidden;
            }}
        }}

        .print-info {{
            text-align: center;
            color: #666;
            margin-top: 20px;
            padding: 20px;
            background: white;
            border-radius: 8px;
        }}

        @media print {{
            .print-info {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 Notas: {presentation_name}</h1>

        <div class="notes-grid">
{cards_content}
        </div>

        <div class="print-info">
            <p><strong>💡 Consejo de impresión:</strong></p>
            <p>Usa Ctrl+P (Cmd+P en Mac) para imprimir. Recomendado: 2 tarjetas por página.</p>
            <p>Total de notas: {len(slides_data)}</p>
        </div>
    </div>
</body>
</html>'''

    return html


def generate_notes(presentation_name):
    """Genera el documento de notas para una presentación"""
    presentation_path = Path(presentation_name)

    if not presentation_path.exists():
        print(f"❌ Error: La carpeta '{presentation_name}' no existe")
        return False

    contenidos_path = presentation_path / 'contenidos.md'
    if not contenidos_path.exists():
        print(f"❌ Error: No se encontró '{contenidos_path}'")
        return False

    print(f"📝 Generando notas para: {presentation_name}")

    # Leer contenido
    with open(contenidos_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parsear
    metadata, markdown_content = parse_yaml_frontmatter(content)
    slides_data = process_markdown_to_notes(markdown_content)

    if not slides_data:
        print(f"⚠️  No se encontraron notas en la presentación")
        return False

    print(f"   ✓ Metadata parseada")
    print(f"   ✓ {len(slides_data)} slides con notas encontradas")

    # Generar HTML
    html = generate_notes_html(presentation_name, metadata, slides_data)

    # Guardar
    output_path = presentation_path / 'notas.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"   ✓ Generado: {output_path}")
    print(f"✅ Notas generadas exitosamente")
    print(f"\n🖨️  Abre en navegador e imprime: {output_path}")
    print(f"💡 Tip: Configura impresión a 2 tarjetas por página")

    return True


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 generate-notes.py <nombre-presentacion>")
        print("\nEjemplo:")
        print("  python3 generate-notes.py equipazgo")
        sys.exit(1)

    presentation_name = sys.argv[1]
    success = generate_notes(presentation_name)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
