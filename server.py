
from http.server import SimpleHTTPRequestHandler
from main import create_map
import socketserver


class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            return super().do_GET()

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        create_map()

        self.wfile.write(bytes('<img src="latest_screenshot.png">', 'utf8'))


def run():
    port = 8000
    with socketserver.TCPServer(('', port), RequestHandler) as httpd:
        print('Serving at port', port)
        httpd.serve_forever()


if __name__ == '__main__':
    run()
