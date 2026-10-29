# SPDX-FileCopyrightText: 2026 Blender Authors
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tests for one MCP port per Blender session: exclusive bind, the instance registry
and the MCP server's instance selection.

Does not require Blender; sockets use OS-assigned ports and the registry a temporary folder.
Run with::

    python tests/test_port_per_session.py

Set ``BLENDER_BIN`` and ``BLENDER_MCP_PROOF_PORT`` (9877-9899) to also run the background Blender proof:
the worktree add-on is loaded with ``--factory-startup`` and an empty ``BLENDER_USER_RESOURCES``,
nothing is installed.

Audit: 2026-10-17-claude-opus-5.5 port-per-session-01 (register R7/R14).
"""

__all__ = ()

import importlib
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import types
import unittest
from unittest import mock

_REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ADDON_DIR = os.path.join(_REPO_DIR, "addon", "blender_mcp_addon")
_MCP_DIR = os.path.join(_REPO_DIR, "mcp")


def _import_addon_module(name: str) -> types.ModuleType:
    """
    Import ``blender_mcp_addon.<name>`` without running the package ``__init__`` (which needs ``bpy``).
    """
    if "blender_mcp_addon" not in sys.modules:
        pkg = types.ModuleType("blender_mcp_addon")
        pkg.__path__ = [_ADDON_DIR]
        sys.modules["blender_mcp_addon"] = pkg
    return importlib.import_module("blender_mcp_addon." + name)


def _import_connection() -> types.ModuleType:
    if _MCP_DIR not in sys.path:
        sys.path.insert(0, _MCP_DIR)
    return importlib.import_module("blmcp.tools_helpers.connection")


server = _import_addon_module("mcp_to_blender_server")
registry = _import_addon_module("instance_registry")
connection = _import_connection()


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("localhost", 0))
        return int(sock.getsockname()[1])


def _dead_pid() -> int:
    proc = subprocess.Popen([sys.executable, "-c", "pass"])
    proc.wait()
    return proc.pid


# -----------------------------------------------------------------------------
# Exclusive bind.

class TestExclusiveBind(unittest.TestCase):

    def tearDown(self) -> None:
        server.stop()

    def test_second_bind_on_same_port_fails(self) -> None:
        port = _free_port()
        server.start("localhost", port)
        self.assertTrue(server.is_running())
        with self.assertRaises(OSError) as ctx:
            server._bind_listening_socket("localhost", port)  # pylint: disable=protected-access
        self.assertIn("already in use", str(ctx.exception))
        self.assertIn("BLENDER_MCP_PORT", str(ctx.exception))

    @unittest.skipUnless(sys.platform == "win32", "SO_REUSEADDR only steals ports on Windows")
    def test_old_reuseaddr_socket_cannot_steal(self) -> None:
        """
        The old add-on bound with ``SO_REUSEADDR``; it must not take a port held exclusively.
        """
        port = _free_port()
        server.start("localhost", port)
        thief = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            thief.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            with self.assertRaises(OSError):
                thief.bind(("localhost", port))
        finally:
            thief.close()

    @unittest.skipUnless(sys.platform == "win32", "SO_REUSEADDR only steals ports on Windows")
    def test_control_two_reuseaddr_sockets_share_a_port(self) -> None:
        """
        Control: the old flag lets two sockets bind one port on Windows (register R7), so the tests above mean something.
        """
        port = _free_port()
        first = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        second = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            for sock in (first, second):
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            first.bind(("localhost", port))
            first.listen(1)
            second.bind(("localhost", port))
        finally:
            first.close()
            second.close()

    def test_port_is_free_again_after_stop(self) -> None:
        port = _free_port()
        server.start("localhost", port)
        server.stop()
        server.start("localhost", port)
        self.assertTrue(server.is_running())


class TestPortFromEnv(unittest.TestCase):

    def test_unset_is_none(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("BLENDER_MCP_PORT", None)
            self.assertIsNone(server.port_from_env())

    def test_value_wins(self) -> None:
        with mock.patch.dict(os.environ, {"BLENDER_MCP_PORT": "9881"}):
            self.assertEqual(server.port_from_env(), 9881)

    def test_invalid_value_is_an_error_not_a_fallback(self) -> None:
        for value in ("abc", "80", "70000"):
            with mock.patch.dict(os.environ, {"BLENDER_MCP_PORT": value}):
                with self.assertRaises(ValueError):
                    server.port_from_env()


# -----------------------------------------------------------------------------
# Registry (add-on writer, both readers).

class _RegistryCase(unittest.TestCase):

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = self._tmp.name


class TestRegistry(_RegistryCase):

    def test_write_refresh_remove(self) -> None:
        with mock.patch.dict(os.environ, {"BLENDER_MCP_SESSION": "agent-a"}):
            path = registry.write("localhost", 9881, "C:/a.blend", binary=sys.executable, directory=self.dir)
        self.assertEqual(os.path.basename(path), "{:d}.json".format(os.getpid()))
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertEqual(data["pid"], os.getpid())
        self.assertEqual(data["port"], 9881)
        self.assertEqual(data["filepath"], "C:/a.blend")
        self.assertEqual(data["session"], "agent-a")
        self.assertTrue(data["started_utc"].endswith("+00:00"))

        self.assertTrue(registry.refresh_filepath("C:/b.blend", directory=self.dir))
        with open(path, encoding="utf-8") as fh:
            self.assertEqual(json.load(fh)["filepath"], "C:/b.blend")

        self.assertTrue(registry.remove(directory=self.dir))
        self.assertFalse(os.path.exists(path))
        self.assertFalse(registry.remove(directory=self.dir))
        self.assertFalse(registry.refresh_filepath("C:/c.blend", directory=self.dir))

    def test_readers_skip_dead_reused_and_broken_records(self) -> None:
        registry.write("localhost", 9882, "live.blend", binary=sys.executable, directory=self.dir)
        registry.write("localhost", 9883, "dead.blend", pid=_dead_pid(), directory=self.dir)
        # This process is alive but is not Blender: a reused pid.
        with open(os.path.join(self.dir, "1.json"), "w", encoding="utf-8") as fh:
            json.dump({"pid": os.getpid(), "port": 9884, "binary": "C:/Blender/blender.exe"}, fh)
        with open(os.path.join(self.dir, "2.json"), "w", encoding="utf-8") as fh:
            fh.write("{not json")
        for reader in (registry.read_live, connection.live_instances):
            live = reader(self.dir)
            self.assertEqual([rec["port"] for rec in live], [9882], reader)

    def test_missing_folder_reads_empty(self) -> None:
        self.assertEqual(registry.read_live(os.path.join(self.dir, "missing")), [])
        self.assertEqual(connection.live_instances(os.path.join(self.dir, "missing")), [])

    def test_add_on_and_server_use_the_same_folder(self) -> None:
        env = {"LOCALAPPDATA": "C:/LocalAppData", "XDG_STATE_HOME": "/state"}
        with mock.patch.dict(os.environ, env):
            os.environ.pop("BLENDER_MCP_REGISTRY_DIR", None)
            self.assertEqual(registry.registry_dir(), connection.registry_dir())
            if sys.platform == "win32":
                self.assertEqual(
                    registry.registry_dir(), os.path.join("C:/LocalAppData", "blender-mcp", "instances"),
                )
        with mock.patch.dict(os.environ, {"BLENDER_MCP_REGISTRY_DIR": self.dir}):
            self.assertEqual(registry.registry_dir(), self.dir)
            self.assertEqual(connection.registry_dir(), self.dir)
            registry.write("localhost", 9885, "x.blend", binary=sys.executable)
            self.assertEqual([rec["port"] for rec in connection.live_instances()], [9885])


# -----------------------------------------------------------------------------
# Instance selection in the MCP server.

def _rec(pid: int, port: int) -> dict[str, object]:
    return {"pid": pid, "port": port, "filepath": "f{:d}.blend".format(pid), "binary": ""}


class TestSelection(_RegistryCase):

    def setUp(self) -> None:
        super().setUp()
        connection._Selection.clear()  # pylint: disable=protected-access
        self.addCleanup(connection._Selection.clear)  # pylint: disable=protected-access
        env = mock.patch.dict(os.environ, {"BLENDER_MCP_REGISTRY_DIR": self.dir})
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop("BLENDER_MCP_PORT", None)
        self.alive: set[int] = set()

    def _add(self, pid: int, port: int) -> None:
        with open(os.path.join(self.dir, "{:d}.json".format(pid)), "w", encoding="utf-8") as fh:
            json.dump(_rec(pid, port), fh)
        self.alive.add(pid)

    def _alive(self, pid: int, _image: str) -> bool:
        return pid in self.alive

    def _params(self) -> tuple[str, int]:
        return connection.get_connection_params(alive_fn=self._alive)

    def test_none_refuses_and_never_defaults_to_9876(self) -> None:
        with self.assertRaises(ConnectionError) as ctx:
            self._params()
        self.assertIn("No running Blender", str(ctx.exception))
        self.assertIn("select_blender_instance(port=...)", str(ctx.exception))

    def test_one_is_used_and_kept(self) -> None:
        self._add(101, 9881)
        self.assertEqual(self._params(), ("localhost", 9881))
        # The chosen Blender goes away and another starts: refuse, do not switch silently.
        self.alive.discard(101)
        self._add(102, 9882)
        with self.assertRaises(ConnectionError) as ctx:
            self._params()
        self.assertIn("no longer running", str(ctx.exception))
        self.assertIn("pid 102 port 9882", str(ctx.exception))

    def test_several_refuse_with_the_list(self) -> None:
        self._add(101, 9876)
        self._add(102, 9881)
        with self.assertRaises(ConnectionError) as ctx:
            self._params()
        message = str(ctx.exception)
        self.assertIn("Several Blender instances", message)
        self.assertIn("pid 101 port 9876 file f101.blend", message)
        self.assertIn("pid 102 port 9881 file f102.blend", message)

    def test_select_by_pid_or_port(self) -> None:
        self._add(101, 9876)
        self._add(102, 9881)
        connection.instance_select(pid=102, alive_fn=self._alive)
        self.assertEqual(self._params(), ("localhost", 9881))
        connection.instance_select(port=9876, alive_fn=self._alive)
        self.assertEqual(self._params(), ("localhost", 9876))
        with self.assertRaises(ValueError):
            connection.instance_select(pid=999, alive_fn=self._alive)
        connection.instance_select(alive_fn=self._alive)
        with self.assertRaises(ConnectionError):
            self._params()

    def test_select_unregistered_port_only_when_it_answers(self) -> None:
        with self.assertRaises(ValueError):
            connection.instance_select(port=9890, alive_fn=self._alive, answers_fn=lambda _port: False)
        result = connection.instance_select(port=9890, alive_fn=self._alive, answers_fn=lambda _port: True)
        self.assertIn("no registry record", str(result["message"]))
        self.assertEqual(self._params(), ("localhost", 9890))

    def test_pinned_port_wins(self) -> None:
        self._add(101, 9876)
        self._add(102, 9881)
        with mock.patch.dict(os.environ, {"BLENDER_MCP_PORT": "9899"}):
            self.assertEqual(self._params(), ("localhost", 9899))
            self.assertEqual(connection.instance_selection()["pinned_port"], 9899)

    def test_send_code_refuses_before_connecting(self) -> None:
        self._add(os.getpid(), 9881)
        self._add(_dead_pid(), 9882)
        with open(os.path.join(self.dir, "x.json"), "w", encoding="utf-8") as fh:
            json.dump(_rec(os.getppid(), 9883), fh)
        with mock.patch.object(connection.socket, "socket", side_effect=AssertionError("connected")):
            with self.assertRaises(ConnectionError) as ctx:
                connection.send_code("result = {}", strict_json=True)
        self.assertIn("Several Blender instances", str(ctx.exception))


# -----------------------------------------------------------------------------
# Optional: a real background Blender on a non-9876 port.

_PROOF_EXPR = (
    "import sys; sys.path.insert(0, {addon_parent!r}); "
    "import blender_mcp_addon; blender_mcp_addon.register()"
)


def _blender_proc(blender_bin: str, env: dict[str, str], *args: str) -> "subprocess.Popen[str]":
    return subprocess.Popen(
        [
            blender_bin, "--background", "--factory-startup", "--online-mode",
            "--python-expr", _PROOF_EXPR.format(addon_parent=os.path.dirname(_ADDON_DIR)),
            "--command", "blender_mcp", *args,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
    )


@unittest.skipUnless(
    os.environ.get("BLENDER_BIN") and os.environ.get("BLENDER_MCP_PROOF_PORT"),
    "set BLENDER_BIN and BLENDER_MCP_PROOF_PORT (9877-9899) for the background Blender proof",
)
class TestBackgroundBlenderProof(_RegistryCase):

    def test_env_port_registry_selection_and_exclusive_bind(self) -> None:
        port = int(os.environ["BLENDER_MCP_PROOF_PORT"])
        self.assertTrue(9877 <= port <= 9899, "proof port must be in 9877-9899, never 9876")
        blender_bin = os.environ["BLENDER_BIN"]
        user_dir = os.path.join(self.dir, "user")
        reg_dir = os.path.join(self.dir, "instances")
        env = {
            **os.environ,
            "BLENDER_USER_RESOURCES": user_dir,
            "BLENDER_MCP_REGISTRY_DIR": reg_dir,
            "BLENDER_MCP_PORT": str(port),
            "BLENDER_MCP_SESSION": "port-per-session-proof",
        }
        first = _blender_proc(blender_bin, env)
        try:
            deadline = time.monotonic() + 60
            records: list[dict[str, object]] = []
            while time.monotonic() < deadline and not records and first.poll() is None:
                records = registry.read_live(reg_dir)
                time.sleep(0.5)
            self.assertEqual(len(records), 1, "no registry record from the background Blender")
            rec = records[0]
            self.assertEqual(rec["pid"], first.pid)
            self.assertEqual(rec["port"], port)
            self.assertEqual(rec["session"], "port-per-session-proof")
            self.assertTrue(rec["background"])
            print("\nproof record:", json.dumps(rec))

            # The MCP server side picks the only live instance and runs code there.
            connection._Selection.clear()  # pylint: disable=protected-access
            with mock.patch.dict(os.environ, {"BLENDER_MCP_REGISTRY_DIR": reg_dir}):
                os.environ.pop("BLENDER_MCP_PORT", None)
                self.assertEqual(connection.get_connection_params(), ("localhost", port))
                reply = connection.send_code(
                    "import bpy, os\nresult = {'pid': os.getpid(), 'version': bpy.app.version_string}\n",
                    strict_json=True,
                )
            self.assertEqual(reply.get("status"), "ok", reply)
            self.assertEqual(reply["result"]["pid"], first.pid)  # type: ignore[index]
            print("proof reply:", json.dumps(reply))

            # Saving refreshes the registered file name (save_post handler).
            blend = os.path.join(self.dir, "saved.blend")
            with mock.patch.dict(os.environ, {"BLENDER_MCP_REGISTRY_DIR": reg_dir}):
                os.environ.pop("BLENDER_MCP_PORT", None)
                saved = connection.send_code(
                    "import bpy\nbpy.ops.wm.save_as_mainfile(filepath={!r})\nresult = {{}}\n".format(blend),
                    strict_json=True,
                )
            self.assertEqual(saved.get("status"), "ok", saved)
            self.assertEqual(
                os.path.normcase(str(registry.read_live(reg_dir)[0]["filepath"])), os.path.normcase(blend),
            )

            # A second Blender asked for the same port fails loudly instead of taking it.
            second = _blender_proc(blender_bin, env)
            out, _ = second.communicate(timeout=120)
            print("second instance exit {:d}:\n{:s}".format(second.returncode, out[-600:]))
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("already in use", out)
            self.assertEqual([r["pid"] for r in registry.read_live(reg_dir)], [first.pid])

            # Stopping the server through MCP ends the CLI loop and removes the record.
            with mock.patch.dict(os.environ, {"BLENDER_MCP_REGISTRY_DIR": reg_dir}):
                os.environ.pop("BLENDER_MCP_PORT", None)
                connection.send_code(
                    "from blender_mcp_addon import mcp_to_blender_server\nmcp_to_blender_server.stop()\nresult = {}\n",
                    strict_json=True,
                )
            out, _ = first.communicate(timeout=60)
            print("first instance exit {:d}:\n{:s}".format(first.returncode, out[-600:]))
            self.assertEqual(os.listdir(reg_dir), [])
        finally:
            if first.poll() is None:
                first.kill()
                first.communicate()
            connection._Selection.clear()  # pylint: disable=protected-access


if __name__ == "__main__":
    unittest.main()
