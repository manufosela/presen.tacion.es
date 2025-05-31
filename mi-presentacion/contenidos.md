---
fontSize: "30px"
colors:
  color: "#0078D7" # Color general para enlaces y elementos interactivos
  main-color: "#DF006E" # Color principal
  background: "#FFFFFF" # Color de fondo
  heading-color: "#DF006E" # Color de títulos principales
  heading2-color: "#0078D7" # Color de subtítulos
  heading3-color: "#000035" # Color de títulos terciarios
  accent-color: "#FF4D94" # Color de acentos
  text-color: "#4A4A4A" # Color del texto
  light-gray: "#F5F5F5" # Gris claro
  dark-gray: "#333333" # Gris oscuro
fonts:
  main-font: "Lato, sans-serif"
  heading-font: "Lato, sans-serif"
  heading-fontsize: "3rem"
theme: "white" # Tema de Reveal.js
---

<!-- SLIDE -->
<!-- markdownlint-disable -->
# presen.tacion.es

Bienvenidos a la documentación de presentaciones basadas en markdown y reveal.js

<!-- NOTES -->

En esta presentación te mostraré como usar presen.tacion.es para crear facilmente presentaciones.

<!-- SLIDE -->

- Markdown => Lenguaje de marcado ligero
- Reveal.js => Libreria JS para presentaciones

Y siguiendo un sencillo convenio, podrás crear y mostrar todas las presentaciones que imagines.

<!-- NOTES -->

- Markdown es un lenguaje de marcado ligero que permite dar formato a texto de forma sencilla usando caracteres especiales
- Reveal.js es una librería JavaScript de código abierto para crear presentaciones en HTML de manera sencilla y visual, al estilo PowerPoint, pero usando el navegador

Ventajas:
- Es sencillo de crear porque solo necesitas saber markdown y seguir un minimo convenio para crear facilmente presentaciones.
- Puedes aprovechar tu documentación en markdown para hacer presentaciones o tus presentaciones como documentación en markdown.


<!-- SLIDE -->

## ¿Cómo funciona esta app?

- Crea una carpeta donde estarán lo archivos de tu presentación
- Si vas a usar imagenes locales, crea una carpeta llamada imagenes (aunque esto no es obligatorio)
- Crea un archivo `contenidos.md` en la carpeta de tu presentación.
- Crea tu contenido en markdown dentro de contenidos.md

<!-- NOTES -->

- Crea una carpeta donde estarán lo archivos de tu presentación
- Si vas a usar imagenes locales, crea una carpeta llamada imagenes (aunque esto no es obligatorio)
- Crea un archivo llamado contenidos.md en dicha carpeta
- Crea tu contenido en markdown dentro de contenidos.md
- Ten en cuenta el convenio para crear diapositivas, subdiapositivas y notas de presentador
- Ten en cuenta el convenio para crear contenido con columnas o con grid o si prefieres usa tablas de markdown

<!-- SUBSLIDE -->

### Metadatos

Al principio del fichero de contenidos.md podemos inicializar metadatos de configuración de la presentación.

Estos metadatos en formato YAML, irán entre --- al principio del fichero contenidos.md

```yaml
---
fontSize: "30px"
colors:
  main-color: "#DF006E"
  background: "#FFFFFF"
  heading-color: "#DF006E"
  heading2-color: "#0078D7"
  heading3-color: "#000035"
theme: "white"
---
```

<!-- NOTES -->

Los posibles valores de configuración de la presentación

```yaml
---
fontSize: "30px"
colors:
  color: "#0078D7" # Color general para enlaces y elementos interactivos
  main-color: "#DF006E" # Color principal
  background: "#FFFFFF" # Color de fondo
  heading-color: "#DF006E" # Color de títulos principales
  heading2-color: "#0078D7" # Color de subtítulos
  heading3-color: "#000035" # Color de títulos terciarios
  accent-color: "#FF4D94" # Color de acentos
  text-color: "#4A4A4A" # Color del texto
  light-gray: "#F5F5F5" # Gris claro
  dark-gray: "#333333" # Gris oscuro
fonts:
  main-font: "Lato, sans-serif"
  heading-font: "Lato, sans-serif"
  heading-fontsize: "3rem"
theme: "white" # Tema de Reveal.js
---
```

<!-- SLIDE -->

## Diapositivas y subdiapositivas

Podrás separar el contenido en diapositivas y subdiapositivas

Añade delante de cada diapositiva ```<!--  SLIDE  -->```

Añade delante de cada subdiapositiva ```<!--  SUBSLIDE  -->```

<!-- SUBSLIDE -->

### Notas para el presentador

Puedes añadir notas para el presentador usando ```<!--  NOTES  -->```
justo después de cada diapositiva o subdiapositiva y antes de la siguiente

<!-- NOTES -->

En las notas también puedes usar markdown estandar para ver estas con estilos visuales

<!-- SUBSLIDE -->

### Marcadores especiales

En markdown podemos crear tablas, pero podemos usar marcadores especiales para crear columnas y grids:

Para columnas tenemos los marcadores ```＄COLUMNS＄, ＄COL＄```

Para grids tenemos los marcadores ```＄GRID＄, ＄ROW＄, ＄CELL＄, ＄END＄```

<!-- SUBSLIDE -->

### Ejemplo de COLUMNAS (1)

Ejemplo de 2 columnas:

$COLUMNS$
$COL$
- Fácil de usar
- Basado en Markdown
- Soporte para NOTES
$COL$
- Temas personalizables
- Imágenes y multimedia
- Diseño responsive
$END$

<!-- SUBSLIDE -->

## Ejemplo de COLUMNAS (2)

Ejemplo de 3 columnas:

$COLUMNS$
$COL$
- Fácil de usar
- Basado en Markdown
$COL$
- Soporte para **NOTES**
- Temas personalizables
$COL$
- Imágenes y multimedia
- Diseño responsive
$END$

<!-- SUBSLIDE -->

### Cómo se escribe

```
＄COLUMNS＄
＄COL＄
Contenido columna 1
＄COL＄
Contenido columna 2
＄END＄
```

<!-- SUBSLIDE -->

### Ejemplo de GRID

$GRID$
$ROW$
$CELL$
**Ventaja 1**

Markdown simple
$CELL$
**Ventaja 2**

NOTES para presentador
$CELL$
**Ventaja 3**

Temas personalizables
$ROW$
$CELL$
**Ventaja 4**

Soporte para imágenes
$CELL$
**Ventaja 5**

Diseño responsive
$CELL$
**Ventaja 6**

Fácil de compartir
$END$

<!-- SUBSLIDE -->

### Cómo se escribe

```markdown
＄GRID＄
＄ROW＄
＄CELL＄
Contenido celda 1
＄CELL＄
Contenido celda 2
＄ROW＄
＄CELL＄
Contenido celda 3
＄CELL＄
Contenido celda 4
＄END＄
```

<!-- SLIDE -->

## Comandos y atajos Reveal.js

Al usar Reveal.js podemos usar los comandos y atajos de este para una navegación básica y avanzada.

<!-- SUBSLIDE -->

### Navegación

- <kbd>→</kbd> / <kbd>←</kbd> o <kbd>Espacio</kbd>: Avanzar/retroceder SLIDE
- <kbd>↓</kbd> / <kbd>↑</kbd>: Navegar entre subSLIDES
- <kbd>Esc</kbd>: Vista general de todas las SLIDES

<!-- SUBSLIDE -->

### Presentación

- <kbd>F</kbd>: Pantalla completa
- <kbd>S</kbd>: Vista del presentador (con NOTES)
- <kbd>B</kbd>: Pantalla en negro
- <kbd>O</kbd>: Vista de esquema

<!-- SLIDE -->

# ¡Gracias!

¿Preguntas?

<!-- NOTES -->

Esta es la última SLIDE.
Es un buen momento para preguntas y respuestas.
