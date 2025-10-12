#!/usr/bin/env python3
"""
Limpia el HTML capturado para que sea standalone
Elimina los scripts de carga dinámica innecesarios
"""
import sys
import re

def clean_standalone_html(html_content, bg_color='#FFFFFF', presentation_name=''):
    """Elimina scripts innecesarios del HTML standalone y agrega inicialización de Reveal"""

    # Agregar data-background-color a todas las <section> que no lo tengan
    # Esto asegura que las slides normales mantengan el color de fondo correcto
    def add_background_to_section(match):
        section_tag = match.group(0)
        # Si ya tiene data-background-color, no modificar (slides invertidas)
        if 'data-background-color' in section_tag:
            return section_tag
        # Agregar data-background-color antes del primer >
        return section_tag.replace('>', f' data-background-color="{bg_color}">', 1)

    html_content = re.sub(r'<section[^>]*>', add_background_to_section, html_content)

    # Corregir rutas de imágenes: eliminar prefijo del nombre de presentación
    if presentation_name:
        # Reemplazar src="presentacion/images/..." con src="images/..."
        html_content = re.sub(
            rf'src="{presentation_name}/images/',
            'src="images/',
            html_content
        )

    # Eliminar el script type="module" completo (toda la lógica de carga dinámica)
    html_content = re.sub(
        r'<script type="module">.*?</script>',
        '',
        html_content,
        flags=re.DOTALL
    )

    # Eliminar el script de auto-reload del modo desarrollo
    html_content = re.sub(
        r'<script>\s*//\s*Recarga automática.*?</script>',
        '',
        html_content,
        flags=re.DOTALL
    )

    # Agregar script de inicialización de Reveal.js antes del </body>
    init_script = '''
    <script>
        // Re-inicialización de Reveal.js para standalone
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof Reveal !== 'undefined') {
                Reveal.initialize({
                    hash: true,
                    slideNumber: true,
                    controls: true,
                    progress: true,
                    center: true,
                    transition: 'fade',
                    transitionSpeed: 'slow',
                    embedded: false,
                    backgroundTransition: 'none'
                });
            }
        });
    </script>
</body>'''

    html_content = html_content.replace('</body>', init_script)

    return html_content

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python3 clean-standalone.py <archivo.html> [color-fondo] [nombre-presentacion]")
        sys.exit(1)

    file_path = sys.argv[1]
    bg_color = sys.argv[2] if len(sys.argv) > 2 else '#FFFFFF'
    presentation_name = sys.argv[3] if len(sys.argv) > 3 else ''

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    cleaned_html = clean_standalone_html(html, bg_color, presentation_name)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_html)

    print("✓ HTML limpiado")
