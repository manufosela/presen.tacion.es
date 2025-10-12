#!/usr/bin/env python3
"""
Limpia el HTML capturado para que sea standalone
Elimina los scripts de carga dinámica innecesarios
"""
import sys
import re

def clean_standalone_html(html_content):
    """Elimina scripts innecesarios del HTML standalone"""

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

    return html_content

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python3 clean-standalone.py <archivo.html>")
        sys.exit(1)

    file_path = sys.argv[1]

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    cleaned_html = clean_standalone_html(html)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_html)

    print("✓ HTML limpiado")
