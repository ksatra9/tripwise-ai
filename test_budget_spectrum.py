import sys
import os
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add project root
_project_root = Path(".").resolve()
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from backend.app.database import SessionLocal
from backend.app.services.extractor import parse_deterministic
from backend.app.services.recommendation_engine import find_recommendations
from backend.app.models import Destination, TransportRoute, Hotel, Restaurant, Attraction

db = SessionLocal()

print("=" * 80)
print("TESTING RECOMMENDATION ENGINE WITH INCREASING BUDGETS")
print("=" * 80)

test_prompts = [
    "Trip from Delhi to Goa with 1 friend for 3 days. Total budget is ₹15,000.",
    "Trip from Delhi to Goa with 1 friend for 3 days. Total budget is ₹35,000.",
    "Trip from Delhi to Goa with 1 friend for 3 days. Total budget is ₹60,000.",
    "Trip from Delhi to Goa with 1 friend for 3 days. Total budget is ₹100,000.",
    "Trip from Delhi to Goa with 1 friend for 3 days. Total budget is ₹200,000.",
    "Trip from Delhi with 1 friend for 3 days. Total budget is ₹15,000. We want beaches and nightlife.",
    "Trip from Delhi with 1 friend for 3 days. Total budget is ₹50,000. We want beaches and nightlife.",
    "Trip from Delhi with 1 friend for 3 days. Total budget is ₹120,000. Luxury hotels and flight.",
]

for prompt in test_prompts:
    print(f"\n--- PROMPT: {prompt} ---")
    prefs = parse_deterministic(prompt)
    print(f"Extracted: Origin={prefs.origin_city}, Dest={prefs.preferred_destination}, Budget={prefs.total_budget_inr}, Days={prefs.duration_days}, Pax={prefs.travellers_count}, Complete={prefs.is_complete}")
    
    db = SessionLocal()
    rec, alts, suggestions = find_recommendations(db, prefs)
    if rec:
        print(f"  RECOMMENDED: {rec.destination.name}")
        print(f"    Transport: {rec.transport_option.mode} @ ₹{rec.transport_option.amount_inr} (total transport: ₹{rec.cost_breakdown.round_trip_transport_inr})")
        print(f"    Hotel: {rec.recommended_hotel.name} ({rec.recommended_hotel.stars}, {rec.recommended_hotel.tier}) @ ₹{rec.recommended_hotel.amount_inr}/night")
        print(f"    Total Cost: ₹{rec.cost_breakdown.total_trip_cost_inr:,} / Budget: ₹{rec.cost_breakdown.budget_inr:,} (Remaining: ₹{rec.cost_breakdown.remaining_budget_inr:,})")
        print(f"    Score: {rec.score} (breakdown: {rec.score_breakdown})")
        print(f"    Match reasons: {rec.match_reasons}")
    else:
        print(f"  NO RECOMMENDATION FOUND!")
        print(f"    Suggestions: {suggestions}")
    db.close()

db.close()
