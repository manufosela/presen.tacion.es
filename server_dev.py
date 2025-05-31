from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import json

class DevHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Añade cabeceras para deshabilitar caché
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        if self.path == '/last-modified':
            files = [
                'presentacion.html',
                'mi-presentacion/contenidos.md'
            ]
            try:
                last_mod = max(os.path.getmtime(f) for f in files)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
                return
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'last_modified': last_mod}).encode())
        else:
            super().do_GET()

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), DevHandler)
    print("[DEV] Serving at http://localhost:8000 (con recarga automática)")
    server.serve_forever() 