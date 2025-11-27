
# GoodFoods Conversational Reservation Assistant  
### Part 1 – Solution Design & Business Strategy

## 1. Context & Vision

GoodFoods has grown from a few popular outlets to a city‑wide brand in Bangalore. That growth is great news, but it has also made something very basic surprisingly hard: **getting a table**.

Today, most reservations still come through phone calls or ad‑hoc online forms. Each outlet picks up its own calls, maintains its own notes, and tries to guess how busy the evening will be. Customers often don’t know which outlet is right for their group, and staff don’t have a single view of upcoming bookings.

The vision for this project is simple:

> “Make booking a GoodFoods table as easy as messaging a friend who knows every outlet, every capacity, and your preferences.”

The conversational assistant should:

- Help guests choose the right outlet for their occasion.
- Book, modify, and cancel reservations without friction.
- Quietly capture the data GoodFoods needs to run smarter operations and marketing.

---

## 2. Business Problems & Opportunities

### 2.1 Problems we’re solving

- **Scattered reservation handling**  
  Each outlet manages its own calls and notes. There’s no central view of who is coming where and when.

- **Under‑utilized capacity**  
  Some outlets regularly run full, while others in nearby areas have empty tables at the same time. There is no systematic way to route guests to outlets with available capacity.

- **Heavy load on staff**  
  A large portion of staff time is spent on calls about directions, “do you have space for 6 at 8 pm?”, or “which outlet is better for a birthday?”. This takes attention away from the in‑house experience.

- **Little structured customer data**  
  Phone bookings rarely capture details like veg‑only preference, kids, parking needs, birthday occasions, etc. This makes it hard to personalize service or run targeted campaigns later.

- **Inconsistent guest experience**  
  The quality of the interaction depends on who picks up the phone. Some guests get detailed guidance; others are simply told “come by, we’ll try”.

### 2.2 Opportunities beyond basic booking

- **Smart routing across outlets**  
  If one outlet is nearly full, the assistant can suggest nearby GoodFoods branches with better availability, instead of turning guests away.

- **Occasion‑aware recommendations**  
  The assistant can propose specific outlets for family dinners, date nights, kids’ birthdays, or office team events, based on tags and capacities already in the dataset.

- **Better demand shaping**  
  By understanding party size and timing, GoodFoods can gently nudge guests towards slightly earlier/later slots or less crowded locations.

- **Foundation for loyalty & CRM**  
  With phone numbers, repeat visits, and preferences captured consistently, GoodFoods can later launch loyalty programs, targeted offers, and feedback loops.

---

## 3. Use Cases (business view)

### 3.1 “I just want a place to go”

A guest messages:

> “We’re 4 people, somewhere around Koramangala tomorrow evening. Can you suggest a place?”

The assistant:

1. Confirms date/time and budget.
2. Suggests 2–3 GoodFoods outlets in and around Koramangala with basic price levels and why each fits.
3. Books the chosen outlet once the guest shares name and phone number.

### 3.2 Handling large groups

A team lead says:

> “We’re 14 people, near Whitefield, Friday night.”

The assistant:

1. Filters outlets by capacity and budget.
2. Suggests only those that comfortably handle 14 people.
3. If one outlet is nearing capacity, offers alternatives in nearby areas proactively.

### 3.3 Managing existing bookings

A guest:

> “What bookings do I have under 98765XXXXX?”  
> “Cancel the Koramangala one for tonight.”

The assistant:

1. Lists upcoming reservations tied to that phone number.
2. Confirms which one to cancel or modify.
3. Updates the reservation status and clearly confirms the change.

### 3.4 Handling fuzzy or messy inputs

Guests often type:

- “yelanhka” instead of “Yelahanka”
- “mg road side” instead of “MG Road”

The assistant uses fuzzy matching to map this to real areas and outlets, instead of failing or asking the user to start over.

---

## 4. Success Metrics & ROI

### 4.1 What we will measure

**Customer‑facing metrics**

- Conversion rate from initial query → confirmed reservation.
- Average time taken to complete a booking.
- Customer satisfaction (simple thumbs‑up/thumbs‑down or NPS after the visit).

**Operational metrics**

- Increase in table utilization during off‑peak hours.
- Reduction in inbound phone calls related to reservations.
- No‑show rate, and whether guests are more likely to modify than simply not turn up.

**Business metrics**

- Net increase in reservations per week across the chain.
- Proportion of bookings successfully routed to less busy outlets.
- Repeat visitor rate (by phone number) over a quarter.

### 4.2 ROI narrative (high‑level)

- Even a **5–10% increase** in reservations during shoulder hours, plus a small reduction in no‑shows, can materially lift revenue for a 60‑outlet chain.
- At the same time, **staff time saved** from fewer phone calls can be redirected to better on‑premise service, which feeds back into higher guest satisfaction and repeat visits.
- The technical footprint is intentionally light (small LLM + SQLite), so infrastructure cost stays modest relative to the potential uplift.

---

## 5. Vertical Expansion: Beyond GoodFoods

The way the system is designed, GoodFoods is essentially a **dataset and a prompt**, not hard‑coded business logic.

This makes it straightforward to adapt to:

- **Other restaurant groups**  
  Swap in a new outlet dataset and tweak brand tone and constraints in the system prompt.

- **Hotel restaurants**  
  Same pattern, but with hotel-specific tags (in‑house guests, brunch, buffet, etc.).

- **Adjacent appointment businesses**  
  - **Cinemas:** showtimes and seats instead of tables and slots.  
  - **Salons/spas:** services and stylists instead of cuisines and outlets.  
  - **Clinics:** doctors, specialities, and appointment windows.

The tools (search, recommend, book, cancel, list) remain the same; only the domain objects and wording change.

---

## 6. Unique Advantages of This Approach

### 6.1 Deeply grounded in GoodFoods data

The assistant is not a generic “restaurant bot”. It knows only GoodFoods outlets, their areas, capacities, cuisines, and tags. This reduces irrelevant suggestions and keeps the conversation on‑brand.

### 6.2 Smart booking, not just form‑filling

Instead of mimicking an online form in chat, the assistant:

- Interprets open‑ended messages (“hanging out near HSR tomorrow night”).
- Proposes curated options with reasons.
- Fixes typos and ambiguous areas.
- Either confirms a booking or very clearly asks for the few missing details.

This feels closer to talking to an informed human host than filling a form.

### 6.3 Simple, extensible architecture

The implementation deliberately avoids heavy frameworks:

- A small Llama model, a thin `llm_client.py`, and a `TOOLS` registry.
- Clear separation of concerns:
  - LLM handles language and intent.
  - Tools handle business logic and persistence.
  - Streamlit handles UI.

Because of this, GoodFoods can:

- Swap models or providers.
- Move from SQLite to a managed database.
- Add new tools (e.g. feedback capture, promo suggestions) with minimal changes.

---

## 7. Implementation Plan (business view)

### Phase 1 – Pilot (current project)

- One‑city focus (Bangalore).
- All GoodFoods outlets onboarded into the dataset.
- Assistant available via web/mobile interface.
- Basic analytics on bookings and utilization.

### Phase 2 – Operational rollout

- Integrate with in‑store systems so staff can see and update reservations.
- Train staff to use the assistant for overbooking and waitlist decisions.
- Start collecting simple feedback after visits.

### Phase 3 – Multi‑brand / Multi‑city

- Extend to partner restaurant groups under a shared platform.
- Enhance analytics and CRM integrations.
- Explore non‑restaurant pilots (e.g. events, salons) using the same architecture.

---

## 8. Assumptions & Limitations

- The current implementation uses a **single small LLM model** (llama‑3.x via Groq) and a simple SQLite DB; in production this would be upgraded to a managed DB and more robust infra.
- Real‑time table availability per time slot is simplified; we assume capacity‑based filtering rather than true slot management.
- Authentication and user identity management (beyond phone number) are out of scope for this challenge but would be required in production.

---

## 9. Summary

The GoodFoods conversational reservation assistant is aimed at more than just “booking a table”. It centralizes reservations, helps route guests to the right outlets, and gives GoodFoods a clean data foundation for operations and marketing. The current prototype shows a clear path from a lightweight MVP to a production‑ready, multi‑brand system that can extend beyond restaurants into any appointment‑driven business.

