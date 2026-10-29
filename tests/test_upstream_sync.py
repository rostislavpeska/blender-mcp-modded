# SPDX-License-Identifier: GPL-3.0-or-later

"""Regression coverage for upstream sync #1 (journal: dev-2026-10-29-codex-01).

Uses real loopback sockets with deterministic backpressure, without Blender or API calls.
Set BLENDER_SYNC_ADDON to a historical add-on directory for the negative control.
"""

__all__ = ()

import importlib
from contextlib import nullcontext
import json
import os
from pathlib import Path
import socket
import sys
import time
import types
import unittest
from unittest import mock

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "mcp"))


def _server():
    # A separate package name avoids executing __init__ (which requires bpy).
    package = types.ModuleType("sync_test_addon")
    package.__path__ = [os.environ.get("BLENDER_SYNC_ADDON", str(_ROOT / "addon/blender_mcp_addon"))]
    sys.modules[package.__name__] = package
    return importlib.import_module(package.__name__ + ".mcp_to_blender_server")


class _BackpressureSocket:
    """Write real bytes, then model a full kernel buffer on alternate sends."""

    def __init__(self, conn):
        self.conn = conn
        self.block_next = False

    def __getattr__(self, name):
        return getattr(self.conn, name)

    def send(self, data):
        if self.block_next:
            self.block_next = False
            raise BlockingIOError("injected full send buffer")
        sent = self.conn.send(data[:4096])
        self.block_next = True
        return sent

    def sendall(self, data):
        data = memoryview(data)
        while data:
            data = data[self.send(data):]


class TestLargeResponses(unittest.TestCase):
    def test_slow_reader_gets_complete_response(self):
        server = _server()
        payload_size = 8 * 1024 * 1024
        server.start("127.0.0.1", 0)
        try:
            address = server._state.sock.getsockname()
            with socket.create_connection(address, timeout=5) as client:
                client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
                server._accept_clients()
                self.assertEqual(len(server._state.clients), 1)
                server._state.clients[0].conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096)
                server._state.clients[0].conn = _BackpressureSocket(server._state.clients[0].conn)
                request = {"type": "execute", "strict_json": True,
                           "code": "result = {'data': 'x' * %d}" % payload_size}
                client.sendall(json.dumps(request).encode() + b"\0")
                # The entire response cannot fit before the client starts reading.
                sandbox = importlib.import_module("sync_test_addon.weak_sandbox")
                with mock.patch.object(sandbox, "WeakSandboxForLLM", nullcontext):
                    server.poll()
                client.setblocking(False)
                received = bytearray()
                deadline = time.monotonic() + 10
                while time.monotonic() < deadline:
                    server.poll()
                    try:
                        chunk = client.recv(65536)
                    except BlockingIOError:
                        time.sleep(0.001)
                        continue
                    if not chunk:
                        break
                    received.extend(chunk)
                    if received.endswith(b"\0"):
                        break
                self.assertTrue(received.endswith(b"\0"),
                                "Response truncated: received %d bytes" % len(received))
                reply = json.loads(received[:-1])
                self.assertEqual(reply["status"], "ok", reply)
                self.assertEqual(reply["result"]["data"], "x" * payload_size)
        finally:
            server.stop()


class TestImageEnvelope(unittest.TestCase):
    def test_images_leave_room_for_json_envelope(self):
        for name in ("get_screenshot_of_area_as_image_toolcode",
                     "get_screenshot_of_window_as_image_toolcode",
                     "read_standard_views_toolcode"):
            with self.subTest(tool=name):
                module = importlib.import_module("blmcp.tools." + name)
                encoded_limit = 4 * ((module._IMAGE_SIZE_LIMIT_IN_BYTES + 2) // 3)
                self.assertLessEqual(encoded_limit + 2048, 1_048_576)


if __name__ == "__main__":
    unittest.main()
