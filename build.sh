#!/bin/bash

# Build script para generar presentaciones standalone

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

# Verificar que existe Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Ejecutar el build
python3 build.py "$PRESENTATION_NAME"
