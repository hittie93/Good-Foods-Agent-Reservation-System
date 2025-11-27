# Tool Calling vs MCP / A2A in this Project

This GoodFoods reservation agent implements a **custom tool calling layer** instead of wiring directly into MCP or A2A, while keeping the same core ideas so it can be migrated later.

## Current Architecture

- The LLM is instructed (via `SYSTEM_PROMPT`) to return JSON of the form:
  - With a tool call:
    ```json
    {
      "tool_call": {
        "name": "<tool_name>",
        "arguments": { ... }
      }
    }
    ```
  - Without a tool:
    ```json
    {
      "tool_call": null,
      "message": "<natural language reply>"
    }
    ```
- `agent.py` parses this JSON and looks up the implementation in the central `TOOLS` registry defined in `tools.py`.
- Each entry in `TOOLS` has:
  - `description`
  - JSON `schema` for arguments
  - `fn`: a Python function that executes the tool.

This mirrors the ideas in modern protocols (MCP/A2A): a **typed tool catalog** plus **model-driven tool selection**, but implemented in a light-weight, framework‑free way suitable for a take‑home assignment.

## Why not full MCP / A2A here?

- The assignment environment is a small, self-contained Streamlit app with no external tool servers.
- Introducing a full MCP server/client stack would add significant boilerplate without changing the business behavior.
- Instead, the project focuses on:
  - Clear separation of concerns (LLM vs tools vs DB).
  - Typed tool schemas, aliases, and smart tools like `smart_book`.
  - Easy extensibility: adding a new tool is a single function + TOOLS entry.

## How this could be upgraded to MCP later

- Wrap the existing tool functions (`search_restaurants`, `create_reservation`, `cancel_reservation`, `list_reservations`, `smart_book`, etc.) as MCP tools exposed by a small MCP server.
- Replace the custom JSON protocol with the standard MCP tool invocation flow while keeping the same business logic.
- This would allow the same GoodFoods tools to be reused by other LLM frontends that speak MCP or A2A.

In summary, this project **implements the core principles of modern tool calling** (typed tools, model‑driven selection, clear separation) in a minimal way, and documents a clear path to a full MCP/A2A integration if required for production.
