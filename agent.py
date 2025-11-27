# agent.py
import json
from typing import List, Dict
from llm_client import call_llama, SYSTEM_PROMPT
from tools import TOOLS

def run_agent(user_query: str, history: List[Dict]) -> Dict:
    # history: list of {"role": "user/assistant", "content": "..."} for context

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [
        {"role": "user", "content": user_query}
    ]
    raw = call_llama(messages)

    # Try to parse JSON, and handle errors gracefully.
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: treat entire content as a natural reply.
        return {
            "assistant_message": raw,
            "tool_used": None,
            "tool_result": None,
            "raw": raw
        }

    tool_call = parsed.get("tool_call")
    if tool_call:
        name = tool_call.get("name")
        args = tool_call.get("arguments", {})
        tool = TOOLS.get(name)
        if not tool:
            return {
                "assistant_message": f"Sorry, I don't recognize the tool '{name}'.",
                "tool_used": None,
                "tool_result": None,
                "raw": raw
            }
        result = tool["fn"](args)

        # Now call the model again to explain result to user
        # Note: Avoid role 'tool' as Groq expects tool_call_id. Provide result in a normal message instead.
        followup_messages = messages + [
            {"role": "assistant", "content": raw},
            {
                "role": "user",
                "content": (
                    f"Tool '{name}' returned: {json.dumps(result)}. "
                    "Using only this tool output and the prior conversation, "
                    "reply to the user with a very short answer: either a single concise "
                    "sentence or a simple list of GoodFoods outlets/locations or the final "
                    "booking details. Do not explain tools or your reasoning."
                ),
            },
        ]
        final_raw = call_llama(followup_messages)
        return {
            "assistant_message": final_raw,
            "tool_used": name,
            "tool_result": result,
            "raw": final_raw
        }

    # No tool needed, just return normal reply
    return {
        "assistant_message": parsed.get("message", raw),
        "tool_used": None,
        "tool_result": None,
        "raw": raw
    }
