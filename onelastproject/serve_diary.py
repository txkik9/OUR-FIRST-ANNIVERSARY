"""Serve only the anniversary page and its known assets on this computer."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent
PORT = 9871
ALLOWED = {
    '/letmecheck.html',
    '/assets/fonts/Mali-Regular.ttf',
    '/assets/fonts/OFL-Mali.txt',
    *(f'/assets/photos/memory-{number}.png' for number in range(1, 7)),
}


class DiaryHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_head(self):
        requested = unquote(urlsplit(self.path).path)
        if requested == '/':
            requested = '/letmecheck.html'
        if requested not in ALLOWED:
            self.send_error(404)
            return None
        self.path = requested
        return super().send_head()

    def list_directory(self, path):
        self.send_error(404)
        return None

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        super().end_headers()


if __name__ == '__main__':
    print(f'Open http://127.0.0.1:{PORT}/letmecheck.html', flush=True)
    print('Only the diary HTML, six photos, and font are available. Ctrl+C to stop.', flush=True)
    with ThreadingHTTPServer(('127.0.0.1', PORT), DiaryHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
