# tools.py
from typing import Dict, Any, List
from datetime import datetime
import difflib
from restaurant_data import search_restaurants, RESTAURANTS, AREAS
from reservation_db import save_reservation, mark_cancelled, list_reservations_by_phone

RESERVATIONS: Dict[str, Dict] = {}  # key = reservation_id

def generate_reservation_id() -> str:
    return f"RES-{len(RESERVATIONS) + 1:06d}"

def tool_search_restaurants(args: Dict[str, Any]) -> Dict[str, Any]:
    results = search_restaurants(
        area=args.get("area"),
        cuisine=args.get("cuisine"),
        min_capacity=args.get("min_capacity"),
        max_cost=args.get("max_cost"),
    )
    return {"restaurants": results}

def tool_create_reservation(args: Dict[str, Any]) -> Dict[str, Any]:
    # In real system, would check slot availability per time.
    required = ["restaurant_id", "name", "phone", "party_size", "datetime"]
    missing = [k for k in required if k not in args or args[k] in (None, "")]
    if missing:
        return {
            "error": "Missing required fields for reservation.",
            "missing_fields": missing,
        }

    reservation_id = generate_reservation_id()
    record = {
        "id": reservation_id,
        "restaurant_id": args["restaurant_id"],
        "name": args["name"],
        "phone": args["phone"],
        "party_size": args["party_size"],
        "datetime": args["datetime"],
        "special_requests": args.get("special_requests", ""),
        "created_at": datetime.utcnow().isoformat(),
    }

    # In-memory store for fast access
    RESERVATIONS[reservation_id] = {**record}

    # Persist to SQLite
    save_reservation({
        **record,
        "status": "active",
        "cancelled_at": None,
    })

    return RESERVATIONS[reservation_id]

def tool_cancel_reservation(args: Dict[str, Any]) -> Dict[str, Any]:
    rid = args.get("reservation_id")
    if rid in RESERVATIONS:
        res = RESERVATIONS.pop(rid)
        res["status"] = "cancelled"

        cancelled_at = datetime.utcnow().isoformat()
        # Update DB record if present
        mark_cancelled(rid, cancelled_at)

        res["cancelled_at"] = cancelled_at
        return {"success": True, "reservation": res}

    return {"success": False, "error": "Reservation ID not found"}

def tool_list_reservations(args: Dict[str, Any]) -> Dict[str, Any]:
    phone = args.get("phone")
    if not phone:
        return {"reservations": []}

    # Load from persistent DB first
    db_rows = list_reservations_by_phone(phone)

    # Also include any in-memory reservations from this session that might not yet
    # have been flushed or that were created before DB persistence was added.
    mem_rows = [r for r in RESERVATIONS.values() if r["phone"] == phone]

    # Merge, preferring in-memory entries for the same id
    by_id = {r["id"]: r for r in db_rows}
    for r in mem_rows:
        by_id[r["id"]] = r

    return {"reservations": list(by_id.values())}

def tool_recommend_restaurants(args: Dict[str, Any]) -> Dict[str, Any]:
    """Recommend restaurants ranked by fit for party size, budget, area, and tags."""
    area = args.get("area")
    cuisine = args.get("cuisine")
    party_size = args.get("party_size")
    max_cost = args.get("max_cost")
    desired_tags: List[str] = args.get("tags") or []

    # Start from the same filtered set as search_restaurants
    candidates = search_restaurants(
        area=area,
        cuisine=cuisine,
        min_capacity=party_size,
        max_cost=max_cost,
    )

    def score(r: Dict[str, Any]) -> float:
        s = 0.0
        # Prefer matching tags
        if desired_tags:
            overlap = len({t.lower() for t in desired_tags} & {t.lower() for t in r.get("tags", [])})
            s += overlap * 3.0
        # Prefer lower cost within budget
        if max_cost:
            s += max(0.0, (max_cost - r["avg_cost_per_person"]) / max_cost)
        # Prefer capacity close to party size but with a bit of buffer
        if party_size:
            excess = r["capacity"] - party_size
            if excess >= 0:
                s += 2.0 - min(excess / 50.0, 2.0)  # smaller excess is better
        return s

    ranked = sorted(candidates, key=score, reverse=True)
    return {"restaurants": ranked[:10]}

def _fuzzy_match(query: str, choices: List[str], cutoff: float = 0.6) -> str | None:
    if not query:
        return None
    matches = difflib.get_close_matches(query.lower(), [c.lower() for c in choices], n=1, cutoff=cutoff)
    if not matches:
        return None
    # Map back to original casing
    target = matches[0]
    for c in choices:
        if c.lower() == target:
            return c
    return None

def tool_smart_book(args: Dict[str, Any]) -> Dict[str, Any]:
    """Smart booking helper.

    - Handles minor typos in area / restaurant name using fuzzy matching.
    - If a clear best restaurant exists, creates the reservation immediately.
    - If ambiguous, returns a clean list of candidate restaurants for the user to pick.
    """

    area = args.get("area")
    restaurant_name = args.get("restaurant_name")
    restaurant_id = args.get("restaurant_id")
    cuisine = args.get("cuisine")
    party_size = args.get("party_size")
    max_cost = args.get("max_cost")
    name = args.get("name")
    phone = args.get("phone")

    # Allow either "datetime" or separate "date"+"time" fields
    dt = args.get("datetime")
    if not dt:
        date = args.get("date")
        time_str = args.get("time")
        if date and time_str:
            dt = f"{date} {time_str}"

    normalized_area = None
    candidates: List[Dict[str, Any]] = []
    chosen: Dict[str, Any] | None = None

    # If restaurant_id is provided (e.g. "GF-007"), select that outlet directly
    if restaurant_id:
        chosen = next((r for r in RESTAURANTS if r["id"] == restaurant_id), None)
        if not chosen:
            return {"error": f"Restaurant with id {restaurant_id} not found"}
        normalized_area = chosen["area"]
        candidates = [chosen]
    else:
        # Fuzzy-correct area name
        normalized_area = _fuzzy_match(area, AREAS) if area else None

        candidates = search_restaurants(
            area=normalized_area or area,
            cuisine=cuisine,
            min_capacity=party_size,
            max_cost=max_cost,
        )

        if not candidates:
            return {
                "error": "No restaurants match your criteria.",
                "normalized_area": normalized_area,
                "suggested_areas": AREAS,
            }

        # If user typed a restaurant name, fuzzy match within candidates
        if restaurant_name:
            names = [c["name"] for c in candidates]
            matched_name = _fuzzy_match(restaurant_name, names)
            if matched_name:
                for c in candidates:
                    if c["name"] == matched_name:
                        chosen = c
                        break

        # If still not chosen, fall back to first recommendation (they are already filtered)
        if not chosen:
            chosen = candidates[0]

    # If we don't yet have passenger details, just return choices instead of booking
    if not (name and phone and party_size and dt):
        return {
            "normalized_area": normalized_area,
            "chosen_restaurant": chosen,
            "candidates": candidates,
            "missing_fields": [
                f
                for f, v in {"name": name, "phone": phone, "party_size": party_size, "datetime": dt}.items()
                if not v
            ],
        }

    # All data present – create reservation via existing tool
    create_args = {
        "restaurant_id": chosen["id"],
        "name": name,
        "phone": phone,
        "party_size": party_size,
        "datetime": dt,
        "special_requests": args.get("special_requests", ""),
    }
    reservation = tool_create_reservation(create_args)
    return {
        "normalized_area": normalized_area,
        "restaurant": chosen,
        "reservation": reservation,
    }

TOOLS = {
    "search_restaurants": {
        "description": "Search restaurants by area, cuisine, capacity, cost",
        "schema": {
            "type": "object",
            "properties": {
                "area": {"type": "string"},
                "cuisine": {"type": "string"},
                "min_capacity": {"type": "integer"},
                "max_cost": {"type": "integer"}
            },
            "required": []
        },
        "fn": tool_search_restaurants
    },
    "create_reservation": {
        "description": "Create a reservation",
        "schema": {
            "type": "object",
            "properties": {
                "restaurant_id": {"type": "string"},
                "name": {"type": "string"},
                "phone": {"type": "string"},
                "party_size": {"type": "integer"},
                "datetime": {"type": "string"},
                "special_requests": {"type": "string"},
            },
            "required": ["restaurant_id", "name", "phone", "party_size", "datetime"]
        },
        "fn": tool_create_reservation
    },
    "cancel_reservation": {
        "description": "Cancel a reservation by ID",
        "schema": {
            "type": "object",
            "properties": {
                "reservation_id": {"type": "string"}
            },
            "required": ["reservation_id"]
        },
        "fn": tool_cancel_reservation
    },
    "list_reservations": {
        "description": "List reservations by phone number",
        "schema": {
            "type": "object",
            "properties": {
                "phone": {"type": "string"}
            },
            "required": ["phone"]
        },
        "fn": tool_list_reservations
    },
    "recommend_restaurants": {
        "description": "Recommend restaurants based on party size, budget, area, cuisine, and tags.",
        "schema": {
            "type": "object",
            "properties": {
                "area": {"type": "string"},
                "cuisine": {"type": "string"},
                "party_size": {"type": "integer"},
                "max_cost": {"type": "integer"},
                "tags": {
                    "type": "array",
                    "items": {"type": "string"}
                },
            },
            "required": []
        },
        "fn": tool_recommend_restaurants
    },
    "smart_book": {
        "description": "Smart booking that auto-corrects area/restaurant typos and either books or returns suggestions.",
        "schema": {
            "type": "object",
            "properties": {
                "area": {"type": "string"},
                "restaurant_name": {"type": "string"},
                "restaurant_id": {"type": "string"},
                "cuisine": {"type": "string"},
                "party_size": {"type": "integer"},
                "max_cost": {"type": "integer"},
                "name": {"type": "string"},
                "phone": {"type": "string"},
                "datetime": {"type": "string"},
                "date": {"type": "string"},
                "time": {"type": "string"},
                "special_requests": {"type": "string"},
            },
            "required": []
        },
        "fn": tool_smart_book
    }
}

# Aliases for common natural tool names the model may use
def tool_book_restaurant(args: Dict[str, Any]) -> Dict[str, Any]:
    return tool_create_reservation(args)

def tool_book_table(args: Dict[str, Any]) -> Dict[str, Any]:
    return tool_create_reservation(args)

def tool_cancel_booking(args: Dict[str, Any]) -> Dict[str, Any]:
    return tool_cancel_reservation(args)

def tool_make_reservation(args: Dict[str, Any]) -> Dict[str, Any]:
    return tool_create_reservation(args)

TOOLS.update({
    "book_restaurant": {
        "description": "Alias of create_reservation.",
        "schema": {
            "type": "object",
            "properties": {
                "restaurant_id": {"type": "string"},
                "name": {"type": "string"},
                "phone": {"type": "string"},
                "party_size": {"type": "integer"},
                "datetime": {"type": "string"},
                "special_requests": {"type": "string"}
            },
            "required": ["restaurant_id", "name", "phone", "party_size", "datetime"]
        },
        "fn": tool_book_restaurant
    },
    "book_table": {
        "description": "Alias of create_reservation.",
        "schema": {
            "type": "object",
            "properties": {
                "restaurant_id": {"type": "string"},
                "name": {"type": "string"},
                "phone": {"type": "string"},
                "party_size": {"type": "integer"},
                "datetime": {"type": "string"},
                "special_requests": {"type": "string"}
            },
            "required": ["restaurant_id", "name", "phone", "party_size", "datetime"]
        },
        "fn": tool_book_table
    },
    "make_reservation": {
        "description": "Alias of create_reservation.",
        "schema": {
            "type": "object",
            "properties": {
                "restaurant_id": {"type": "string"},
                "name": {"type": "string"},
                "phone": {"type": "string"},
                "party_size": {"type": "integer"},
                "datetime": {"type": "string"},
                "special_requests": {"type": "string"}
            },
            "required": ["restaurant_id", "name", "phone", "party_size", "datetime"]
        },
        "fn": tool_make_reservation
    },
    "cancel_booking": {
        "description": "Alias of cancel_reservation.",
        "schema": {
            "type": "object",
            "properties": {
                "reservation_id": {"type": "string"}
            },
            "required": ["reservation_id"]
        },
        "fn": tool_cancel_booking
    }
})

# Alias for 'find_restaurants' -> search_restaurants
def tool_find_restaurants(args: Dict[str, Any]) -> Dict[str, Any]:
    return tool_search_restaurants(args)

TOOLS.update({
    "find_restaurants": {
        "description": "Alias of search_restaurants.",
        "schema": {
            "type": "object",
            "properties": {
                "area": {"type": "string"},
                "cuisine": {"type": "string"},
                "min_capacity": {"type": "integer"},
                "max_cost": {"type": "integer"}
            },
            "required": []
        },
        "fn": tool_find_restaurants
    }
})

def tool_get_restaurants(args):
    """Wrapper so that LLM calls to 'get_restaurants' still work."""
    return tool_search_restaurants(args)

def tool_get_restaurant_details(args):
    """
    Very simple detail fetcher.
    Expect arguments: { "restaurant_id": "GF-001" }
    """
    rid = args.get("restaurant_id")
    restaurant = next((r for r in RESTAURANTS if r["id"] == rid), None)
    if not restaurant:
        return {"error": f"Restaurant with id {rid} not found"}
    return {"restaurant": restaurant}

TOOLS.update({
    "get_restaurants": {
        "description": "Search restaurants (alias of search_restaurants).",
        "schema": {
            "type": "object",
            "properties": {
                "area": {"type": "string"},
                "cuisine": {"type": "string"},
                "min_capacity": {"type": "integer"},
                "max_cost": {"type": "integer"}
            },
            "required": []
        },
        "fn": tool_get_restaurants
    },
    "get_restaurant_details": {
        "description": "Get details of a single restaurant by id.",
        "schema": {
            "type": "object",
            "properties": {
                "restaurant_id": {"type": "string"}
            },
            "required": ["restaurant_id"]
        },
        "fn": tool_get_restaurant_details
    }
})