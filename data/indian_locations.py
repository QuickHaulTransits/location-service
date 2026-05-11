
STATES = [
    {"id": "karnataka", "name": "Karnataka"},
    {"id": "maharashtra", "name": "Maharashtra"},
    {"id": "delhi", "name": "Delhi"},
    {"id": "andhra_pradesh", "name": "Andhra Pradesh"},
    {"id": "tamil_nadu", "name": "Tamil Nadu"},
    {"id": "telangana", "name": "Telangana"},
    {"id": "west_bengal", "name": "West Bengal"},
]

DISTRICTS = {
    "karnataka": [
        {"id": "bangalore", "name": "Bangalore"},
        {"id": "mysore", "name": "Mysore"},
        {"id": "hubli", "name": "Hubli"},
        {"id": "mangalore", "name": "Mangalore"},
        {"id": "belgaum", "name": "Belgaum"},
        {"id": "gulbarga", "name": "Gulbarga"},
        {"id": "davanagere", "name": "Davanagere"},
        {"id": "shimoga", "name": "Shimoga"},
    ],
    "maharashtra": [
        {"id": "mumbai", "name": "Mumbai"},
        {"id": "pune", "name": "Pune"},
        {"id": "nagpur", "name": "Nagpur"},
        {"id": "nashik", "name": "Nashik"},
        {"id": "aurangabad", "name": "Aurangabad"},
        {"id": "solapur", "name": "Solapur"},
        {"id": "amravati", "name": "Amravati"},
        {"id": "kolhapur", "name": "Kolhapur"},
    ],
    "delhi": [
        {"id": "new_delhi", "name": "New Delhi"},
        {"id": "north_delhi", "name": "North Delhi"},
        {"id": "south_delhi", "name": "South Delhi"},
        {"id": "east_delhi", "name": "East Delhi"},
        {"id": "west_delhi", "name": "West Delhi"},
        {"id": "central_delhi", "name": "Central Delhi"},
        {"id": "north_west_delhi", "name": "North West Delhi"},
    ],
    "andhra_pradesh": [
        {"id": "visakhapatnam", "name": "Visakhapatnam"},
        {"id": "vijayawada", "name": "Vijayawada"},
        {"id": "guntur", "name": "Guntur"},
        {"id": "nellore", "name": "Nellore"},
        {"id": "kurnool", "name": "Kurnool"},
        {"id": "rajahmundry", "name": "Rajahmundry"},
        {"id": "tirupati", "name": "Tirupati"},
    ],
    "tamil_nadu": [
        {"id": "chennai", "name": "Chennai"},
        {"id": "coimbatore", "name": "Coimbatore"},
        {"id": "madurai", "name": "Madurai"},
        {"id": "trichy", "name": "Tiruchirappalli"},
        {"id": "salem", "name": "Salem"},
        {"id": "tirunelveli", "name": "Tirunelveli"},
        {"id": "erode", "name": "Erode"},
    ],
    "telangana": [
        {"id": "hyderabad", "name": "Hyderabad"},
        {"id": "warangal", "name": "Warangal"},
        {"id": "nizamabad", "name": "Nizamabad"},
        {"id": "karimnagar", "name": "Karimnagar"},
        {"id": "ramagundam", "name": "Ramagundam"},
        {"id": "khammam", "name": "Khammam"},
        {"id": "mahbubnagar", "name": "Mahbubnagar"},
    ],
    "west_bengal": [
        {"id": "kolkata", "name": "Kolkata"},
        {"id": "howrah", "name": "Howrah"},
        {"id": "durgapur", "name": "Durgapur"},
        {"id": "asansol", "name": "Asansol"},
        {"id": "siliguri", "name": "Siliguri"},
        {"id": "bardhaman", "name": "Bardhaman"},
        {"id": "malda", "name": "Malda"},
    ],
}

CENTERS = {
    "karnataka": {
        "bangalore": [
            {"id": "blr_majestic", "name": "Majestic Central Hub", "address": "Tank Bund Road, Majestic, Bangalore", "phone": "080-22223333"},
            {"id": "blr_whitefield", "name": "Whitefield Logistics Center", "address": "ITPL Main Road, Whitefield", "phone": "080-44445555"},
        ],
        "mysore": [
            {"id": "mys_suburb", "name": "Mysore Suburb Hub", "address": "Lashkar Mohalla, Mysore", "phone": "0821-2525252"},
        ],
        "hubli": [
            {"id": "hubli_main", "name": "Hubli Junction Hub", "address": "Station Road, Hubli", "phone": "0836-2350001"},
        ],
        "mangalore": [
            {"id": "mng_port", "name": "Mangalore Port Hub", "address": "Panambur, Mangalore", "phone": "0824-2407222"},
        ],
    },
    "maharashtra": {
        "mumbai": [
            {"id": "mum_andheri", "name": "Andheri Cargo Hub", "address": "Andheri East, Mumbai", "phone": "022-28282828"},
            {"id": "mum_vashi", "name": "Vashi Distribution Center", "address": "Sector 17, Vashi, Navi Mumbai", "phone": "022-27272727"},
        ],
        "pune": [
            {"id": "pune_hinjewadi", "name": "Hinjewadi Tech Hub", "address": "Phase 1, Hinjewadi, Pune", "phone": "020-66667777"},
        ],
    },
    "delhi": {
        "new_delhi": [
            {"id": "del_connaught", "name": "CP Distribution Point", "address": "Connaught Place, New Delhi", "phone": "011-23232323"},
        ],
    },
    "andhra_pradesh": {
        "visakhapatnam": [
            {"id": "viz_port", "name": "Vizag Port Logistics", "address": "Port Area, Visakhapatnam", "phone": "0891-2525252"},
        ],
    },
    "tamil_nadu": {
        "chennai": [
            {"id": "chn_guindy", "name": "Guindy Industrial Hub", "address": "Guindy, Chennai", "phone": "044-22224444"},
        ],
    },
    "telangana": {
        "hyderabad": [
            {"id": "hyd_hitech", "name": "HITEC City Hub", "address": "Madhapur, Hyderabad", "phone": "040-23110000"},
        ],
    },
    "west_bengal": {
        "kolkata": [
            {"id": "kol_saltlake", "name": "Salt Lake Sector V Hub", "address": "Salt Lake, Kolkata", "phone": "033-23570000"},
        ],
    },
}

# Add generic hubs for any district that doesn't have one explicitly defined
for state_id, state_districts in DISTRICTS.items():
    if state_id not in CENTERS:
        CENTERS[state_id] = {}
    
    for district in state_districts:
        district_id = district["id"]
        if district_id not in CENTERS[state_id]:
            CENTERS[state_id][district_id] = [
                {
                    "id": f"{district_id}_hub",
                    "name": f"{district['name']} Regional Hub",
                    "address": f"Main Market Area, {district['name']}",
                    "phone": f"0{len(district_id)}-55554444"
                }
            ]

def get_all_states():
    return STATES

def get_districts_by_state(state_id):
    return DISTRICTS.get(state_id, [])

def get_centers_by_district(state_id, district_id):
    state_centers = CENTERS.get(state_id, {})
    return state_centers.get(district_id, [])

def get_center_by_id(center_id):
    """Find a center by its ID across all states and districts"""
    for state_id in CENTERS:
        for district_id in CENTERS[state_id]:
            for center in CENTERS[state_id][district_id]:
                if center["id"] == center_id:
                    return center
    return None
