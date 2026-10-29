# SPDX-FileCopyrightText: 2026 Blender Authors
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
CLI command handler for running the MCP server in background mode.

Started via ``blender --background file.blend --command blender_mcp``.
"""

__all__ = (
    "cli_execute",
)

import argparse

from . import execute_blocking
from . import instance_registry
from . import mcp_to_blender_server


def cli_execute(argv: list[str]) -> int:
    """
    Block and serve MCP requests until interrupted.
    """
    parser = argparse.ArgumentParser(
        prog="blender_mcp",
        description=(
            "Start the Blender MCP server. "
            "Deferred responses are not supported in background mode; "
            "each request must complete before returning."
        ),
    )
    parser.add_argument(
        "--host",
        default=mcp_to_blender_server.DEFAULT_HOST,
        help="Host to bind to.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to listen on (default: {:s}, else {:d}).".format(
            mcp_to_blender_server.ENV_PORT, mcp_to_blender_server.DEFAULT_PORT,
        ),
    )
    args = parser.parse_args(argv)

    try:
        port = args.port
        if port is None:
            port = mcp_to_blender_server.port_from_env()
        if port is None:
            port = mcp_to_blender_server.DEFAULT_PORT
        mcp_to_blender_server.start(args.host, port)
    except Exception as ex:  # pylint: disable=broad-exception-caught
        print("Error: {:s}".format(str(ex)))
        return 1

    try:
        record = instance_registry.write_for_this_blender(args.host, port)
    except OSError as ex:
        record = "not registered ({:s})".format(str(ex))
    print("MCP server started on {:s}:{:d} ({:s}), press Ctrl+C to exit.".format(args.host, port, record))

    try:
        execute_blocking.run()
    finally:
        mcp_to_blender_server.stop()
        instance_registry.remove()
    return 0
