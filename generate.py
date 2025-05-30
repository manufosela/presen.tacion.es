import os

def generate_index_html():
  # Directorios a ignorar
  ignored_dirs = {'lib', 'fonts', 'dist', 'node_modules', 'public'}
  
  html = [
    '<!DOCTYPE html>',
    '<html lang="es">',
    '<head>',
    '  <meta charset="UTF-8">',
    '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '  <title>Presentaciones</title>',
    '  <link rel="stylesheet" href="https://unpkg.com/@picocss/pico@1.*/css/pico.min.css">',
    '  <style>',
    '    .local-presentation {',
    '      margin-top: 2rem;',
    '      padding: 1rem;',
    '      border: 1px solid var(--primary);',
    '      border-radius: 0.5rem;',
    '    }',
    '    .local-presentation h2 {',
    '      margin-top: 0;',
    '    }',
    '  </style>',
    '</head>',
    '<body>',
    '  <main class="container">',
    '    <h1>Presentaciones</h1>',
    '    ',
    '    <div class="local-presentation">',
    '      <h2>Cargar Presentación Local</h2>',
    '      <form id="localForm">',
    '        <label for="localFolder">',
    '          Selecciona la carpeta de la presentación',
    '          <input type="file" id="localFolder" webkitdirectory directory multiple>',
    '        </label>',
    '        <button type="submit">Cargar Presentación</button>',
    '      </form>',
    '    </div>',
    '    ',
    '    <h2>Presentaciones Disponibles</h2>',
    '    <ul id="presentationsList">',
  ]

  for folder in sorted(os.listdir('.')):
    if folder.startswith('.') or not os.path.isdir(folder) or folder in ignored_dirs:
      continue

    # Verifica si existe el archivo contenidos.md o content.md
    if os.path.exists(os.path.join(folder, 'contenidos.md')) or os.path.exists(os.path.join(folder, 'content.md')):
      # Enlaza a presentacion.html pasando el directorio como parámetro
      label = f"{folder}"
      html.append(f'      <li><a href="presentacion.html?presentacion={label}">{label}</a></li>')

  html += [
    '    </ul>',
    '  </main>',
    '  ',
    '  <script>',
    '    // Manejar el formulario de carga local',
    '    document.getElementById("localForm").addEventListener("submit", async (e) => {',
    '      e.preventDefault();',
    '      const files = document.getElementById("localFolder").files;',
    '      ',
    '      if (files.length === 0) {',
    '        alert("Por favor, selecciona una carpeta");',
    '        return;',
    '      }',
    '      ',
    '      // Crear un objeto con los archivos',
    '      const presentationFiles = {};',
    '      for (const file of files) {',
    '        const path = file.webkitRelativePath;',
    '        presentationFiles[path] = file;',
    '      }',
    '      ',
    '      // Verificar si existe contenidos.md',
    '      if (!presentationFiles["contenidos.md"]) {',
    '        alert("La carpeta seleccionada no contiene un archivo contenidos.md");',
    '        return;',
    '      }',
    '      ',
    '      // Guardar los archivos en sessionStorage',
    '      for (const [path, file] of Object.entries(presentationFiles)) {',
    '        const reader = new FileReader();',
    '        reader.onload = (e) => {',
    '          sessionStorage.setItem(`local_${path}`, e.target.result);',
    '        };',
    '        reader.readAsText(file);',
    '      }',
    '      ',
    '      // Redirigir a la presentación',
    '      const folderName = files[0].webkitRelativePath.split("/")[0];',
    '      window.location.href = `presentacion.html?presentacion=local_${folderName}`;',
    '    });',
    '  </script>',
    '</body>',
    '</html>'
  ]

  with open("index.html", "w", encoding="utf-8") as f:
    f.write("\n".join(html))
  print("✅ index.html generado con éxito.")

if __name__ == "__main__":
  generate_index_html()
