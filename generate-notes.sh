#!/bin/bash

# Script para generar notas de presentación en formato imprimible

if [ -z "$1" ]; then
    echo "❌ Error: Debes especificar el nombre de la presentación"
    echo ""
    echo "Uso: ./generate-notes.sh <nombre-presentacion>"
    echo ""
    echo "Ejemplo:"
    echo "  ./generate-notes.sh equipazgo"
    exit 1
fi

PRESENTATION_NAME="$1"

# Verificar que existe Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Ejecutar el generador
python3 generate-notes.py "$PRESENTATION_NAME"
