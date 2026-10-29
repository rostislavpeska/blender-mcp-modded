# SPDX-License-Identifier: GPL-3.0-or-later

"""
Sketchfab tools: search public models, preview one, and resolve a downloadable
model to a temporary file URL for import_canonical_model.

- sketchfab_search / sketchfab_preview call Sketchfab's PUBLIC API directly (no
  auth, no n8n).
- sketchfab_download calls the gated n8n `sketchfab-download` webhook, which
  holds the Sketchfab API token and returns a short-lived model URL. Feed the
  returned glb_url to import_canonical_model (it handles the glTF ZIP too).

Config (shared with the text->3D tools; see mcp/.env.example):
  * THREED_WEBHOOK_BASE     base URL of your n8n instance (required for download)
  * THREED_WEBHOOK_API_KEY  the "X-API-Key" gate secret
"""

__all__ = ("register",)

import json
import os
import urllib.error
import urllib.parse
import urllib.request

from dotenv import load_dotenv  # pylint: disable=import-error
from mcp.server.fastmcp import FastMCP, Image  # pylint: disable=import-error,no-name-in-module
from mcp.types import ToolAnnotations  # pylint: disable=import-error,no-name-in-module

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env"))

_SEARCH_URL = "https://api.sketchfab.com/v3/search"


def _config() -> tuple[str, str]:
    base = os.environ.get("THREED_WEBHOOK_BASE", "").rstrip("/")
    key = os.environ.get("THREED_WEBHOOK_API_KEY", "")
    return base, key


def _get_json(url: str, timeout: float = 30.0) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as ex:
        return {"error": True, "http_status": ex.code, "body": ex.read().decode("utf-8", errors="replace")}
    except (urllib.error.URLError, TimeoutError, ValueError) as ex:
        return {"error": True, "message": str(ex)}


def _pick_thumbnail(result: dict) -> str | None:
    images = ((result.get("thumbnails") or {}).get("images")) or []
    if not images:
        return None
    images = sorted(images, key=lambda i: i.get("width", 0))
    for img in images:
        if img.get("width", 0) >= 640:
            return img.get("url")
    return images[-1].get("url")


def register(mcp: FastMCP) -> None:
    @mcp.tool(annotations=ToolAnnotations(title="Sketchfab Search", readOnlyHint=True))
    def sketchfab_search(query: str, downloadable: bool = True, limit: int = 12) -> dict[str, object]:
        """
        Search Sketchfab for 3D models (public API). Returns candidates, each with
        uid, name, a preview thumbnail_url, license, faces, downloadable and
        viewer_url. Then sketchfab_preview(thumbnail_url) to see one, and
        sketchfab_download(uid) + import_canonical_model(glb_url) to bring it in.
        """
        params = {"type": "models", "q": query, "count": max(1, min(24, int(limit)))}
        if downloadable:
            params["downloadable"] = "true"
        data = _get_json(_SEARCH_URL + "?" + urllib.parse.urlencode(params))
        if data.get("error"):
            return data
        out = []
        for r in data.get("results", []):
            lic = r.get("license") or {}
            out.append({
                "uid": r.get("uid"),
                "name": r.get("name"),
                "thumbnail_url": _pick_thumbnail(r),
                "license": lic.get("label") if isinstance(lic, dict) else lic,
                "faces": r.get("faceCount"),
                "downloadable": r.get("isDownloadable"),
                "viewer_url": r.get("viewerUrl"),
            })
        return {"count": len(out), "results": out}

    @mcp.tool(annotations=ToolAnnotations(title="Sketchfab Preview", readOnlyHint=True))
    def sketchfab_preview(thumbnail_url: str) -> Image:
        """
        Fetch a Sketchfab model's preview thumbnail (the thumbnail_url from
        sketchfab_search) and return it as an image, so you can judge a model
        before importing it.
        """
        with urllib.request.urlopen(urllib.request.Request(thumbnail_url), timeout=30) as resp:
            data = resp.read()
        fmt = "png" if thumbnail_url.lower().split("?")[0].endswith(".png") else "jpeg"
        return Image(data=data, format=fmt)

    @mcp.tool(annotations=ToolAnnotations(title="Sketchfab Download"))
    def sketchfab_download(uid: str) -> dict[str, object]:
        """
        Resolve a downloadable Sketchfab model (by uid from sketchfab_search) to a
        short-lived model URL via the gated n8n webhook (which holds the Sketchfab
        token). Returns {glb_url, is_zip}. Feed glb_url to import_canonical_model
        (it unpacks the glTF ZIP automatically).
        """
        base, key = _config()
        if not base:
            return {"error": True, "message": "THREED_WEBHOOK_BASE not set (see mcp/.env.example)."}
        payload = json.dumps({"uid": uid}).encode("utf-8")
        req = urllib.request.Request(base + "/webhook/sketchfab-download", data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        if key:
            req.add_header("X-API-Key", key)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8") or "{}")
        except urllib.error.HTTPError as ex:
            return {"error": True, "http_status": ex.code, "body": ex.read().decode("utf-8", errors="replace")}
        except (urllib.error.URLError, TimeoutError, ValueError) as ex:
            return {"error": True, "message": str(ex)}
