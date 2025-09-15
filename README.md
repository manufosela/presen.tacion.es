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
  background: "#FFFFFF"      # Color de fondo
  heading-color: "#DF006E"   # Color de títulos principales
  heading2-color: "#0078D7"  # Color de subtítulos
  heading3-color: "#000035"  # Color de títulos terciarios
  accent-color: "#FF4D94"    # Color de acentos
  text-color: "#4A4A4A"      # Color del texto
  light-gray: "#F5F5F5"      # Gris claro
  dark-gray: "#333333"       # Gris oscuro
  # Colores para clases CSS personalizadas
  quote-bg: "#DF006E"        # Fondo para slides de frases (quote-slide)
  question-bg: "#999999"     # Fondo para slides de preguntas (question-slide)
fonts:
  main-font: "Lato, sans-serif"
  heading-font: "Lato, sans-serif"
  heading-fontsize: "3rem"   # Tamaño de títulos principales
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
- `<!-- SUBSLIDE -->`: Marca el inicio de una subdiapositiva (navegación vertical)
- `<!-- NOTES -->`: Marca el inicio de las notas del presentador (solo visibles en la vista del presentador)
- `<!-- CLASS: nombre-clase -->`: Aplica una clase CSS personalizada a la diapositiva

#### Clases CSS Personalizadas

Puedes aplicar estilos visuales personalizados a tus diapositivas usando el comentario `<!-- CLASS: nombre-clase -->`. El sistema incluye varias clases predefinidas:

##### Clases Disponibles

**`title-slide`** - Slide de título principal:
```markdown
<!-- SLIDE -->
<!-- CLASS: title-slide -->

# Título Principal

Subtítulo o descripción
```
- Gradiente de fondo con colores principales
- Texto blanco con sombras
- Diseño centrado que ocupa toda la pantalla
- Ideal para portadas y títulos de sección

**`quote-slide`** - Frases destacadas:
```markdown
<!-- SLIDE -->
<!-- CLASS: quote-slide -->

## Frase Importante

**El texto más relevante de tu presentación**

Detalles adicionales...
```
- Recuadro central horizontal con fondo del color principal
- Texto blanco con sombras
- Bordes redondeados y efecto de sombra
- Perfecto para citas, frases clave y mensajes importantes

**`question-slide`** - Preguntas interactivas:
```markdown
<!-- SLIDE -->
<!-- CLASS: question-slide -->

## ¿Pregunta para la audiencia?

$COLUMNS$
$COL$
### OPCIÓN A
$COL$
### OPCIÓN B
$END$
```
- Fondo gris que ocupa toda la pantalla
- Texto blanco con contraste
- Ideal para encuestas, preguntas interactivas y votaciones

**`content-slide`** - Contenido estándar:
```markdown
<!-- SLIDE -->
<!-- CLASS: content-slide -->

## Título de Contenido

- Lista de elementos
- Más información
- Detalles adicionales
```
- Diseño estándar con acentos de color
- Bordes y líneas de énfasis en color principal
- Para contenido normal y listas

##### Ejemplo Completo

```markdown
---
colors:
  main-color: "#E91E63"      # Rosa vibrante
  heading-color: "#E91E63"   # Color de títulos
  question-bg: "#999999"     # Gris para preguntas
  quote-bg: "#E91E63"        # Color para frases
---

<!-- SLIDE -->
<!-- CLASS: title-slide -->

# Mi Presentación

Una presentación con estilo

<!-- SLIDE -->
<!-- CLASS: question-slide -->

## ¿Qué prefieres?

$COLUMNS$
$COL$
### OPCIÓN A
$COL$
### OPCIÓN B
$END$

<!-- SLIDE -->
<!-- CLASS: quote-slide -->

## Mensaje Clave

**Esta es la idea más importante de la presentación**

<!-- SLIDE -->
<!-- CLASS: content-slide -->

## Contenido Detallado

- Punto importante 1
- Punto importante 2
- Conclusiones
```

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

### Instalación

1. Clonar el repositorio

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

## Desarrollo avanzado: recarga automática y servidor de desarrollo

Para facilitar el desarrollo y ver los cambios en tiempo real al editar el archivo `contenidos.md`, el proyecto incluye un **servidor de desarrollo** con recarga automática.

### ¿Qué hace el servidor de desarrollo?
- Sirve los archivos estáticos sin caché (siempre verás la última versión de cada archivo).
- Detecta cambios en el archivo `contenidos.md` y recarga automáticamente la página en el navegador.
- En modo desarrollo, la app ignora el `sessionStorage` y siempre lee el `.md` real del disco.

### ¿Cómo usarlo?

1. **Lanza el servidor de desarrollo:**
   ```bash
   ./startdev.sh
   ```
   Este script ejecuta `generate.py` y luego inicia el servidor de desarrollo en el puerto 8000.

2. **Abre la presentación en el navegador:**
   - Accede a: `http://localhost:8000/presentacion.html?presentacion=local_mi-presentacion`
   - (Cambia `mi-presentacion` por el nombre de tu carpeta de presentación)

3. **Edita el archivo `contenidos.md`**
   - Cada vez que guardes cambios, la página se recargará automáticamente y verás el contenido actualizado.

### Diferencias con el modo producción
- **Desarrollo:**
  - El navegador siempre lee el `.md` real del disco.
  - No se usa `sessionStorage` para el contenido local.
  - El servidor fuerza cabeceras para evitar cualquier caché.
  - Recarga automática al detectar cambios.
- **Producción:**
  - El contenido local se puede cargar desde `sessionStorage` para mayor rendimiento.
  - El servidor puede usar caché.

### Requisitos adicionales para desarrollo
- Python 3.x
- No necesitas instalar nada más: el servidor de desarrollo está incluido en el repositorio.

### Flujo recomendado para desarrollo
1. Edita tu `contenidos.md` en la carpeta de la presentación.
2. Deja abierto el navegador en `http://localhost:8000/presentacion.html?presentacion=local_mi-presentacion`.
3. Cada vez que guardes, verás los cambios reflejados al instante.

## Guía de Diseño Visual

### Mejores Prácticas para Clases CSS

#### Cuándo usar cada clase:

- **`title-slide`**:
  - Slide de portada principal
  - Inicio de nuevas secciones importantes
  - Máximo 1-2 por presentación

- **`quote-slide`**:
  - Frases memorable o citas importantes
  - Mensajes clave que quieres destacar
  - Reflexiones o conclusiones importantes
  - Ideal para crear impacto visual

- **`question-slide`**:
  - Preguntas interactivas a la audiencia
  - Encuestas rápidas o votaciones
  - Momentos de participación
  - Preguntas retóricas importantes

- **`content-slide`**:
  - Contenido explicativo estándar
  - Listas y puntos detallados
  - Información de apoyo
  - Slides de transición

#### Consejos de diseño:

1. **Mantener consistencia**: Usa el mismo tipo de clase para contenido similar
2. **Crear ritmo visual**: Alterna entre diferentes tipos de slides para mantener el interés
3. **Menos es más**: No abuses de las `quote-slide`, resérvalas para momentos clave
4. **Colores coherentes**: Asegúrate de que los colores en la metadata combinen bien
5. **Texto legible**: Las `question-slide` y `quote-slide` funcionan mejor con poco texto

#### Ejemplo de flujo visual efectivo:

```markdown
<!-- Portada -->
<!-- CLASS: title-slide -->

<!-- Contenido introductorio -->
<!-- CLASS: content-slide -->

<!-- Pregunta interactiva -->
<!-- CLASS: question-slide -->

<!-- Más contenido -->
<!-- CLASS: content-slide -->

<!-- Mensaje clave -->
<!-- CLASS: quote-slide -->

<!-- Cierre -->
<!-- CLASS: title-slide -->
```

### Personalización Avanzada

Si necesitas estilos completamente personalizados, puedes:

1. **Definir colores personalizados** en la metadata:
   ```yaml
   colors:
     custom-bg: "#Tu-Color"
     custom-text: "#Otro-Color"
   ```

2. **Crear nuevas clases CSS** editando `presentacion.html` (requiere conocimientos técnicos)

3. **Combinar con elementos markdown** como negritas, cursivas y listas para mayor variedad visual
