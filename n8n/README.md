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
| `generate-3d.workflow.json` | `POST /webhook/generate-3d` | prompt -> (OpenRouter image) -> submit to fal Trellis queue -> returns `{ job_id, status_url, response_url }` |
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

## Notes

- Uses fal's **queue** endpoint (`queue.fal.run/fal-ai/trellis`) so generation is
  async; the MCP's `wait_for_3d_job` polls `3d-job-status` until done.
- The image step returns base64; it is wrapped as a `data:` URI and passed to fal
  as `image_url`.
- A future version may replace n8n with direct in-Python OpenRouter + fal calls
  (`OPENROUTER_API_KEY` / `FAL_KEY`) for a zero-infrastructure setup.
