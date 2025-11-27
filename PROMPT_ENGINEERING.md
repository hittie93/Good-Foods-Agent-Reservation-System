# Prompt Engineering Approach – GoodFoods Conversational Assistant

This document explains how the system prompt and tool-calling behavior for the GoodFoods assistant were designed and iterated.

## 1. Starting from behavior, not APIs

The first step was to think like a GoodFoods host, not like a developer:

- How should the assistant talk to guests?
- What questions should it ask before confirming a booking?
- When should it suggest alternatives vs. just taking an order?

That behaviour was written out in plain language (tone, flow of questions, brand rules), and only then converted into a structured `SYSTEM_PROMPT` for the LLM.

## 2. Clear separation between user language and tools

The prompt makes a strong distinction between:

- **User-facing replies:** natural language, friendly, no mention of tools, APIs, or JSON.
- **Internal actions:** always executed via tools (`search_restaurants`, `smart_book`, `create_reservation`, `list_reservations`, etc.).

The model is told to treat tools as an internal capability and to rely on them for all data access and state changes, instead of trying to “fake” bookings in pure text.

## 3. Tight JSON tool-calling contract

To keep the agent logic simple and robust, the prompt describes a small JSON protocol the model must follow:

- When a tool is needed:

```json
{
  "tool_call": {
    "name": "<tool_name>",
    "arguments": { ... }
  }
}
```

- When no tool is needed:

```json
{
  "tool_call": null,
  "message": "<natural language reply>"
}
```

`agent.py` depends on this format to decide whether to execute a tool or just show the `message` field. Keeping the contract explicit in the prompt makes the behaviour more stable.

## 4. Guided slot-filling for bookings

The prompt lists exactly which pieces of information are required **before** a reservation can be confirmed:

- restaurant choice
- date
- time
- party size
- guest name
- contact phone number
- special requests (optional)

If any of these are missing, the assistant is instructed to ask specific follow-up questions rather than vague “Can you share more details?” prompts. This turns free‑form chat into a structured booking flow without exposing a form.

## 5. Smart booking via `smart_book`

Instead of having the model manually reason through all edge cases, a higher-level tool `smart_book` was created and described in the prompt. The model is encouraged to:

- Use `smart_book` when the user gives partial information about area/restaurant.
- Let the tool handle typos and fuzzy matches (e.g. “yelanhka” → “Yelahanka”).
- Rely on the tool to either pick the best restaurant or return a list of candidates + missing fields.

This reduces prompt complexity and keeps most business logic in Python rather than in free‑text instructions.

## 6. Iteration from real failures

The prompt was refined based on how the model actually behaved during testing:

- **Issue: invented bookings and IDs**  
  Early on, the model sometimes replied with “Your booking is confirmed” and a fake ID (e.g. `GF-1234`) without ever calling a reservation tool.
  
  **Fix in prompt:** explicitly require that the assistant **must not** claim a booking is confirmed unless a reservation tool has returned an object with an `id`, and must use that ID in the summary.

- **Issue: JSON leaking into the UI**  
  At times, the raw JSON (including `tool_call`) appeared in the chat.
  
  **Fix in prompt + UI:** clarify that tools are internal only. On the UI side, `app.py` strips the JSON and displays only the `message` field.

- **Issue: incomplete bookings**  
  The model sometimes tried to book without name or phone.
  
  **Fix in prompt:** reinforce the list of mandatory fields and tell the assistant to ask for missing ones before creating the reservation.

Each of these cycles tightened the instructions and made the tool-calling behaviour more reliable.

## 7. Why this matters

By combining:

- a business-driven system prompt,
- a small, explicit JSON protocol,
- clear slot-filling rules, and
- iteration guided by failures,

the GoodFoods assistant stays close to how a real human host would behave while still being easy to integrate and debug from an engineering perspective.
