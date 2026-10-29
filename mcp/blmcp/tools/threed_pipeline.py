# SPDX-License-Identifier: GPL-3.0-or-later

"""
Text -> 3D and image -> 3D pipeline tools (async), driving the n8n webhooks.

These tools do NOT touch Blender; they call the n8n pipeline over HTTP:
  * generate_3d      -> POST /webhook/generate-3d    (returns job handles fast)
  * wait_for_3d_job  -> POST /webhook/3d-job-status  (polls until the .glb is ready)

generate_3d request body (JSON):
  * text mode:   {"prompt": str, "image_model": str}   (unchanged since the first version)
  * image mode:  {"prompt": str, "image_url": str}     image_url = http(s) URL or
                 data:image/...;base64 URI; prompt is only a label. Needs the
                 "Has Input Image?" branch of ../../n8n/generate-3d.workflow.json.

Then feed the resulting glb_url to ``import_canonical_model`` to bring the model
into the Blender scene.

Config (environment variables on the MCP server; see mcp/.env.example and the
importable workflows in ../../n8n/). This MCP ships no default host:
  * THREED_WEBHOOK_BASE     base URL of YOUR n8n instance (required, no default).
  * THREED_WEBHOOK_API_KEY  sent as the "X-API-Key" header (the gate secret).
"""

__all__ = (
    "register",
)

import base64
import binascii
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

# Input images (image mode). A local file is sent inline as a data: URI, so it
# must fit n8n's default webhook payload cap (N8N_PAYLOAD_SIZE_MAX = 16 MiB):
# 8 MiB of image is ~10.7 MiB of base64.
_IMAGE_MIME_BY_EXT = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}
_IMAGE_MAX_BYTES = 8 * 1024 * 1024
_IMAGE_MAX_MB = _IMAGE_MAX_BYTES // (1024 * 1024)
_IMAGE_TYPES_TEXT = ".png, .jpg/.jpeg or .webp"


def _sniff_image_mime(data: bytes) -> str:
    # Content check, so a renamed or broken file fails here, not at fal.
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    return ""


def _check_image_bytes(data: bytes, mime: str, what: str) -> None:
    if not data:
        raise ValueError("{:s} is empty.".format(what))
    if len(data) > _IMAGE_MAX_BYTES:
        raise ValueError("{:s} is {:.1f} MB; the limit is {:d} MB (n8n webhook payload cap).".format(
            what, len(data) / (1024 * 1024), _IMAGE_MAX_MB))
    sniffed = _sniff_image_mime(data)
    if sniffed != mime:
        raise ValueError("{:s} is declared as {:s} but its content is {:s}.".format(
            what, mime, sniffed or "not a PNG, JPEG or WEBP image"))


def _check_data_uri(uri: str) -> None:
    header, sep, payload = uri.partition(",")
    mime = header[len("data:"):].lower()
    if not sep or not mime.endswith(";base64"):
        raise ValueError("image data: URI must look like data:image/png;base64,<data>.")
    mime = mime[:-len(";base64")]
    if mime not in _IMAGE_MIME_BY_EXT.values():
        raise ValueError("image data: URI type {:s} is not supported; use image/png, image/jpeg or image/webp.".format(
            mime or "(none)"))
    # Size guard before decoding: base64 is 4 characters per 3 bytes.
    if len(payload) > (_IMAGE_MAX_BYTES // 3 + 1) * 4:
        raise ValueError("image data: URI is larger than {:d} MB (n8n webhook payload cap).".format(_IMAGE_MAX_MB))
    try:
        data = base64.b64decode(payload, validate=True)
    except (binascii.Error, ValueError) as ex:
        raise ValueError("image data: URI is not valid base64 ({:s}).".format(str(ex))) from ex
    _check_image_bytes(data, mime, "image data: URI")


def _local_image_to_data_uri(path: str) -> str:
    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        raise ValueError(
            "image file not found: {:s} (give a local file path, an http(s) URL or a data: URI).".format(path))
    ext = os.path.splitext(path)[1].lower()
    mime = _IMAGE_MIME_BY_EXT.get(ext)
    if mime is None:
        raise ValueError("image file type {:s} is not supported; use {:s}.".format(ext or "(none)", _IMAGE_TYPES_TEXT))
    size = os.path.getsize(path)
    if size > _IMAGE_MAX_BYTES:
        raise ValueError("image file is {:.1f} MB; the limit is {:d} MB (n8n webhook payload cap).".format(
            size / (1024 * 1024), _IMAGE_MAX_MB))
    with open(path, "rb") as fh:
        data = fh.read()
    _check_image_bytes(data, mime, "image file {:s}".format(os.path.basename(path)))
    return "data:{:s};base64,{:s}".format(mime, base64.b64encode(data).decode("ascii"))


def _image_to_url(image: str) -> str:
    """
    Return the ``image_url`` value for *image* (http(s) URL, data: URI or local
    path). Raise ``ValueError`` with a readable message when it is unusable.
    """
    lower = image.lower()
    if lower.startswith(("http://", "https://")):
        return image
    if lower.startswith("data:"):
        _check_data_uri(image)
        return image
    return _local_image_to_data_uri(image)


def _config() -> tuple[str, str]:
    # No default host: this MCP is instance-agnostic. Point THREED_WEBHOOK_BASE
    # at YOUR n8n (importing the workflows in ../n8n/). See mcp/.env.example.
    base = os.environ.get("THREED_WEBHOOK_BASE", "").rstrip("/")
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
    def generate_3d(prompt: str = "", image_model: str = "", image: str = "") -> dict[str, object]:
        """
        Start 3D generation (TRELLIS) via the n8n pipeline (async). Two modes:

        * Text mode (no *image*): *prompt* describes ONLY the object (e.g. "a
          rusty iron lantern"). The server wraps it in a product-shot prompt
          (isolated object, plain light-grey background), renders that image with
          *image_model* (default google/gemini-2.5-flash-image) and sends the
          image to TRELLIS.
        * Image mode (*image* given): your image goes straight to TRELLIS; no
          image is generated and *image_model* is ignored. *image* is a local
          file path (.png, .jpg/.jpeg or .webp, at most 8 MB; sent inline as a
          data: URI), a public http(s) URL that fal can fetch without auth, or a
          ``data:image/png|jpeg|webp;base64,...`` URI. *prompt* is optional here
          and only sent as a label. Best input: one whole object, centred, on a
          plain light background, no other objects.

        Characters: TRELLIS builds the mesh in exactly the pose it sees, so state
        the pose precisely, as the target skeleton's bind pose in degrees, e.g.
        "T-pose: arms straight out to the sides at 90 degrees from the body,
        palms down, legs straight, feet shoulder-width apart, facing the camera"
        or "A-pose: arms 45 degrees below horizontal". In text mode put this in
        *prompt*; in image mode the image itself must already show that pose.

        Returns immediately with ``job_id``, ``status_url`` and ``response_url``.
        Pass ``status_url`` + ``response_url`` to ``wait_for_3d_job`` to get the
        finished ``glb_url``, then ``import_canonical_model(glb_url)`` to bring it
        into the scene.

        Image mode needs the n8n workflow with the "Has Input Image?" branch
        (n8n/README.md); an older workflow ignores *image* and runs text mode
        on *prompt* instead.
        """
        base, key = _config()
        if not base:
            return {"error": True, "message": "THREED_WEBHOOK_BASE is not set - point it at your n8n instance (see mcp/.env.example)."}
        image = image.strip()
        if image:
            try:
                image_url = _image_to_url(image)
            except ValueError as ex:
                return {"error": True, "message": str(ex)}
            return _post(base + "/webhook/generate-3d",
                         {"prompt": prompt, "image_url": image_url}, key, timeout=120.0)
        if not prompt.strip():
            return {"error": True, "message": "Give a prompt (text mode) or an image (image mode)."}
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
        if not base:
            return {"status": "error", "message": "THREED_WEBHOOK_BASE is not set - point it at your n8n instance (see mcp/.env.example)."}
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
