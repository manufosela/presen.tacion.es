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
transition: "fade" # Transición entre slides
transitionSpeed: "default" # Velocidad de transición
---

<!-- SLIDE -->
<!-- markdownlint-disable -->

# Sistema de Presentaciones en Markdown

Este sistema permite crear presentaciones en Markdown que se convierten automáticamente en presentaciones web interactivas usando Reveal.js.

<!-- SLIDE -->
## Estructura de una Presentación

Cada presentación debe estar en su propio directorio con la siguiente estructura:

```
nombre-presentacion/
├── contenidos.md      # Contenido principal de la presentación
├── images/           # Directorio para imágenes
│   ├── imagen1.webp
│   └── imagen2.webp
└── template.webp     # Imagen de fondo (opcional, proporción 16:9 recomendada)
```
<!-- SLIDE -->

### Configuración de la Presentación

Al inicio del archivo `contenidos.md`, puedes configurar el aspecto de la presentación usando metadatos entre `---`:

```markdown
---
fontSize: "30px"
colors:
  color: "#0078D7"           # Color general para enlaces y elementos interactivos
  main-color: "#DF006E"      # Color principal
  background: "#333333"      # Color de fondo
  heading-color: "#DF006E"   # Color de títulos principales
  heading2-color: "#0078D7"  # Color de subtítulos
  heading3-color: "#000035"  # Color de títulos terciarios
  accent-color: "#FF4D94"    # Color de acentos
  text-color: "#4A4A4A"      # Color del texto
  light-gray: "#F5F5F5"      # Gris claro
  dark-gray: "#333333"       # Gris oscuro
fonts:
  main-font: "Lato, sans-serif"
  heading-font: "Lato, sans-serif"
theme: "white"              # Tema de Reveal.js
transition: "fade"          # Transición entre slides
transitionSpeed: "default"  # Velocidad de transición
---
```

<!-- SLIDE -->

### Estructura del Contenido

El contenido se organiza en diapositivas usando comentarios especiales:

```markdown
<!--  SLIDE  -->

# Título de la Diapositiva

Contenido de la diapositiva...

<!--  SUBSLIDE  -->

### Título de la Subdiapositiva

Contenido de la subdiapositiva...

<!--  NOTES  -->
Notas para el presentador...
```

<!-- SLIDE -->

#### Comentarios Especiales

- `<!-- SLIDE -->`: Marca el inicio de una nueva diapositiva
- `<!-- SUBSLIDE -->`: Marca el inicio de una nueva subdiapositiva
- `<!-- NOTES -->`: Marca el inicio de las notas del presentador (solo visibles en la vista del presentador)
- `<!-- BACKGROUND: ruta-imagen -->`: Aplica una imagen de fondo específica a la diapositiva

<!-- SLIDE -->

#### Formato de Columnas

Para crear columnas en una diapositiva:

```markdown
＄COLUMNS＄
＄COL＄
Contenido de la primera columna
＄COL＄
Contenido de la segunda columna
＄END＄
```
<!-- SLIDE -->

#### Formato de Grid

Para crear una cuadrícula:

```markdown
＄GRID＄
＄ROW＄
＄CELL＄
Contenido de la celda 1
＄CELL＄
Contenido de la celda 2
＄ROW＄
＄CELL＄
Contenido de la celda 3
＄CELL＄
Contenido de la celda 4
＄END＄
```

<!-- SLIDE -->

### Imágenes

Las imágenes deben colocarse en el directorio `images/` de la presentación y referenciarse así:

```markdown
![Descripción de la imagen](images/nombre-imagen.webp)
```

<!-- SLIDE -->

## Desarrollo y Pruebas

<!-- SLIDE -->

### Requisitos

- Python 3.x

<!-- SLIDE -->

### Instalación

1. Clonar el repositorio

<!-- SLIDE -->

### Ejecución en Desarrollo

1. Iniciar el servidor de desarrollo:
```bash
./start.sh
```

Este script:
- Ejecuta el generador de `index.html`
- Inicia el servidor web en un puerto disponible (3000-3010)
- Muestra la URL en la consola

<!-- SLIDE -->

2. Abrir la URL mostrada en el navegador (ejemplo: `http://localhost:3000`)

<!-- SLIDE -->

### Vista del Presentador

Para acceder a la vista del presentador (con notas):
1. Presiona `S` durante la presentación
2. Se abrirá una nueva ventana con las notas del presentador

<!-- SLIDE -->

## Temas Disponibles

Reveal.js incluye varios temas que puedes usar en la configuración:
$COLUMNS$
$COL$
- white (por defecto)
- black
- league
- beige
- sky
- night
- serif
- simple
$COL$
- solarized
- blood
- moon
- dracula
- monokai
- contrast
- custom
$END$

Puedes ver una vista previa de todos los temas en la [documentación oficial de Reveal.js](https://revealjs.com/themes/).

<!-- SLIDE -->

## Transiciones

Puedes configurar transiciones suaves entre slides:

```yaml
transition: "fade"          # Tipo de transición
transitionSpeed: "slow"     # Velocidad de transición
```

<!-- SLIDE -->

### Tipos de transiciones

$COLUMNS$
$COL$
- **`none`** - Sin transición
- **`fade`** - Desvanecimiento
- **`slide`** - Deslizamiento
$COL$
- **`zoom`** - Efecto zoom
- **`cube`** - Efecto cubo 3D
- **`page`** - Efecto página
$END$

**Velocidades:** `slow`, `default`, `fast`

<!-- SLIDE -->

### Navegación para transiciones

**Para ver las transiciones usar:**
- **← → (flechas)** o **Espacio**
- **↑ ↓** para subslides
- **Esc** para vista general
- **F** pantalla completa
- **S** vista presentador

⚠️ **No usar scroll del ratón**

<!-- SLIDE -->

## GitHub Pages

El sistema funciona directamente en GitHub Pages:

1. **Sube tu repositorio a GitHub**
2. **Configura Pages:** Settings → Pages → Branch main
3. **Accede:** `https://usuario.github.io/repo/`

✅ Hosting gratuito • ✅ HTTPS • ✅ No servidor Python

<!-- SLIDE -->

## Desarrollo avanzado: recarga automática y servidor de desarrollo

Para facilitar el desarrollo y ver los cambios en tiempo real al editar el archivo `contenidos.md`, el proyecto incluye un **servidor de desarrollo** con recarga automática.

<!-- SLIDE -->

### ¿Qué hace el servidor de desarrollo?
- Sirve los archivos estáticos sin caché (siempre verás la última versión de cada archivo).
- Detecta cambios en el archivo `contenidos.md` y recarga automáticamente la página en el navegador.
- En modo desarrollo, la app ignora el `sessionStorage` y siempre lee el `.md` real del disco.

<!-- SLIDE -->

### ¿Cómo usarlo?

1. **Lanza el servidor de desarrollo:**
   ```bash
   ./startdev.sh
   ```
   Este script ejecuta `generate.py` y luego inicia el servidor de desarrollo en el puerto 8000.

<!-- SLIDE -->

2. **Abre la presentación en el navegador:**
   - Accede a: `http://localhost:8000/presentacion.html?presentacion=local_mi-presentacion`
   - (Cambia `mi-presentacion` por el nombre de tu carpeta de presentación)

<!-- SLIDE -->

3. **Edita el archivo `contenidos.md`**
   - Cada vez que guardes cambios, la página se recargará automáticamente y verás el contenido actualizado.

<!-- SLIDE -->

### Diferencias con el modo producción
- **Desarrollo:**
  - El navegador siempre lee el `.md` real del disco.
  - No se usa `sessionStorage` para el contenido local.
  - El servidor fuerza cabeceras para evitar cualquier caché.
  - Recarga automática al detectar cambios.
- **Producción:**
  - El contenido local se puede cargar desde `sessionStorage` para mayor rendimiento.
  - El servidor puede usar caché.

<!-- SLIDE -->

### Requisitos adicionales para desarrollo
- Python 3.x
- No necesitas instalar nada más: el servidor de desarrollo está incluido en el repositorio.

<!-- SLIDE -->

### Flujo recomendado para desarrollo
1. Edita tu `contenidos.md` en la carpeta de la presentación.
2. Deja abierto el navegador en `http://localhost:8000/presentacion.html?presentacion=local_mi-presentacion`.
3. Cada vez que guardes, verás los cambios reflejados al instante.

<!-- SLIDE -->

## FIN de README

Puedes consultar em eñ repositorio este [README](https://github.com/manufosela/presen.tacion.es)
