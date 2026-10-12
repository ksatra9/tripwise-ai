# TripWise AI — Personalized Travel Itinerary Recommendation System

A full-stack, budget-honest travel recommendation platform focused on travel within India. The system takes **one natural language trip request** through a single free-text input box, extracts validated preferences via Google Gemini (with an autonomous deterministic regex/NLP fallback), enforces a **strict mathematical affordability filter**, and generates a transparent, day-by-day itinerary with verified local establishments and itemized costs.

---

## Key Highlights & Product Rules

1. **Hard Affordability Filter**: The total estimated trip cost never exceeds the user's stated total budget. Candidates exceeding budget are strictly rejected before ranking.
2. **True Full-Trip Cost Math**: Costs are calculated in pure integer INR for the **entire trip** and **all travellers combined**, including round-trip transit, hotel rooms ($\lceil\text{travellers} / 2\rceil \times \text{nights}$), meals ($3\times\text{travellers}\times\text{days}$), attraction entry tickets, local transfers, and a mandatory **10% emergency contingency reserve**.
3. **Zero Hallucinated Rates or Establishments**: Python code—not the LLM—performs all arithmetic, affordability filtering, and scoring. The LLM is strictly constrained to approved database entities with an autonomous grounded validation guard.
4. **Honest Data Attribution**: Every price record displays its `data_status` (`demo`, `historical`, `verified_snapshot`, or `live_quote`), price unit, and checked date. Sample seed records are visibly tagged: `"Demo data — illustrative estimates, not verified listings or bookable prices."`
5. **Targeted Clarification**: If essential information (origin, budget, duration, or party size) is missing or budget scope is ambiguous (per person vs total), the system asks **exactly ONE targeted question** instead of guessing.
6. **Graceful No-Trip-Found View**: When no option fits an impossible budget, constructive adjustments (minimum required budget, reduced duration, or nearer hubs) are suggested.

---

## Directory Structure

```
RS MINI/
├── backend/
│   ├── app/
│   │   ├── config.py                 # App settings, GEMINI_MODEL, database & CORS config
│   │   ├── database.py               # SQLAlchemy SQLite engine & sessionmaker
│   │   ├── models.py                 # DB models: Destination, TransportRoute, Hotel, Restaurant, Attraction
│   │   ├── schemas.py                # Pydantic schemas: preferences, cost breakdowns, daily plans, candidates
│   │   ├── services/
│   │   │   ├── extractor.py          # Gemini structured extractor + deterministic NLP regex/rule fallback
│   │   │   ├── cost_calculator.py    # Strict integer INR math, room capacity ceiling, 10% contingency
│   │   │   ├── recommendation_engine.py # Hard budget cutoff + multi-factor scoring
│   │   │   ├── itinerary_builder.py  # Builds day-by-day plan strictly from real DB records
│   │   │   ├── explainer.py          # Gemini conversational summary with strict grounding validation
│   │   │   └── data_importer.py      # Kaggle dataset inspector & importer for real CSV/JSON data
│   │   ├── routers/
│   │   │   ├── plan.py               # POST /api/plan
│   │   │   └── destinations.py       # GET /api/destinations, GET /api/destinations/{id}
│   │   ├── main.py                   # FastAPI app, CORS middleware, lifespan startup & seed trigger
│   │   └── seed_data.py              # 5 rich destinations (Rishikesh, Jaipur, Agra, Goa, Kochi) with verified routes
│   ├── tests/
│   │   ├── conftest.py               # In-memory SQLite with StaticPool & TestClient fixtures
│   │   ├── test_extraction.py        # Example prompt, missing budget, ambiguous scope, LLM fallback
│   │   ├── test_cost_calculator.py   # Group transit, room ceiling, multi-night stay, 10% contingency
│   │   ├── test_recommendation.py    # Exactly-at-budget acceptance, over-budget rejection, route lookup
│   │   └── test_api.py               # End-to-end API plan, clarification flow, prevention of invented records
│   ├── requirements.txt
│   ├── .env.example
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── types/travel.ts           # TypeScript interfaces matching backend models
│   │   ├── services/api.ts           # Fetch client for /api/plan and /api/destinations
│   │   ├── components/
│   │   │   ├── Navbar.tsx            # Brand header ("TripWise AI") with reset and live status
│   │   │   ├── HeroSearch.tsx        # Single free-text box, sample prompts, keyboard shortcuts
│   │   │   ├── ClarificationCard.tsx # Single targeted question card with quick action pills
│   │   │   ├── CostBreakdownCard.tsx # Transparent itemized cost table, 10% contingency, room math
│   │   │   ├── HotelCard.tsx         # Hotel details with rate per room, rooms needed, total stay cost
│   │   │   ├── RestaurantList.tsx    # Curated meal recommendations with location & price band
│   │   │   ├── DayByDayPlan.tsx      # Day-by-day itinerary grouped logically by area
│   │   │   ├── AlternativesList.tsx  # Alternative affordable candidate cards
│   │   │   ├── NoTripFound.tsx       # Graceful "no affordable trip" view with adjustment suggestions
│   │   │   ├── DataDisclaimerBadge.tsx # Prominent estimate disclaimer & source metadata
│   │   │   └── LoadingState.tsx      # Multi-step calculation radar & progress indicator
│   │   ├── App.tsx                   # Master page state coordinator
│   │   ├── main.tsx
│   │   ├── index.css                 # Tailwind directives and warm travel aesthetic design system
│   │   └── tests/
│   │       ├── App.test.tsx          # Frontend tests for submission, loading, clarification, success, errors
│   │       └── setupTests.ts
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── tsconfig.json
├── import_kaggle_data.py             # Standalone CLI script to inspect and import Kaggle datasets
├── README.md
└── run_demo.bat                      # Windows one-click launcher
```

---

## Mathematical Budget Formula

All cost math is executed deterministically in integer INR:

$$\text{Nights} = \max(1, \text{Days} - 1)$$

$$\text{Rooms Needed} = \left\lceil \frac{\text{Travellers}}{2} \right\rceil$$

1. **Round-Trip Transport**: $\text{Rate per Person} \times \text{Travellers}$
2. **Hotel Accommodation**: $\text{Nightly Room Rate} \times \text{Nights} \times \text{Rooms Needed}$
3. **Food & Dining**: $\text{Avg Meal Cost} \times 3\text{ meals} \times \text{Travellers} \times \text{Days}$
4. **Sightseeing Tickets**: $\sum (\text{Attraction Entry Fee}) \times \text{Travellers}$
5. **Local Transfers**: $\text{Daily Group Commute Rate (₹700)} \times \text{Days}$
6. **Subtotal**: $\sum (\text{Transport} + \text{Hotel} + \text{Food} + \text{Attractions} + \text{Local Commute})$
7. **Emergency Contingency**: $\lceil \text{Subtotal} \times 0.10 \rceil$ ($10\%$ safety buffer)
8. **Total Trip Cost**: $\text{Subtotal} + \text{Contingency}$

$$\text{Hard Filter}: \quad \text{Total Trip Cost} \le \text{User Stated Budget}$$

---

## Recommendation & Scoring Algorithm

Affordable candidates are ranked using an interpretable composite score $[0, 100]$:
- **Interest Match (35%)**: Jaccard overlap between requested interests (nature, food, culture, adventure, spiritual, beach) and destination/attraction categories.
- **Budget Headroom & Value (20%)**: Rewards trips that leave a comfortable financial buffer (5% to 40% unspent cushion) without leaving excessive funds unused.
- **Season Suitability (15%)**: Match between destination's `best_seasons` and visiting window.
- **Travel Convenience (15%)**: Shorter transit time from origin city.
- **Itinerary Variety & Popularity (15%)**: Diversity and rating of available sights.

Every response exposes the exact `score_breakdown` for auditing and transparency.

---

## Setup & Run Commands

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm

### 1. Backend Setup

```bash
# Navigate to project root
cd "RS MINI"

# Install backend dependencies
pip install -r backend/requirements.txt

# (Optional) Set your Gemini API key in backend/.env
# If omitted, the system seamlessly runs on its deterministic local parser!
copy backend\.env.example backend\.env
```

Start the backend server:
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
The backend starts at `http://localhost:8000`. Swagger documentation is available at `http://localhost:8000/docs`.

### 2. Frontend Setup

In a separate terminal:
```bash
cd "RS MINI/frontend"

# Install dependencies (already prepared)
npm install

# Start Vite development server
npm run dev
```
Open `http://localhost:5173` in your browser.

### 3. Optional: Inspect & Import Full Kaggle Datasets

To inspect the included Kaggle dataset files and import all 100 destinations into SQLite:
```bash
python import_kaggle_data.py
```

---

## Running Automated Tests

### Backend Tests (24 pytest tests)
```bash
python -m pytest backend/tests
```
Verifies:
- Extracting trip details from example prompt
- Missing budget clarification
- Ambiguous budget scope clarification
- Room capacity ceiling division
- Multiple-night hotel stay math
- Group transport scaling
- Mandatory 10% contingency calculation
- Exactly-at-budget acceptance
- Over-budget hard rejection
- Unsupported origin handling
- Prevention of invented records in recommendations
- LLM failure fallback to local parser

### Frontend Tests (5 Vitest tests)
```bash
cd frontend
npm run test
```
Verifies:
- Text submission & input interaction
- Loading state radar
- Clarification question rendering
- Successful itinerary & cost breakdown rendering
- Network error handling

---

## Example API Request and Response

### Request
`POST /api/plan`
```json
{
  "prompt": "I am travelling from Delhi with one friend for 3 days. Our total budget is ₹20,000. We like nature and local food."
}
```

### Response
```json
{
  "status": "success",
  "clarification_question": null,
  "extracted_preferences": {
    "origin_city": "Delhi",
    "total_budget_inr": 20000,
    "is_budget_ambiguous_or_per_person": false,
    "duration_days": 3,
    "travellers_count": 2,
    "interests": ["nature", "food"],
    "is_complete": true
  },
  "recommended_trip": {
    "destination": {
      "id": 1,
      "name": "Rishikesh",
      "state": "Uttarakhand",
      "region": "North India",
      "category": "Nature;Spirituality;Adventure;Food",
      "best_seasons": "Autumn, Winter, Spring (Sep-Apr)",
      "ideal_days": 3,
      "popularity_score": 9.2,
      "safety_rating": 8.8,
      "description": "Yoga capital of the world on the banks of the sacred Ganges in the Himalayan foothills.",
      "data_status": "historical"
    },
    "cost_breakdown": {
      "round_trip_transport_inr": 2900,
      "hotel_stay_inr": 3700,
      "food_inr": 4860,
      "attractions_inr": 400,
      "local_transport_inr": 2100,
      "subtotal_inr": 13960,
      "contingency_inr": 1396,
      "total_trip_cost_inr": 15356,
      "budget_inr": 20000,
      "remaining_budget_inr": 4644,
      "is_within_budget": true,
      "items": [
        {
          "category": "Round-Trip Transport",
          "unit_cost_inr": 1450,
          "units": 2,
          "multiplier_description": "2 traveller(s) × ₹1,450 round-trip (Jan Shatabdi / Vande Bharat Express)",
          "total_inr": 2900,
          "price_unit": "per_person_round_trip",
          "data_status": "demo",
          "verification_note": "Demo / schedule estimate. Not a live reservation quote."
        },
        {
          "category": "Hotel Accommodation",
          "unit_cost_inr": 1850,
          "units": 2,
          "multiplier_description": "1 room(s) × 2 night(s) × ₹1,850/night (Ganga Nature Riverside Retreat [Sample Stay])",
          "total_inr": 3700,
          "price_unit": "per_room_per_night",
          "data_status": "demo",
          "verification_note": "Illustrative / cleaned dataset estimate. Confirm with property directly."
        },
        {
          "category": "Emergency Contingency Reserve (10%)",
          "unit_cost_inr": 1396,
          "units": 1,
          "multiplier_description": "Mandatory 10% safety buffer for unplanned delays or surge pricing",
          "total_inr": 1396,
          "price_unit": "total_reserve",
          "data_status": "verified_snapshot",
          "verification_note": "Financial safety margin calculated mathematically."
        }
      ]
    },
    "recommended_hotel": {
      "id": 1,
      "destination_id": 1,
      "name": "Ganga Nature Riverside Retreat [Sample Stay]",
      "city": "Rishikesh",
      "stars": "3-star equivalent",
      "rating": 4.4,
      "amenities": "River view, Free Wi-Fi, Mountain deck, Pure veg cafe",
      "amount_inr": 1850,
      "is_sample_entry": true
    },
    "score": 88.5,
    "score_breakdown": {
      "interest_match": 100.0,
      "season_suitability": 90.0,
      "budget_headroom": 95.0,
      "travel_convenience": 85.0,
      "itinerary_variety": 80.0
    },
    "match_reasons": [
      "Strong match for your interest in Nature, Food",
      "Saves ₹4,644 in contingency buffer (23% unspent)",
      "Fast Jan Shatabdi / Vande Bharat Express connection (~4.5 hrs from Delhi)"
    ]
  },
  "alternatives": [],
  "ai_explanation": "We recommend Rishikesh, Uttarakhand as the ideal match for your 3-day trip from Delhi with 2 travellers. The total estimated trip cost is ₹15,356, leaving a safe financial headroom of ₹4,644 within your ₹20,000 budget.",
  "disclaimer": "Estimated prices; confirm before booking. All hotel, restaurant, and transport rates are sample or historical estimates, not live verified bookable quotes."
}
```
