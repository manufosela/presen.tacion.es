#!/bin/bash

# Generar los archivos necesarios
python3 generate.py

# Lanzar el servidor de desarrollo con recarga automática
python3 server_dev.py 