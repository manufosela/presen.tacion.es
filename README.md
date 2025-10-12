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
fonts:
  main-font: "Lato, sans-serif"
  heading-font: "Lato, sans-serif"
  heading-fontsize: "3rem"   # Tamaño de títulos principales
theme: "white"              # Tema de Reveal.js
transition: "fade"          # Transición entre slides
transitionSpeed: "default"  # Velocidad de transición
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
- `<!-- BACKGROUND: ruta-imagen -->`: Aplica una imagen de fondo específica a la diapositiva
- `<!-- INVERTED -->`: Invierte los colores de fondo y texto de la diapositiva (usa `text-color` como fondo y `background` como color de texto)

#### Imágenes de Fondo por Slide

Puedes aplicar imágenes de fondo específicas a cada diapositiva usando el comentario `<!-- BACKGROUND: ruta-imagen -->`. Esto te permite tener diferentes fondos para diferentes slides dentro de la misma presentación.

##### Sintaxis y Ejemplos

**Imagen de fondo básica:**
```markdown
<!-- SLIDE -->
<!-- BACKGROUND: images/fondo-slide1.webp -->

# Título con Fondo Personalizado

Contenido de la slide...
```

**Imagen de fondo con contenido:**
```markdown
<!-- SLIDE -->
<!-- BACKGROUND: images/fondo-inspirador.webp -->

## Frase Motivacional

**Con un fondo visual impactante**
```

**Diferentes fondos para diferentes tipos de contenido:**
```markdown
<!-- SLIDE -->
<!-- BACKGROUND: images/portada.webp -->

# Mi Presentación

Portada con imagen específica

<!-- SLIDE -->
<!-- BACKGROUND: images/fondo-contenido.webp -->

## Contenido Principal

- Punto 1
- Punto 2

<!-- SLIDE -->
<!-- BACKGROUND: images/fondo-pregunta.webp -->

## ¿Cuál prefieres?

$COLUMNS$
$COL$
### OPCIÓN A
$COL$
### OPCIÓN B
$END$
```

##### Organización de Imágenes

**Estructura recomendada:**
```
mi-presentacion/
├── contenidos.md
├── template.webp          # Fondo global (opcional)
└── images/
    ├── portada.webp        # Fondo para slide título
    ├── fondo-contenido.webp # Fondo para slides de contenido
    ├── fondo-pregunta.webp  # Fondo para slides de preguntas
    ├── fondo-conclusion.webp # Fondo para slide final
    ├── logo.webp           # Imágenes dentro del contenido
    └── grafico.webp
```

##### Notas Importantes

- **Precedencia**: Las imágenes de fondo por slide tienen prioridad sobre `template.webp`
- **Formatos soportados**: `.webp`, `.png`, `.jpg`, `.jpeg`
- **Rendimiento**: Las imágenes se cargan automáticamente según el entorno (local/GitHub Pages)
- **Tamaño recomendado**: 1920x1080 o proporción 16:9 para mejor visualización
- **Optimización**: Usa formato `.webp` para mejor compresión sin pérdida de calidad

#### Slides con Colores Invertidos

Puedes invertir los colores de fondo y texto de slides específicas usando el marcador `<!-- INVERTED -->`. Esto es ideal para destacar frases impactantes o crear contraste visual en momentos clave de tu presentación.

##### Cómo funciona

El sistema toma los colores definidos en tu metadata YAML y los invierte:
- **Fondo de la slide**: usa el color `text-color`
- **Texto de la slide**: usa el color `background`

##### Ejemplo de uso

```markdown
---
fontSize: "32px"
colors:
  text-color: "#000000"      # Negro
  background: "#FFB6C1"      # Rosa claro
---

<!-- SLIDE -->

# Slide normal

Fondo rosa, texto negro (colores por defecto)

<!-- SLIDE -->
<!-- INVERTED -->

**Frase impactante con colores invertidos**

Fondo negro, texto rosa (colores invertidos)

<!-- SLIDE -->

# Otra slide normal

Vuelve a los colores por defecto
```

##### Casos de uso recomendados

- **Frases destacadas**: Citas o mensajes clave que quieres resaltar
- **Transiciones**: Crear impacto visual entre secciones
- **Slides de cierre**: Llamadas a la acción o mensajes finales
- **Contrastes temáticos**: Separar contenido positivo/negativo, antes/después, etc.

##### Combinación con otras funcionalidades

Puedes combinar `<!-- INVERTED -->` con otros marcadores:

```markdown
<!-- SLIDE -->
<!-- INVERTED -->

### Si no te gustan las personas, no lideres

<!-- NOTES -->
Nota sobre esta frase impactante con colores invertidos
```

**Nota**: Los colores invertidos son específicos de cada presentación según su configuración YAML, manteniendo la coherencia visual de tu diseño.

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

### Despliegue en GitHub Pages

El sistema está diseñado para funcionar directamente en GitHub Pages:

1. **Sube tu repositorio a GitHub**
2. **Configura GitHub Pages:**
   - Ve a Settings → Pages
   - Selecciona "Deploy from a branch"
   - Elige la rama `main` y carpeta `/ (root)`
3. **Accede a tu presentación:**
   - URL: `https://tu-usuario.github.io/tu-repositorio/`
   - Presentación específica: `https://tu-usuario.github.io/tu-repositorio/presentacion.html?presentacion=nombre-carpeta`

**Ventajas de GitHub Pages:**
- ✅ Hosting gratuito
- ✅ HTTPS automático
- ✅ No requiere servidor Python
- ✅ Actualizaciones automáticas con cada push

### Vista del Presentador

Para acceder a la vista del presentador (con notas):
1. Presiona `S` durante la presentación
2. Se abrirá una nueva ventana con las notas del presentador

### Navegación de la Presentación

**Controles básicos:**
- **← → (flechas)** o **Espacio**: Navegar entre slides principales
- **↑ ↓ (flechas)**: Navegar entre subslides verticales
- **Esc**: Vista general de todas las slides
- **F**: Pantalla completa
- **S**: Vista del presentador
- **B**: Pantalla en negro
- **O**: Vista de esquema

**Importante:** Para que las transiciones funcionen correctamente, usa los controles de Reveal.js (flechas, espacio) en lugar del scroll del ratón.

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

## Transiciones

Puedes configurar transiciones suaves entre slides usando los metadatos YAML:

```yaml
transition: "fade"          # Tipo de transición
transitionSpeed: "slow"     # Velocidad de transición
```

### Tipos de transiciones disponibles:

- **`none`** - Sin transición (cambio inmediato)
- **`fade`** - Desvanecimiento suave (recomendado)
- **`slide`** - Deslizamiento horizontal (por defecto)
- **`zoom`** - Efecto de zoom hacia adentro/afuera
- **`cube`** - Efecto cubo 3D (si está disponible)
- **`page`** - Efecto de página

### Velocidades disponibles:

- **`slow`** - Transición lenta
- **`default`** - Velocidad estándar
- **`fast`** - Transición rápida

### Navegación para ver transiciones:

Las transiciones solo funcionan al usar la navegación nativa de Reveal.js:
- **Teclas de flecha** (← → ↑ ↓)
- **Barra espaciadora**
- **Controles de navegación** en pantalla
- **Presiona `Esc`** para vista general de todas las slides

**Nota:** Las transiciones NO funcionan con scroll del ratón o PageUp/PageDown.

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
transition: "fade"
transitionSpeed: "default"
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

## Generar Presentación Standalone (Build)

El sistema incluye un generador que crea una versión standalone de tu presentación en un único archivo HTML autónomo, ideal para compartir o publicar sin depender de `presentacion.html`.

### ¿Qué hace el build?

El comando de build genera un archivo `index.html` dentro de la carpeta de tu presentación que:
- **Es completamente autónomo**: No depende de `presentacion.html`
- **Usa Reveal.js local**: Referencias a `../reveal.js/` (no CDN)
- **Mantiene imágenes externas**: Las imágenes permanecen en `images/` como archivos externos
- **Incluye todos los estilos**: CSS inline basado en tu configuración YAML
- **Soporta todas las funcionalidades**: columnas, grids, slides invertidas, imágenes de fondo, notas del presentador

### Cómo usar el build

```bash
./build.sh nombre-presentacion
```

**Ejemplo:**
```bash
./build.sh equipazgo
```

Este comando:
1. Lee el archivo `equipazgo/contenidos.md`
2. Parsea los metadatos YAML y el contenido Markdown
3. Procesa todos los marcadores especiales (SLIDE, SUBSLIDE, NOTES, INVERTED, COLUMNS, GRID, BACKGROUND)
4. Genera `equipazgo/index.html` con todo integrado

### Requisitos

- **Python 3.x**
- **PyYAML**: Instalar con `pip3 install pyyaml`
- **Reveal.js local**: Debe estar en `reveal.js/` (ya incluido en el proyecto)

### Estructura después del build

```
equipazgo/
├── contenidos.md          # Fuente original
├── index.html            # Presentación standalone generada
└── images/               # Imágenes (externas, referenciadas por index.html)
    ├── manufosela.png
    └── grancias.png
```

### Abrir la presentación

Después del build, puedes abrir la presentación de varias formas:

**1. Directamente en el navegador:**
```bash
firefox equipazgo/index.html
```

**2. Servir con un servidor web simple:**
```bash
cd equipazgo
python3 -m http.server 8080
# Abre http://localhost:8080
```

**3. Subir a cualquier hosting estático:**
- GitHub Pages
- Netlify
- Vercel
- Servidor web propio

### Ventajas del build

- ✅ **Portabilidad**: Un solo archivo HTML + carpeta de imágenes
- ✅ **Sin dependencias externas**: No necesita CDN ni conexión a internet
- ✅ **Funciona offline**: Ideal para presentar sin conexión
- ✅ **Fácil de compartir**: Solo envía la carpeta con el `index.html` e `images/`
- ✅ **Control total**: Todos los estilos y configuración embebidos
- ✅ **Rápido**: No depende de cargas externas

### Cuándo usar el build

**Usa el build cuando:**
- Necesites compartir la presentación con otros
- Vayas a presentar sin conexión a internet
- Quieras publicar en hosting estático
- Necesites una versión inmutable de la presentación

**Usa el modo desarrollo cuando:**
- Estés editando activamente el contenido
- Quieras ver cambios en tiempo real
- Necesites iterar rápidamente en el diseño

### Funcionalidades soportadas

El build procesa y genera correctamente:
- ✅ Metadatos YAML (colores, fuentes, tema, transiciones)
- ✅ Slides y subslides (`<!-- SLIDE -->`, `<!-- SUBSLIDE -->`)
- ✅ Slides invertidas (`<!-- INVERTED -->`)
- ✅ Imágenes de fondo por slide (`<!-- BACKGROUND: ruta -->`)
- ✅ Notas del presentador (`<!-- NOTES -->`)
- ✅ Columnas (`$COLUMNS$`, `$COL$`, `$END$`)
- ✅ Grids (`$GRID$`, `$ROW$`, `$CELL$`, `$END$`)
- ✅ Markdown completo (encabezados, listas, negritas, imágenes, etc.)

### Ejemplo completo

```bash
# 1. Crear presentación
mkdir mi-presentacion
mkdir mi-presentacion/images

# 2. Editar contenido
nano mi-presentacion/contenidos.md

# 3. Añadir imágenes
cp foto.png mi-presentacion/images/

# 4. Generar standalone
./build.sh mi-presentacion

# 5. Abrir en navegador
firefox mi-presentacion/index.html

# Output esperado:
# 📦 Construyendo presentación: mi-presentacion
#    ✓ Metadata parseada
#    ✓ 5 slides procesadas
#    ✓ Generado: mi-presentacion/index.html
# ✅ Build completado exitosamente
```

## Generar Notas para Imprimir

El sistema incluye un generador de notas que crea un documento HTML optimizado para imprimir en formato tarjeta postal, ideal para llevar tus notas del presentador en formato físico durante la presentación.

### ¿Qué hace el generador de notas?

El comando genera un archivo `notas.html` dentro de la carpeta de tu presentación que:
- **Formato tarjeta postal**: Tamaño ~A6 (280px altura), perfecto para llevar en mano
- **Información completa**: Número de slide, título extraído automáticamente y notas del presentador
- **Colores de tu presentación**: Usa los colores definidos en tu YAML para mantener coherencia visual
- **Optimizado para impresión**: Diseñado para imprimir 2 tarjetas por página
- **Numeración inteligente**: Incluye subslides (ej: #1, #2, #4.1, #4.2)
- **Solo slides con notas**: Genera tarjetas únicamente para las slides que tienen `<!-- NOTES -->`

### Cómo usar el generador

```bash
./generate-notes.sh nombre-presentacion
```

**Ejemplo:**
```bash
./generate-notes.sh equipazgo
```

Este comando:
1. Lee el archivo `equipazgo/contenidos.md`
2. Extrae todas las slides que tienen notas (`<!-- NOTES -->`)
3. Para cada slide, extrae el título automáticamente del contenido
4. Genera `equipazgo/notas.html` con tarjetas listas para imprimir

### Requisitos

- **Python 3.x**
- **PyYAML**: Instalar con `pip3 install pyyaml`

### Estructura después de generar notas

```
equipazgo/
├── contenidos.md          # Fuente original
├── index.html            # Presentación standalone (si ejecutaste build)
├── notas.html            # Notas para imprimir ✨ NUEVO
└── images/               # Imágenes
```

### Cómo imprimir las notas

**1. Abrir en navegador:**
```bash
firefox equipazgo/notas.html
```

**2. Imprimir (Ctrl+P / Cmd+P):**
- **Recomendado**: Configurar impresión a "2 tarjetas por página"
- **Orientación**: Vertical (portrait)
- **Márgenes**: Normales o mínimos

**3. Alternativa - Una tarjeta por página:**
- Útil para tarjetas más grandes y legibles
- Ideal si tienes muchas notas por slide

### Características de las tarjetas

Cada tarjeta incluye:

```
┌─────────────────────────────────┐
│ #4.1  ¿Qué es el equipazgo?    │ ← Número y título
├─────────────────────────────────┤
│                                 │
│ Cuando trabajamos en equipo    │
│ como developers, ¿cada uno      │ ← Notas del presentador
│ hace lo suyo o nos              │   formateadas
│ coordinamos?                    │
│                                 │
│ ...                             │
└─────────────────────────────────┘
```

### Ventajas de usar notas impresas

- ✅ **No dependes de dispositivos**: No necesitas laptop o tablet durante la presentación
- ✅ **Fácil consulta rápida**: Mira tus notas sin interrumpir el flujo visual
- ✅ **Backup confiable**: Si falla la tecnología, tus notas siguen ahí
- ✅ **Profesional**: Llevar tarjetas físicas se ve más natural que mirar un dispositivo
- ✅ **Numeradas**: Sabes exactamente en qué slide estás (#1, #2.1, etc.)
- ✅ **Portátiles**: Formato tarjeta postal fácil de llevar y consultar

### Ejemplo de uso completo

```bash
# 1. Crear presentación con notas
nano equipazgo/contenidos.md

# Añadir notas a tus slides:
# <!-- NOTES -->
# Puntos clave a mencionar durante la presentación...

# 2. Generar notas para imprimir
./generate-notes.sh equipazgo

# Output:
# 📝 Generando notas para: equipazgo
#    ✓ Metadata parseada
#    ✓ 7 slides con notas encontradas
#    ✓ Generado: equipazgo/notas.html
# ✅ Notas generadas exitosamente
#
# 🖨️  Abre en navegador e imprime: equipazgo/notas.html
# 💡 Tip: Configura impresión a 2 tarjetas por página

# 3. Abrir y revisar
firefox equipazgo/notas.html

# 4. Imprimir (Ctrl+P)
# - Selecciona impresora
# - Configura 2 páginas por hoja (recomendado)
# - Imprime

# 5. Presentar con confianza 🎤
```

### Personalización del formato

El documento generado incluye:
- **Diseño responsive**: Se adapta a pantalla e impresión automáticamente
- **Grid flexible**: 2 columnas en impresión, adaptable en pantalla
- **Estilos de impresión**: Optimizados específicamente para papel
- **Colores de tu presentación**: Mantiene la identidad visual

### Cuándo usar notas impresas

**Usa notas impresas cuando:**
- Presentas en un lugar sin garantía de conectividad
- Quieres tener un backup físico de seguridad
- Prefieres no depender de dispositivos durante la presentación
- Das una presentación importante y quieres máxima preparación
- El venue no permite laptops/tablets en el escenario

**Combina con vista del presentador cuando:**
- Tienes dos pantallas disponibles
- Quieres las notas también en digital (presiona `S` en la presentación)
- Las notas impresas son el backup y la vista digital es primaria

## Guía de Diseño Visual

### Consejos de diseño:

1. **Colores coherentes**: Asegúrate de que los colores en la metadata combinen bien
2. **Imágenes de fondo efectivas**:
   - Usa imágenes con suficiente contraste para que el texto sea legible
   - Considera oscurecer o desenfocar imágenes muy detalladas
   - Mantén consistencia visual entre slides relacionadas
   - Usa `template.webp` para fondo global e imágenes específicas solo cuando añadan valor

### Personalización Avanzada

Si necesitas estilos personalizados, puedes definir colores en la metadata:

```yaml
colors:
  main-color: "#Tu-Color"
  background: "#Tu-Fondo"
  heading-color: "#Tu-Color-Títulos"
```
