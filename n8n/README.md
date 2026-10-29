# n8n workflows for the text-to-3D pipeline

The `generate_3d` / `wait_for_3d_job` MCP tools (`mcp/blmcp/tools/threed_pipeline.py`)
are thin HTTP clients — they call two webhooks that you host on **your own**
[n8n](https://n8n.io) instance. This folder contains those two workflows so you
can run the pipeline on your own infrastructure. Nothing points at anyone else's
server.

> The other MCP tools (`place_standard_cameras`, `read_standard_views`,
> `import_canonical_model`, and everything from upstream) need **none** of this.

## What the two workflows do

| File | Webhook | Role |
|---|---|---|
| `generate-3d.workflow.json` | `POST /webhook/generate-3d` | prompt -> (OpenRouter image) -> submit to fal Trellis queue -> returns `{ job_id, status_url, response_url }`; or, with `image_url` in the body, your image -> fal Trellis queue (see [Input-image mode](#input-image-mode-image---3d)) |
| `3d-job-status.workflow.json` | `POST /webhook/3d-job-status` | polls fal and returns `{ status, glb_url }` when the model is ready |

Both are gated by an `X-API-Key` header (see step 3).

## Setup

1. **Import** both JSON files into n8n (Workflows -> Import from File).
2. **Create two credentials** and attach them to the HTTP nodes (each node has a
   `notes` hint):
   - **OpenRouter** — credential type *OpenRouter* (`openRouterApi`); used by
     `OpenRouter - Text to Image`.
   - **fal.ai** — credential type *Header Auth*: Name `Authorization`, Value
     `Key <YOUR_FAL_KEY>`; used by `fal.ai - Trellis Image to 3D`, `fal status`,
     and `fal result`.
3. **Set the gate key**: in each workflow's **Check API Key** node, replace
   `REPLACE_WITH_YOUR_WEBHOOK_API_KEY` with a secret of your choice. Use the
   **same** value in both workflows, and put it in the MCP's
   `THREED_WEBHOOK_API_KEY` (see `mcp/.env.example`).
4. **Activate** both workflows.
5. **Point the MCP at your n8n**: set `THREED_WEBHOOK_BASE=https://your-n8n-host`
   and `THREED_WEBHOOK_API_KEY=<the gate key>` (env vars or `mcp/.env`).

## Input-image mode (image -> 3D)

`generate-3d` takes an optional input image. With one, the image goes straight
to TRELLIS: no image is generated, so a call costs one fal job and no OpenRouter
call. Without one, the text path runs exactly as before.

**Webhook body** (`POST /webhook/generate-3d`, header `X-API-Key`):

| Mode | Body | Path in the workflow |
|---|---|---|
| text (unchanged) | `{ "prompt": "<object only>", "image_model": "<OpenRouter model or empty>" }` | Has Input Image? false -> Compose Prompt -> OpenRouter -> Build Image Data URI -> fal |
| image | `{ "prompt": "<optional label>", "image_url": "<https URL or data:image/...;base64,...>" }` | Has Input Image? true -> Use Input Image -> fal |

The response is the same in both modes: `{ job_id, status_url, response_url, status }`.

The two nodes added after **Check API Key** (true output):

- **Has Input Image?** (IF): true when `body.image_url` is a string that is not
  empty after trimming. Expression:
  `{{ typeof ($json.body || {}).image_url === 'string' ? $json.body.image_url.trim() : '' }}`,
  operator *String -> is not empty*.
- **Use Input Image** (Edit Fields / Set, manual mapping, other fields not
  included): `image_data_uri` (String) = `{{ $json.body.image_url.trim() }}`.
  This is the field the fal node already reads (`image_url = {{ $json.image_data_uri }}`).
  Its output goes to that existing fal node.

Every other node, parameter and credential reference is unchanged.

**MCP side:** `generate_3d(image=...)` takes a local file path, an http(s) URL or
a `data:` URI; `prompt` becomes optional there and is only sent as a label. A
local file must be `.png`, `.jpg`/`.jpeg` or `.webp` and at most **8 MB**; it is
sent inline as a `data:` URI. The 8 MB cap keeps the request under n8n's default
webhook payload limit (`N8N_PAYLOAD_SIZE_MAX`, 16 MiB), because base64 adds a third.

**fal input limits:** the `fal-ai/trellis-2` API page lists `image_url` as the only
required input. It documents no image format, size or resolution limit, and says
a Base64 data URI can be passed as a file input. fal's CDN docs add that data URIs
inflate the request and slow it down (they are discouraged for large files), that
URLs must be fetchable without cookies or auth headers, and that each model may
enforce its own limits. The text path has always sent a `data:` URI of the
generated image, so data URIs of a few MB already work with this pipeline.

**Best input image:** one whole object, centred, on a plain light background, no
other objects. TRELLIS builds the mesh in exactly the pose it sees. For a character,
the image must already show the target skeleton's bind pose. In text mode, state
that pose in degrees in the prompt (e.g. "T-pose: arms straight out to the sides
at 90 degrees, palms down, legs straight").

**Publish before use.** A workflow without the two nodes ignores `image_url` and
runs the text path on `prompt` (a paid image generation plus a TRELLIS job on the
wrong input).

### Publishing the input-image mode on an existing n8n

Option A, by hand in the live workflow (recommended: it keeps your credentials,
gate key and any local changes, such as a different fal endpoint):

1. Open the *3D Model Generator* workflow in the n8n editor.
2. Add an **If** node named `Has Input Image?`, with one condition: value
   `{{ typeof ($json.body || {}).image_url === 'string' ? $json.body.image_url.trim() : '' }}`,
   operator *String -> is not empty*.
3. Add an **Edit Fields (Set)** node named `Use Input Image`: mode *Manual Mapping*,
   field `image_data_uri`, type *String*, value `{{ $json.body.image_url.trim() }}`,
   *Include Other Input Fields* off.
4. Rewire: **Check API Key** true -> `Has Input Image?`; `Has Input Image?` true ->
   `Use Input Image` -> the existing fal Trellis node; `Has Input Image?` false ->
   **Compose Prompt**. Leave **Check API Key** false -> **Reject**.
5. Check that the fal node's `image_url` body field still reads `{{ $json.image_data_uri }}`.
6. Save. If your n8n shows a **Publish** button, publish too; otherwise saving an
   active workflow updates the production webhook.

Option B, import: Workflows -> Import from File creates a **new** workflow from
`generate-3d.workflow.json`. Set the gate key and attach both credentials (Setup
steps 2-3). Make the fal URL match what you run now, deactivate the old workflow,
then activate the new one: two active workflows cannot share the
`generate-3d` path.

## Notes

- Uses fal's **queue** endpoint (`queue.fal.run/fal-ai/trellis`) so generation is
  async; the MCP's `wait_for_3d_job` polls `3d-job-status` until done.
- The image step returns base64; it is wrapped as a `data:` URI and passed to fal
  as `image_url`.
- A future version may replace n8n with direct in-Python OpenRouter + fal calls
  (`OPENROUTER_API_KEY` / `FAL_KEY`) for a zero-infrastructure setup.
