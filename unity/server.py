# serve.py — 放在构建输出目录(与 index.html 同级)
import http.server, socketserver, os

PORT = 8000

CONTENT_TYPES = {
    ".js": "application/javascript",
    ".wasm": "application/wasm",
    ".data": "application/octet-stream",
    ".symbols.json": "application/octet-stream",
}

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 1. secure context 必需的三个头
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cross-Origin-Resource-Policy", "cross-origin")
        # 2. .br 文件加 Content-Encoding
        path = self.path.split("?")[0]
        if path.endswith(".br"):
            self.send_header("Content-Encoding", "br")
        super().end_headers()

    def guess_type(self, path):
        # 让 foo.wasm.br 返回正确的内层 MIME 类型
        if path.endswith(".br"):
            inner = os.path.splitext(path[:-3])[1]
            return CONTENT_TYPES.get(inner, "application/octet-stream")
        return super().guess_type(path)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving on http://localhost:{PORT}")
    httpd.serve_forever()