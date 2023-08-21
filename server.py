import http.server
import socketserver

PORT = 8000

class FileUploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        file_content = self.rfile.read(content_length)

        with open('received_file.txt', 'wb') as f:
            f.write(file_content)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'File received successfully')

with socketserver.TCPServer(("", PORT), FileUploadHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
