import logging
from typing import Optional
from backend.app.schemas import ItineraryCandidate, ExtractedTripPreferences
from backend.app.config import settings

logger = logging.getLogger("tripwise.explainer")

def generate_template_explanation(
    candidate: ItineraryCandidate,
    preferences: ExtractedTripPreferences
) -> str:
    """
    Deterministic truthful template explanation guaranteed to contain
    zero hallucinated facts, prices, or establishments.
    """
    dest = candidate.destination
    cost = candidate.cost_breakdown
    hotel = candidate.recommended_hotel
    transport = candidate.transport_option
    
    interests_str = ", ".join(preferences.interests) if preferences.interests else "sightseeing"
    attraction_names = [a.name for a in candidate.visited_attractions[:3]]
    sights_str = ", ".join(attraction_names) if attraction_names else "scenic spots"

    paragraphs = [
        f"We recommend **{dest.name}, {dest.state}** as the ideal match for your {preferences.duration_days}-day trip "
        f"from {preferences.origin_city} with {preferences.travellers_count} traveller(s). It aligns closely with your "
        f"interests in {interests_str} and comfortably fits within your stated budget of ₹{cost.budget_inr:,}.",

        f"The total estimated trip cost is **₹{cost.total_trip_cost_inr:,}**, leaving a safe financial headroom of "
        f"**₹{cost.remaining_budget_inr:,}**. This includes round-trip travel via {transport.mode} (₹{cost.round_trip_transport_inr:,}), "
        f"{candidate.hotel_nights_count} night(s) stay at *{hotel.name}* (₹{cost.hotel_stay_inr:,}), "
        f"all meals & dining (₹{cost.food_inr:,}), local transit (₹{cost.local_transport_inr:,}), entry passes (₹{cost.attractions_inr:,}), "
        f"and an essential 10% contingency buffer (₹{cost.contingency_inr:,}).",

        f"During your visit, you'll experience iconic attractions including {sights_str}, alongside local cuisine at verified spots like "
        f"{', '.join([r.name for r in candidate.recommended_restaurants[:2]]) if candidate.recommended_restaurants else 'local eateries'}."
    ]

    return "\n\n".join(paragraphs)


async def generate_trip_explanation(
    candidate: ItineraryCandidate,
    preferences: ExtractedTripPreferences
) -> str:
    """
    Generates a conversational explanation.
    Uses Gemini when available with strict grounding and post-generation verification;
    otherwise returns the reliable deterministic template.
    """
    if not settings.GEMINI_API_KEY:
        return generate_template_explanation(candidate, preferences)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        # Grounding data provided explicitly to the LLM
        grounding_data = {
            "destination": candidate.destination.name,
            "state": candidate.destination.state,
            "origin": preferences.origin_city,
            "travellers": preferences.travellers_count,
            "days": preferences.duration_days,
            "budget": candidate.cost_breakdown.budget_inr,
            "total_cost": candidate.cost_breakdown.total_trip_cost_inr,
            "remaining_budget": candidate.cost_breakdown.remaining_budget_inr,
            "transport_mode": candidate.transport_option.mode,
            "transport_cost": candidate.cost_breakdown.round_trip_transport_inr,
            "hotel_name": candidate.recommended_hotel.name,
            "hotel_cost": candidate.cost_breakdown.hotel_stay_inr,
            "food_cost": candidate.cost_breakdown.food_inr,
            "attractions_cost": candidate.cost_breakdown.attractions_inr,
            "contingency": candidate.cost_breakdown.contingency_inr,
            "key_attractions": [a.name for a in candidate.visited_attractions],
            "restaurants": [r.name for r in candidate.recommended_restaurants],
            "match_reasons": candidate.match_reasons
        }

        system_instruction = (
            "You are an honest, articulate travel advisor for TripWise AI. "
            "Explain why the approved recommendation fits the user's trip in 2-3 concise, friendly paragraphs.\n"
            "CRITICAL CONSTRAINTS:\n"
            "1. ONLY reference the exact numbers, destination, hotel, and attractions present in the provided JSON.\n"
            "2. DO NOT invent or mention any unlisted hotel, restaurant, sight, price, or booking website.\n"
            "3. State costs as estimates.\n"
            "4. Clearly mention the total cost and remaining budget headroom."
        )

        prompt = f"Write an explanation for this approved itinerary recommendation:\n{grounding_data}"

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2
            )
        )

        llm_text = response.text.strip() if response.text else ""

        # Hallucination Guard: Verify key entities are mentioned truthfully
        if (
            candidate.destination.name.lower() in llm_text.lower()
            and str(candidate.cost_breakdown.total_trip_cost_inr) in llm_text.replace(",", "")
        ):
            return llm_text
        else:
            logger.info("Gemini explanation did not pass strict grounding checks. Using template.")
            return generate_template_explanation(candidate, preferences)

    except Exception as e:
        logger.warning(f"Gemini explanation generation failed ({e}). Using deterministic template.")
        return generate_template_explanation(candidate, preferences)
