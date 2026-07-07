"""Almasna Altaswiqi brief factory as a local HTTP service.

``POST /api/brief`` accepts ``{"text": "...", "brand": "..."}`` and returns a
complete content brief: keywords, angle, title, meta, channel, CTA, outline
and quality score — the schema downstream publishers consume.
"""

from __future__ import annotations

from http.server import ThreadingHTTPServer
from typing import Any

from .core import content_brief
from .http_base import BaseServiceHandler, build_server


def _brief_route(data: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    text = str(data.get("text") or "").strip()
    if not text:
        return 400, {"ok": False, "error": "missing 'text'"}
    brand = str(data.get("brand") or "CarbonFlow")
    return 200, {"ok": True, **content_brief(text, brand=brand)}


class Handler(BaseServiceHandler):
    post_routes = {"/api/brief": staticmethod(_brief_route)}


def create_server(host: str | None = None, port: int | None = None) -> ThreadingHTTPServer:
    return build_server(Handler, host=host, port=port)


def run_server(host: str | None = None, port: int | None = None) -> None:
    from .version import __version__

    server = create_server(host=host, port=port)
    print(f"almasna service v{__version__}: http://{server.server_address[0]}:{server.server_address[1]}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
