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
        "coords": [47.59232, -122.20016],
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
            "Welcome to the Enatai Residence at 10425 SE 20th Street — a brand-new modern luxury home available "
            "for presale near downtown Bellevue. Four thousand five hundred seventeen square feet, five bedrooms, "
            "five baths, and a three-car garage on a nine-thousand-five-hundred-square-foot lot. It's built with "
            "expert craftsmanship and carefully selected materials, with smart-home technology, solar power, and "
            "energy-efficient systems throughout. Open living spaces flow seamlessly into a covered patio and a "
            "private backyard — privacy without compromising on convenience, in one of Bellevue's most coveted neighborhoods."
        ),
        "scenes": [
            {
                "id": "hook", "title": "An Enatai Presale",
                "text": "Welcome to the Enatai Residence at 10425 SE 20th Street — a brand-new, 4,517-square-foot modern "
                        "luxury home, available now for presale just minutes from downtown Bellevue.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/03/10425_ENATAI-RESIDENCE_01-1.jpg",
                          "caption": "Sunset render — 10425 SE 20th Street"},
            },
            {
                "id": "architecture", "title": "Modern Luxury, Expert Craftsmanship",
                "text": "This is modern luxury built with expert craftsmanship and carefully selected materials — "
                        "a brand-new residence that offers privacy without compromising on the convenience of downtown Bellevue just minutes away.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/03/10425_ENATAI-RESIDENCE_01-2.jpg",
                          "caption": "Facade — natural materials, modern silhouette"},
            },
            {
                "id": "interior", "title": "Open Living, Indoor-Outdoor Flow",
                "text": "Inside, open living spaces flow seamlessly into a covered patio and a private backyard. "
                        "It's a flexible floor plan, designed to adapt to how you actually live and entertain.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/03/10425_ENATAI-RESIDENCE_01-3.jpg",
                          "caption": "Open great room concept"},
            },
            {
                "id": "rooms", "title": "Five Bedrooms, Spa-Inspired Suite",
                "text": "Five bedrooms and five full baths, anchored by a spa-inspired primary suite. Smart-home "
                        "technology, solar power, and energy-efficient systems are built in throughout the home.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/03/10425_ENATAI-RESIDENCE_01-4.jpg",
                          "caption": "Primary suite concept"},
            },
            {
                "id": "outdoor", "title": "Covered Patio & Private Backyard",
                "text": "The home sits on a 9,541-square-foot lot with a private backyard and a covered patio — "
                        "true indoor-outdoor living, with quiet seclusion just minutes from the city.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/03/10425_ENATAI-RESIDENCE_01-5.jpg",
                          "caption": "Outdoor lounge & landscape"},
            },
            {
                "id": "neighborhood", "title": "Enatai — Quiet, Close to Everything",
                "text": "Enatai is a tranquil residential pocket of Bellevue near Lake Washington — privacy and quiet, "
                        "while staying minutes from downtown Bellevue's shops, dining, and freeways.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/03/10425_ENATAI-RESIDENCE_01-6.jpg",
                          "caption": "Aerial view of Enatai"},
                "map": {"center": [47.59232, -122.20016], "zoom": 15,
                        "markers": [{"lat": 47.59232, "lng": -122.20016, "label": "10425 SE 20th St", "kind": "home"}]},
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
                            {"lat": 47.59232, "lng": -122.20016, "label": "10425 SE 20th St",     "kind": "home"},
                            {"lat": 47.58907, "lng": -122.19822, "label": "Enatai Elementary (8/10)",  "kind": "school"},
                            {"lat": 47.62783, "lng": -122.21085, "label": "Chinook Middle (8/10)",     "kind": "school"},
                            {"lat": 47.60423, "lng": -122.19843, "label": "Bellevue High (10/10)",     "kind": "school"},
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
                            {"lat": 47.59232, "lng": -122.20016, "label": "10425 SE 20th St",        "kind": "home"},
                            {"lat": 47.57939, "lng": -122.19748, "label": "Enatai Beach Park",         "kind": "park"},
                            {"lat": 47.58918, "lng": -122.18711, "label": "Mercer Slough Nature Park", "kind": "park"},
                            {"lat": 47.59965, "lng": -122.21002, "label": "Chism Beach Park",          "kind": "park"},
                            {"lat": 47.57872, "lng": -122.16729, "label": "QFC — Factoria",            "kind": "shop"},
                        ]},
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "312": {
        "address": "312 160th Ave NE, Bellevue WA 98008",
        "neighborhood": "Crossroads / Bel-Red",
        "city": "Bellevue",
        "coords": [47.61298, -122.12665],
        "specs": {
            "status": "Pending",
            "price": "$3,158,000",
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
            "312 160th Avenue NE is contemporary luxury near Bellevue, Sammamish, and the Microsoft campus, offered "
            "at three million one hundred fifty-eight thousand dollars. A 4,400-square-foot residence with five "
            "bedrooms and four-and-a-quarter baths, built with exceptional craftsmanship and carefully selected "
            "materials. Open living spaces extend to a covered terrace and a private backyard, with a spa-inspired "
            "primary suite, smart-home technology, and solar energy throughout — privacy without compromising on convenience."
        ),
        "scenes": [
            {
                "id": "hook", "title": "Sophistication in Every Detail",
                "text": "312 160th Avenue NE — a brand-new contemporary luxury residence, four thousand four hundred "
                        "square feet near Bellevue, Sammamish, and the Microsoft campus.",
                "media": {"type": "video",
                          "url": "https://bellshireinc.com/wp-content/uploads/2026/02/6524_Cinematoc_4K_Branded_New_Music_v3-3.mp4",
                          "caption": "Cinematic property tour"},
            },
            {
                "id": "architecture", "title": "Contemporary Modern",
                "text": "Contemporary luxury, built with exceptional craftsmanship and carefully selected materials — "
                        "a brand-new residence designed for privacy without compromising on convenience.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2025/07/1-web-or-mls-312-160th-ave-ne.jpg",
                          "caption": "Front elevation"},
            },
            {
                "id": "interior", "title": "Sun-Filled Open Plan",
                "text": "Inside, open living spaces flow through to a covered terrace and a private backyard — "
                        "bright, modern, and designed for both everyday living and entertaining.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2025/07/8-web-or-mls-312-160th-ave-ne.jpg",
                          "caption": "Great room with stone fireplace"},
            },
            {
                "id": "rooms", "title": "Signature Spaces",
                "text": "A spa-inspired primary suite anchors five bedrooms and four-and-a-quarter baths. Smart-home "
                        "technology and solar energy systems are integrated throughout the home.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2025/07/12-web-or-mls-312-160th-ave-ne.jpg",
                          "caption": "Chef's kitchen"},
            },
            {
                "id": "outdoor", "title": "Covered Terrace & Backyard",
                "text": "Open living extends outdoors to a covered terrace and a private backyard on an 8,250-square-foot "
                        "lot — your own quiet retreat, minutes from the city.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2025/07/22-web-or-mls-312-160th-ave-ne.jpg",
                          "caption": "Outdoor entertaining"},
            },
            {
                "id": "neighborhood", "title": "Near Bellevue, Sammamish & Microsoft",
                "text": "The home sits in the Crossroads area of Bellevue, near Sammamish and the Microsoft campus — "
                        "an easy commute to the Eastside's major tech employers, with the quiet of a residential street.",
                "media": {"type": "image",
                          "url": "https://bellshireinc.com/wp-content/uploads/2025/07/2-web-or-mls-312-160th-ave-ne.jpg",
                          "caption": "Aerial — Crossroads neighborhood"},
                "map": {"center": [47.61298, -122.12665], "zoom": 14,
                        "markers": [{"lat": 47.61298, "lng": -122.12665, "label": "312 160th Ave NE", "kind": "home"}]},
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
                            {"lat": 47.61298, "lng": -122.12665, "label": "312 160th Ave NE",        "kind": "home"},
                            {"lat": 47.63039, "lng": -122.12027, "label": "Sherwood Forest Elem (5/10)", "kind": "school"},
                            {"lat": 47.62578, "lng": -122.14028, "label": "Highland Middle (4/10)",      "kind": "school"},
                            {"lat": 47.63017, "lng": -122.12443, "label": "Interlake High (10/10)",      "kind": "school"},
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
                            {"lat": 47.61298, "lng": -122.12665, "label": "312 160th Ave NE",   "kind": "home"},
                            {"lat": 47.62008, "lng": -122.12703, "label": "Crossroads Park",     "kind": "park"},
                            {"lat": 47.58781, "lng": -122.13999, "label": "Robinswood Park",     "kind": "park"},
                            {"lat": 47.60664, "lng": -122.17748, "label": "Wilburton Hill Park", "kind": "park"},
                            {"lat": 47.61780, "lng": -122.12800, "label": "QFC — Crossroads", "kind": "shop"},
                        ]},
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "218": {
        "address": "218 109th Avenue SE, Bellevue WA 98004",
        "neighborhood": "Downtown Bellevue / Surrey Downs",
        "city": "Bellevue",
        "coords": [47.60744, -122.19480],
        "specs": {
            "status": "Pending",
            "price": "$4,500,000",
            "beds": 5, "baths": 4.25, "sqft": 4400, "garage": 2,
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
            "218 109th Avenue SE is a brand-new modern luxury home in the heart of Bellevue's Surrey Downs, near "
            "top-rated schools and parks — offered at four million five hundred thousand dollars. Five bedrooms, "
            "four-and-a-quarter baths, 4,400 square feet, with a separate study and a gourmet chef's kitchen featuring "
            "a premium Thermador appliance package. There are two living spaces — including a home theater and a game "
            "room — plus smart-home technology, EV chargers, and energy-efficient LED lighting throughout."
        ),
        "scenes": [
            {"id": "hook", "title": "Modern Luxury in the Heart of Bellevue",
             "text": "218 109th Avenue SE — a brand-new modern luxury residence in Bellevue's Surrey Downs, "
                     "near top-rated schools and parks.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/002_2-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Front view"}},
            {"id": "architecture", "title": "Brand-New Modern Luxury",
             "text": "A brand-new modern luxury build in the heart of Bellevue — clean contemporary design and "
                     "premium craftsmanship throughout, minutes from downtown.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/003_3-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Modern facade"}},
            {"id": "interior", "title": "Chef's Kitchen & Two Living Spaces",
             "text": "Inside, a gourmet chef's kitchen with a premium Thermador appliance package anchors the main level, "
                     "opening to two living spaces — including a home theater and a game room — plus a separate study.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/004_4-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Great room"}},
            {"id": "rooms", "title": "Signature Rooms",
             "text": "Five bedrooms and four-and-a-quarter baths, with smart-home technology, EV chargers, and "
                     "energy-efficient LED lighting integrated throughout the home.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/005_5-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Primary suite"}},
            {"id": "outdoor", "title": "Outdoor Living",
             "text": "A spacious main-level patio is built for outdoor dining, opening to a large backyard with "
                     "seamless indoor-outdoor living — private, yet minutes from the heart of the city.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/006_6-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Backyard"}},
            {"id": "neighborhood", "title": "Surrey Downs — In the Heart of Bellevue",
             "text": "Surrey Downs is a quiet residential pocket in the heart of Bellevue — minutes from downtown "
                     "Bellevue's shops, dining, and parks, with top-rated schools close by.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/007_7-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Surrey Downs neighborhood"},
             "map": {"center": [47.60744, -122.19480], "zoom": 15,
                     "markers": [{"lat": 47.60744, "lng": -122.19480, "label": "218 109th Ave SE", "kind": "home"}]}},
            {"id": "schools", "title": "Bellevue's Top Schools",
             "text": "Bellevue High School — a perfect 10 out of 10 on GreatSchools — is a seven-minute walk. Enatai "
                     "Elementary and Chinook Middle, both rated 8 out of 10, are within a mile. All three sit in the "
                     "Bellevue School District, the top-ranked public district in Washington.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/008_8-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Walking distance to top schools"},
             "map": {"center": [47.6060, -122.1930], "zoom": 14,
                     "markers": [
                         {"lat": 47.60744, "lng": -122.19480, "label": "218 109th Ave SE",       "kind": "home"},
                         {"lat": 47.58907, "lng": -122.19822, "label": "Enatai Elementary (8/10)",  "kind": "school"},
                         {"lat": 47.62783, "lng": -122.21085, "label": "Chinook Middle (8/10)",     "kind": "school"},
                         {"lat": 47.60423, "lng": -122.19843, "label": "Bellevue High (10/10)",     "kind": "school"},
                     ]}},
            {"id": "lifestyle", "title": "Parks, Lake & Lifestyle",
             "text": "Surrey Downs Park is around the corner. Bellevue Downtown Park and Meydenbauer Bay Park's "
                     "lakefront beach and marina on Lake Washington are just minutes away.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/009_9-print-218-109th-ave-se_196-scaled.jpg",
                       "caption": "Urban Bellevue lifestyle"},
             "map": {"center": [47.6070, -122.1920], "zoom": 14,
                     "markers": [
                         {"lat": 47.60744, "lng": -122.19480, "label": "218 109th Ave SE",      "kind": "home"},
                         {"lat": 47.60419, "lng": -122.19181, "label": "Surrey Downs Park",      "kind": "park"},
                         {"lat": 47.61247, "lng": -122.20456, "label": "Downtown Park",          "kind": "park"},
                         {"lat": 47.61221, "lng": -122.21137, "label": "Meydenbauer Bay Park",   "kind": "park"},
                         {"lat": 47.61821, "lng": -122.18459, "label": "Whole Foods — Bellevue", "kind": "shop"},
                     ]}},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "1224": {
        "address": "1224 108th Ave SE, Bellevue WA 98004",
        "neighborhood": "Enatai / Surrey Downs",
        "city": "Bellevue",
        "coords": [47.59851, -122.19611],
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
            "1224 108th Avenue SE is modern luxury in the heart of Bellevue — a newly constructed estate of 6,713 "
            "square feet with six bedrooms, seven-and-a-half baths, and a three-car garage, offered at six million "
            "four hundred fifty thousand dollars. It has a separate study and a gourmet chef's kitchen with premium "
            "Thermador appliances, two living spaces, and a daylit basement with a second kitchen and a home theater. "
            "Outside: a private terrace with direct basement access, a main-level deck for dining, and an expansive "
            "backyard shaded by century-old pine trees."
        ),
        "scenes": [
            {"id": "hook", "title": "A Modern Bellevue Estate",
             "text": "1224 108th Avenue SE — modern luxury in the heart of Bellevue. A newly constructed estate: "
                     "6,713 square feet, six bedrooms, seven-and-a-half baths.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/1-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Estate entrance"}},
            {"id": "architecture", "title": "Modern Estate Architecture",
             "text": "A newly constructed, three-level modern estate finished to the highest standard — modern luxury "
                     "in one of Bellevue's most established neighborhoods.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/3-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Architectural facade"}},
            {"id": "interior", "title": "Chef's Kitchen & Two Living Spaces",
             "text": "Inside, a gourmet chef's kitchen with premium Thermador appliances and a separate study anchor "
                     "the main level, with two living spaces designed for entertaining.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/5-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Great room"}},
            {"id": "rooms", "title": "Three Levels, Daylit Basement",
             "text": "Six bedrooms and seven-and-a-half baths across three levels, including a daylit basement with "
                     "a second kitchen and a private home theater — plus EV chargers and smart-home technology throughout.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/8-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Primary suite"}},
            {"id": "outdoor", "title": "Terrace, Deck & Century-Old Pines",
             "text": "Outside: a private terrace with direct basement access, a main-level deck designed for outdoor "
                     "dining, and an expansive backyard shaded by century-old pine trees.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/12-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Pool and outdoor kitchen"}},
            {"id": "neighborhood", "title": "Heart of Bellevue, Near the Lake",
             "text": "The estate sits in one of Bellevue's most established residential neighborhoods near Lake "
                     "Washington — mature trees, generous lots, and only minutes from downtown Bellevue.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/2-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Enatai aerial"},
             "map": {"center": [47.59851, -122.19611], "zoom": 14,
                     "markers": [{"lat": 47.59851, "lng": -122.19611, "label": "1224 108th Ave SE", "kind": "home"}]}},
            {"id": "schools", "title": "Walk to Bellevue High",
             "text": "Bellevue High School — a perfect 10 out of 10 on GreatSchools — is a five-minute walk. Enatai "
                     "Elementary and Chinook Middle, both rated 8 out of 10, round out a school assignment that's among "
                     "the most coveted on the Eastside.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/4-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Top schools all within a mile"},
             "map": {"center": [47.5945, -122.1950], "zoom": 14,
                     "markers": [
                         {"lat": 47.59851, "lng": -122.19611, "label": "1224 108th Ave SE",       "kind": "home"},
                         {"lat": 47.58907, "lng": -122.19822, "label": "Enatai Elementary (8/10)",  "kind": "school"},
                         {"lat": 47.62783, "lng": -122.21085, "label": "Chinook Middle (8/10)",     "kind": "school"},
                         {"lat": 47.60423, "lng": -122.19843, "label": "Bellevue High (10/10)",     "kind": "school"},
                     ]}},
            {"id": "lifestyle", "title": "Lake, Parks, City",
             "text": "Mercer Slough Nature Park's wetlands and trails are nearby, with Bellefields Nature Park and "
                     "Meydenbauer Bay Park on Lake Washington close by. Downtown Bellevue is just minutes away.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2025/06/7-web-or-mls-1224-108th-ave-se.jpg",
                       "caption": "Lakeside lifestyle"},
             "map": {"center": [47.5955, -122.1900], "zoom": 13,
                     "markers": [
                         {"lat": 47.59851, "lng": -122.19611, "label": "1224 108th Ave SE",        "kind": "home"},
                         {"lat": 47.5990, "lng": -122.1875, "label": "Bellefields Nature Park",   "kind": "park"},
                         {"lat": 47.58918, "lng": -122.18711, "label": "Mercer Slough Nature Park", "kind": "park"},
                         {"lat": 47.61221, "lng": -122.21137, "label": "Meydenbauer Bay Park",      "kind": "park"},
                         {"lat": 47.61821, "lng": -122.18459, "label": "Whole Foods — Bellevue",     "kind": "shop"},
                     ]}},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "1071": {
        "address": "1071 102nd Place SE, Bellevue WA 98004",
        "neighborhood": "Enatai",
        "city": "Bellevue",
        "coords": [47.60042, -122.20449],
        "specs": {
            "status": "Sold",
            "price": "Price on request",
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
            "1071 102nd Place SE is brand-new construction in Bellevue — 5,920 square feet with five bedrooms, five "
            "baths, and a two-car garage. It's an open floor plan with high ceilings and oversized windows, hardwood "
            "and heated floors, a large kitchen with stainless steel appliances, walk-in closets, and city-light "
            "views. As Bellshire puts it — your dream home is here."
        ),
        "scenes": [
            {"id": "hook", "title": "Brand-New Construction in Bellevue",
             "text": "1071 102nd Place SE — brand-new construction in Bellevue, 5,920 square feet with five bedrooms "
                     "and five baths.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_4.jpg",
                       "caption": "Cinematic property tour"}},
            {"id": "architecture", "title": "Light-Filled New Build",
             "text": "New construction with an open, light-filled design — high ceilings, oversized windows, "
                     "and quality finishes throughout.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_4.jpg",
                       "caption": "Front elevation"}},
            {"id": "interior", "title": "Open, Light-Filled Living",
             "text": "Inside, an open floor plan with high ceilings and oversized windows, hardwood and heated floors, "
                     "and a large kitchen finished with stainless steel appliances.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_7.jpg",
                       "caption": "Open plan interior"}},
            {"id": "rooms", "title": "Five Bedrooms, City-Light Views",
             "text": "Five bedrooms and five full baths with generous walk-in closets — comfortable, modern living, "
                     "with city-light views from the upper level.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_11-scaled.jpg",
                       "caption": "Primary suite"}},
            {"id": "outdoor", "title": "Private Outdoor Space",
             "text": "A private yard rounds out the home — quiet seclusion in an established Bellevue neighborhood, "
                     "just minutes from Lake Washington and downtown.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_16.jpg",
                       "caption": "Outdoor lounge"}},
            {"id": "neighborhood", "title": "Quiet, Established Bellevue",
             "text": "The home sits in a quiet, established Bellevue neighborhood near Lake Washington — great schools, "
                     "parks, and downtown Bellevue all close by.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_22.jpg",
                       "caption": "Enatai from above"},
             "map": {"center": [47.60042, -122.20449], "zoom": 15,
                     "markers": [{"lat": 47.60042, "lng": -122.20449, "label": "1071 102nd Pl SE", "kind": "home"}]}},
            {"id": "schools", "title": "Top-Ranked Bellevue Schools",
             "text": "Enatai Elementary — an 8 out of 10 — is three blocks away. Chinook Middle also rates an 8, and "
                     "Bellevue High earns a perfect 10, both within a mile. Walkable schools, top-tier ratings — the "
                     "Eastside's golden combination.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_23.jpg",
                       "caption": "Walk to top schools"},
             "map": {"center": [47.5910, -122.2000], "zoom": 14,
                     "markers": [
                         {"lat": 47.60042, "lng": -122.20449, "label": "1071 102nd Pl SE",        "kind": "home"},
                         {"lat": 47.58907, "lng": -122.19822, "label": "Enatai Elementary (8/10)",  "kind": "school"},
                         {"lat": 47.62783, "lng": -122.21085, "label": "Chinook Middle (8/10)",     "kind": "school"},
                         {"lat": 47.60423, "lng": -122.19843, "label": "Bellevue High (10/10)",     "kind": "school"},
                     ]}},
            {"id": "lifestyle", "title": "Lake, Parks, City",
             "text": "Enatai Beach Park, with its swim dock and kayak launch on Lake Washington, is close by, along "
                     "with Mercer Slough's nature trails. Downtown Bellevue is just a short drive.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_12.jpg",
                       "caption": "Lake Washington nearby"},
             "map": {"center": [47.5910, -122.2000], "zoom": 13,
                     "markers": [
                         {"lat": 47.60042, "lng": -122.20449, "label": "1071 102nd Pl SE",          "kind": "home"},
                         {"lat": 47.57939, "lng": -122.19748, "label": "Enatai Beach Park",          "kind": "park"},
                         {"lat": 47.59965, "lng": -122.21002, "label": "Chism Beach Park",           "kind": "park"},
                         {"lat": 47.58918, "lng": -122.18711, "label": "Mercer Slough Nature Park",  "kind": "park"},
                         {"lat": 47.57872, "lng": -122.16729, "label": "QFC — Factoria",             "kind": "shop"},
                     ]}},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "1305": {
        "address": "1305 North 50th Street, Seattle WA 98103",
        "neighborhood": "Woodland Park / Wallingford",
        "city": "Seattle",
        "coords": [47.66480, -122.34164],
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
            "1305 North 50th Street is a newly constructed Seattle home right next to Woodland Park, offered at two "
            "million four hundred thousand dollars. Three thousand one hundred twenty square feet with four bedrooms "
            "plus a den, three-and-a-half baths, and a two-car garage. It has territorial views from the upper-floor "
            "bedrooms, an open kitchen with Thermador appliances, a glass staircase, and a rooftop deck with an "
            "outdoor patio. Smart-home technology, EV chargers, an efficient split-system air conditioning with heat "
            "pumps, and hardwood and heated floors throughout — near Green Lake and minutes from downtown Seattle."
        ),
        "scenes": [
            {"id": "hook", "title": "New Home by Woodland Park",
             "text": "1305 North 50th Street — a brand-new Seattle home right next to Woodland Park, near Green Lake "
                     "and minutes from downtown.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_3-2.jpg",
                       "caption": "Front view"}},
            {"id": "architecture", "title": "Newly Constructed",
             "text": "Newly constructed with high-end materials and luxurious finishes — a bright, modern home "
                     "designed for north-Seattle living.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_4-2.jpg",
                       "caption": "Architectural facade"}},
            {"id": "interior", "title": "Open Kitchen & Glass Staircase",
             "text": "Inside, an open kitchen with Thermador appliances, a striking glass staircase, hardwood and "
                     "heated floors, and a second family room.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_7-2.jpg",
                       "caption": "Open living"}},
            {"id": "rooms", "title": "Four Bedrooms + Den",
             "text": "Four bedrooms plus a den and three-and-a-half baths, with light-filled territorial views from "
                     "the upper-floor bedrooms and walk-in closets.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_11-2.jpg",
                       "caption": "Primary suite"}},
            {"id": "outdoor", "title": "Rooftop Deck & Backyard",
             "text": "A rooftop deck with an outdoor patio and a private backyard — plus EV chargers, an efficient "
                     "split-system A/C with heat pumps, smart-home tech, sprinklers, and gutter guards.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_16-2.jpg",
                       "caption": "Backyard"}},
            {"id": "neighborhood", "title": "Next to Woodland Park",
             "text": "The home sits next to Woodland Park in north Seattle — green space and the zoo right at your "
                     "door, Green Lake nearby, and an easy trip to downtown Seattle.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_23-2.jpg",
                       "caption": "Wallingford streets"},
             "map": {"center": [47.66480, -122.34164], "zoom": 15,
                     "markers": [{"lat": 47.66480, "lng": -122.34164, "label": "1305 N 50th St", "kind": "home"}]}},
            {"id": "schools", "title": "Seattle Schools",
             "text": "Hamilton International Middle School is four blocks away — an 8 out of 10 on GreatSchools and a "
                     "designated IB World School. B.F. Day Elementary rates a 9, and the new Lincoln High School earns a "
                     "perfect 10, completing the catchment.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_27-2.jpg",
                       "caption": "Walk-to-school neighborhood"},
             "map": {"center": [47.6640, -122.3450], "zoom": 14,
                     "markers": [
                         {"lat": 47.66480, "lng": -122.34164, "label": "1305 N 50th St",            "kind": "home"},
                         {"lat": 47.65516, "lng": -122.34915, "label": "B.F. Day Elementary (9/10)",  "kind": "school"},
                         {"lat": 47.65750, "lng": -122.33803, "label": "Hamilton International (8/10)","kind": "school"},
                         {"lat": 47.65994, "lng": -122.33966, "label": "Lincoln High (10/10)",        "kind": "school"},
                     ]}},
            {"id": "lifestyle", "title": "Parks & North Seattle Life",
             "text": "Woodland Park and its zoo are right next door, Green Lake's three-mile loop is close by, and "
                     "Gas Works Park's iconic skyline views are a short trip away.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_28-2.jpg",
                       "caption": "Wallingford lifestyle"},
             "map": {"center": [47.6650, -122.3400], "zoom": 13,
                     "markers": [
                         {"lat": 47.66480, "lng": -122.34164, "label": "1305 N 50th St",   "kind": "home"},
                         {"lat": 47.65860, "lng": -122.33742, "label": "Wallingford Playfield", "kind": "park"},
                         {"lat": 47.64560, "lng": -122.33493, "label": "Gas Works Park",        "kind": "park"},
                         {"lat": 47.67775, "lng": -122.33237, "label": "Green Lake Park",       "kind": "park"},
                         {"lat": 47.64890, "lng": -122.35030, "label": "PCC — Fremont",         "kind": "shop"},
                     ]}},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "4920": {
        "address": "4920 Stone Ave N, Seattle WA 98103",
        "neighborhood": "Woodland Park / Fremont",
        "city": "Seattle",
        "coords": [47.66451, -122.34197],
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
            "4920 Stone Avenue North is a brand-new Seattle home near Woodland Park, offered at two million two "
            "hundred thousand dollars. Two thousand six hundred ninety square feet with three bedrooms, "
            "three-and-a-half baths, and a two-car garage. It has light-filled territorial views from the upper-floor "
            "bedrooms, an open kitchen with Thermador appliances, a glass staircase, and a rooftop deck. Smart-home "
            "technology, EV chargers, and an efficient split-system air conditioning with heat pumps — close to Green "
            "Lake and minutes from downtown Seattle."
        ),
        "scenes": [
            {"id": "hook", "title": "New Home near Woodland Park",
             "text": "4920 Stone Avenue North — a brand-new Seattle home near Woodland Park, close to Green Lake "
                     "and downtown.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_3-1.jpg",
                       "caption": "Tour video"}},
            {"id": "architecture", "title": "Brand-New Construction",
             "text": "Brand-new construction with high-end materials and luxurious finishes — a bright, modern, "
                     "light-filled home in north Seattle.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_4-1.jpg",
                       "caption": "Facade"}},
            {"id": "interior", "title": "Open Kitchen & Glass Staircase",
             "text": "Inside, an open kitchen with Thermador appliances, a glass staircase, hardwood and heated "
                     "floors, and oversized windows that fill the home with light.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_6-1.jpg",
                       "caption": "Open living"}},
            {"id": "rooms", "title": "Three Bedrooms, Light-Filled",
             "text": "Three bedrooms and three-and-a-half baths, with light-filled territorial views from the "
                     "upper-floor bedrooms and walk-in closets.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_7-1.jpg",
                       "caption": "Primary suite"}},
            {"id": "outdoor", "title": "Rooftop Deck & Backyard",
             "text": "A rooftop deck and a private backyard — plus EV chargers, an efficient split-system A/C with "
                     "heat pumps, smart-home tech, sprinklers, and gutter guards.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_9-1.jpg",
                       "caption": "Backyard"}},
            {"id": "neighborhood", "title": "Near Woodland Park & Green Lake",
             "text": "The home sits near Woodland Park in north Seattle — green space close by, Green Lake nearby, "
                     "and an easy trip into downtown Seattle.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_10-1.jpg",
                       "caption": "Tangletown streets"},
             "map": {"center": [47.66451, -122.34197], "zoom": 15,
                     "markers": [{"lat": 47.66451, "lng": -122.34197, "label": "4920 Stone Ave N", "kind": "home"}]}},
            {"id": "schools", "title": "Schools You Can Walk To",
             "text": "Hamilton International Middle School — an 8 out of 10 IB World School — is four blocks away. "
                     "B.F. Day Elementary rates a 9 and Lincoln High a perfect 10, completing the catchment — all three "
                     "within a mile and all walkable.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_11-1.jpg",
                       "caption": "Schools nearby"},
             "map": {"center": [47.6650, -122.3450], "zoom": 14,
                     "markers": [
                         {"lat": 47.66451, "lng": -122.34197, "label": "4920 Stone Ave N",         "kind": "home"},
                         {"lat": 47.65516, "lng": -122.34915, "label": "B.F. Day Elementary (9/10)",  "kind": "school"},
                         {"lat": 47.65750, "lng": -122.33803, "label": "Hamilton International (8/10)","kind": "school"},
                         {"lat": 47.65994, "lng": -122.33966, "label": "Lincoln High (10/10)",        "kind": "school"},
                     ]}},
            {"id": "lifestyle", "title": "Parks & North Seattle Life",
             "text": "Woodland Park, Green Lake's three-mile loop, and Gas Works Park are all close by — and "
                     "downtown Seattle is just a short drive.",
             "media": {"type": "image",
                       "url": "https://bellshireinc.com/wp-content/uploads/2023/11/web_12-1.jpg",
                       "caption": "Walkable Seattle lifestyle"},
             "map": {"center": [47.6660, -122.3400], "zoom": 13,
                     "markers": [
                         {"lat": 47.66451, "lng": -122.34197, "label": "4920 Stone Ave N",  "kind": "home"},
                         {"lat": 47.65860, "lng": -122.33742, "label": "Wallingford Playfield", "kind": "park"},
                         {"lat": 47.64560, "lng": -122.33493, "label": "Gas Works Park",        "kind": "park"},
                         {"lat": 47.67775, "lng": -122.33237, "label": "Green Lake Park",       "kind": "park"},
                         {"lat": 47.64890, "lng": -122.35030, "label": "PCC — Fremont",         "kind": "shop"},
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


# ──────────────────────────────────────────────────────────────────────────
# PHOTO TAGS — gallery photos classified by room/area, so the voice assistant,
# chatbot and tours can surface a SPECIFIC photo on request. PHOTO_GALLERIES
# mirrors the site gallery order; PHOTO_TAGS holds 0-based indices into it
# (identical to the frontend PROPERTY_PHOTO_TAGS).  Tagged: 218, 312, 1224.
# ──────────────────────────────────────────────────────────────────────────
PHOTO_GALLERIES = {
    "218": [
        "https://bellshireinc.com/wp-content/uploads/2025/06/002_2-print-218-109th-ave-se_196-scaled.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/005_5-print-218-109th-ave-se_894-scaled.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/006_6-print-218-109th-ave-se_260-scaled.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/007_7-print-218-109th-ave-se_690-scaled.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/009_9-print-218-109th-ave-se_918-scaled.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/010_10-print-218-109th-ave-se_285-scaled.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/011_11-print-218-109th-ave-se_501-scaled.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/013_13-print-218-109th-ave-se_61-scaled.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/014_14-print-218-109th-ave-se_351-scaled.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/019_19-print-218-109th-ave-se_713-scaled.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/023_23-print-218-109th-ave-se_664-scaled.jpg"
    ],
    "312": [
        "https://bellshireinc.com/wp-content/uploads/2025/07/1-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/2-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/3-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/4-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/5-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/6-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/7-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/8-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/9-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/10-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/11-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/12-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/13-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/14-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/15-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/17-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/18-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/19-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/20-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/21-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/22-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/23-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/24-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/25-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/26-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/27-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/28-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/29-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/30-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/31-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/33-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/34-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/35-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/36-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/37-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/38-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/39-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/40-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/41-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/42-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/43-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/44-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/45-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/46-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/47-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/48-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/49-web-or-mls-312-160th-ave-ne.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/07/50-web-or-mls-312-160th-ave-ne.jpg"
    ],
    "1224": [
        "https://bellshireinc.com/wp-content/uploads/2025/06/1-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/2-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/3-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/4-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/5-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/6-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/7-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/8-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/9-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/10-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/11-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/12-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/13-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/14-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/15-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/16-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/17-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/18-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/19-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/20-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/21-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/22-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/23-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/24-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/25-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/26-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/27-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/28-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/29-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/30-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/31-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/32-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/33-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/34-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/35-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/36-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/37-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/38-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/39-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/40-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/41-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/42-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/43-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/44-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/45-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/46-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/47-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/48-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/49-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/50-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/51-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/52-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/53-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/54-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/55-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/56-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/57-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/58-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/59-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/60-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/61-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/62-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/63-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/64-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/65-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/66-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/67-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/68-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/69-web-or-mls-1224-108th-ave-se.jpg",
        "https://bellshireinc.com/wp-content/uploads/2025/06/70-web-or-mls-1224-108th-ave-se.jpg"
    ],
}

PHOTO_TAGS = {
    "218": {"exterior": [0], "front": [0], "garage": [0], "entry": [2, 7], "stairs": [2], "living": [3, 4], "great_room": [3, 4], "kitchen": [5, 8, 9], "wet_bar": [8], "dining": [1, 6, 7], "backyard": [10], "patio": [10], "deck": [10]},
    "312": {"exterior": [0, 1, 39, 40, 41], "front": [0, 1, 40, 41], "garage": [0, 40], "aerial": [42, 43, 44, 45, 46], "entry": [2, 3, 36], "living": [4, 7, 8, 21, 22, 47], "great_room": [5, 6], "family": [22], "stairs": [5, 6, 20], "kitchen": [12, 14, 15, 16, 17], "dining": [13, 18], "guest_bath": [19], "powder": [19], "half_bath": [19], "bedroom": [23, 32, 34], "master": [25, 26], "master_bedroom": [25, 26], "master_bath": [27, 28], "master_bathroom": [27, 28], "bathroom": [24, 29, 33, 35], "bathrooms": [24, 29, 33, 35], "walk_in_closet": [30, 31], "closet": [30, 31], "backyard": [9, 10, 11, 37, 38], "patio": [10, 11, 37], "deck": [37], "view": [43, 44, 45, 46]},
    "1224": {"exterior": [0, 1, 2, 3, 4, 43], "front": [1, 2, 3], "garage": [2], "entry": [5, 8, 13, 14, 43], "foyer": [8, 13, 14], "office": [9], "study": [9], "living": [6, 7, 15, 16], "great_room": [6, 7, 16], "family": [44, 54, 58], "family_room": [44, 54, 58], "dining": [10, 45], "kitchen": [17, 18, 19, 20, 22, 23, 50, 57, 60, 61], "pantry": [21, 53], "wine_cellar": [12, 63], "wine": [12, 63], "stairs": [31, 49, 62, 64, 65], "staircase": [31, 49, 62, 64, 65], "guest_bath": [11], "powder": [11], "half_bath": [11], "bedroom": [24, 29, 38], "guest_bedroom": [24], "master": [26, 32, 33], "master_bedroom": [26, 32, 33], "master_bath": [34, 35, 36, 47, 67, 69], "master_bathroom": [34, 35, 36, 47, 67, 69], "bathroom": [25, 27, 28, 30, 37, 39, 40, 48, 52], "bathrooms": [25, 27, 28, 30, 37, 39, 40, 48, 52], "closet": [42], "walk_in_closet": [42], "laundry": [41, 46], "basement": [49, 51, 54, 55, 56, 58, 59, 66], "lower_level": [49, 51, 54, 55, 56, 58, 59, 66], "wet_bar": [55, 59], "second_kitchen": [55, 56], "backyard": [44, 58], "patio": [44, 58], "deck": [44, 58], "view": [9, 36]},
}

def get_photos(property_id: str, category: str):
    """Return full photo URLs for a tagged room/area of a property (or [])."""
    gallery = PHOTO_GALLERIES.get(property_id) or []
    tags = PHOTO_TAGS.get(property_id) or {}
    key = (category or '').strip().lower().replace(' ', '_').replace('-', '_')
    return [gallery[i] for i in (tags.get(key) or []) if 0 <= i < len(gallery)]
