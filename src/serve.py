import http.server, os, sys, urllib.parse
ROOT = os.path.abspath(sys.argv[1])
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
        f = os.path.join(ROOT, p.lstrip("/"))
        if p == "/": return os.path.join(ROOT, "index.html")
        if os.path.isfile(f): return f
        if os.path.isfile(f + ".html"): return f + ".html"
        return os.path.join(ROOT, "__missing__")
    def send_error(self, code, *a, **k):
        if code == 404:
            body = open(os.path.join(ROOT, "404.html"), "rb").read()
            self.send_response(404); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers(); self.wfile.write(body)
        else: super().send_error(code, *a, **k)
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(("127.0.0.1", 8765), H).serve_forever()
