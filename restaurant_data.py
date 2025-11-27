"""Static restaurant dataset and basic search utilities for GoodFoods."""

from typing import List, Dict

CUISINES = [
    "Italian",
    "North Indian",
    "South Indian",
    "Continental",
]

AREAS = [
    "Indiranagar",
    "Koramangala",
    "Whitefield",
    "HSR Layout",
    "MG Road",
    "BTM Layout",
    "Hebbal",
    "Yelahanka",
    "Marathahalli",
    "Vijayanagar",
]

RESTAURANTS: List[Dict] = [
    {
        "id": "GF-001",
        "name": "GoodFoods Indiranagar #1",
        "area": "Indiranagar",
        "city": "Bangalore",
        "capacity": 120,
        "cuisine": ["Italian"],
        "avg_cost_per_person": 850,
        "has_outdoor_seating": True,
        "is_veg_only": False,
        "tags": ["date-night", "parking"],
    },
    {
        "id": "GF-002",
        "name": "GoodFoods Koramangala #1",
        "area": "Koramangala",
        "city": "Bangalore",
        "capacity": 80,
        "cuisine": ["Italian", "Continental"],
        "avg_cost_per_person": 700,
        "has_outdoor_seating": False,
        "is_veg_only": False,
        "tags": ["date-night"],
    },
    {
        "id": "GF-003",
        "name": "GoodFoods Whitefield #2",
        "area": "Whitefield",
        "city": "Bangalore",
        "capacity": 70,
        "cuisine": ["Italian"],
        "avg_cost_per_person": 800,
        "has_outdoor_seating": False,
        "is_veg_only": True,
        "tags": ["veg", "date-night"],
    },
    {
        "id": "GF-004",
        "name": "GoodFoods HSR Layout #2",
        "area": "HSR Layout",
        "city": "Bangalore",
        "capacity": 150,
        "cuisine": ["Italian"],
        "avg_cost_per_person": 950,
        "has_outdoor_seating": True,
        "is_veg_only": False,
        "tags": ["date-night", "parking"],
    },
    {
        "id": "GF-005",
        "name": "GoodFoods MG Road #2",
        "area": "MG Road",
        "city": "Bangalore",
        "capacity": 70,
        "cuisine": ["Italian"],
        "avg_cost_per_person": 900,
        "has_outdoor_seating": True,
        "is_veg_only": False,
        "tags": ["date-night", "premium"],
    },
    {
        "id": "GF-006",
        "name": "GoodFoods BTM Layout #3",
        "area": "BTM Layout",
        "city": "Bangalore",
        "capacity": 60,
        "cuisine": ["Italian"],
        "avg_cost_per_person": 650,
        "has_outdoor_seating": False,
        "is_veg_only": False,
        "tags": ["family"],
    },
    {
        "id": "GF-007",
        "name": "GoodFoods Hebbal #1",
        "area": "Hebbal",
        "city": "Bangalore",
        "capacity": 110,
        "cuisine": ["Italian"],
        "avg_cost_per_person": 900,
        "has_outdoor_seating": True,
        "is_veg_only": False,
        "tags": ["premium", "date-night"],
    },
    {
        "id": "GF-008",
        "name": "GoodFoods Yelahanka #1",
        "area": "Yelahanka",
        "city": "Bangalore",
        "capacity": 130,
        "cuisine": ["Italian"],
        "avg_cost_per_person": 850,
        "has_outdoor_seating": True,
        "is_veg_only": False,
        "tags": ["date-night", "family"],
    },
    {
        "id": "GF-009",
        "name": "GoodFoods Marathahalli #1",
        "area": "Marathahalli",
        "city": "Bangalore",
        "capacity": 140,
        "cuisine": ["Italian"],
        "avg_cost_per_person": 950,
        "has_outdoor_seating": True,
        "is_veg_only": False,
        "tags": ["date-night", "groups"],
    },
    {
        "id": "GF-010",
        "name": "GoodFoods Vijayanagar #1",
        "area": "Vijayanagar",
        "city": "Bangalore",
        "capacity": 100,
        "cuisine": ["Italian"],
        "avg_cost_per_person": 850,
        "has_outdoor_seating": True,
        "is_veg_only": False,
        "tags": ["premium", "family"],
    },
    # Extra outlets to reach ~60 locations
    {"id": "GF-011", "name": "GoodFoods Indiranagar #2", "area": "Indiranagar", "city": "Bangalore", "capacity": 90,  "cuisine": ["Italian", "Continental"], "avg_cost_per_person": 800, "has_outdoor_seating": False, "is_veg_only": False, "tags": ["date-night"]},
    {"id": "GF-012", "name": "GoodFoods Indiranagar #3", "area": "Indiranagar", "city": "Bangalore", "capacity": 60,  "cuisine": ["North Indian"],          "avg_cost_per_person": 600, "has_outdoor_seating": False, "is_veg_only": False, "tags": ["family"]},
    {"id": "GF-013", "name": "GoodFoods Indiranagar #4", "area": "Indiranagar", "city": "Bangalore", "capacity": 140, "cuisine": ["Pan-Asian"],             "avg_cost_per_person": 950, "has_outdoor_seating": True,  "is_veg_only": False, "tags": ["premium", "groups"]},

    {"id": "GF-014", "name": "GoodFoods Koramangala #2", "area": "Koramangala", "city": "Bangalore", "capacity": 120, "cuisine": ["Italian"],               "avg_cost_per_person": 800, "has_outdoor_seating": True,  "is_veg_only": False, "tags": ["groups"]},
    {"id": "GF-015", "name": "GoodFoods Koramangala #3", "area": "Koramangala", "city": "Bangalore", "capacity": 70,  "cuisine": ["South Indian"],         "avg_cost_per_person": 350, "has_outdoor_seating": False, "is_veg_only": True,  "tags": ["veg", "budget"]},
    {"id": "GF-016", "name": "GoodFoods Koramangala #4", "area": "Koramangala", "city": "Bangalore", "capacity": 150, "cuisine": ["North Indian"],        "avg_cost_per_person": 700, "has_outdoor_seating": True,  "is_veg_only": False, "tags": ["family", "groups"]},

    {"id": "GF-017", "name": "GoodFoods Whitefield #3",  "area": "Whitefield",  "city": "Bangalore", "capacity": 90,  "cuisine": ["Italian"],             "avg_cost_per_person": 750, "has_outdoor_seating": False, "is_veg_only": False, "tags": ["date-night"]},
    {"id": "GF-018", "name": "GoodFoods Whitefield #4",  "area": "Whitefield",  "city": "Bangalore", "capacity": 160, "cuisine": ["North Indian"],        "avg_cost_per_person": 650, "has_outdoor_seating": True,  "is_veg_only": False, "tags": ["groups", "corporate"]},
    {"id": "GF-019", "name": "GoodFoods Whitefield #5",  "area": "Whitefield",  "city": "Bangalore", "capacity": 65,  "cuisine": ["South Indian"],        "avg_cost_per_person": 320, "has_outdoor_seating": False, "is_veg_only": True,  "tags": ["veg"]},

    {"id": "GF-020", "name": "GoodFoods HSR Layout #3",  "area": "HSR Layout",  "city": "Bangalore", "capacity": 80,  "cuisine": ["Italian"],             "avg_cost_per_person": 700, "has_outdoor_seating": False, "is_veg_only": False, "tags": ["family"]},
    {"id": "GF-021", "name": "GoodFoods HSR Layout #4",  "area": "HSR Layout",  "city": "Bangalore", "capacity": 180, "cuisine": ["North Indian"],        "avg_cost_per_person": 750, "has_outdoor_seating": True,  "is_veg_only": False, "tags": ["groups", "corporate"]},
    {"id": "GF-022", "name": "GoodFoods HSR Layout #5",  "area": "HSR Layout",  "city": "Bangalore", "capacity": 60,  "cuisine": ["South Indian"],        "avg_cost_per_person": 280, "has_outdoor_seating": False, "is_veg_only": True,  "tags": ["veg", "budget"]},

    {"id": "GF-023", "name": "GoodFoods MG Road #3",     "area": "MG Road",    "city": "Bangalore", "capacity": 90,  "cuisine": ["Italian", "Continental"], "avg_cost_per_person": 1000, "has_outdoor_seating": True,  "is_veg_only": False, "tags": ["premium", "date-night"]},
    {"id": "GF-024", "name": "GoodFoods MG Road #4",     "area": "MG Road",    "city": "Bangalore", "capacity": 60,  "cuisine": ["Mexican"],              "avg_cost_per_person": 800,  "has_outdoor_seating": False, "is_veg_only": False, "tags": ["groups"]},
    {"id": "GF-025", "name": "GoodFoods MG Road #5",     "area": "MG Road",    "city": "Bangalore", "capacity": 140, "cuisine": ["Pan-Asian"],            "avg_cost_per_person": 1100, "has_outdoor_seating": True,  "is_veg_only": False, "tags": ["corporate"]},

    {"id": "GF-026", "name": "GoodFoods BTM Layout #4",  "area": "BTM Layout",  "city": "Bangalore", "capacity": 80,  "cuisine": ["North Indian"],        "avg_cost_per_person": 550, "has_outdoor_seating": False, "is_veg_only": False, "tags": ["budget", "family"]},
    {"id": "GF-027", "name": "GoodFoods BTM Layout #5",  "area": "BTM Layout",  "city": "Bangalore", "capacity": 140, "cuisine": ["Italian"],             "avg_cost_per_person": 750, "has_outdoor_seating": True,  "is_veg_only": False, "tags": ["groups"]},
    {"id": "GF-028", "name": "GoodFoods BTM Layout #6",  "area": "BTM Layout",  "city": "Bangalore", "capacity": 60,  "cuisine": ["South Indian"],        "avg_cost_per_person": 260, "has_outdoor_seating": False, "is_veg_only": True,  "tags": ["veg"]},

    {"id": "GF-029", "name": "GoodFoods Hebbal #2",      "area": "Hebbal",     "city": "Bangalore", "capacity": 90,  "cuisine": ["Italian"],             "avg_cost_per_person": 850, "has_outdoor_seating": False, "is_veg_only": False, "tags": ["date-night"]},
    {"id": "GF-030", "name": "GoodFoods Hebbal #3",      "area": "Hebbal",     "city": "Bangalore", "capacity": 160, "cuisine": ["North Indian"],        "avg_cost_per_person": 700, "has_outdoor_seating": True,  "is_veg_only": False, "tags": ["groups", "corporate"]},
    {"id": "GF-031", "name": "GoodFoods Hebbal #4",      "area": "Hebbal",     "city": "Bangalore", "capacity": 70,  "cuisine": ["South Indian"],        "avg_cost_per_person": 320, "has_outdoor_seating": False, "is_veg_only": True,  "tags": ["veg"]},

    {"id": "GF-032", "name": "GoodFoods Yelahanka #2",   "area": "Yelahanka",  "city": "Bangalore", "capacity": 110, "cuisine": ["Italian"],             "avg_cost_per_person": 800, "has_outdoor_seating": True,  "is_veg_only": False, "tags": ["family"]},
    {"id": "GF-033", "name": "GoodFoods Yelahanka #3",   "area": "Yelahanka",  "city": "Bangalore", "capacity": 70,  "cuisine": ["North Indian"],        "avg_cost_per_person": 550, "has_outdoor_seating": False, "is_veg_only": False, "tags": ["budget"]},
    {"id": "GF-034", "name": "GoodFoods Yelahanka #4",   "area": "Yelahanka",  "city": "Bangalore", "capacity": 150, "cuisine": ["Pan-Asian"],            "avg_cost_per_person": 900, "has_outdoor_seating": True,  "is_veg_only": False, "tags": ["groups"]},

    {"id": "GF-035", "name": "GoodFoods Marathahalli #4", "area": "Marathahalli", "city": "Bangalore", "capacity": 90,  "cuisine": ["Italian"],         "avg_cost_per_person": 800, "has_outdoor_seating": False, "is_veg_only": False, "tags": ["date-night"]},
    {"id": "GF-036", "name": "GoodFoods Marathahalli #5", "area": "Marathahalli", "city": "Bangalore", "capacity": 170, "cuisine": ["North Indian"],    "avg_cost_per_person": 720, "has_outdoor_seating": True,  "is_veg_only": False, "tags": ["groups", "corporate"]},
    {"id": "GF-037", "name": "GoodFoods Marathahalli #6", "area": "Marathahalli", "city": "Bangalore", "capacity": 65,  "cuisine": ["South Indian"],    "avg_cost_per_person": 310, "has_outdoor_seating": False, "is_veg_only": True,  "tags": ["veg", "budget"]},

    {"id": "GF-038", "name": "GoodFoods Vijayanagar #4", "area": "Vijayanagar", "city": "Bangalore", "capacity": 120, "cuisine": ["North Indian"],        "avg_cost_per_person": 600, "has_outdoor_seating": True,  "is_veg_only": False, "tags": ["family"]},
    {"id": "GF-039", "name": "GoodFoods Vijayanagar #5", "area": "Vijayanagar", "city": "Bangalore", "capacity": 75,  "cuisine": ["South Indian"],        "avg_cost_per_person": 320, "has_outdoor_seating": False, "is_veg_only": True,  "tags": ["veg"]},

    {"id":"GF-040","name":"GoodFoods Electronic City #1","area":"Electronic City","city":"Bangalore","capacity":150,"cuisine":["North Indian","Chinese"],"avg_cost_per_person":550,"has_outdoor_seating":True,"is_veg_only":False,"tags":["corporate"]},
    {"id":"GF-041","name":"GoodFoods Electronic City #2","area":"Electronic City","city":"Bangalore","capacity":100,"cuisine":["Italian"],"avg_cost_per_person":850,"has_outdoor_seating":False,"is_veg_only":False,"tags":["date-night"]},
    {"id":"GF-042","name":"GoodFoods Electronic City #3","area":"Electronic City","city":"Bangalore","capacity":70,"cuisine":["South Indian"],"avg_cost_per_person":300,"has_outdoor_seating":False,"is_veg_only":True,"tags":["veg"]},

    {"id":"GF-043","name":"GoodFoods Airport Road #1","area":"Airport Road","city":"Bangalore","capacity":200,"cuisine":["Continental"],"avg_cost_per_person":1200,"has_outdoor_seating":True,"is_veg_only":False,"tags":["premium"]},
    {"id":"GF-044","name":"GoodFoods Airport Road #2","area":"Airport Road","city":"Bangalore","capacity":95,"cuisine":["North Indian"],"avg_cost_per_person":700,"has_outdoor_seating":False,"is_veg_only":False,"tags":["family"]},
    {"id":"GF-045","name":"GoodFoods Airport Road #3","area":"Airport Road","city":"Bangalore","capacity":80,"cuisine":["Chinese"],"avg_cost_per_person":600,"has_outdoor_seating":True,"is_veg_only":False,"tags":["groups"]},

    {"id":"GF-046","name":"GoodFoods Marathahalli #1","area":"Marathahalli","city":"Bangalore","capacity":140,"cuisine":["Italian"],"avg_cost_per_person":950,"has_outdoor_seating":True,"is_veg_only":False,"tags":["date-night"]},
    {"id":"GF-047","name":"GoodFoods Marathahalli #2","area":"Marathahalli","city":"Bangalore","capacity":70,"cuisine":["South Indian"],"avg_cost_per_person":300,"has_outdoor_seating":False,"is_veg_only":True,"tags":["veg"]},
    {"id":"GF-048","name":"GoodFoods Marathahalli #3","area":"Marathahalli","city":"Bangalore","capacity":160,"cuisine":["North Indian"],"avg_cost_per_person":750,"has_outdoor_seating":True,"is_veg_only":False,"tags":["groups"]},

    {"id":"GF-049","name":"GoodFoods Vijayanagar #1","area":"Vijayanagar","city":"Bangalore","capacity":100,"cuisine":["Italian"],"avg_cost_per_person":850,"has_outdoor_seating":True,"is_veg_only":False,"tags":["premium"]},
    {"id":"GF-050","name":"GoodFoods Vijayanagar #2","area":"Vijayanagar","city":"Bangalore","capacity":60,"cuisine":["North Indian"],"avg_cost_per_person":500,"has_outdoor_seating":False,"is_veg_only":False,"tags":["budget"]},
    {"id":"GF-051","name":"GoodFoods Vijayanagar #3","area":"Vijayanagar","city":"Bangalore","capacity":140,"cuisine":["South Indian"],"avg_cost_per_person":350,"has_outdoor_seating":False,"is_veg_only":True,"tags":["veg"]},

    {"id":"GF-052","name":"GoodFoods Malleshwaram #1","area":"Malleshwaram","city":"Bangalore","capacity":135,"cuisine":["North Indian"],"avg_cost_per_person":700,"has_outdoor_seating":True,"is_veg_only":False,"tags":["groups"]},
    {"id":"GF-053","name":"GoodFoods Malleshwaram #2","area":"Malleshwaram","city":"Bangalore","capacity":85,"cuisine":["Pan-Asian"],"avg_cost_per_person":650,"has_outdoor_seating":False,"is_veg_only":False,"tags":["date-night"]},
    {"id":"GF-054","name":"GoodFoods Malleshwaram #3","area":"Malleshwaram","city":"Bangalore","capacity":60,"cuisine":["South Indian"],"avg_cost_per_person":300,"has_outdoor_seating":False,"is_veg_only":True,"tags":["veg"]},

    {"id":"GF-055","name":"GoodFoods Ulsoor #1","area":"Ulsoor","city":"Bangalore","capacity":150,"cuisine":["Continental"],"avg_cost_per_person":950,"has_outdoor_seating":True,"is_veg_only":False,"tags":["premium"]},
    {"id":"GF-056","name":"GoodFoods Ulsoor #2","area":"Ulsoor","city":"Bangalore","capacity":70,"cuisine":["Mexican"],"avg_cost_per_person":700,"has_outdoor_seating":False,"is_veg_only":False,"tags":["groups"]},
    {"id":"GF-057","name":"GoodFoods Ulsoor #3","area":"Ulsoor","city":"Bangalore","capacity":120,"cuisine":["North Indian"],"avg_cost_per_person":600,"has_outdoor_seating":True,"is_veg_only":False,"tags":["family"]},

    {"id":"GF-058","name":"GoodFoods Richmond Town #1","area":"Richmond Town","city":"Bangalore","capacity":160,"cuisine":["Italian"],"avg_cost_per_person":1200,"has_outdoor_seating":True,"is_veg_only":False,"tags":["premium","date-night"]},
    {"id":"GF-059","name":"GoodFoods Richmond Town #2","area":"Richmond Town","city":"Bangalore","capacity":100,"cuisine":["South Indian"],"avg_cost_per_person":350,"has_outdoor_seating":False,"is_veg_only":True,"tags":["veg"]},
    {"id":"GF-060","name":"GoodFoods Richmond Town #3","area":"Richmond Town","city":"Bangalore","capacity":140,"cuisine":["Pan-Asian"],"avg_cost_per_person":800,"has_outdoor_seating":True,"is_veg_only":False,"tags":["corporate"]}
]

def search_restaurants(
    area: str | None = None,
    cuisine: str | None = None,
    min_capacity: int | None = None,
    max_cost: int | None = None
) -> List[Dict]:
    results = RESTAURANTS
    if area:
        results = [r for r in results if r["area"].lower() == area.lower()]
    if cuisine:
        results = [r for r in results if cuisine.lower() in
                   [c.lower() for c in r["cuisine"]]]
    if min_capacity:
        results = [r for r in results if r["capacity"] >= min_capacity]
    if max_cost:
        results = [r for r in results if r["avg_cost_per_person"] <= max_cost]
    return results[:20]  # limit results
