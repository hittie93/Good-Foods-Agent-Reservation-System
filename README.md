# GoodFoods Conversational Reservation Agent

An end-to-end conversational AI assistant that helps users find and book tables at **GoodFoods** restaurants across Bangalore.

This project is built as part of the Sarvam AI LLM challenge. It focuses on:

- Business strategy and solution design (Part 1).
- A fully working technical implementation (Part 2) with:
  - Streamlit frontend
  - Llama model via Groq
  - Tool-calling agent
  - Static restaurant dataset (~60 outlets)
  - SQLite-backed reservation storage

---

## 1. Demo Video (Required)

> **Placeholder**: Add your Loom / YouTube link here before submission.
>
> Example: `https://www.loom.com/share/your-demo-link`

In the demo, show at least:

- A full booking flow via chat (from vague intent to confirmed reservation).
- Recommendation behavior (assistant suggests outlets based on area/party size).
- Viewing bookings in **My Reservations** by phone number.
- Cancellation or modification flow.

---

## 2. Project Structure

```text
AI_agent_Restraunt/
├─ app.py                  # Streamlit UI (chat + My Reservations)
├─ agent.py                # Agent orchestration (LLM + tools)
├─ llm_client.py           # Llama (Groq) client + system prompt
├─ tools.py                # Tool registry + business logic
├─ restaurant_data.py      # Static GoodFoods dataset (~60 outlets)
├─ reservation_db.py       # SQLite persistence helpers
├─ reservations.db         # SQLite database (created at runtime)
├─ MCP_A2A_NOTE.md         # Notes on tool calling vs MCP/A2A
├─ GOODFOODS_SOLUTION_DESIGN.md  # Part 1 business/strategy document
├─ requirements.txt        # Python dependencies
└─ ... (virtualenv, etc.)
```

---

## 3. Setup Instructions

### 3.1 Prerequisites

- Python 3.10+
- A Groq API key with access to a small Llama model (e.g. `llama-3.1-8b-instant`).

### 3.2 Install dependencies

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3.3 Environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

### 3.4 Run the app

```bash
streamlit run app.py
```

Open the local URL shown in the terminal (usually `http://localhost:8501`).

---

## 4. How the Agent Works

### 4.1 LLM & Prompting

- `llm_client.py` wraps the Groq Chat Completions API around a small Llama model.
- `SYSTEM_PROMPT` defines:
  - GoodFoods context (single brand with many Bangalore outlets).
  - Domain behavior for recommendations, booking, and cancellation.
  - Style guidelines (concise, friendly, minimal clarifications).
  - An **internal JSON protocol**:
    - When tools are needed, the model returns:
      ```json
      { "tool_call": { "name": "<tool_name>", "arguments": { ... } } }
      ```
    - When no tools are needed:
      ```json
      { "tool_call": null, "message": "<reply>" }
      ```

### 4.2 Agent & Tool Calling

- `agent.py`:
  - Sends the conversation (system + history + new user turn) to the LLM.
  - Parses the JSON output.
  - If `tool_call` is present:
    - Looks up the tool in `TOOLS` (from `tools.py`).
    - Executes it and gets a Python result.
    - Calls the LLM again with the tool result to generate a final user-facing message.
  - If `tool_call` is `null`, it returns the `message` field directly.

This ensures the **LLM, not the UI code**, decides when to search, recommend, book, list, or cancel.

### 4.3 Tools & Business Logic

Defined in `tools.py`:

- `search_restaurants` – filter outlets by area, cuisine, capacity, and max cost.
- `recommend_restaurants` – rank outlets by tags, budget fit, and capacity proximity.
- `create_reservation` – validates inputs, creates a reservation ID, and writes to DB.
- `cancel_reservation` – marks a reservation as cancelled.
- `list_reservations` – fetches reservations by phone (from SQLite + in-memory cache).
- `smart_book` – higher-level helper that:
  - Handles typos in areas/restaurant names via fuzzy matching.
  - Either auto-selects a restaurant and books, or returns a list of candidates + missing fields.

Aliases like `book_restaurant`, `book_table`, `make_reservation`, `find_restaurants` are added so the LLM can use more natural tool names.

### 4.4 Data & Persistence

- `restaurant_data.py` contains ~60 GoodFoods outlets with:
  - `id`, `name`, `area`, `city`, `capacity`, `cuisine`, `avg_cost_per_person`, `tags`.
- `reservation_db.py`:
  - Manages `reservations.db` (SQLite).
  - Functions:
    - `save_reservation(rec)`
    - `mark_cancelled(res_id, cancelled_at)`
    - `list_reservations_by_phone(phone)`

The app can be migrated to a cloud DB (PostgreSQL, MySQL, etc.) by swapping this module.

---

## 5. Streamlit Frontend & UX

- `app.py` provides two tabs:
  - **Chat** – main conversational interface.
    - Shows user and assistant turns.
    - Hides internal JSON, only rendering the `message` part of the LLM output.
  - **My Reservations** – view reservations by phone.
    - Input: phone number.
    - Calls `tool_list_reservations` and renders a clean bullet list with:
      - outlet name & area
      - datetime
      - party size
      - reservation ID

The UX is intentionally minimal and mobile-friendly for quick usage.

---

## 6. Prompt Engineering & Conversation Design

Key strategies used:

- **Single authoritative system prompt** (`SYSTEM_PROMPT`) describing:
  - Brand constraints (GoodFoods only, no external restaurants).
  - Domain behavior for recommendations, booking, and cancellation.
  - Style guidelines (concise, friendly, minimal clarifications).
- **Tool-calling protocol** baked into the prompt so the model knows how to:
  - Decide whether a tool is needed.
  - Construct `tool_call` objects with appropriate arguments.
- **Smart booking behavior** via `smart_book`:
  - Encourages the LLM to delegate fuzzy matching and booking to a single tool instead of manually reasoning.
- **Concise style**: keep replies short, with bullet lists for options.

See `GOODFOODS_SOLUTION_DESIGN.md` for more on the business-side reasoning.

---

## 7. Example Conversations

### 7.1 Simple booking

1. User: "Hey, I am hanging out with friends tomorrow, help me book a restaurant."
2. Assistant: Asks for area, time, and party size.
3. User: "Koramangala, 7 pm, 4 people."
4. Assistant: Suggests 2–3 GoodFoods outlets in Koramangala with capacity and price bands.
5. User: Chooses one and provides name + phone.
6. Assistant: Confirms booking with reservation ID and summary.
7. User: Later, in **My Reservations**, enters phone and sees the booking.

### 7.2 Recommendations by constraints

1. User: "We are 10 people near Whitefield, budget around ₹600 per person."
2. Assistant: Uses `recommend_restaurants` to rank outlets.
3. Presents 2–5 options tagged as good for groups and within budget.

### 7.3 Cancellation

1. User: "Cancel my booking for tonight under 98765XXXXX."
2. Assistant: Lists active reservations and asks which one.
3. After user confirms, calls `cancel_reservation` and reports status.

---

## 8. Business Strategy Summary

See **GOODFOODS_SOLUTION_DESIGN.md** for the full Part 1 document.

Highlights:

- Solves fragmented reservations and inconsistent customer experience.
- Creates a unified data layer for utilization, segmentation, and marketing.
- Designed for vertical expansion into other restaurant chains and adjacent appointment-based sectors (cinemas, salons, clinics).

---

## 9. Assumptions & Limitations

- Uses a single small LLM via Groq; in production a more robust deployment and monitoring would be required.
- Slot-level availability (per 15/30 minutes) is simplified to capacity filtering.
- Authentication beyond phone number is not implemented.
- MCP/A2A are not fully wired; instead a custom tool-calling protocol is used, with `MCP_A2A_NOTE.md` documenting how this could evolve.

---

## 10. Future Enhancements

- Richer availability logic (per time slot, per outlet).
- Management dashboard for outlet and chain-level KPIs.
- Multi-brand, multi-city support with per-brand prompts and policies.
- Integration with CRM and notification channels (SMS/WhatsApp/email) for reminders and feedback.

---

## 11. Submission Checklist

- [x] End-to-end reservation agent with Streamlit frontend.
- [x] 50–100 restaurant locations with varying capacities and cuisines.
- [x] Recommendation tools for venue selection.
- [x] Small Llama model via Groq.
- [x] Custom tool-calling architecture, model-driven intent.
- [x] SQLite persistence for reservations.
- [x] Business strategy document (`GOODFOODS_SOLUTION_DESIGN.md`).
- [x] README with setup, prompt design notes, and example conversations.

Before submitting, remember to:

- Add the **demo video link**.
- Share the private GitHub repo with the required reviewers.
- Verify that `.env` is not committed.