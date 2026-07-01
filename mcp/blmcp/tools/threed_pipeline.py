# SPDX-License-Identifier: GPL-3.0-or-later

"""
Text -> 3D pipeline tools (async), driving the n8n webhooks.

These tools do NOT touch Blender; they call the n8n pipeline over HTTP:
  * generate_3d      -> POST /webhook/generate-3d    (returns job handles fast)
  * wait_for_3d_job  -> POST /webhook/3d-job-status  (polls until the .glb is ready)

Then feed the resulting glb_url to ``import_canonical_model`` to bring the model
into the Blender scene.

Config (environment variables on the MCP server):
  * THREED_WEBHOOK_BASE     default "https://n8n.aifounders.cz"
  * THREED_WEBHOOK_API_KEY  sent as the "X-API-Key" header (gate); optional
                            until the n8n webhook gate is enabled.
"""

__all__ = (
    "register",
)

import json
import os
import time
import urllib.error
import urllib.request

from dotenv import load_dotenv  # pylint: disable=import-error
from mcp.server.fastmcp import FastMCP  # pylint: disable=import-error,no-name-in-module
from mcp.types import ToolAnnotations  # pylint: disable=import-error,no-name-in-module

# Load a repo-local .env (mcp/.env) as a FALLBACK only — real environment
# variables always take precedence (load_dotenv default: override=False). So in
# production the host-injected env wins and the .env is ignored/absent; locally
# it supplies the secret the MSIX Claude Desktop host fails to pass. 12-factor.
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env"))

_FAILED_STATES = ("failed", "error", "cancelled")


def _config() -> tuple[str, str]:
    base = os.environ.get("THREED_WEBHOOK_BASE", "https://n8n.aifounders.cz").rstrip("/")
    key = os.environ.get("THREED_WEBHOOK_API_KEY", "")
    return base, key


def _post(url: str, payload: dict, api_key: str, timeout: float) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    if api_key:
        req.add_header("X-API-Key", api_key)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as ex:
        body = ex.read().decode("utf-8", errors="replace")
        return {"error": True, "http_status": ex.code, "body": body}
    except (urllib.error.URLError, TimeoutError, ValueError) as ex:
        return {"error": True, "message": str(ex)}


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        annotations=ToolAnnotations(title="Generate 3D (async)")
    )
    def generate_3d(prompt: str, image_model: str = "") -> dict[str, object]:
        """
        Start text-to-3D generation via the n8n pipeline (async).

        Returns immediately with ``job_id``, ``status_url`` and ``response_url``.
        Pass ``status_url`` + ``response_url`` to ``wait_for_3d_job`` to get the
        finished ``glb_url``, then ``import_canonical_model(glb_url)`` to bring it
        into the scene.

        *prompt* should describe ONLY the object (e.g. "a rusty iron lantern").
        The isolation/background instructions are added server-side.
        """
        base, key = _config()
        return _post(base + "/webhook/generate-3d",
                     {"prompt": prompt, "image_model": image_model}, key, timeout=120.0)

    @mcp.tool(
        annotations=ToolAnnotations(title="Wait for 3D Job", readOnlyHint=True)
    )
    def wait_for_3d_job(
        status_url: str,
        response_url: str,
        timeout_seconds: int = 300,
        poll_interval: float = 6.0,
    ) -> dict[str, object]:
        """
        Poll a 3D generation job (from ``generate_3d``) until the model is ready.

        Returns ``{"status": "completed", "glb_url": ...}`` on success — feed the
        ``glb_url`` to ``import_canonical_model``. Returns a ``timeout`` or
        ``failed`` status otherwise.
        """
        base, key = _config()
        url = base + "/webhook/3d-job-status"
        deadline = time.monotonic() + float(timeout_seconds)
        last: dict = {}
        while time.monotonic() < deadline:
            resp = _post(url, {"status_url": status_url, "response_url": response_url}, key, timeout=40.0)
            last = resp
            if resp.get("error"):
                return {"status": "error", "detail": resp}
            state = str(resp.get("status", "")).lower()
            if state == "completed" and resp.get("glb_url"):
                return {"status": "completed", "glb_url": resp["glb_url"]}
            if state in _FAILED_STATES:
                return {"status": "failed", "detail": resp}
            time.sleep(poll_interval)
        return {"status": "timeout", "last": last}
