#!/usr/bin/env python3
"""Minimal static file server for local preview.

Used instead of `python3 -m http.server` because that CLI evaluates
`os.getcwd()` at import time (argparse default), which is blocked in the
sandboxed preview environment. We serve a fixed, absolute directory instead.
"""
import functools
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8099"))

handler = functools.partial(SimpleHTTPRequestHandler, directory=ROOT)
with ThreadingHTTPServer(("127.0.0.1", PORT), handler) as httpd:
    print(f"Serving {ROOT} at http://127.0.0.1:{PORT}")
    httpd.serve_forever()
