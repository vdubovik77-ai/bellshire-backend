from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, HTMLResponse
import httpx
import os
import sqlite3
import json as _json
import uuid
import datetime as _dt
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Voice Assistant API")

# ── Database ──────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "conversations.db")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "bellshire2024")

def _db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _init_db():
    conn = _db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id          TEXT PRIMARY KEY,
            started_at  TEXT NOT NULL,
            updated_at  TEXT NOT NULL,
            source      TEXT DEFAULT 'chat',
            messages    TEXT NOT NULL DEFAULT '[]',
            fields      TEXT NOT NULL DEFAULT '{}',
            meeting     TEXT,
            ip_address  TEXT,
            consent     INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

_init_db()

app.add_middleware(
    CORSMiddleware,
    # Allow localhost + any Cloudflare Tunnel domain (*.trycloudflare.com)
    allow_origin_regex=r"^(https?://(localhost|127\.0\.0\.1)(:\d+)?|https://[a-z0-9-]+\.trycloudflare\.com|https://[a-z0-9-]+\.pages\.dev)$",
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VOICE = os.getenv("VOICE", "shimmer")

BASE_INSTRUCTIONS = (
    "You are Alexandra, a senior AI real estate consultant at Bellshire Homes — a luxury homebuilder in Bellevue, Washington. "
    "You are warm, professional, and knowledgeable about luxury real estate. "
    "CRITICAL LANGUAGE RULE: Always respond in the SAME language the user speaks. If they speak Ukrainian — respond only in Ukrainian. If English — respond only in English. Never mix languages. "
    "Keep responses concise and conversational — this is a voice call, not a text chat. "
    "You can help with: property tours, pricing, custom builds, neighborhoods, financing options, and scheduling appointments. "
    "Bellshire Homes builds luxury custom homes in the greater Bellevue area.\n\n"
    "== ABOUT BELLSHIRE HOMES ==\n"
    "Bellshire Homes is a full-service luxury home builder and renovation company in Bellevue, WA.\n"
    "- Office: 1071 102nd Place SE, Bellevue, WA 98004\n"
    "- Phone: +1 (425) 658 6939\n"
    "- Email: office@bellshireinc.com\n"
    "- Business hours: Monday–Friday, 9:00 AM – 6:00 PM PST\n\n"
    "== AVAILABLE PROPERTIES ==\n"
    "1. 10425 SE 20th St, Bellevue WA — PRESALE — 5 bed/5 bath/4,517 SF\n"
    "2. 312 160th Ave NE, Bellevue WA — $3,500,000 — 5 bed/4.25 bath/4,400 SF\n"
    "3. 218 109th Avenue SE, Bellevue WA — $4,500,000 — 5 bed/4.25 bath/4,400 SF\n"
    "4. 1224 108th Ave SE, Bellevue WA — $6,450,000 — 6 bed/7.5 bath/6,713 SF\n"
    "5. 1071 102nd Place SE, Bellevue WA — $4,200,000 — 5 bed/5 bath/5,920 SF\n"
    "6. 1305 North 50th Street, Seattle WA — $2,400,000 — 4 bed/3.5 bath/3,120 SF\n"
    "7. 4920 Stone Ave N, Seattle WA — $2,200,000 — 3 bed/3.5 bath/2,690 SF\n\n"
    "== SERVICES ==\n"
    "Custom Homes, Room Additions, Kitchen & Bath Remodels, Full Renovations.\n\n"
    "== GUIDED PROPERTY TOURS ==\n"
    "Every listing has a scripted, cinematic Guided Tour player available in two modes:\n"
    "  • SHORT pitch (~60 sec, 3 scenes) — quick overview.\n"
    "  • FULL tour  (~4 min, 8 scenes)  — architecture, interior, signature rooms,\n"
    "    outdoor, neighborhood, schools, parks.\n"
    "When a client asks about a SPECIFIC property by address/number/id, OFFER:\n"
    "  'Would you like me to give you a quick 60-second tour, or the full guided tour?'\n"
    "When the client AGREES (says yes / show me / tell me more / walk me through / give me the tour),\n"
    "IMMEDIATELY call the tool `open_property_tour(property_id, mode)`.\n"
    "The tour player will open full-screen with cinematic photos/video + neighborhood map.\n"
    "Then the player will send you each scene's narration text as a system message starting\n"
    "with 'TOUR NARRATION MODE' — read it verbatim, unhurried, like a luxury concierge.\n"
    "Do NOT add intros, comments, or 'as you can see' — just the scene text. The UI advances\n"
    "automatically when you finish each scene.\n"
)

CHAT_SYSTEM_PROMPT = (
    BASE_INSTRUCTIONS +
    "\n== YOUR TASKS ==\n\n"
    "CRITICAL RULE: After EVERY single reply you MUST append TWO special blocks (hidden from display):\n\n"
    "BLOCK 1 — always include, with ALL accumulated values filled in (never reset to null once filled):\n"
    "<F>{\"name\":null,\"email\":null,\"phone\":null,\"budget\":null,\"area\":null,\"style\":null,\"timeline\":null,\"broker\":null,\"done\":false}</F>\n\n"
    "BLOCK 2 — include ONLY when a meeting is FULLY confirmed (property + date + time + client email all agreed):\n"
    "<MEETING>{\"property\":\"address\",\"date\":\"YYYY-MM-DD\",\"time\":\"HH:MM\",\"duration\":60,\"clientName\":\"Name\",\"clientEmail\":\"email\",\"notes\":\"\"}</MEETING>\n\n"
    "IMPORTANT: In the <F> block, carry forward ALL previously collected values — never lose information between turns. "
    "Set done=true only when name+email+phone+budget are all filled.\n\n"
    "CONVERSATION STYLE: Keep replies SHORT (2-3 sentences). Be warm and professional. "
    "Naturally collect: Name, Email, Phone, Budget, Area, Home Style, Timeline, Broker. "
    "Never ask more than 2 questions at once. "
    "BOOKING ALGORITHM (strict order): "
    "(1) Collect NAME, PHONE, EMAIL (read the email back to confirm). "
    "(2) Agree on property + day + time for each tour the client wants. "
    "(3) If the client wants SEVERAL tours on different days/times, gather them all. "
    "(4) FINAL VERIFICATION (mandatory): once name + (email or phone) are known and every day/time is agreed, "
    "say 'Let's verify the schedule once more —' and read back EVERY appointment (property, day, date, time) "
    "plus the client's email, then ask 'Is everything correct?'. If they correct anything, update and repeat step 4. "
    "(5) Only AFTER a clear positive answer to the final verification do you include the <MEETING> block and tell "
    "them the invite(s) + confirmation email are on the way. "
    "Append one <MEETING> block per confirmed tour (multiple blocks allowed for multiple tours)."
)

VOICE_INSTRUCTIONS = (
    BASE_INSTRUCTIONS +
    "When the conversation starts, introduce yourself: say your name is Alexandra, that you are an AI real estate consultant at Bellshire Homes, and ask how you can help today. "
    "CRITICAL: Always respond in the SAME language the user speaks. If they switch to Ukrainian — respond in Ukrainian. "
    "Keep all voice responses short — 1 to 3 sentences maximum. "
    "\n\n== BOOKING ALGORITHM (follow this order strictly) ==\n"
    "STEP 1 — Collect the client's NAME, then PHONE, then EMAIL (one or two at a time, never all at once). "
    "Always read the email back to confirm you heard it correctly before moving on.\n"
    "STEP 2 — Agree on the property, the DAY and the TIME for each tour the client wants.\n"
    "STEP 3 — MULTIPLE TOURS: if the client wants to see several properties on different days or times, "
    "gather every one of them (property + day + time) before finalizing.\n"
    "STEP 4 — FINAL VERIFICATION (mandatory): once name + (email or phone) are known AND every day/time is agreed, "
    "say: 'Let's verify the schedule once more —' then read back EVERY appointment "
    "(property, day, date, time) AND the client's email, and ask 'Is everything correct?'. "
    "If the client corrects anything (email, name, a date, a time), update it and repeat STEP 4 with the corrected details.\n"
    "STEP 5 — Only AFTER the client gives a clear positive answer to the final verification "
    "('yes', 'correct', 'that's right', 'confirm') do you confirm the booking and tell them the calendar "
    "invite(s) and confirmation email are on the way.\n"
    "Never confirm a booking before STEP 5."
)


from pydantic import BaseModel
from typing import List, Dict, Any

class SessionRequest(BaseModel):
    voice: str = ""


class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage] = []


@app.post("/session")
async def create_session(body: SessionRequest = SessionRequest()):
    """Returns an ephemeral token for the browser to connect directly via WebRTC (GA API)."""
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")

    voice = body.voice or VOICE
    instructions = VOICE_INSTRUCTIONS

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            "https://api.openai.com/v1/realtime/client_secrets",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "session": {
                    "type": "realtime",
                    "model": "gpt-realtime",
                    "instructions": instructions,
                    "audio": {
                        "input": {
                            "turn_detection": {
                                "type": "semantic_vad",
                                "interrupt_response": True,
                            },
                            "transcription": {
                                "model": "whisper-1",
                            },
                        },
                        "output": {
                            "voice": voice,
                        },
                    },
                }
            },
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


@app.post("/sdp")
async def proxy_sdp(request: Request):
    """Proxy SDP offer to OpenAI WebRTC endpoint to avoid CORS issues."""
    auth_header = request.headers.get("Authorization", "")
    body = await request.body()

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.openai.com/v1/realtime/calls",
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/sdp",
            },
            content=body,
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type="application/sdp",
    )


GREET_PROMPT = (
    "You are Alexandra, a senior AI real estate consultant at Bellshire Homes — a luxury homebuilder in Bellevue, Washington. "
    "Introduce yourself warmly in 2-3 sentences: say your name, that you are an AI consultant at Bellshire Homes, "
    "and ask how you can help the visitor today. Be professional and welcoming. "
    "Then append: <F>{\"name\":null,\"email\":null,\"phone\":null,\"budget\":null,\"area\":null,\"style\":null,\"timeline\":null,\"broker\":null,\"done\":false}</F>"
)

@app.post("/chat")
async def chat(body: ChatRequest):
    """Chat endpoint — GPT-4o with full Bellshire system prompt."""
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")

    # Special greeting trigger — bot introduces itself without a user message
    if len(body.messages) == 1 and body.messages[0].content == "__GREET__":
        messages = [
            {"role": "system", "content": GREET_PROMPT},
            {"role": "user", "content": "start"}
        ]
    else:
        messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]
        for m in body.messages:
            messages.append({"role": m.role, "content": m.content})

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o",
                "max_tokens": 800,
                "messages": messages,
            },
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    text = data["choices"][0]["message"]["content"]
    return {"text": text}


def _get_analyze_prompt():
    today = _dt.date.today()
    weekday = today.strftime('%A')
    iso = today.isoformat()
    return (
    f"Today is {weekday}, {iso}. "
    "When resolving relative day names (Monday, Tuesday … Sunday): find the NEXT occurrence of that weekday AFTER today. "
    f"Example: if today is {weekday} {iso} and user says 'Friday', the date is the coming Friday. "
    "You are a data extraction assistant for Bellshire Homes real estate. "
    "You will receive TWO clearly labelled sections:\n\n"
    "=== SECTION A: CLIENT MESSAGES ONLY ===\n"
    "Use ONLY this section to extract client info fields. "
    "These are verbatim messages from the human client. "
    "Never add information from Section B into the fields.\n\n"
    "=== SECTION B: FULL CONVERSATION ===\n"
    "Use ONLY this section to detect meeting confirmations. "
    "Alexandra is the AI consultant — her lines are NOT client data.\n\n"
    "EXTRACT:\n"
    "1. CLIENT INFO (from SECTION A only): Extract what the CLIENT explicitly stated about themselves. "
    "Return null for anything not mentioned — never guess, never infer from Alexandra's lines.\n"
    "Fields: name, email, phone, budget (e.g. '$3M–$4M'), area (client's preferred neighborhood), "
    "style (Modern/Transitional/Traditional/Craftsman), timeline (e.g. '3–6 months'), broker (Yes/No).\n"
    "IMPORTANT — CORRECTIONS: This rule applies EQUALLY to EVERY field "
    "(name, email, phone, budget, area, style, timeline, broker), not just name. "
    "Scan the WHOLE conversation and for EACH field independently use the value from the "
    "LATEST message that mentions it; a later value MUST replace an earlier one. Examples: "
    "'Vyacheslav' then later 'Viacheslav' → name = 'Viacheslav'. "
    "'area 23-108th Street' then later '1224 108th Ave SE' → area = '1224 108th Ave SE'. "
    "Treat ANY later mention of a previously-stated field as a correction — never keep the stale value.\n\n"
    "2. MEETINGS (from SECTION B only): Extract an ARRAY of one or more confirmed meetings. "
    "Return meetings ONLY if ALL FIVE are true:\n"
    "   a) The client's NAME is already known (from CLIENT INFO section A)\n"
    "   b) The client's EMAIL or PHONE is already known (from CLIENT INFO section A)\n"
    "   c) For EACH tour, a specific date AND time were agreed\n"
    "   d) Alexandra performed a FINAL VERIFICATION — she read the full schedule back "
    "      ('Let's verify the schedule once more …') listing every appointment + the email\n"
    "   e) The client gave a clear AFFIRMATIVE answer to that final verification "
    "      ('yes', 'correct', 'that's right', 'confirm', 'perfect')\n"
    "   If ANY of (a)(b)(c)(d)(e) is missing → meetings MUST be an empty array [].\n"
    "   A client merely SUGGESTING a time, or confirming BEFORE the final verification recap, does NOT count.\n"
    "   IMPORTANT: If the client CORRECTS a date/time/email/name, use the CORRECTED value.\n\n"
    "   MULTIPLE TOURS: if the client agreed to several tours on different days/times, "
    "   output ONE object per tour in the array. If only one tour, output a single-element array.\n\n"
    "   Each meeting object has:\n"
    "   - property: address mentioned, or 'Bellshire Homes Property Tour' if none\n"
    "   - dayMentioned: the EXACT day word used, lowercase — one of "
    "'monday'..'sunday','today','tomorrow', OR an explicit ISO date 'YYYY-MM-DD'. Just echo it.\n"
    "   - date: best-guess YYYY-MM-DD (server recomputes from dayMentioned — fallback only)\n"
    "   - time: HH:MM 24h ('after 3pm' → '15:00', 'morning' → '10:00', default '10:00')\n"
    "   - duration: 60\n"
    "   - clientName, clientEmail: from collected client info\n"
    "   - notes: any extra details\n\n"
    "Return ONLY this exact JSON (no markdown, no explanation):\n"
    '{"fields":{"name":null,"email":null,"phone":null,"budget":null,"area":null,"style":null,"timeline":null,"broker":null,"done":false},'
    '"meetings":[]}'
    "\n\nSet fields.done=true only if name+email+phone+budget are ALL filled."
    )

ANALYZE_PROMPT = _get_analyze_prompt()

EXTRACT_PROMPT = (
    "You are a data extraction assistant. Below are messages written by the CLIENT (human user). "
    "Extract client information that was explicitly mentioned by the client. "
    "Return ONLY a valid JSON object (use null for anything not mentioned, never guess): "
    '{"name":null,"email":null,"phone":null,"budget":null,"area":null,"style":null,"timeline":null,"broker":null,"done":false} '
    "CORRECTIONS — IMPORTANT: This rule applies EQUALLY to EVERY field "
    "(name, email, phone, budget, area, style, timeline, broker), not just name. "
    "Scan the WHOLE conversation and for EACH field independently use the value from the "
    "LATEST message that mentions it. A later message correcting an earlier value MUST replace it. "
    "Examples: "
    "'My name is Vyacheslav' then later 'Viacheslav' → name = 'Viacheslav'. "
    "'area 23-108th Street' then later '1224 108th Ave SE' → area = '1224 108th Ave SE'. "
    "'budget 2 million' then later '3 to 4 million' → budget = '$3M–$4M'. "
    "Never keep an earlier value once the client has restated that field. "
    "Field rules: "
    "'name' = client's own name if the client stated it. "
    "'email' = email address if the client gave it. "
    "'phone' = phone number if the client gave it. "
    "'budget' = budget/price range if the client mentioned it (e.g. '$3M–$4M'). "
    "'area' = preferred area/neighborhood if the client mentioned it. "
    "'style' = home style (Modern/Transitional/Traditional/Craftsman) if the client mentioned it. "
    "'timeline' = timeline if the client mentioned it (e.g. '3–6 months'). "
    "'broker' = 'Yes' or 'No' if the client mentioned working with a broker. "
    "Set 'done' to true only if name, email, phone, and budget are ALL filled. "
    "Return ONLY the raw JSON object — no explanation, no markdown, no code blocks."
)


_WEEKDAYS = {
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
    "friday": 4, "saturday": 5, "sunday": 6,
}

def _resolve_meeting_date(day_mentioned, model_date):
    """Compute the real ISO date in Python (the LLM is unreliable at date math).

    - 'monday'..'sunday' → next occurrence AFTER today (never today/past)
    - 'today' / 'tomorrow' → relative to today
    - explicit 'YYYY-MM-DD' → used as-is if valid & not in the past
    - falls back to the model's date, but forces it into the future if the
      model picked a past year (e.g. its 2023 training bias).
    """
    today = _dt.date.today()

    def future_fix(d):
        # Push a past date forward to this year, then next year if still past.
        if d < today:
            try:
                d = d.replace(year=today.year)
            except ValueError:
                d = d.replace(year=today.year, day=28)
            if d < today:
                d = d.replace(year=today.year + 1)
        return d

    dm = (day_mentioned or "").strip().lower()

    # Explicit ISO date echoed by the model
    if len(dm) == 10 and dm[4] == "-" and dm[7] == "-":
        try:
            return future_fix(_dt.date.fromisoformat(dm)).isoformat()
        except Exception:
            pass

    if "today" in dm:
        return today.isoformat()
    if "tomorrow" in dm:
        return (today + _dt.timedelta(days=1)).isoformat()

    for name, idx in _WEEKDAYS.items():
        if name in dm:
            days_ahead = (idx - today.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7  # "Monday" said on a Monday → NEXT Monday
            return (today + _dt.timedelta(days=days_ahead)).isoformat()

    # Fallback: trust the model's date but never let it be in the past
    if model_date:
        try:
            return future_fix(_dt.date.fromisoformat(str(model_date)[:10])).isoformat()
        except Exception:
            pass

    # Last resort: a week from today
    return (today + _dt.timedelta(days=7)).isoformat()


def _client_only_text(messages) -> str:
    """Return only the client/user messages as plain text for field extraction."""
    lines = [m.content for m in messages if m.role == "user"]
    return "\n".join(lines) if lines else "(no client messages yet)"


def _full_conv_text(messages) -> str:
    """Return the full conversation with speaker labels for meeting detection."""
    lines = []
    for m in messages:
        label = "Client" if m.role == "user" else "Alexandra"
        lines.append(f"{label}: {m.content}")
    return "\n".join(lines)


@app.post("/extract")
async def extract_fields(body: ChatRequest):
    """Extract form fields — uses CLIENT messages only to avoid AI data pollution."""
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")

    client_text = _client_only_text(body.messages)

    messages = [
        {"role": "system", "content": EXTRACT_PROMPT},
        {"role": "user", "content": f"Client messages:\n\n{client_text}\n\nReturn the JSON now:"}
    ]

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "max_tokens": 200,
                "temperature": 0,
                "messages": messages,
            },
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    text = response.json()["choices"][0]["message"]["content"].strip()
    try:
        import json as _json
        fields = _json.loads(text)
    except Exception:
        fields = {}
    return {"fields": fields}


@app.post("/analyze")
async def analyze_conversation(body: ChatRequest):
    """Extract form fields (client-only) AND meeting data (full conversation)."""
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")

    # Section A: client messages only → for field extraction (no AI data pollution)
    section_a = _client_only_text(body.messages)
    # Section B: full conversation → for meeting detection (needs Alexandra's confirmations)
    section_b = _full_conv_text(body.messages)

    user_content = (
        f"=== SECTION A: CLIENT MESSAGES ONLY ===\n{section_a}\n\n"
        f"=== SECTION B: FULL CONVERSATION ===\n{section_b}\n\n"
        "Return the JSON extraction now:"
    )

    # Regenerate prompt each request so today's date is always current
    messages = [
        {"role": "system", "content": _get_analyze_prompt()},
        {"role": "user", "content": user_content}
    ]

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "max_tokens": 300,
                "temperature": 0,
                "messages": messages,
            },
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    text = response.json()["choices"][0]["message"]["content"].strip()
    try:
        data = _json.loads(text)
    except Exception:
        data = {"fields": {}, "meeting": None}

    # ── Server-side safeguard + normalisation of the meetings array ──
    fields = data.get("fields") or {}

    # Accept both the new `meetings` array and a legacy single `meeting`.
    raw_meetings = data.get("meetings")
    if raw_meetings is None:
        single = data.get("meeting")
        raw_meetings = [single] if single else []
    if not isinstance(raw_meetings, list):
        raw_meetings = [raw_meetings] if raw_meetings else []

    has_name  = bool((fields.get("name")  or "").strip())
    has_email = bool((fields.get("email") or "").strip())
    has_phone = bool((fields.get("phone") or "").strip())

    clean_meetings = []
    if has_name and (has_email or has_phone):
        for m in raw_meetings:
            if not isinstance(m, dict):
                continue
            # Date computed in Python (LLM unreliable at weekday→date + year bias)
            m["date"] = _resolve_meeting_date(m.get("dayMentioned"), m.get("date"))
            # Normalise time to HH:MM
            t = str(m.get("time") or "10:00").strip()
            m["time"] = t[:5] if (len(t) >= 5 and t[2] == ":") else "10:00"
            m.pop("dayMentioned", None)
            m.setdefault("duration", 60)
            m.setdefault("property", "Bellshire Homes Property Tour")
            # Always sync identity from the authoritative corrected fields
            if (fields.get("email") or "").strip():
                m["clientEmail"] = fields["email"].strip()
            if (fields.get("name") or "").strip():
                m["clientName"] = fields["name"].strip()
            clean_meetings.append(m)

    data["meetings"] = clean_meetings
    # Backward-compat: keep `meeting` = first one (or null) for older frontend code
    data["meeting"] = clean_meetings[0] if clean_meetings else None

    return data


@app.get("/health")
async def health():
    return {"status": "ok"}


# ── Property Guided Tour ──────────────────────────────────────────────────────
from properties_tour import get_tour, PROPERTIES

@app.get("/property/{property_id}/tour")
async def property_tour(property_id: str, mode: str = "tour"):
    """Return the scripted presentation for a property.

    mode='pitch'  → short hook + 3 hero scenes (~45-60 sec read).
    mode='tour'   → full 8-scene guided experience (~3-5 min).

    Frontend renders one scene at a time, syncing media + map with the text
    (voice mode reads each scene aloud; chat mode displays as bubbles).
    """
    if mode not in ("pitch", "tour"):
        raise HTTPException(status_code=400, detail="mode must be 'pitch' or 'tour'")
    data = get_tour(property_id, mode)
    if not data:
        raise HTTPException(status_code=404, detail=f"No tour for property {property_id}")
    return data

@app.get("/property")
async def property_list():
    """Lightweight directory so the frontend (and the AI) can discover
    which properties have a tour available."""
    return {
        "properties": [
            {"id": pid, "address": p["address"], "city": p["city"],
             "neighborhood": p["neighborhood"], "status": p["specs"]["status"]}
            for pid, p in PROPERTIES.items()
        ]
    }


# ── Conversation Storage ──────────────────────────────────────────────────────

from typing import Optional, Any

class SaveRequest(BaseModel):
    session_id: str
    source: str = "chat"          # "chat" | "voice"
    messages: list = []
    fields: dict = {}
    meeting: Optional[dict] = None
    consent: bool = False

@app.post("/conversation/save")
async def save_conversation(body: SaveRequest, request: Request):
    """Upsert a conversation session — called after every exchange and on modal close."""
    now = _dt.datetime.utcnow().isoformat()
    ip  = request.client.host if request.client else None

    conn = _db()
    existing = conn.execute("SELECT id FROM conversations WHERE id = ?", (body.session_id,)).fetchone()

    if existing:
        conn.execute(
            "UPDATE conversations SET updated_at=?, source=?, messages=?, fields=?, meeting=? WHERE id=?",
            (now,
             body.source,
             _json.dumps(body.messages, ensure_ascii=False),
             _json.dumps(body.fields,   ensure_ascii=False),
             _json.dumps(body.meeting,  ensure_ascii=False) if body.meeting else None,
             body.session_id)
        )
    else:
        conn.execute(
            "INSERT INTO conversations (id, started_at, updated_at, source, messages, fields, meeting, ip_address, consent) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (body.session_id, now, now, body.source,
             _json.dumps(body.messages, ensure_ascii=False),
             _json.dumps(body.fields,   ensure_ascii=False),
             _json.dumps(body.meeting,  ensure_ascii=False) if body.meeting else None,
             ip, 1 if body.consent else 0)
        )

    conn.commit()
    conn.close()
    return {"status": "saved"}


# ── Admin Panel ───────────────────────────────────────────────────────────────

@app.get("/admin/conversations", response_class=HTMLResponse)
async def admin_conversations(token: str = "", request: Request = None):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

    conn  = _db()
    rows  = conn.execute(
        "SELECT id, started_at, updated_at, source, fields, meeting, consent, ip_address "
        "FROM conversations ORDER BY started_at DESC LIMIT 200"
    ).fetchall()
    conn.close()

    cards = ""
    for r in rows:
        f   = _json.loads(r["fields"]) if r["fields"] else {}
        m   = _json.loads(r["meeting"]) if r["meeting"] else None
        src = "🎙 Voice" if r["source"] == "voice" else "💬 Chat"
        name    = f.get("name")    or "—"
        email   = f.get("email")   or "—"
        phone   = f.get("phone")   or "—"
        budget  = f.get("budget")  or "—"
        area    = f.get("area")    or "—"
        style   = f.get("style")   or "—"
        timeline= f.get("timeline")or "—"
        broker  = f.get("broker")  or "—"
        consent = "✅ Yes" if r["consent"] else "⚠️ No"
        mt = ""
        if m:
            mt = (f'<div class="mtag">📅 Meeting: {m.get("date","?")} {m.get("time","?")} — '
                  f'{m.get("property","?")}</div>')
        cards += f"""
        <div class="card">
          <div class="card-head">
            <span class="src">{src}</span>
            <span class="dt">{r["started_at"][:16].replace("T"," ")} UTC</span>
            <span class="sid">{r["id"][:8]}…</span>
            <span class="ip">{r["ip_address"] or "—"}</span>
          </div>
          <div class="fields">
            <span><b>Name:</b> {name}</span>
            <span><b>Email:</b> {email}</span>
            <span><b>Phone:</b> {phone}</span>
            <span><b>Budget:</b> {budget}</span>
            <span><b>Area:</b> {area}</span>
            <span><b>Style:</b> {style}</span>
            <span><b>Timeline:</b> {timeline}</span>
            <span><b>Broker:</b> {broker}</span>
            <span><b>Consent:</b> {consent}</span>
          </div>
          {mt}
          <div class="detail-link">
            <a href="/admin/conversation/{r["id"]}?token={token}">View full transcript →</a>
          </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><title>Bellshire Homes — Conversations</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:'Segoe UI',sans-serif;background:#f4f4f6;color:#222;padding:24px}}
    h1{{font-size:1.4rem;margin-bottom:4px;color:#1a2e2b}}
    .sub{{font-size:.8rem;color:#888;margin-bottom:20px}}
    .card{{background:#fff;border-radius:10px;padding:16px 20px;margin-bottom:12px;
           box-shadow:0 1px 4px rgba(0,0,0,.08);border-left:4px solid #4a9e95}}
    .card-head{{display:flex;gap:12px;align-items:center;margin-bottom:10px;flex-wrap:wrap}}
    .src{{font-size:.75rem;font-weight:700;color:#4a9e95}}
    .dt{{font-size:.72rem;color:#888}}
    .sid{{font-size:.65rem;color:#bbb;font-family:monospace}}
    .ip{{font-size:.65rem;color:#bbb}}
    .fields{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:6px 14px;
             font-size:.78rem;color:#444;margin-bottom:8px}}
    .fields b{{color:#222}}
    .mtag{{margin-top:8px;font-size:.78rem;background:#e8f5f4;color:#2d7a73;
            padding:5px 10px;border-radius:6px;display:inline-block}}
    .detail-link{{margin-top:10px;font-size:.75rem}}
    .detail-link a{{color:#4a9e95;text-decoration:none}}
    .detail-link a:hover{{text-decoration:underline}}
    .total{{font-size:.78rem;color:#666;margin-bottom:16px}}
  </style>
</head>
<body>
  <h1>Bellshire Homes · Client Conversations</h1>
  <p class="sub">Stored in accordance with applicable data protection law. Access restricted.</p>
  <p class="total">Total records: {len(rows)}</p>
  {cards if cards else '<p style="color:#888">No conversations yet.</p>'}
</body>
</html>"""


@app.get("/admin/conversation/{session_id}", response_class=HTMLResponse)
async def admin_conversation_detail(session_id: str, token: str = ""):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

    conn = _db()
    row  = conn.execute("SELECT * FROM conversations WHERE id = ?", (session_id,)).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Not found")

    msgs    = _json.loads(row["messages"]) if row["messages"] else []
    fields  = _json.loads(row["fields"])   if row["fields"]   else {}
    meeting = _json.loads(row["meeting"])  if row["meeting"]  else None

    bubbles = ""
    for msg in msgs:
        role  = msg.get("role", "user")
        text  = msg.get("content", "")
        # Strip internal <F> and <MEETING> tags for display
        text  = text.replace("<F>", "").replace("</F>", "").replace("<MEETING>", "").replace("</MEETING>", "").strip()
        if not text:
            continue
        align = "right" if role == "user" else "left"
        bg    = "#4a9e95" if role == "user" else "#f0f0f0"
        col   = "#fff"    if role == "user" else "#222"
        lbl   = "Client"  if role == "user" else "Alexandra"
        bubbles += f"""
        <div style="display:flex;justify-content:{align};margin-bottom:10px">
          <div style="max-width:72%;background:{bg};color:{col};padding:9px 13px;
               border-radius:12px;font-size:.82rem;line-height:1.5">
            <div style="font-size:.6rem;opacity:.6;margin-bottom:3px;text-transform:uppercase;
                 letter-spacing:.1em">{lbl}</div>
            {text}
          </div>
        </div>"""

    meeting_html = ""
    if meeting:
        meeting_html = f"""
        <div style="background:#e8f5f4;border-radius:8px;padding:12px 16px;margin-top:16px;font-size:.82rem">
          <b>📅 Scheduled Meeting</b><br>
          Property: {meeting.get("property","—")}<br>
          Date: {meeting.get("date","—")} · Time: {meeting.get("time","—")}<br>
          Client: {meeting.get("clientName","—")} · {meeting.get("clientEmail","—")}
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><title>Conversation {session_id[:8]}</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:'Segoe UI',sans-serif;background:#f4f4f6;color:#222;padding:24px;max-width:760px;margin:0 auto}}
    h1{{font-size:1.2rem;margin-bottom:4px;color:#1a2e2b}}
    .meta{{font-size:.74rem;color:#888;margin-bottom:20px}}
    .back{{font-size:.78rem;color:#4a9e95;text-decoration:none;display:block;margin-bottom:14px}}
    .back:hover{{text-decoration:underline}}
    .chat{{background:#fff;border-radius:10px;padding:16px;box-shadow:0 1px 4px rgba(0,0,0,.08)}}
  </style>
</head>
<body>
  <a class="back" href="/admin/conversations?token={token}">← Back to all conversations</a>
  <h1>Conversation {session_id[:8]}…</h1>
  <div class="meta">
    {row["started_at"][:16].replace("T"," ")} UTC ·
    Source: {row["source"]} ·
    IP: {row["ip_address"] or "—"} ·
    Consent: {"Yes" if row["consent"] else "No"}
  </div>
  <div class="chat">
    {bubbles if bubbles else "<p style='color:#888;font-size:.82rem'>No messages.</p>"}
  </div>
  {meeting_html}
</body>
</html>"""
