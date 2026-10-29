# SPDX-FileCopyrightText: 2026 Blender Authors
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tests for the text/image -> 3D pipeline tools (``blmcp/tools/threed_pipeline.py``)
and the shipped n8n workflow export they call (``n8n/generate-3d.workflow.json``).

No network, no n8n, no Blender: the HTTP post is mocked. Run with::

    python -m unittest tests.test_threed_pipeline -v
"""

__all__ = ()

import base64
import importlib
import json
import os
import sys
import tempfile
import unittest
from typing import Any, Callable
from unittest import mock

# Root of the repository.
_REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MCP_DIR = os.path.join(_REPO_DIR, "mcp")
_WORKFLOW_PATH = os.path.join(_REPO_DIR, "n8n", "generate-3d.workflow.json")

_BASE = "https://n8n.example.test"
_TEST_KEY = "unit-test-key"
_JOB = {"job_id": "job-1", "status_url": "s", "response_url": "r", "status": "queued"}

_PNG_BYTES = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32
_JPEG_BYTES = b"\xff\xd8\xff\xe0" + b"\x00" * 32
_WEBP_BYTES = b"RIFF\x24\x00\x00\x00WEBPVP8 " + b"\x00" * 32


def _import_pipeline() -> Any:
    if _MCP_DIR not in sys.path:
        sys.path.insert(0, _MCP_DIR)
    return importlib.import_module("blmcp.tools.threed_pipeline")


class _FakeMCP:
    """
    Collects the functions registered with ``@mcp.tool(...)``.
    """

    def __init__(self) -> None:
        self.tools: dict[str, Callable[..., Any]] = {}

    def tool(self, **_kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
            self.tools[fn.__name__] = fn
            return fn
        return deco


class _FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._raw = json.dumps(payload).encode("utf-8")

    def read(self) -> bytes:
        return self._raw

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None


class TestGenerate3d(unittest.TestCase):
    """
    ``generate_3d``: text mode body unchanged, image mode body, input checks.
    """

    def setUp(self) -> None:
        self.module = _import_pipeline()
        fake = _FakeMCP()
        self.module.register(fake)
        self.generate_3d = fake.tools["generate_3d"]
        self.requests: list[Any] = []

        def fake_urlopen(req: Any, timeout: float = 0.0) -> _FakeResponse:
            self.requests.append(req)
            return _FakeResponse(_JOB)

        patches = [
            mock.patch.object(self.module.urllib.request, "urlopen", side_effect=fake_urlopen),
            mock.patch.dict(os.environ, {"THREED_WEBHOOK_BASE": _BASE, "THREED_WEBHOOK_API_KEY": _TEST_KEY}),
        ]
        for patcher in patches:
            patcher.start()
            self.addCleanup(patcher.stop)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    # -----------------------------------------------------------------
    # Helpers.

    def _file(self, name: str, data: bytes) -> str:
        path = os.path.join(self.tmp.name, name)
        with open(path, "wb") as fh:
            fh.write(data)
        return path

    def _sent_body(self) -> dict[str, Any]:
        self.assertEqual(len(self.requests), 1, "expected exactly one POST")
        req = self.requests[0]
        self.assertEqual(req.full_url, _BASE + "/webhook/generate-3d")
        self.assertEqual(req.get_method(), "POST")
        self.assertEqual(req.get_header("X-api-key"), _TEST_KEY)
        self.assertEqual(req.get_header("Content-type"), "application/json")
        body = json.loads(req.data.decode("utf-8"))
        assert isinstance(body, dict)
        return body

    def _assert_refused(self, result: dict[str, object], *fragments: str) -> None:
        self.assertEqual(self.requests, [], "nothing may be sent when the input is refused")
        self.assertIs(result.get("error"), True)
        message = str(result.get("message", ""))
        for fragment in fragments:
            self.assertIn(fragment, message)

    # -----------------------------------------------------------------
    # Text mode: the request body is exactly what it always was.

    def test_text_mode_body_unchanged(self) -> None:
        result = self.generate_3d("a rusty iron lantern")
        self.assertEqual(result, _JOB)
        self.assertEqual(self._sent_body(), {"prompt": "a rusty iron lantern", "image_model": ""})

    def test_text_mode_passes_image_model(self) -> None:
        self.generate_3d("a barrel", image_model="openai/gpt-image-1")
        self.assertEqual(self._sent_body(), {"prompt": "a barrel", "image_model": "openai/gpt-image-1"})

    def test_blank_image_is_text_mode(self) -> None:
        self.generate_3d("a barrel", image="   ")
        self.assertEqual(self._sent_body(), {"prompt": "a barrel", "image_model": ""})

    def test_needs_prompt_or_image(self) -> None:
        self._assert_refused(self.generate_3d(), "prompt", "image")
        self._assert_refused(self.generate_3d("   "), "prompt", "image")

    def test_missing_base_url_is_refused(self) -> None:
        with mock.patch.dict(os.environ, {"THREED_WEBHOOK_BASE": ""}):
            self._assert_refused(self.generate_3d("a barrel"), "THREED_WEBHOOK_BASE")

    # -----------------------------------------------------------------
    # Image mode: local files.

    def test_local_png_sent_as_data_uri(self) -> None:
        path = self._file("pose.png", _PNG_BYTES)
        self.generate_3d(image=path)
        expected = "data:image/png;base64," + base64.b64encode(_PNG_BYTES).decode("ascii")
        self.assertEqual(self._sent_body(), {"prompt": "", "image_url": expected})

    def test_local_image_prompt_is_label(self) -> None:
        path = self._file("pose.png", _PNG_BYTES)
        self.generate_3d("pirate in T-pose", image=path, image_model="ignored/model")
        body = self._sent_body()
        self.assertEqual(set(body), {"prompt", "image_url"})
        self.assertEqual(body["prompt"], "pirate in T-pose")

    def test_local_jpeg_and_webp_mime_by_extension(self) -> None:
        cases = [
            ("a.jpg", _JPEG_BYTES, "image/jpeg"),
            ("b.JPEG", _JPEG_BYTES, "image/jpeg"),
            ("c.webp", _WEBP_BYTES, "image/webp"),
            ("d.PNG", _PNG_BYTES, "image/png"),
        ]
        for name, data, mime in cases:
            with self.subTest(name=name):
                self.requests.clear()
                self.generate_3d(image=self._file(name, data))
                url = self._sent_body()["image_url"]
                self.assertTrue(url.startswith("data:{:s};base64,".format(mime)), url[:40])
                self.assertEqual(base64.b64decode(url.split(",", 1)[1]), data)

    def test_unsupported_extension_refused(self) -> None:
        for name in ("a.gif", "a.bmp", "a.tga", "noext"):
            with self.subTest(name=name):
                path = self._file(name, _PNG_BYTES)
                self._assert_refused(self.generate_3d(image=path), "not supported", ".png")

    def test_file_over_8_mb_refused(self) -> None:
        path = self._file("big.png", _PNG_BYTES)
        with open(path, "r+b") as fh:
            fh.truncate(8 * 1024 * 1024 + 1)
        self._assert_refused(self.generate_3d(image=path), "8 MB")

    def test_file_of_exactly_8_mb_accepted(self) -> None:
        path = self._file("edge.png", _PNG_BYTES)
        with open(path, "r+b") as fh:
            fh.truncate(8 * 1024 * 1024)
        self.generate_3d(image=path)
        self.assertTrue(self._sent_body()["image_url"].startswith("data:image/png;base64,"))

    def test_missing_file_refused(self) -> None:
        missing = os.path.join(self.tmp.name, "nope.png")
        self._assert_refused(self.generate_3d(image=missing), "not found")

    def test_empty_file_refused(self) -> None:
        self._assert_refused(self.generate_3d(image=self._file("empty.png", b"")), "empty")

    def test_content_must_match_extension(self) -> None:
        self._assert_refused(self.generate_3d(image=self._file("fake.png", _JPEG_BYTES)), "image/png", "image/jpeg")
        self.requests.clear()
        self._assert_refused(self.generate_3d(image=self._file("text.jpg", b"hello world")), "not a PNG")

    # -----------------------------------------------------------------
    # Image mode: URLs and data URIs.

    def test_http_urls_passed_through(self) -> None:
        for url in ("https://example.test/pose.png", "http://example.test/a.webp?x=1"):
            with self.subTest(url=url):
                self.requests.clear()
                self.generate_3d(image=url)
                self.assertEqual(self._sent_body(), {"prompt": "", "image_url": url})

    def test_data_uri_passed_through(self) -> None:
        uri = "data:image/png;base64," + base64.b64encode(_PNG_BYTES).decode("ascii")
        self.generate_3d("label", image=uri)
        self.assertEqual(self._sent_body(), {"prompt": "label", "image_url": uri})

    def test_bad_data_uris_refused(self) -> None:
        png_b64 = base64.b64encode(_PNG_BYTES).decode("ascii")
        cases = [
            ("data:text/plain;base64," + png_b64, "not supported"),
            ("data:image/gif;base64," + png_b64, "not supported"),
            ("data:image/png," + png_b64, "base64"),
            ("data:image/png;base64", "base64"),
            ("data:image/png;base64,***not-base64***", "not valid base64"),
            ("data:image/jpeg;base64," + png_b64, "image/jpeg"),
        ]
        for uri, fragment in cases:
            with self.subTest(uri=uri[:30]):
                self._assert_refused(self.generate_3d(image=uri), fragment)

    def test_oversized_data_uri_refused_before_decoding(self) -> None:
        uri = "data:image/png;base64," + "A" * ((8 * 1024 * 1024 // 3 + 2) * 4)
        with mock.patch.object(self.module.base64, "b64decode") as decode:
            self._assert_refused(self.generate_3d(image=uri), "8 MB")
            decode.assert_not_called()

    # -----------------------------------------------------------------
    # Tool description (what agents read).

    def test_docstring_documents_both_modes_and_pose(self) -> None:
        doc = self.generate_3d.__doc__ or ""
        for fragment in ("Text mode", "Image mode", "data: URI", "8 MB", "bind pose in degrees", "Has Input Image?"):
            self.assertIn(fragment, doc)
        doc.encode("ascii")  # The tool listing must stay ASCII.


class TestGenerate3dWorkflowExport(unittest.TestCase):
    """
    ``n8n/generate-3d.workflow.json``: the "Has Input Image?" branch is wired
    in front of the text path, which itself is unchanged.
    """

    workflow: dict[str, Any]
    nodes: dict[str, dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        with open(_WORKFLOW_PATH, encoding="utf-8") as fh:
            cls.workflow = json.load(fh)
        cls.nodes = {node["name"]: node for node in cls.workflow["nodes"]}

    def _targets(self, source: str) -> list[list[str]]:
        outputs = self.workflow["connections"][source]["main"]
        return [[link["node"] for link in output] for output in outputs]

    def test_node_names_and_ids_unique(self) -> None:
        names = [node["name"] for node in self.workflow["nodes"]]
        ids = [node["id"] for node in self.workflow["nodes"]]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(ids), len(set(ids)))

    def test_all_connections_point_at_existing_nodes(self) -> None:
        for source, kinds in self.workflow["connections"].items():
            self.assertIn(source, self.nodes)
            for output in kinds["main"]:
                for link in output:
                    self.assertIn(link["node"], self.nodes, "{:s} -> {:s}".format(source, link["node"]))

    def test_branch_wiring(self) -> None:
        self.assertEqual(self._targets("Check API Key"), [["Has Input Image?"], ["Reject"]])
        self.assertEqual(self._targets("Has Input Image?"), [["Use Input Image"], ["Compose Prompt"]])
        self.assertEqual(self._targets("Use Input Image"), [["fal.ai - Trellis Image to 3D"]])
        # Text path unchanged.
        self.assertEqual(self._targets("Compose Prompt"), [["OpenRouter - Text to Image"]])
        self.assertEqual(self._targets("OpenRouter - Text to Image"), [["Build Image Data URI"]])
        self.assertEqual(self._targets("Build Image Data URI"), [["fal.ai - Trellis Image to 3D"]])
        self.assertEqual(self._targets("fal.ai - Trellis Image to 3D"), [["Respond Job Handles"]])

    def test_has_input_image_checks_non_empty_string(self) -> None:
        node = self.nodes["Has Input Image?"]
        self.assertEqual(node["type"], "n8n-nodes-base.if")
        conditions = node["parameters"]["conditions"]["conditions"]
        self.assertEqual(len(conditions), 1)
        condition = conditions[0]
        self.assertIn("body.image_url", condition["leftValue"])
        self.assertIn("typeof", condition["leftValue"])
        self.assertEqual(condition["operator"]["type"], "string")
        self.assertEqual(condition["operator"]["operation"], "notEmpty")

    def test_use_input_image_feeds_the_field_trellis_reads(self) -> None:
        node = self.nodes["Use Input Image"]
        self.assertEqual(node["type"], "n8n-nodes-base.set")
        assignments = node["parameters"]["assignments"]["assignments"]
        self.assertEqual([a["name"] for a in assignments], ["image_data_uri"])
        self.assertIn("body.image_url", assignments[0]["value"])
        trellis = self.nodes["fal.ai - Trellis Image to 3D"]["parameters"]["bodyParameters"]["parameters"]
        self.assertEqual(trellis, [{"name": "image_url", "value": "={{ $json.image_data_uri }}"}])


if __name__ == "__main__":
    unittest.main()
