# Blender MCP

## Overview

A lightweight MCP (Model Context Protocol) server for Blender.
It offers a natural language interface with Blender's Python API,
improving access to documentation, and allowing users to explore
and understand complex setups.

Read the documentation at [blender.org/lab/mcp-server](https://www.blender.org/lab/mcp-server/)

> **This is a modded fork** of the official [`blender_mcp`](https://projects.blender.org/lab/blender_mcp)
> (kept as the `upstream` remote). It retains the official tools and adds
> standardized cameras, canonical import, text/image-to-3D, Sketchfab tools,
> and explicit selection between Blender sessions. The latter intentionally
> changes connection selection; see "Several Blender instances" below.
>
> Official baseline: [`dbbf836`](https://projects.blender.org/lab/blender_mcp/commit/dbbf836ad4b1025f14a2b3b504c43903f39e0b04),
> checked on 2026-10-29 ([sync issue #1](https://github.com/rostislavpeska/blender-mcp-modded/issues/1)).
> MCP package version 1.0.2; the official add-on manifest still says 1.0.0.

## Modded additions

### Extra tools (`mcp/blmcp/tools/`)

- **`place_standard_cameras`** - drop 4 bounds-fit cameras (front/right/back/left)
  aimed at the scene centre, in a hidden collection. `target_collection` /
  `ignore_object_names` control what gets framed (e.g. exclude a huge ground plane).
- **`read_standard_views`** - render all standard cameras into a single 2x2
  contact-sheet image, so a scene can be understood from every angle in one call.
- **`import_canonical_model`** - import a `.glb/.gltf/.obj/.fbx` or glTF ZIP (URL or local path)
  and canonicalize it: joined to one mesh, transforms applied, uniformly scaled so
  its largest dimension = `target_size`, origin set to `center` or `bottom`, and
  placed at the world origin.
- **`generate_3d` / `wait_for_3d_job`** - async text-to-3D. `generate_3d(prompt)`
  kicks off an n8n pipeline (text -> image -> [TRELLIS](https://github.com/microsoft/TRELLIS))
  and returns job handles; `wait_for_3d_job(...)` polls until the `.glb` is ready.
  `generate_3d(image=...)` (local png/jpeg/webp up to 8 MB, http(s) URL or `data:` URI)
  skips the image generation and sends your image to TRELLIS (needs the updated
  workflow, see [n8n/README.md](n8n/README.md#input-image-mode-image---3d)).
  Pair with `import_canonical_model` for a full **prompt -> object-in-scene** loop.
- **`sketchfab_search` / `sketchfab_preview` / `sketchfab_download`** - search
  public model metadata, inspect a thumbnail, and request a download URL. Search
  and preview use the public API; download requires your separately hosted
  `sketchfab-download` n8n webhook. That workflow is not included in this repo.
- **`list_blender_instances` / `select_blender_instance`** - choose the target
  Blender process by PID or port using its instance registry.

### Config (generation, job status, and Sketchfab download)

These tools are thin HTTP clients for n8n webhooks that **you host on your
own n8n**. This MCP is instance-agnostic - it ships **no** default host. Import the
workflows in [`n8n/`](n8n/) (see `n8n/README.md`), then set:

| Variable | Required | Notes |
|---|---|---|
| `THREED_WEBHOOK_BASE` | yes | base URL of *your* n8n, e.g. `https://n8n.example.com` |
| `THREED_WEBHOOK_API_KEY` | yes | the `X-API-Key` gate secret you set in both workflows |

For local dev, copy `mcp/.env.example` -> `mcp/.env` and fill these in (`.env` is
gitignored). In production, inject real environment variables instead - `load_dotenv`
runs with `override=False`, so real env always wins and the `.env` is ignored. Every
other tool (cameras, import, and all upstream tools) needs **no** configuration.

## Design notes, technical debt & contributing

The extra tools live in separate modules under `mcp/blmcp/tools/`, following
upstream's tool-pair convention. Shared changes are limited to connection and
instance selection, add-on startup/registration, the additional prompt guidance,
and the `python-dotenv` dependency. Official tool implementations and reference
documentation are retained from the pinned baseline. The reference parser also
recognizes the new `details` blocks without hiding their nested API methods.

### Updating from official Blender Lab

The first sync reconstructed the historical delta from official `98b0e49` to
`dbbf836`, applied it on top of the fork, and recorded `dbbf836` as a merge parent.
The fork originally had an unrelated root. Recording the real upstream parent
restores a normal merge base for future updates; it does not erase the fork's
history. Subsequent updates can use `git fetch upstream` and
`git merge upstream/main` on a review branch.

The 2026-10-29 sync includes the upstream nonblocking partial-write fix, 2 KiB
image-envelope allowance, MCP dependency bound below version 2, Blender 5.2
reference data, generated tool documentation, and GPL license. The contact-sheet
tool now uses the same envelope allowance. The dependency lock is updated too.
Strict parsing of the new `blf.types` page exposed an upstream parser gap;
the added `details` handler preserves its title and nested method lookup.

Before installing an update:

1. Compare against the pinned upstream revision. Every existing upstream tool
   and reference document must remain present; inspect each shared-file change.
2. Run the unit tests below, including the tool-list snapshot. Refresh that
   snapshot only after reviewing added or changed tools. Regenerate the public
   tool list with `python _misc/readme_update_from_tools.py`.
3. Run the opt-in proofs in a factory Blender with isolated user resources.
   They use no paid services and never connect to the owner's port 9876.
4. Back up the installed add-on and MCP launch configuration. Close Blender
   after the owner saves or chooses what to do with unsaved work. Replace the
   add-on only while Blender is closed: lazy imports can otherwise mix revisions.
   Restart the MCP client too, then verify its tool list and the target instance.
   Roll back both components from the backup if activation fails.

From the repository root, with dependencies installed using `uv sync --project mcp`:

```sh
uv run --project mcp python -m unittest tests.test_tool_listing tests.test_rst_parse tests.test_rst_search tests.test_mcp_server tests.test_port_per_session tests.test_threed_pipeline tests.test_upstream_sync -q
```

Set `BLENDER_BIN` to a Blender executable and `BLENDER_MCP_PROOF_PORT` to a free
port in 9877-9899 to run `tests/test_port_per_session.py TestBackgroundBlenderProof`.
With `BLENDER_BIN`, run `tests/test_modded_blender.py` for two-part GLB and ZIP
import, normalization, protected-object preservation, and repeatable camera
placement. These native proofs were run on Blender 5.1.2. Contact-sheet pixels
still need a GUI check; the background proof only verifies its documented refusal.
External generation and Sketchfab credentials/services require separate checks.
The upstream GUI integration suite uses fixed ports, including 9876, and must
run in a disposable environment without an owner's Blender session.

**Known technical debt (honest list):**

- **n8n coupling for `generate_3d` / `wait_for_3d_job`.** These call an external
  n8n instance (fal Trellis + OpenRouter, via webhooks). It was the fastest path
  on top of an existing n8n stack, but it is infrastructure-heavy for others. The
  cleaner design - direct in-Python OpenRouter + fal calls, keys in env, no n8n -
  is deferred (see the note in `n8n/README.md`).
- **`.env` as a host workaround.** The local secret lives in `mcp/.env` (dotenv)
  chiefly because the Windows/MSIX Claude Desktop build does not reliably pass a
  config `env` block to the spawned server process. On a normal host the env is
  passed directly and the `.env` is unnecessary.
- **The `prompts.yml` edit** adds default camera guidance; a cleaner version
  would make that guidance opt-in rather than editing the shared prompt.

**We are open to collaborating.** The camera-framing tools
(`place_standard_cameras` / `read_standard_views`) and `import_canonical_model`
are pure-Blender, have no external dependencies, and are the kind of thing that
could reasonably live upstream - we would be glad to contribute them to the
official [`blender_mcp`](https://projects.blender.org/lab/blender_mcp). The
text-to-3D pipeline would want the in-Python rework first. Issues, PRs, and ideas
are welcome; if you are building similar things, please reach out.

----

The project is deliberately small, maintainable, and does no more than
necessary. It has two components that communicate over a TCP socket:

- A **Blender add-on** that runs inside Blender and executes requests.
- An **MCP server** that runs as a separate process, launched by the
  MCP client (e.g. [Llama.cpp](https://projects.blender.org/lab/blender_mcp/wiki/Llama.cpp)).

The data flow is:
```
MCP Client  ⇐ MCP/stdio ⇒  blender-mcp  ⇐ TCP socket ⇒  Blender Add-on
```


## Blender Add-on

Located in ``addon/blender_mcp_addon/``.

A Blender extension that allows the MCP server to communicate with a
running Blender instance. It must be installed and enabled for any of
the MCP tools to work.

The add-on provides a preferences panel for configuring the host, port,
and an optional auto-start setting.

### Several Blender instances (one port per session)

Each Blender binds its own port: the ``BLENDER_MCP_PORT`` environment variable (set by a
launcher) wins over the Port preference, so the normal launch stays on 9876 while a
review Blender started with ``BLENDER_MCP_PORT=9877`` sits beside it. On Windows the
port is bound with ``SO_EXCLUSIVEADDRUSE``: a second Blender asking for a taken port
fails with "already in use" (shown in the preferences, the console and a popup)
instead of silently taking the port over.

After binding, the add-on writes ``%LOCALAPPDATA%\blender-mcp\instances\<pid>.json``
(``$XDG_STATE_HOME/blender-mcp/instances`` elsewhere, ``BLENDER_MCP_REGISTRY_DIR`` to
override) with its pid, port, blend file, start time and the ``BLENDER_MCP_SESSION``
label, refreshes the file name on load/save and removes the record on exit.

The MCP server uses ``BLENDER_MCP_PORT`` as an explicit pin. Without it, it talks to the
only registered instance (and keeps it for the session), refuses with the list when
several run, and never falls back to 9876 silently. ``list_blender_instances`` and
``select_blender_instance(pid|port)`` choose per MCP server process, i.e. per session.

### Functionality Overview

Note that this is intended to be a fairly minimal add-on.

Connectivity
   - Auto-start (optional), is non-blocking any issues can be viewed from the preferences.
   - Configurable polling intervals (active and idle rates) from preferences to avoid excessive overhead.
   - Client timeout protection - stalled connections are evicted.
   - Start/stop operators accessible from the preferences panel.
   - Deferred responses are supported only by the interactive add-on server;
     background mode requires requests to complete synchronously and rejects deferred results.




## MCP Server

Located in ``mcp/blmcp/``, installed as a Python package with the
entry point ``blender-mcp``.

An MCP client launches this process and communicates with it over
stdio. The server connects to the add-on's TCP socket to relay
requests to Blender.

``mcp/blmcp/data/``
   Data files bundled with the package.

   - ``prompts.yml`` provides instructions sent to the LLM at
     connection time.
   - ``api/`` contains Blender Python API reference in RST format.
   - ``manual/`` contains Blender user manual excerpts in RST format.

``mcp/blmcp/tools/``
   Each tool is a single module, auto-discovered at startup.
   Modules ending in ``_toolcode`` contain code that runs inside
   Blender (sent to the add-on for execution) and are skipped during
   discovery.

``mcp/blmcp/tools_helpers/``
   Shared utilities used by tools. Tools should not import from each
   other; shared logic lives here instead.


### Tools

See [readme_tools.rst](readme_tools.rst) for the tools the MCP server exposes.
