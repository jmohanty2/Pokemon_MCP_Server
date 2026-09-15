# Pokémon MCP Server for ChatGPT

This project reproduces the MCP server from 2MinutesPy's **“Building an MCP
server in 2 minutes”** video. It exposes the same three tools:

- `get_pokemon_info(name)` — fetch live Pokémon types, abilities, and stats
- `create_tournament_squad()` — build the video's six-Pokémon squad
- `list_popular_pokemon()` — list the video's popular tournament picks

The only important change is the connection method. The video uses local
`stdio`; ChatGPT needs a remotely reachable MCP endpoint. This project therefore
defaults to **Streamable HTTP** at `/mcp`.

No OpenAI API key or PokéAPI key is required.

## What is happening, in plain English?

1. You ask ChatGPT a Pokémon question.
2. ChatGPT chooses one of this server's three tools.
3. The server calls the public PokéAPI when live data is needed.
4. The server sends the Pokémon information back to ChatGPT.

## Run it locally

You need Python 3.11 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python server.py
```

The MCP URL is:

```text
http://localhost:8000/mcp
```

ChatGPT cannot call that localhost URL directly. Local running is for testing;
use the deployment section to give ChatGPT a public HTTPS URL.

Run the automated tests:

```bash
pytest
```

Run the live PokéAPI smoke test:

```bash
PYTHONPATH=. python scripts/smoke_test.py
```

## Deploy it for ChatGPT

The included `Dockerfile` works on Render, Railway, Fly.io, Google Cloud Run,
Azure Container Apps, or another Docker host. The easiest beginner route is:

1. Create a GitHub repository and upload this project's files.
2. In Render, choose **New → Blueprint** and select that repository.
3. Deploy the `render.yaml` blueprint.
4. Copy the public Render URL and add `/mcp` to the end.

Example:

```text
https://pokemon-chatgpt-mcp-xxxx.onrender.com/mcp
```

Free hosts may sleep when unused, so the first tool call can take longer.

## Connect it to ChatGPT

After deployment:

1. Open **ChatGPT → Settings → Security and login**.
2. Turn on **Developer mode**.
3. Open **ChatGPT Plugins** and select the plus button.
4. Create a connection named `Pokemon MCP`.
5. Enter your complete public URL, including `/mcp`.
6. Review the three discovered tools and save the connection.
7. In a new chat, enable `Pokemon MCP` from the tools menu.

If Developer mode or Plugins is not shown, custom MCP connections may not be
enabled for your current account or workspace yet.

## Prompts to test in ChatGPT

```text
Use Pokemon MCP to tell me Pikachu's type, abilities, and stats.
```

```text
Use Pokemon MCP to list the popular tournament Pokémon.
```

```text
Use Pokemon MCP to build me the tournament squad.
```

## Optional: run like the original video

To use the original local `stdio` transport with an MCP-compatible desktop
client:

```bash
MCP_TRANSPORT=stdio python server.py
```

## Security note

This server contains only read-only Pokémon tools and no private data. Because
it has no authentication, anyone who knows the deployed URL can call it. Add
authentication before reusing this pattern for private files, accounts, or
write actions.

## Sources

- Video source repository: <https://github.com/Sachin-crypto/Pokemon-MCP-Server>
- PokéAPI: <https://pokeapi.co/>
- OpenAI remote MCP guide: <https://developers.openai.com/api/docs/mcp>
