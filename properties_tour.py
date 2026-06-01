"""
Property tour data — narrative scripts + media + maps for every Bellshire listing.

Two modes per property:
  - PITCH ("hook"): a single inspiring paragraph + 3-4 hero shots, ~45-60 sec.
  - TOUR  ("guided"): 8 scenes, each with text + matching media + optional map action,
                       ~3-5 min total. Scenes flow: hook → architecture → interior →
                       signature rooms → outdoor → neighborhood (map) → schools →
                       parks/lifestyle (map).

Each scene is a dict:
  {
    "id": "hook" | "architecture" | ...,
    "title": short label shown in UI ("Architecture & Style"),
    "text":  what Alexandra says (1-3 sentences),
    "media": { "type": "image" | "video", "url": "...", "caption": "..." },
    "map":   {                                         # optional
      "center": [lat, lng], "zoom": 14,
      "markers": [ { "lat": ..., "lng": ..., "label": "...", "kind": "home|school|park" } ],
    },
  }

The /property/{id}/tour endpoint serves these directly; the frontend reads them and
drives the chat bubble / voice transcript / map / media display in lockstep.
"""

# Photo URLs map to existing bellshireinc.com WordPress assets we already pull in
# project galleries — no new uploads required.

PROPERTIES = {
    # ──────────────────────────────────────────────────────────────────────────
    "10425": {
        "address": "10425 SE 20th St, Bellevue WA 98004",
        "neighborhood": "Enatai",
        "city": "Bellevue",
        "coords": [47.5828, -122.1990],
        "specs": {
            "status": "Presale",
            "price": "Presale",
            "beds": 5, "baths": 5, "sqft": 4517,
            "lot": "0.21 acre", "yearBuilt": 2026, "style": "Contemporary Northwest",
        },
        "schools": [
            {"name": "Enatai Elementary",      "rating": 8,  "distance": "0.4 mi", "grades": "K-5",  "kind": "public"},
            {"name": "Chinook Middle School",  "rating": 8,  "distance": "1.2 mi", "grades": "6-8",  "kind": "public"},
            {"name": "Bellevue High School",   "rating": 10, "distance": "1.8 mi", "grades": "9-12", "kind": "public"},
        ],
        "parks": [
            {"name": "Enatai Beach Park",        "distance": "0.5 mi", "features": "Lake Washington access, kayak launch, swimming dock"},
            {"name": "Mercer Slough Nature Park","distance": "1.0 mi", "features": "320 acres of wetland, boardwalk trails, blueberry farm"},
            {"name": "Chism Beach Park",          "distance": "1.6 mi", "features": "lakefront beach, picnic areas"},
        ],
        "pitch": (
            "Welcome to 10425 SE 20th Street — a presale opportunity in Enatai, one of Bellevue's most coveted "
            "lakeside neighborhoods. Imagine a 4,517 square-foot contemporary residence designed around natural "
            "light, with five bedrooms, five baths, and architectural details you typically only find in custom "
            "Pacific Northwest estates. Lake Washington is a five-minute walk; Bellevue's top-ranked schools sit "
            "just down the block. This is the rare chance to own a brand-new home in a neighborhood where almost "
            "nothing comes to market."
        ),
        "scenes": [
            {
                "id": "hook", "title": "An Enatai Presale",
                "text": "Welcome to 10425 SE 20th Street — a brand-new 4,517 square-foot residence rising in Enatai, "
                        "one of the few Bellevue neighborhoods that still feels like a hidden lakeside village.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/03/10425_ENATAI-RESIDENCE_01-1.jpg",
                          "caption": "Sunset render — 10425 SE 20th Street"},
            },
            {
                "id": "architecture", "title": "Contemporary Northwest",
                "text": "The architecture blends warm cedar, blackened steel, and floor-to-ceiling glass — "
                        "a contemporary Pacific Northwest language that lets the surrounding trees do half the design work.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/03/10425_ENATAI-RESIDENCE_01-2.jpg",
                          "caption": "Facade — natural materials, modern silhouette"},
            },
            {
                "id": "interior", "title": "Open Living, Quiet Flow",
                "text": "Inside, the main floor opens around a double-height great room. A chef's kitchen with "
                        "butler's pantry connects to a covered outdoor lounge — the house is designed for entertaining "
                        "and for the seven months of soft Pacific light.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/03/10425_ENATAI-RESIDENCE_01-3.jpg",
                          "caption": "Open great room concept"},
            },
            {
                "id": "rooms", "title": "Five Bedrooms, Five Baths",
                "text": "Five bedrooms and five full baths — including a primary suite on the main floor and "
                        "a private guest wing upstairs. Every bath is finished with European fixtures and natural stone.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/03/10425_ENATAI-RESIDENCE_01-4.jpg",
                          "caption": "Primary suite concept"},
            },
            {
                "id": "outdoor", "title": "The Lot & Outdoor Living",
                "text": "The 0.21 acre lot is fully landscaped: a flat backyard, mature evergreens for privacy, "
                        "and a covered loggia with a built-in fireplace that extends the living season into October.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/03/10425_ENATAI-RESIDENCE_01-5.jpg",
                          "caption": "Outdoor lounge & landscape"},
            },
            {
                "id": "neighborhood", "title": "Enatai — Bellevue's Lake Village",
                "text": "Enatai is the quiet pocket between Mercer Slough and Lake Washington. Most properties "
                        "stay in families for decades — this is the rare new build in a neighborhood almost no one leaves.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/03/10425_ENATAI-RESIDENCE_01-6.jpg",
                          "caption": "Aerial view of Enatai"},
                "map": {"center": [47.5828, -122.1990], "zoom": 15,
                        "markers": [{"lat": 47.5828, "lng": -122.1990, "label": "10425 SE 20th St", "kind": "home"}]},
            },
            {
                "id": "schools", "title": "Top-rated Bellevue Schools",
                "text": "Enatai Elementary — an 8 out of 10 on GreatSchools — sits four blocks away. "
                        "Chinook Middle rates an 8, and Bellevue High earns a perfect 10 out of 10, ranking among Washington's very best.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/03/10425_ENATAI-RESIDENCE_01-7.jpg",
                          "caption": "Walking distance to top schools"},
                "map": {"center": [47.5840, -122.1980], "zoom": 14,
                        "markers": [
                            {"lat": 47.5828, "lng": -122.1990, "label": "10425 SE 20th St",     "kind": "home"},
                            {"lat": 47.5862, "lng": -122.2002, "label": "Enatai Elementary (8/10)",  "kind": "school"},
                            {"lat": 47.5751, "lng": -122.1859, "label": "Chinook Middle (8/10)",     "kind": "school"},
                            {"lat": 47.5908, "lng": -122.1923, "label": "Bellevue High (10/10)",     "kind": "school"},
                        ]},
            },
            {
                "id": "lifestyle", "title": "Parks, Water & Lifestyle",
                "text": "Enatai Beach Park is a half-mile away — kayak launch, swim dock, and one of the only "
                        "sandy beaches on the east side of Lake Washington. Mercer Slough's 320-acre nature park is "
                        "your weekend trail network. Downtown Bellevue is a five-minute drive.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/03/10425_ENATAI-RESIDENCE_01-1.jpg",
                          "caption": "Lake Washington at your doorstep"},
                "map": {"center": [47.5830, -122.1900], "zoom": 13,
                        "markers": [
                            {"lat": 47.5828, "lng": -122.1990, "label": "10425 SE 20th St",        "kind": "home"},
                            {"lat": 47.5871, "lng": -122.1957, "label": "Enatai Beach Park",         "kind": "park"},
                            {"lat": 47.5856, "lng": -122.1820, "label": "Mercer Slough Nature Park", "kind": "park"},
                            {"lat": 47.5778, "lng": -122.2078, "label": "Chism Beach Park",          "kind": "park"},
                        ]},
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "312": {
        "address": "312 160th Ave NE, Bellevue WA 98008",
        "neighborhood": "Crossroads / Bel-Red",
        "city": "Bellevue",
        "coords": [47.6285, -122.1356],
        "specs": {
            "status": "For Sale",
            "price": "$3,500,000",
            "beds": 5, "baths": 4.25, "sqft": 4400,
            "lot": "0.20 acre", "yearBuilt": 2024, "style": "Contemporary Modern",
        },
        "schools": [
            {"name": "Sherwood Forest Elementary", "rating": 5,  "distance": "0.5 mi", "grades": "K-5",  "kind": "public"},
            {"name": "Highland Middle School",      "rating": 4, "distance": "0.9 mi", "grades": "6-8",  "kind": "public"},
            {"name": "Interlake High School",       "rating": 10, "distance": "1.4 mi", "grades": "9-12", "kind": "public"},
        ],
        "parks": [
            {"name": "Crossroads Park",        "distance": "0.4 mi", "features": "tennis, water park, summer concerts"},
            {"name": "Wilburton Hill Park",     "distance": "1.6 mi", "features": "Bellevue Botanical Garden, trails"},
            {"name": "Robinswood Park",         "distance": "1.0 mi", "features": "dog park, off-leash trails, equestrian"},
        ],
        "pitch": (
            "312 160th Avenue NE is contemporary luxury at its most refined — a 4,400 square-foot residence on a "
            "quiet Bellevue lot with five bedrooms, a chef's kitchen, and a backyard built for outdoor entertaining. "
            "The home sits in the Sherwood Forest pocket of Crossroads — walking distance to top-ranked schools, "
            "Crossroads Park, and ten minutes from downtown Bellevue and Microsoft's Redmond campus."
        ),
        "scenes": [
            {
                "id": "hook", "title": "Sophistication in Every Detail",
                "text": "312 160th Avenue NE — a brand-new contemporary residence where four thousand four hundred "
                        "square feet of refined design meet one of Bellevue's most family-loved neighborhoods.",
                "media": {"type": "video",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/02/6524_Cinematoc_4K_Branded_New_Music_v3-3.mp4",
                          "caption": "Cinematic property tour"},
            },
            {
                "id": "architecture", "title": "Contemporary Modern",
                "text": "Clean horizontal lines, blackened metal accents, and warm wood paneling — a contemporary "
                        "language that feels both modern and timeless. Built in 2024 to the highest current energy code.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2025/07/1-web-or-mls-312-160th-ave-ne.jpg",
                          "caption": "Front elevation"},
            },
            {
                "id": "interior", "title": "Sun-Filled Open Plan",
                "text": "Inside, an open kitchen-living-dining flows through walls of glass to the outdoor terrace. "
                        "Wide-plank European oak, vaulted ceilings, and a 16-foot stone fireplace anchor the great room.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2025/07/8-web-or-mls-312-160th-ave-ne.jpg",
                          "caption": "Great room with stone fireplace"},
            },
            {
                "id": "rooms", "title": "Signature Spaces",
                "text": "A chef's kitchen with Wolf and Sub-Zero appliances, a primary suite with private deck and "
                        "spa bath, plus four additional bedrooms. The lower level features a media room and dedicated "
                        "home office.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2025/07/12-web-or-mls-312-160th-ave-ne.jpg",
                          "caption": "Chef's kitchen"},
            },
            {
                "id": "outdoor", "title": "Backyard & Lot",
                "text": "The fully landscaped 0.2 acre lot includes a covered outdoor kitchen, gas fire feature, "
                        "and a flat lawn perfect for kids or a future pool. Mature trees provide complete privacy.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2025/07/22-web-or-mls-312-160th-ave-ne.jpg",
                          "caption": "Outdoor entertaining"},
            },
            {
                "id": "neighborhood", "title": "Crossroads — Family Bellevue",
                "text": "This pocket of Crossroads is Bellevue's family heartland — mature streets, large lots, and "
                        "walking access to parks. Ten minutes to downtown Bellevue, twelve minutes to Microsoft, "
                        "and a fifteen-minute drive across 520 to Seattle.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2025/07/2-web-or-mls-312-160th-ave-ne.jpg",
                          "caption": "Aerial — Crossroads neighborhood"},
                "map": {"center": [47.6285, -122.1356], "zoom": 14,
                        "markers": [{"lat": 47.6285, "lng": -122.1356, "label": "312 160th Ave NE", "kind": "home"}]},
            },
            {
                "id": "schools", "title": "Bellevue School District",
                "text": "The headline here is Interlake High — a perfect 10 out of 10 on GreatSchools and home to a "
                        "renowned International Baccalaureate program, placing it in Washington's top five percent. "
                        "Sherwood Forest Elementary and Highland Middle are both within a mile, rated 5 and 4 today, "
                        "all inside the Bellevue School District — consistently the top public district in the state.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2025/07/3-web-or-mls-312-160th-ave-ne.jpg",
                          "caption": "Top-ranked schools nearby"},
                "map": {"center": [47.6280, -122.1380], "zoom": 14,
                        "markers": [
                            {"lat": 47.6285, "lng": -122.1356, "label": "312 160th Ave NE",        "kind": "home"},
                            {"lat": 47.6336, "lng": -122.1349, "label": "Sherwood Forest Elem (5/10)", "kind": "school"},
                            {"lat": 47.6203, "lng": -122.1303, "label": "Highland Middle (4/10)",      "kind": "school"},
                            {"lat": 47.6233, "lng": -122.1599, "label": "Interlake High (10/10)",      "kind": "school"},
                        ]},
            },
            {
                "id": "lifestyle", "title": "Parks & Lifestyle",
                "text": "Crossroads Park is four blocks away — tennis courts, splash pads, and summer concert series. "
                        "Robinswood Park has off-leash trails, and Wilburton Hill is home to the Bellevue Botanical "
                        "Garden. Crossroads Mall and Whole Foods are five minutes by car.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2025/07/5-web-or-mls-312-160th-ave-ne.jpg",
                          "caption": "Family Bellevue living"},
                "map": {"center": [47.6285, -122.1400], "zoom": 13,
                        "markers": [
                            {"lat": 47.6285, "lng": -122.1356, "label": "312 160th Ave NE",   "kind": "home"},
                            {"lat": 47.6309, "lng": -122.1322, "label": "Crossroads Park",     "kind": "park"},
                            {"lat": 47.6256, "lng": -122.1450, "label": "Robinswood Park",     "kind": "park"},
                            {"lat": 47.6173, "lng": -122.1530, "label": "Wilburton Hill Park", "kind": "park"},
                        ]},
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "218": {
        "address": "218 109th Avenue SE, Bellevue WA 98004",
        "neighborhood": "Downtown Bellevue / Surrey Downs",
        "city": "Bellevue",
        "coords": [47.6079, -122.1923],
        "specs": {
            "status": "Pending",
            "price": "$4,500,000",
            "beds": 5, "baths": 4.25, "sqft": 4400,
            "lot": "0.18 acre", "yearBuilt": 2025, "style": "Urban Contemporary",
        },
        "schools": [
            {"name": "Enatai Elementary",     "rating": 8,  "distance": "0.8 mi", "grades": "K-5",  "kind": "public"},
            {"name": "Chinook Middle School", "rating": 8,  "distance": "1.0 mi", "grades": "6-8",  "kind": "public"},
            {"name": "Bellevue High School",  "rating": 10, "distance": "0.7 mi", "grades": "9-12", "kind": "public"},
        ],
        "parks": [
            {"name": "Surrey Downs Park",   "distance": "0.3 mi", "features": "playground, basketball, picnic"},
            {"name": "Downtown Park",        "distance": "0.9 mi", "features": "Bellevue's signature park — pond, canopy walkway"},
            {"name": "Meydenbauer Bay Park", "distance": "1.2 mi", "features": "lakefront beach, marina, swim area"},
        ],
        "pitch": (
            "218 109th Avenue SE is urban contemporary luxury, three blocks from Bellevue Square and a six-minute walk "
            "to Bellevue High. Five bedrooms, 4.25 baths, 4,400 square feet of polished design — and you can walk to "
            "the best restaurants, parks, and schools on the Eastside. This is what 'walk-to-everything Bellevue' looks like."
        ),
        "scenes": [
            {"id": "hook", "title": "Walk-to-Everything Bellevue",
             "text": "218 109th Avenue SE — a brand-new urban residence three blocks from Bellevue Square, a short walk to "
                     "the city's best parks, and inside the catchment for Bellevue's top schools.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/002_2-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Front view"}},
            {"id": "architecture", "title": "Urban Contemporary",
             "text": "Crisp horizontal lines, dark brick accents, and a steel-and-glass front door — the architecture "
                     "feels at home in downtown Bellevue's evolving skyline.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/003_3-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Modern facade"}},
            {"id": "interior", "title": "Light-Filled Open Plan",
             "text": "Inside: 22-foot vaulted ceilings, a glass-walled great room, and a chef's kitchen with hidden "
                     "appliance pantry — designed for both gallery-quiet weekday mornings and Saturday-night dinner parties.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/004_4-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Great room"}},
            {"id": "rooms", "title": "Signature Rooms",
             "text": "Five bedrooms, including a main-floor primary suite with private patio and a glass-walled walk-in "
                     "closet. The upper level features a media room and three en-suite bedrooms.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/005_5-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Primary suite"}},
            {"id": "outdoor", "title": "Outdoor Living",
             "text": "The fully fenced backyard includes a covered outdoor kitchen, gas fire feature, and a low-maintenance "
                     "turf lawn. Mature trees on every property line keep the lot private despite the urban location.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/006_6-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Backyard"}},
            {"id": "neighborhood", "title": "Surrey Downs — In the Heart of Bellevue",
             "text": "Surrey Downs is the rare quiet residential pocket inside Bellevue's urban core. Bellevue Square, "
                     "the new Light Rail station, and three of the city's top restaurants are all within a six-minute walk.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/007_7-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Surrey Downs neighborhood"},
             "map": {"center": [47.6079, -122.1923], "zoom": 15,
                     "markers": [{"lat": 47.6079, "lng": -122.1923, "label": "218 109th Ave SE", "kind": "home"}]}},
            {"id": "schools", "title": "Bellevue's Top Schools",
             "text": "Bellevue High School — a perfect 10 out of 10 on GreatSchools — is a seven-minute walk. Enatai "
                     "Elementary and Chinook Middle, both rated 8 out of 10, are within a mile. All three sit in the "
                     "Bellevue School District, the top-ranked public district in Washington.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/008_8-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Walking distance to top schools"},
             "map": {"center": [47.6060, -122.1930], "zoom": 14,
                     "markers": [
                         {"lat": 47.6079, "lng": -122.1923, "label": "218 109th Ave SE",       "kind": "home"},
                         {"lat": 47.5862, "lng": -122.2002, "label": "Enatai Elementary (8/10)",  "kind": "school"},
                         {"lat": 47.5751, "lng": -122.1859, "label": "Chinook Middle (8/10)",     "kind": "school"},
                         {"lat": 47.5908, "lng": -122.1923, "label": "Bellevue High (10/10)",     "kind": "school"},
                     ]}},
            {"id": "lifestyle", "title": "Parks, Lake & Lifestyle",
             "text": "Downtown Park's canopy walkway is a nine-minute walk; Meydenbauer Bay Park gives you a beach and "
                     "marina on Lake Washington. The Spring District and Wilburton Light Rail stations are minutes away — "
                     "Seattle is a 12-minute train ride.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/009_9-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Urban Bellevue lifestyle"},
             "map": {"center": [47.6070, -122.1920], "zoom": 14,
                     "markers": [
                         {"lat": 47.6079, "lng": -122.1923, "label": "218 109th Ave SE",      "kind": "home"},
                         {"lat": 47.6093, "lng": -122.1894, "label": "Surrey Downs Park",      "kind": "park"},
                         {"lat": 47.6133, "lng": -122.1974, "label": "Downtown Park",          "kind": "park"},
                         {"lat": 47.6188, "lng": -122.2020, "label": "Meydenbauer Bay Park",   "kind": "park"},
                     ]}},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "1224": {
        "address": "1224 108th Ave SE, Bellevue WA 98004",
        "neighborhood": "Enatai / Surrey Downs",
        "city": "Bellevue",
        "coords": [47.5961, -122.1936],
        "specs": {
            "status": "Sold",
            "price": "$6,450,000",
            "beds": 6, "baths": 7.5, "sqft": 6713,
            "lot": "0.28 acre", "yearBuilt": 2024, "style": "Modern Estate",
        },
        "schools": [
            {"name": "Enatai Elementary",     "rating": 8,  "distance": "0.4 mi", "grades": "K-5",  "kind": "public"},
            {"name": "Chinook Middle School", "rating": 8,  "distance": "0.7 mi", "grades": "6-8",  "kind": "public"},
            {"name": "Bellevue High School",  "rating": 10, "distance": "0.5 mi", "grades": "9-12", "kind": "public"},
        ],
        "parks": [
            {"name": "Bellefields Nature Park",  "distance": "0.6 mi", "features": "wetland trails, wildlife viewing"},
            {"name": "Mercer Slough Nature Park","distance": "0.8 mi", "features": "320-acre nature reserve, canoe tours"},
            {"name": "Meydenbauer Bay Park",      "distance": "1.1 mi", "features": "lakefront beach, marina"},
        ],
        "pitch": (
            "1224 108th Avenue SE is a 6,713 square-foot modern estate — six bedrooms, seven and a half baths, every "
            "luxury detail you can name. Set on a quarter-acre in Enatai, half a mile from Bellevue High, and a "
            "stone's throw from Lake Washington. This is the kind of trophy property that defines a generation of "
            "Bellevue luxury."
        ),
        "scenes": [
            {"id": "hook", "title": "A Modern Bellevue Estate",
             "text": "1224 108th Avenue SE — a 6,713 square-foot modern estate, six bedrooms, seven and a half baths, "
                     "every detail considered. This is what the top of the Bellevue market looks like in 2024.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/1-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Estate entrance"}},
            {"id": "architecture", "title": "Modern Estate Architecture",
             "text": "Soaring rooflines, blackened steel, and warm wood — the architecture feels at once contemporary "
                     "and rooted in the Pacific Northwest. Every angle was designed for a piece of art.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/3-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Architectural facade"}},
            {"id": "interior", "title": "Cathedral-Scale Living",
             "text": "Twenty-eight-foot ceilings in the great room, walls of glass overlooking the courtyard, and a "
                     "chef's kitchen with butler's pantry, hidden scullery, and a 13-foot island.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/5-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Great room"}},
            {"id": "rooms", "title": "Signature Rooms",
             "text": "Six bedrooms, all en-suite. A primary suite that occupies the entire west wing with private "
                     "spa, sauna, and walk-in closets. A media room, wine cellar, and a dedicated home office.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/8-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Primary suite"}},
            {"id": "outdoor", "title": "Resort-Scale Outdoor",
             "text": "The 0.28-acre lot includes a heated pool, outdoor kitchen, fire pit terrace, and a guest casita — "
                     "every element designed to make this house the place where everyone wants to gather.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/12-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Pool and outdoor kitchen"}},
            {"id": "neighborhood", "title": "Enatai — Old Money Bellevue",
             "text": "Enatai is the quiet old-money pocket between Surrey Downs and Lake Washington. Mature trees, "
                     "wide lots, and the rare neighborhood where new construction is genuinely welcomed.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/2-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Enatai aerial"},
             "map": {"center": [47.5961, -122.1936], "zoom": 14,
                     "markers": [{"lat": 47.5961, "lng": -122.1936, "label": "1224 108th Ave SE", "kind": "home"}]}},
            {"id": "schools", "title": "Walk to Bellevue High",
             "text": "Bellevue High School — a perfect 10 out of 10 on GreatSchools — is a five-minute walk. Enatai "
                     "Elementary and Chinook Middle, both rated 8 out of 10, round out a school assignment that's among "
                     "the most coveted on the Eastside.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/4-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Top schools all within a mile"},
             "map": {"center": [47.5945, -122.1950], "zoom": 14,
                     "markers": [
                         {"lat": 47.5961, "lng": -122.1936, "label": "1224 108th Ave SE",       "kind": "home"},
                         {"lat": 47.5862, "lng": -122.2002, "label": "Enatai Elementary (8/10)",  "kind": "school"},
                         {"lat": 47.5751, "lng": -122.1859, "label": "Chinook Middle (8/10)",     "kind": "school"},
                         {"lat": 47.5908, "lng": -122.1923, "label": "Bellevue High (10/10)",     "kind": "school"},
                     ]}},
            {"id": "lifestyle", "title": "Lake, Parks, City",
             "text": "Mercer Slough is at your back door — 320 acres of wetlands and canoe trails. Meydenbauer Bay Park "
                     "and the lake beach are a mile away. Downtown Bellevue is six minutes by car; Microsoft is twelve.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/7-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Lakeside lifestyle"},
             "map": {"center": [47.5955, -122.1900], "zoom": 13,
                     "markers": [
                         {"lat": 47.5961, "lng": -122.1936, "label": "1224 108th Ave SE",        "kind": "home"},
                         {"lat": 47.5990, "lng": -122.1875, "label": "Bellefields Nature Park",   "kind": "park"},
                         {"lat": 47.5856, "lng": -122.1820, "label": "Mercer Slough Nature Park", "kind": "park"},
                         {"lat": 47.6188, "lng": -122.2020, "label": "Meydenbauer Bay Park",      "kind": "park"},
                     ]}},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "1071": {
        "address": "1071 102nd Place SE, Bellevue WA 98004",
        "neighborhood": "Enatai",
        "city": "Bellevue",
        "coords": [47.5915, -122.2056],
        "specs": {
            "status": "Sold",
            "price": "$4,200,000",
            "beds": 5, "baths": 5, "sqft": 5920,
            "lot": "0.25 acre", "yearBuilt": 2023, "style": "Transitional Modern",
        },
        "schools": [
            {"name": "Enatai Elementary",     "rating": 8,  "distance": "0.3 mi", "grades": "K-5",  "kind": "public"},
            {"name": "Chinook Middle School", "rating": 8,  "distance": "1.0 mi", "grades": "6-8",  "kind": "public"},
            {"name": "Bellevue High School",  "rating": 10, "distance": "1.0 mi", "grades": "9-12", "kind": "public"},
        ],
        "parks": [
            {"name": "Enatai Beach Park",         "distance": "0.4 mi", "features": "swim dock, kayak launch, picnic shelters"},
            {"name": "Chism Beach Park",           "distance": "1.2 mi", "features": "lakefront beach"},
            {"name": "Mercer Slough Nature Park",  "distance": "1.1 mi", "features": "wetlands, canoe tours"},
        ],
        "pitch": (
            "1071 102nd Place SE is 5,920 square feet of transitional modern luxury on a quarter-acre Enatai lot. "
            "Five bedrooms, five baths, walls of glass framing the trees, and three minutes to Enatai Beach. "
            "A great example of what custom Bellevue luxury looks like."
        ),
        "scenes": [
            {"id": "hook", "title": "Transitional Modern in Enatai",
             "text": "1071 102nd Place SE — 5,920 square feet of transitional modern design on a quarter-acre lot in Enatai, "
                     "the rare Bellevue neighborhood that still feels like a lakeside village.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_4.jpg",
                       "caption": "Cinematic property tour"}},
            {"id": "architecture", "title": "Transitional Modern",
             "text": "The architecture bridges classic Northwest craft with modern detailing — wide eaves, board-and-batten "
                     "siding, and a black-trimmed window grid that reads timeless rather than trendy.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_4.jpg",
                       "caption": "Front elevation"}},
            {"id": "interior", "title": "Curated Interior",
             "text": "Soaring ceilings, white oak floors, and a chef's kitchen with calacatta marble waterfall island. "
                     "The dining room opens through accordion doors to a covered outdoor lounge.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_7.jpg",
                       "caption": "Open plan interior"}},
            {"id": "rooms", "title": "Five Suites",
             "text": "Five bedrooms, five full baths. Primary suite on the main floor with private deck. Upstairs: "
                     "four bedrooms, a bonus room, and a dedicated study with built-ins.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_11-scaled.jpg",
                       "caption": "Primary suite"}},
            {"id": "outdoor", "title": "Outdoor Living",
             "text": "Covered loggia with stone fireplace, outdoor kitchen, and a flat fenced backyard. Mature evergreens "
                     "line the property — total privacy in an otherwise tight lot pattern.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_16.jpg",
                       "caption": "Outdoor lounge"}},
            {"id": "neighborhood", "title": "Enatai — Bellevue's Hidden Pocket",
             "text": "Enatai is the lakeside enclave between Surrey Downs and Mercer Slough. Most homes here are decades "
                     "old and tightly held — new construction at this scale is rare.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_22.jpg",
                       "caption": "Enatai from above"},
             "map": {"center": [47.5915, -122.2056], "zoom": 15,
                     "markers": [{"lat": 47.5915, "lng": -122.2056, "label": "1071 102nd Pl SE", "kind": "home"}]}},
            {"id": "schools", "title": "Top-Ranked Bellevue Schools",
             "text": "Enatai Elementary — an 8 out of 10 — is three blocks away. Chinook Middle also rates an 8, and "
                     "Bellevue High earns a perfect 10, both within a mile. Walkable schools, top-tier ratings — the "
                     "Eastside's golden combination.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_23.jpg",
                       "caption": "Walk to top schools"},
             "map": {"center": [47.5910, -122.2000], "zoom": 14,
                     "markers": [
                         {"lat": 47.5915, "lng": -122.2056, "label": "1071 102nd Pl SE",        "kind": "home"},
                         {"lat": 47.5862, "lng": -122.2002, "label": "Enatai Elementary (8/10)",  "kind": "school"},
                         {"lat": 47.5751, "lng": -122.1859, "label": "Chinook Middle (8/10)",     "kind": "school"},
                         {"lat": 47.5908, "lng": -122.1923, "label": "Bellevue High (10/10)",     "kind": "school"},
                     ]}},
            {"id": "lifestyle", "title": "Lake, Parks, City",
             "text": "Enatai Beach Park is four blocks away — swim dock, kayak launch, and one of the only sandy beaches "
                     "on the east shore of Lake Washington. Downtown Bellevue is a five-minute drive.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_12.jpg",
                       "caption": "Lake Washington nearby"},
             "map": {"center": [47.5910, -122.2000], "zoom": 13,
                     "markers": [
                         {"lat": 47.5915, "lng": -122.2056, "label": "1071 102nd Pl SE",          "kind": "home"},
                         {"lat": 47.5871, "lng": -122.1957, "label": "Enatai Beach Park",          "kind": "park"},
                         {"lat": 47.5778, "lng": -122.2078, "label": "Chism Beach Park",           "kind": "park"},
                         {"lat": 47.5856, "lng": -122.1820, "label": "Mercer Slough Nature Park",  "kind": "park"},
                     ]}},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "1305": {
        "address": "1305 North 50th Street, Seattle WA 98103",
        "neighborhood": "Wallingford",
        "city": "Seattle",
        "coords": [47.6648, -122.3429],
        "specs": {
            "status": "Sold",
            "price": "$2,400,000",
            "beds": 4, "baths": 3.5, "sqft": 3120,
            "lot": "0.10 acre", "yearBuilt": 2023, "style": "Modern Craftsman",
        },
        "schools": [
            {"name": "B.F. Day Elementary",       "rating": 9, "distance": "0.5 mi", "grades": "K-5",  "kind": "public"},
            {"name": "Hamilton International MS", "rating": 8, "distance": "0.4 mi", "grades": "6-8",  "kind": "public"},
            {"name": "Lincoln High School",        "rating": 10, "distance": "1.0 mi", "grades": "9-12", "kind": "public"},
        ],
        "parks": [
            {"name": "Wallingford Playfield",  "distance": "0.5 mi", "features": "playground, tennis, off-leash hours"},
            {"name": "Gas Works Park",          "distance": "0.9 mi", "features": "lakefront, kite hill, Sunday market"},
            {"name": "Green Lake Park",         "distance": "1.2 mi", "features": "3-mile loop, swimming, paddleboarding"},
        ],
        "pitch": (
            "1305 North 50th Street is modern craftsman luxury in the heart of Wallingford — Seattle's most walkable, "
            "most loved family neighborhood. 3,120 square feet, four bedrooms, and you can walk to Gas Works Park, "
            "Green Lake, and the Sunday farmer's market. A perfect example of what new Seattle construction can be "
            "when it respects the neighborhood that surrounds it."
        ),
        "scenes": [
            {"id": "hook", "title": "Modern Wallingford",
             "text": "1305 North 50th Street — a brand-new modern craftsman in Wallingford, one of Seattle's most "
                     "walkable family neighborhoods.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_3-2.jpg",
                       "caption": "Front view"}},
            {"id": "architecture", "title": "Modern Craftsman",
             "text": "A respectful update to Wallingford's craftsman roots — gabled rooflines, cedar accents, and a "
                     "covered front porch, paired with modern fenestration and energy systems.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_4-2.jpg",
                       "caption": "Architectural facade"}},
            {"id": "interior", "title": "Open Plan Interior",
             "text": "Open kitchen-living-dining, white oak floors, and a sun-filled rear extension with sliding glass "
                     "doors to the deck. Designed for the way Seattle families actually live.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_7-2.jpg",
                       "caption": "Open living"}},
            {"id": "rooms", "title": "Four Bedrooms",
             "text": "Four bedrooms across three floors. Primary suite on the upper level with vaulted ceiling and "
                     "private deck. The lower level adds a media room and a home office.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_11-2.jpg",
                       "caption": "Primary suite"}},
            {"id": "outdoor", "title": "Wallingford Backyard",
             "text": "The fully fenced backyard is rare for this part of Seattle — flat, sunny, and big enough for a "
                     "swing set and a vegetable garden. Detached two-car garage with EV charging.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_16-2.jpg",
                       "caption": "Backyard"}},
            {"id": "neighborhood", "title": "Wallingford — Family Seattle",
             "text": "Wallingford is the family heart of north Seattle — tree-lined streets, an active community "
                     "center, and one of the city's best Sunday farmer's markets. South Lake Union and Amazon are "
                     "an eight-minute drive.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_23-2.jpg",
                       "caption": "Wallingford streets"},
             "map": {"center": [47.6648, -122.3429], "zoom": 15,
                     "markers": [{"lat": 47.6648, "lng": -122.3429, "label": "1305 N 50th St", "kind": "home"}]}},
            {"id": "schools", "title": "Seattle Schools",
             "text": "Hamilton International Middle School is four blocks away — an 8 out of 10 on GreatSchools and a "
                     "designated IB World School. B.F. Day Elementary rates a 9, and the new Lincoln High School earns a "
                     "perfect 10, completing the catchment.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_27-2.jpg",
                       "caption": "Walk-to-school neighborhood"},
             "map": {"center": [47.6640, -122.3450], "zoom": 14,
                     "markers": [
                         {"lat": 47.6648, "lng": -122.3429, "label": "1305 N 50th St",            "kind": "home"},
                         {"lat": 47.6589, "lng": -122.3503, "label": "B.F. Day Elementary (9/10)",  "kind": "school"},
                         {"lat": 47.6692, "lng": -122.3460, "label": "Hamilton International (8/10)","kind": "school"},
                         {"lat": 47.6738, "lng": -122.3469, "label": "Lincoln High (10/10)",        "kind": "school"},
                     ]}},
            {"id": "lifestyle", "title": "Parks & Wallingford Life",
             "text": "Gas Works Park is a nine-minute walk — Seattle's most iconic skyline view. Green Lake Park is a "
                     "few blocks further, with its three-mile loop. The Wallingford Sunday market is two blocks away.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_28-2.jpg",
                       "caption": "Wallingford lifestyle"},
             "map": {"center": [47.6650, -122.3400], "zoom": 13,
                     "markers": [
                         {"lat": 47.6648, "lng": -122.3429, "label": "1305 N 50th St",   "kind": "home"},
                         {"lat": 47.6620, "lng": -122.3398, "label": "Wallingford Playfield", "kind": "park"},
                         {"lat": 47.6456, "lng": -122.3344, "label": "Gas Works Park",        "kind": "park"},
                         {"lat": 47.6810, "lng": -122.3300, "label": "Green Lake Park",       "kind": "park"},
                     ]}},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "4920": {
        "address": "4920 Stone Ave N, Seattle WA 98103",
        "neighborhood": "Wallingford / Tangletown",
        "city": "Seattle",
        "coords": [47.6663, -122.3434],
        "specs": {
            "status": "Sold",
            "price": "$2,200,000",
            "beds": 3, "baths": 3.5, "sqft": 2690,
            "lot": "0.09 acre", "yearBuilt": 2022, "style": "Contemporary Craftsman",
        },
        "schools": [
            {"name": "B.F. Day Elementary",       "rating": 9, "distance": "0.5 mi", "grades": "K-5",  "kind": "public"},
            {"name": "Hamilton International MS", "rating": 8, "distance": "0.4 mi", "grades": "6-8",  "kind": "public"},
            {"name": "Lincoln High School",        "rating": 10, "distance": "0.9 mi", "grades": "9-12", "kind": "public"},
        ],
        "parks": [
            {"name": "Wallingford Playfield",     "distance": "0.4 mi", "features": "playground, tennis"},
            {"name": "Gas Works Park",             "distance": "0.9 mi", "features": "lakefront, skyline view"},
            {"name": "Green Lake Park",            "distance": "1.0 mi", "features": "3-mile loop, swim beach"},
        ],
        "pitch": (
            "4920 Stone Avenue North is contemporary craftsman in Wallingford — three bedrooms, three and a half baths, "
            "2,690 square feet of intelligent design. Walk to Gas Works Park, Green Lake, and Seattle's best Sunday "
            "farmer's market. A perfectly-sized Seattle family home in one of the city's most loved neighborhoods."
        ),
        "scenes": [
            {"id": "hook", "title": "Contemporary Craftsman",
             "text": "4920 Stone Avenue North — a contemporary craftsman residence in the heart of Wallingford, designed "
                     "for a Seattle family that wants to walk everywhere.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_3-1.jpg",
                       "caption": "Tour video"}},
            {"id": "architecture", "title": "Modern Update on a Craftsman Block",
             "text": "Gabled rooflines and natural wood details respect the Wallingford streetscape; modern proportions "
                     "and a steel-and-glass front entry signal the contemporary interior.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_4-1.jpg",
                       "caption": "Facade"}},
            {"id": "interior", "title": "Light-Filled Living",
             "text": "Open kitchen-dining-living with sliding doors to the backyard deck. Wide-plank oak floors, a 12-foot "
                     "island, and integrated appliances designed for daily Seattle family life.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_6-1.jpg",
                       "caption": "Open living"}},
            {"id": "rooms", "title": "Three Bedrooms",
             "text": "Three bedrooms, three and a half baths. Primary suite with vaulted ceiling and walk-in closet. "
                     "Two additional bedrooms on the upper floor. The lower level includes a flex room and home office.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_7-1.jpg",
                       "caption": "Primary suite"}},
            {"id": "outdoor", "title": "Wallingford Backyard",
             "text": "A fully fenced backyard with a deck, mature trees, and a low-maintenance turf lawn. Detached "
                     "garage with EV charging is rare for this density.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_9-1.jpg",
                       "caption": "Backyard"}},
            {"id": "neighborhood", "title": "Wallingford / Tangletown",
             "text": "Tangletown is the pocket between Wallingford and Green Lake — quiet residential streets, a local "
                     "bakery and bookstore three blocks away, and an eight-minute drive to South Lake Union.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_10-1.jpg",
                       "caption": "Tangletown streets"},
             "map": {"center": [47.6663, -122.3434], "zoom": 15,
                     "markers": [{"lat": 47.6663, "lng": -122.3434, "label": "4920 Stone Ave N", "kind": "home"}]}},
            {"id": "schools", "title": "Schools You Can Walk To",
             "text": "Hamilton International Middle School — an 8 out of 10 IB World School — is four blocks away. "
                     "B.F. Day Elementary rates a 9 and Lincoln High a perfect 10, completing the catchment — all three "
                     "within a mile and all walkable.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_11-1.jpg",
                       "caption": "Schools nearby"},
             "map": {"center": [47.6650, -122.3450], "zoom": 14,
                     "markers": [
                         {"lat": 47.6663, "lng": -122.3434, "label": "4920 Stone Ave N",         "kind": "home"},
                         {"lat": 47.6589, "lng": -122.3503, "label": "B.F. Day Elementary (9/10)",  "kind": "school"},
                         {"lat": 47.6692, "lng": -122.3460, "label": "Hamilton International (8/10)","kind": "school"},
                         {"lat": 47.6738, "lng": -122.3469, "label": "Lincoln High (10/10)",        "kind": "school"},
                     ]}},
            {"id": "lifestyle", "title": "Parks & Wallingford Life",
             "text": "Gas Works Park, Green Lake, and Wallingford Playfield are all within a mile. The Sunday farmer's "
                     "market is two blocks away. Downtown Seattle is a ten-minute drive; Amazon's South Lake Union "
                     "campus is eight.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_12-1.jpg",
                       "caption": "Walkable Seattle lifestyle"},
             "map": {"center": [47.6660, -122.3400], "zoom": 13,
                     "markers": [
                         {"lat": 47.6663, "lng": -122.3434, "label": "4920 Stone Ave N",  "kind": "home"},
                         {"lat": 47.6620, "lng": -122.3398, "label": "Wallingford Playfield", "kind": "park"},
                         {"lat": 47.6456, "lng": -122.3344, "label": "Gas Works Park",        "kind": "park"},
                         {"lat": 47.6810, "lng": -122.3300, "label": "Green Lake Park",       "kind": "park"},
                     ]}},
        ],
    },
}


def get_tour(property_id: str, mode: str = "tour") -> dict | None:
    """Return tour data for the given property and mode.

    mode='pitch' → returns just the pitch paragraph + the first 3 hero scenes
                   (hook/architecture/interior) for the quick presentation.
    mode='tour'  → returns all 8 scenes for the full guided experience.
    """
    p = PROPERTIES.get(property_id)
    if not p:
        return None
    base = {
        "id": property_id,
        "address": p["address"],
        "neighborhood": p["neighborhood"],
        "city": p["city"],
        "coords": p["coords"],
        "specs": p["specs"],
        "schools": p["schools"],
        "parks": p["parks"],
    }
    if mode == "pitch":
        base["pitch"] = p["pitch"]
        base["scenes"] = p["scenes"][:3]   # hook + architecture + interior
        base["mode"] = "pitch"
    else:
        base["scenes"] = p["scenes"]
        base["mode"] = "tour"
    return base
