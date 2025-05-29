# Sistema de Presentaciones en Markdown

Este sistema permite crear presentaciones en Markdown que se convierten automáticamente en presentaciones web interactivas usando Reveal.js.

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
theme: "white"              # Tema de Reveal.js (white, black, league, beige, sky, night, serif, simple, solarized)
---
```

### Estructura del Contenido

El contenido se organiza en diapositivas usando comentarios especiales:

```markdown
<!-- SLIDE -->

# Título de la Diapositiva

Contenido de la diapositiva...

<!-- NOTES -->
Notas para el presentador...
```

#### Comentarios Especiales

- `<!-- SLIDE -->`: Marca el inicio de una nueva diapositiva
- `<!-- NOTES -->`: Marca el inicio de las notas del presentador (solo visibles en la vista del presentador)

#### Formato de Columnas

Para crear columnas en una diapositiva:

```markdown
$COLUMNS$
$COL$
Contenido de la primera columna
$COL$
Contenido de la segunda columna
$END$
```

#### Formato de Grid

Para crear una cuadrícula:

```markdown
$GRID$
$ROW$
$CELL$
Contenido de la celda 1
$CELL$
Contenido de la celda 2
$ROW$
$CELL$
Contenido de la celda 3
$CELL$
Contenido de la celda 4
$END$
```

### Imágenes

Las imágenes deben colocarse en el directorio `images/` de la presentación y referenciarse así:

```markdown
![Descripción de la imagen](images/nombre-imagen.webp)
```

## Desarrollo y Pruebas

### Requisitos

- Python 3.x
- Node.js y npm

### Instalación

1. Clonar el repositorio
2. Instalar dependencias:
```bash
npm install
```

### Ejecución en Desarrollo

1. Iniciar el servidor de desarrollo:
```bash
./start.sh
```

Este script:
- Ejecuta el generador de `index.html`
- Inicia el servidor web en un puerto disponible (3000-3010)
- Muestra la URL en la consola

2. Abrir la URL mostrada en el navegador (ejemplo: `http://localhost:3000`)

### Vista del Presentador

Para acceder a la vista del presentador (con notas):
1. Presiona `S` durante la presentación
2. Se abrirá una nueva ventana con las notas del presentador

## Temas Disponibles

Reveal.js incluye varios temas que puedes usar en la configuración:
- white (por defecto)
- black
- league
- beige
- sky
- night
- serif
- simple
- solarized
- blood
- moon
- dracula
- monokai
- contrast
- custom

Puedes ver una vista previa de todos los temas en la [documentación oficial de Reveal.js](https://revealjs.com/themes/).

## Ejemplo de Presentación

```markdown
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

<!-- SLIDE -->

# Título Principal

Contenido de la primera diapositiva

<!-- NOTES -->
Notas para el presentador sobre esta diapositiva

<!-- SLIDE -->

## Subtítulo

$COLUMNS$
$COL$
Contenido de la primera columna
$COL$
Contenido de la segunda columna
$END$

<!-- NOTES -->
Notas sobre las columnas
``` 