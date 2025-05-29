#!/bin/bash

echo "🚀 Generando index.html..."
python3 generate.py

echo "🌐 Iniciando servidor..."
python3 server.py 