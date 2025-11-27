 # app.py
import json
import streamlit as st
from agent import run_agent
from tools import tool_list_reservations
from restaurant_data import RESTAURANTS

st.set_page_config(page_title="GoodFoods AI Reservation Agent", page_icon="🍽️")

st.title("🍽️ GoodFoods Reservation Assistant")

if "history" not in st.session_state:
    st.session_state.history = []

tab_chat, tab_reservations = st.tabs(["Chat", "My Reservations"])

with tab_chat:
    for turn in st.session_state.history:
        with st.chat_message("user"):
            st.write(turn["user"])
        with st.chat_message("assistant"):
            text = turn["assistant"]
            # If the assistant_message is JSON with a 'message' field, show only that
            if isinstance(text, str) and text.strip().startswith("{"):
                try:
                    parsed = json.loads(text)
                    if isinstance(parsed, dict) and "message" in parsed:
                        text = parsed["message"]
                except json.JSONDecodeError:
                    pass
            st.write(text)

    user_input = st.chat_input("Ask me to book a table, modify, or cancel a reservation...")

    if user_input:
        try:
            result = run_agent(user_input, [
                {"role": "user", "content": h["user"]}
                for h in st.session_state.history
            ] + [
                {"role": "assistant", "content": h["assistant"]}
                for h in st.session_state.history
            ])
        except RuntimeError as e:
            msg = str(e)
            if "rate_limit_exceeded" in msg or "429" in msg:
                st.error("Our AI service is getting a bit busy right now. Please wait a few seconds and try again.")
            else:
                st.error("Something went wrong while talking to the AI service. Please try again in a moment.")
        else:
            st.session_state.history.append({
                "user": user_input,
                "assistant": result["assistant_message"]
            })

            st.rerun()

with tab_reservations:
    st.subheader("View your reservations")
    phone = st.text_input("Enter your phone number")
    if st.button("Show my reservations") and phone:
        # Call the reservation tool directly for a clean UI
        result = tool_list_reservations({"phone": phone})
        reservations = result.get("reservations", [])

        if not reservations:
            st.info("No reservations found for this phone number.")
        else:
            # Build a quick lookup from restaurant_id to name/area
            id_to_restaurant = {r["id"]: r for r in RESTAURANTS}
            for res in reservations:
                rinfo = id_to_restaurant.get(res["restaurant_id"], {})
                name = rinfo.get("name", res["restaurant_id"])
                area = rinfo.get("area", "")
                st.markdown(
                    f"- **{name}** ({area}) — {res['datetime']} — "
                    f"{res['party_size']} people — Reservation ID: `{res['id']}`"
                )

