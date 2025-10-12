#!/bin/bash

# Script para generar index.html capturando el HTML renderizado automáticamente
# Usa Chrome headless para renderizar la presentación y capturar el código fuente

if [ -z "$1" ]; then
    echo "❌ Error: Debes especificar el nombre de la presentación"
    echo ""
    echo "Uso: ./build.sh <nombre-presentacion>"
    echo ""
    echo "Ejemplo:"
    echo "  ./build.sh equipazgo"
    exit 1
fi

PRESENTATION_NAME="$1"
PRESENTATION_PATH="./$PRESENTATION_NAME"

# Verificar que existe la presentación
if [ ! -d "$PRESENTATION_PATH" ]; then
    echo "❌ Error: La carpeta '$PRESENTATION_NAME' no existe"
    exit 1
fi

echo "📦 Generando HTML para: $PRESENTATION_NAME"

# Verificar que existe Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Verificar que existe Chrome
if ! command -v google-chrome &> /dev/null; then
    echo "❌ Error: Google Chrome no está instalado"
    echo "   Necesario para renderizar la presentación automáticamente"
    exit 1
fi

# Iniciar servidor temporal
PORT=8765

echo "🌐 Iniciando servidor temporal en puerto $PORT..."

# Iniciar servidor en background
python3 -m http.server $PORT > /dev/null 2>&1 &
SERVER_PID=$!

# Esperar a que el servidor esté listo
sleep 2

# URL de la presentación
URL="http://localhost:$PORT/presentacion.html?presentacion=$PRESENTATION_NAME"

echo "🔄 Capturando HTML desde: $URL"
echo "⏳ Renderizando presentación con Chrome headless..."

# Capturar HTML renderizado con Chrome headless
# Esperamos 5 segundos para que cargue completamente (Reveal.js, marked.js, etc)
TEMP_HTML=$(mktemp)

timeout 15 google-chrome --headless --disable-gpu --no-sandbox \
    --virtual-time-budget=5000 \
    --dump-dom "$URL" > "$TEMP_HTML" 2>/dev/null

# Verificar que se capturó contenido
if [ ! -s "$TEMP_HTML" ]; then
    echo "❌ Error: No se pudo capturar el HTML"
    kill $SERVER_PID 2>/dev/null
    rm "$TEMP_HTML"
    exit 1
fi

# Guardar en el destino
OUTPUT_PATH="$PRESENTATION_PATH/index.html"
mv "$TEMP_HTML" "$OUTPUT_PATH"

# Detener servidor
kill $SERVER_PID 2>/dev/null

# Verificar resultado
if [ -f "$OUTPUT_PATH" ]; then
    FILE_SIZE=$(du -h "$OUTPUT_PATH" | cut -f1)
    echo "✓ HTML capturado y guardado"
    echo "✅ Build completado exitosamente"
    echo ""
    echo "📄 Generado: $OUTPUT_PATH ($FILE_SIZE)"
    echo ""
    echo "🌐 Para ver la presentación:"
    echo "   firefox $OUTPUT_PATH"
else
    echo "❌ Error: No se pudo guardar el archivo"
    exit 1
fi
