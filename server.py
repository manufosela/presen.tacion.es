import http.server
import socketserver
import os
from urllib.parse import urlparse, parse_qs
import socket

def find_free_port(start_port=3000, max_port=3010):
    for port in range(start_port, max_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise RuntimeError('No se encontró ningún puerto disponible')

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parsear la URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        # Si es la ruta raíz, servir index.html
        if path == '/':
            self.serve_file('index.html')
            return

        # Si es /presentacion, servir presentacion.html
        if path == '/presentacion':
            self.serve_file('presentacion.html')
            return

        # Para cualquier otra ruta, intentar servir el archivo directamente
        self.serve_file(path.lstrip('/'))

    def serve_file(self, filepath):
        try:
            # Si el archivo existe, servirlo
            if os.path.exists(filepath):
                self.send_response(200)
                # Determinar el tipo de contenido
                if filepath.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                elif filepath.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif filepath.endswith('.md'):
                    self.send_header('Content-type', 'text/markdown')
                elif filepath.endswith('.html'):
                    self.send_header('Content-type', 'text/html')
                elif filepath.endswith('.webp'):
                    self.send_header('Content-type', 'image/webp')
                elif filepath.endswith('.png'):
                    self.send_header('Content-type', 'image/png')
                elif filepath.endswith('.jpg') or filepath.endswith('.jpeg'):
                    self.send_header('Content-type', 'image/jpeg')
                else:
                    self.send_header('Content-type', 'application/octet-stream')
                
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")
        except Exception as e:
            print(f"Error serving {filepath}: {str(e)}")
            self.send_error(500, "Internal server error")

def run_server():
    port = find_free_port()
    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        print(f"Servidor corriendo en http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server() 