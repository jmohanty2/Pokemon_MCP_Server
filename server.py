"""Pokémon MCP server from the 2MinutesPy video, adapted for ChatGPT.

The three tools intentionally match the original project:
1. get_pokemon_info
2. create_tournament_squad
3. list_popular_pokemon

The original video used the local ``stdio`` transport. ChatGPT needs a remote
HTTP endpoint, so this version defaults to MCP's Streamable HTTP transport.
"""

from __future__ import annotations

import os

import httpx
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
MCP_TRANSPORT = os.getenv("MCP_TRANSPORT", "streamable-http")
POKEAPI_BASE = "https://pokeapi.co/api/v2"

mcp = FastMCP(
    "Pokemon MCP Server",
    instructions=(
        "Use these read-only tools to look up live Pokemon data, list popular "
        "Pokemon, or create the six-Pokemon tournament squad from the original demo."
    ),
    host=HOST,
    port=PORT,
    streamable_http_path="/mcp",
)


@mcp.custom_route("/health", methods=["GET"])
async def health_check(_: Request) -> JSONResponse:
    """Give hosting platforms a simple readiness endpoint."""
    return JSONResponse({"status": "ok"})


async def fetch_pokemon_data(name: str) -> dict:
    """Fetch one Pokémon record from PokéAPI, returning an empty dict on failure."""
    normalized_name = name.strip().lower()
    if not normalized_name or len(normalized_name) > 100:
        return {}

    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(f"{POKEAPI_BASE}/pokemon/{normalized_name}")
            if response.status_code == 200:
                return response.json()
    except (httpx.HTTPError, ValueError):
        pass
    return {}


@mcp.tool()
async def get_pokemon_info(name: str) -> str:
    """Get detailed live information about a Pokémon by name."""
    data = await fetch_pokemon_data(name)
    if not data:
        return f"No data found for Pokémon: {name}"

    stats = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
    types = [item["type"]["name"] for item in data["types"]]
    abilities = [item["ability"]["name"] for item in data["abilities"]]

    return (
        f"Name: {data['name'].capitalize()}\n"
        f"Types: {', '.join(types)}\n"
        f"Abilities: {', '.join(abilities)}\n"
        f"Stats: {', '.join(f'{key}: {value}' for key, value in stats.items())}\n"
        f"Source: {POKEAPI_BASE}/pokemon/{data['name']}"
    )


@mcp.tool()
async def create_tournament_squad() -> str:
    """Create the powerful six-Pokémon tournament squad from the video."""
    top_pokemon = [
        "charizard",
        "garchomp",
        "lucario",
        "dragonite",
        "metagross",
        "gardevoir",
    ]
    squad = []

    for name in top_pokemon:
        data = await fetch_pokemon_data(name)
        if data:
            squad.append(data["name"].capitalize())

    if not squad:
        return "PokéAPI is temporarily unavailable, so the squad could not be created."
    return "Tournament Squad:\n" + "\n".join(squad)


@mcp.tool()
async def list_popular_pokemon() -> str:
    """List the six popular tournament-ready Pokémon from the video."""
    return "\n".join(
        [
            "Charizard",
            "Garchomp",
            "Lucario",
            "Dragonite",
            "Metagross",
            "Gardevoir",
        ]
    )


if __name__ == "__main__":
    mcp.run(transport=MCP_TRANSPORT)
