import re
import json
import logging
from typing import Optional, List, Dict, Any, Tuple
from backend.app.schemas import ExtractedTripPreferences
from backend.app.config import settings

logger = logging.getLogger("tripwise.extractor")

KNOWN_ORIGIN_CITIES = [
    "delhi", "new delhi", "mumbai", "bangalore", "bengaluru", "chennai", "kolkata",
    "hyderabad", "pune", "ahmedabad", "jaipur", "lucknow", "kochi", "cochin",
    "chandigarh", "bhopal", "patna", "indore", "surat", "nagpur", "guwahati",
    "trivandrum", "thiruvananthapuram", "varanasi", "dehradun", "amritsar", "goa"
]

KNOWN_DESTINATIONS = {
    "rishikesh": "Rishikesh",
    "jaipur": "Jaipur",
    "agra": "Agra",
    "goa": "Goa",
    "kochi": "Kochi",
    "cochin": "Kochi",
    "manali": "Manali",
    "shimla": "Shimla",
    "udaipur": "Udaipur",
    "varanasi": "Varanasi (Kashi)",
    "kashi": "Varanasi (Kashi)",
    "banaras": "Varanasi (Kashi)",
    "amritsar": "Amritsar",
    "ladakh": "Ladakh (Leh)",
    "leh": "Ladakh (Leh)",
    "ooty": "Ooty (Udhagamandalam)",
    "munnar": "Munnar",
    "gokarna": "Gokarna",
    "hampi": "Hampi",
    "darjeeling": "Darjeeling",
    "gangtok": "Gangtok & East Sikkim",
    "pondicherry": "Pondicherry (Puducherry)",
    "puducherry": "Pondicherry (Puducherry)",
    "haridwar": "Haridwar",
    "coorg": "Coorg (Kodagu)",
    "kodagu": "Coorg (Kodagu)",
    "spiti": "Spiti Valley",
    "spiti valley": "Spiti Valley",
    "jaisalmer": "Jaisalmer (Thar Desert & Fort Town)",
    "kerala": "Kerala Backwaters (Alappuzha & Kumarakom)",
    "alleppey": "Kerala Backwaters (Alappuzha & Kumarakom)",
    "alappuzha": "Kerala Backwaters (Alappuzha & Kumarakom)",
    "dharamshala": "Dharamshala & McLeod Ganj",
    "mcleodganj": "Dharamshala & McLeod Ganj",
    "mcleod ganj": "Dharamshala & McLeod Ganj",
    "wayanad": "Wayanad",
    "shillong": "Shillong",
    "cherrapunji": "Cherrapunji & Mawsmai Area (Sohra region)",
    "mussoorie": "Mussoorie",
    "nainital": "Nainital",
    "mahabaleshwar": "Mahabaleshwar & Panchgani",
    "kanyakumari": "Kanyakumari",
    "chikmagalur": "Chikmagalur",
    "khajuraho": "Khajuraho & Panna National Park",
}

INTEREST_KEYWORDS = {
    "nature": ["nature", "wildlife", "scenic", "greenery", "hills", "mountain", "mountains", "forest", "valley", "lake", "falls", "waterfall"],
    "food": ["food", "cuisine", "local food", "culinary", "dishes", "eating", "street food", "dining", "gastronomy", "seafood"],
    "adventure": ["adventure", "trekking", "hiking", "rafting", "camping", "sports", "scuba", "paragliding", "safari"],
    "culture": ["culture", "cultural", "heritage", "history", "historical", "palace", "fort", "forts", "museum", "tradition", "architecture"],
    "spirituality": ["spiritual", "temple", "temples", "ghats", "yoga", "meditation", "ashram", "holy", "pilgrimage", "peaceful", "peace", "religious"],
    "beach": ["beach", "beaches", "coastal", "sea", "ocean", "sand", "coasts"],
    "nightlife": ["nightlife", "party", "parties", "clubs", "pubs", "shacks", "music"]
}

def parse_deterministic(text: str) -> ExtractedTripPreferences:
    """
    Deterministic rule-based NLP extraction for Indian travel queries.
    Reliable local parser when Gemini API is unavailable or unconfigured.
    """
    text_clean = text.strip()
    text_lower = text_clean.lower()

    # 0. Check Clarification tags in text (e.g. "(Clarification: manali)")
    preferred_destination: Optional[str] = None
    origin_city: Optional[str] = None

    clarifications = re.findall(r'\(clarification:\s*([^)]+)\)', text_lower)
    for clar in clarifications:
        clar = clar.strip()
        for d_key, d_val in KNOWN_DESTINATIONS.items():
            if re.search(r'\b' + re.escape(d_key) + r'\b', clar):
                preferred_destination = d_val
                break
        for c in KNOWN_ORIGIN_CITIES:
            if re.search(r'\b' + re.escape(c) + r'\b', clar):
                origin_city = c.title()
                if origin_city.lower() in ["new delhi", "delhi"]:
                    origin_city = "Delhi"
                elif origin_city.lower() in ["bengaluru", "bangalore"]:
                    origin_city = "Bangalore"
                elif origin_city.lower() in ["cochin", "kochi"]:
                    origin_city = "Kochi"
                break

    # 1. Extract Preferred Destination (if not yet clarified)
    if not preferred_destination:
        dest_patterns = [
            r'(?:to|visit|visiting|trip to|travel to|heading to|head to|holiday in|vacation in|explore|destination(?:\s+is|:)?)\s+([a-zA-Z\s]+?)(?:\s+from|\s+with|\s+for|\s+on|\s+and|\.|\,|$|\))',
            r'in\s+([a-zA-Z\s]+?)(?:\s+from|\s+with|\s+for|\s+on|\s+and|\.|\,|$|\))'
        ]
        for pattern in dest_patterns:
            match = re.search(pattern, text_lower)
            if match:
                candidate = match.group(1).strip()
                for d_key, d_val in KNOWN_DESTINATIONS.items():
                    if re.search(r'\b' + re.escape(d_key) + r'\b', candidate):
                        preferred_destination = d_val
                        break
                if preferred_destination:
                    break

    if not preferred_destination:
        # Fallback scan for known destination keywords not preceded by 'from'
        for d_key, d_val in KNOWN_DESTINATIONS.items():
            from_preceded = re.search(r'from\s+[a-zA-Z\s]*\b' + re.escape(d_key) + r'\b', text_lower)
            if not from_preceded and re.search(r'\b' + re.escape(d_key) + r'\b', text_lower):
                preferred_destination = d_val
                break

    # 2. Extract Origin City
    if not origin_city:
        origin_patterns = [
            r'(?:travel(?:l)?ing|travelling|leaving|starting|departing|coming|flying from|heading out from)\s+(?:from\s+)?([a-zA-Z\s]+?)(?:\s+with|\s+for|\s+to|\s+on|\s+and|\.|\,|$|\))',
            r'from\s+([a-zA-Z\s]+?)(?:\s+to|\s+with|\s+for|\s+on|\s+and|\.|\,|$|\))',
            r'origin(?:\s+is|:)?\s*([a-zA-Z\s]+?)(?:\s+to|\s+with|\s+for|\s+on|\s+and|\.|\,|$|\))'
        ]
        for pattern in origin_patterns:
            match = re.search(pattern, text_lower)
            if match:
                candidate = match.group(1).strip()
                for city in KNOWN_ORIGIN_CITIES:
                    if re.search(r'\b' + re.escape(city) + r'\b', candidate):
                        origin_city = city.title()
                        if origin_city.lower() in ["new delhi", "delhi"]:
                            origin_city = "Delhi"
                        elif origin_city.lower() in ["bengaluru", "bangalore"]:
                            origin_city = "Bangalore"
                        elif origin_city.lower() in ["cochin", "kochi"]:
                            origin_city = "Kochi"
                        break
                if origin_city:
                    break
    
    if not origin_city:
        for city in KNOWN_ORIGIN_CITIES:
            # Check standalone word boundaries, but do not match if it is the target destination
            if preferred_destination and city.lower() in preferred_destination.lower():
                continue
            if re.search(r'(?:to|visit)\s+' + re.escape(city) + r'\b', text_lower):
                continue
            if re.search(r'\b' + re.escape(city) + r'\b', text_lower):
                origin_city = city.title()
                if origin_city.lower() in ["new delhi", "delhi"]:
                    origin_city = "Delhi"
                elif origin_city.lower() in ["bengaluru", "bangalore"]:
                    origin_city = "Bangalore"
                break


    # 2. Extract Travellers Count
    travellers_count: Optional[int] = None
    with_friends_match = re.search(r'with\s+(\d+|two|three|four|five|one|a)\s+friends?', text_lower)
    num_word_map = {"one": 1, "a": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    if with_friends_match:
        n_val = with_friends_match.group(1)
        count = num_word_map.get(n_val, int(n_val) if n_val.isdigit() else 1)
        travellers_count = count + 1
    elif re.search(r'\b(solo|alone|by myself|just me)\b', text_lower):
        travellers_count = 1
    elif re.search(r'\bwith\s+my\s+(?:wife|husband|partner|spouse)\b|\bcouple\b|\bme\s+and\s+my\s+(?:friend|wife|husband|partner)\b', text_lower):
        travellers_count = 2
    else:
        # Match general numbers of people
        pax_match = re.search(r'(\d+)\s*(?:people|travellers|travelers|pax|persons|adults|members|of us)', text_lower)
        if pax_match:
            travellers_count = int(pax_match.group(1))
        else:
            family_match = re.search(r'family\s+of\s+(\d+)', text_lower)
            if family_match:
                travellers_count = int(family_match.group(1))

    # 3. Extract Duration Days
    duration_days: Optional[int] = None
    days_match = re.search(r'(\d+)\s*(?:day|days|d\b)', text_lower)
    if days_match:
        duration_days = int(days_match.group(1))
    else:
        nights_match = re.search(r'(\d+)\s*(?:night|nights|n\b)', text_lower)
        if nights_match:
            duration_days = int(nights_match.group(1)) + 1
        elif re.search(r'\bweekend\b', text_lower):
            duration_days = 2
        elif re.search(r'\blong\s+weekend\b', text_lower):
            duration_days = 3
        elif re.search(r'\ba\s+week\b|\bone\s+week\b', text_lower):
            duration_days = 7

    # 4. Extract Budget in INR & Check Scope
    total_budget_inr: Optional[int] = None
    is_budget_ambiguous_or_per_person = False

    # Regex for currency figures: ₹20,000, Rs. 20000, 20k, 20,000, 20000 INR
    budget_match = re.search(r'(?:₹|rs\.?|inr)?\s*(\d{1,3}(?:,\d{3})+|\d+)\s*(?:k|thousand)?\s*(?:rs|inr|rupees)?', text_lower)
    
    # More specific search around budget keyword
    budget_kw_match = re.search(r'(?:budget|cost|spend|limit|approx|around|under|max)?\s*(?:of|is|:)?\s*(?:₹|rs\.?|inr)?\s*(\d{1,3}(?:,\d{3})+|\d+)\s*(k|thousand)?\s*(?:rs|inr|rupees)?', text_lower)

    # Let's find all numbers with currency or 'k' or 'budget'
    budget_candidates = re.findall(r'(?:₹|rs\.?|inr|\b)\s*(\d{1,3}(?:,\d{3})+|\d+)\s*(k|thousand)?\s*(?:rs|inr|rupees|\b)', text_lower)
    
    # Let's specifically isolate the budget number
    # e.g., "₹20,000" or "20k" or "budget is 20000"
    target_num_str = None
    is_k = False

    # Try explicit currency symbol first
    explicit_symbol = re.search(r'(?:₹|rs\.?|inr)\s*(\d{1,3}(?:,\d{3})+|\d+)\s*(k|thousand)?', text_lower)
    if explicit_symbol:
        target_num_str = explicit_symbol.group(1).replace(",", "")
        is_k = bool(explicit_symbol.group(2))
    elif "budget" in text_lower:
        kw_idx = text_lower.find("budget")
        substr = text_lower[kw_idx:kw_idx+40]
        num_m = re.search(r'(\d{1,3}(?:,\d{3})+|\d+)\s*(k|thousand)?', substr)
        if num_m:
            target_num_str = num_m.group(1).replace(",", "")
            is_k = bool(num_m.group(2))
    elif budget_kw_match:
        # Fallback to general number that isn't duration or traveller
        for match in re.finditer(r'(\d{1,3}(?:,\d{3})+|\d+)\s*(k|thousand)?', text_lower):
            val_str = match.group(1).replace(",", "")
            val_k = bool(match.group(2))
            val = int(val_str) * (1000 if val_k else 1)
            # Avoid picking traveller count or days count
            if val != travellers_count and val != duration_days and val >= 1000:
                target_num_str = val_str
                is_k = val_k
                break

    if target_num_str and target_num_str.isdigit():
        base_val = int(target_num_str)
        if is_k or (base_val < 500 and "k" in text_lower):
            total_budget_inr = base_val * 1000
        else:
            total_budget_inr = base_val

    # Check budget scope ambiguity
    if total_budget_inr is not None:
        if re.search(r'\b(per\s+person|per\s+head|each|per\s+traveller)\b', text_lower):
            # Stated per person
            if travellers_count and travellers_count > 1:
                total_budget_inr = total_budget_inr * travellers_count
            else:
                is_budget_ambiguous_or_per_person = True
        elif re.search(r'\b(total|our\s+total|all\s+together|overall|combined|in\s+total)\b', text_lower):
            # Explicitly total
            is_budget_ambiguous_or_per_person = False
        else:
            # If travellers count > 1 and neither 'per person' nor 'total' is stated, flag as ambiguous if budget looks small (< 8000 per person)
            # Or rule 8: "Never silently assume whether a stated budget is per person or total. Clarify ambiguous budget scope."
            if travellers_count and travellers_count > 1 and not re.search(r'\b(total|our\s+total|in\s+total)\b', text_lower):
                # Prompt rule: "If essential information is missing, ask ONE concise follow-up question instead of guessing."
                # Example: "Our total budget is ₹20,000" explicitly says "total".
                # If the user says "budget is 10000" with 2 people, we must clarify.
                is_budget_ambiguous_or_per_person = True

    # 5. Extract Interests
    detected_interests: List[str] = []
    for category, kws in INTEREST_KEYWORDS.items():
        for kw in kws:
            if kw in text_lower:
                if category not in detected_interests:
                    detected_interests.append(category)
                break

    # 6. Extract Accommodation Tier
    accommodation_tier: Optional[str] = None
    if re.search(r'\b(luxury|5-star|5 star|five star|resort|palace|grand|heritage palace|villas?)\b', text_lower):
        accommodation_tier = "Luxury"
    elif re.search(r'\b(budget|hostel|dorm|cheap|backpacker|affordable|homestay|guest\s*house)\b', text_lower):
        accommodation_tier = "Budget"
    elif re.search(r'\b(mid-range|mid range|3-star|4-star|comfort|boutique)\b', text_lower):
        accommodation_tier = "Mid-range"

    # 7. Extract Transport Preference
    transport_preference: Optional[str] = None
    if re.search(r'\b(flight|fly|flying|by air|plane|flights|air travel|airfare)\b', text_lower):
        transport_preference = "Flight"
    elif re.search(r'\b(train|rail|railway|vande bharat|shatabdi|rajdhani|express train)\b', text_lower):
        transport_preference = "Train"
    elif re.search(r'\b(bus|volvo|sleeper bus|road trip)\b', text_lower):
        transport_preference = "Bus"

    # 8. Check Completeness & Determine Single Targeted Clarification Question
    missing_field: Optional[str] = None
    follow_up_question: Optional[str] = None

    if not origin_city:
        missing_field = "origin_city"
        if preferred_destination:
            follow_up_question = f"Which city in India will you be travelling from to reach {preferred_destination}?"
        else:
            follow_up_question = "Which city in India will you be travelling from?"
    elif total_budget_inr is None:
        missing_field = "total_budget_inr"
        follow_up_question = "What is your total budget in INR for the entire trip?"
    elif is_budget_ambiguous_or_per_person:
        missing_field = "budget_scope"
        follow_up_question = f"Is your stated budget of ₹{total_budget_inr:,} the total budget for all travellers or per person?"
    elif not duration_days or duration_days <= 0:
        missing_field = "duration_days"
        follow_up_question = "How many days are you planning for this trip?"
    elif not travellers_count or travellers_count <= 0:
        missing_field = "travellers_count"
        follow_up_question = "How many travellers will be going on this trip?"

    is_complete = (missing_field is None)

    return ExtractedTripPreferences(
        origin_city=origin_city,
        total_budget_inr=total_budget_inr,
        is_budget_ambiguous_or_per_person=is_budget_ambiguous_or_per_person,
        duration_days=duration_days,
        travellers_count=travellers_count,
        interests=detected_interests,
        preferred_destination=preferred_destination,
        accommodation_tier=accommodation_tier,
        transport_preference=transport_preference,
        is_complete=is_complete,
        missing_field=missing_field,
        follow_up_question=follow_up_question
    )


async def extract_preferences(text: str) -> ExtractedTripPreferences:
    """
    Extract preferences using Google Gemini if GEMINI_API_KEY is available.
    Strictly falls back to deterministic rule-based extractor if absent or error occurs.
    """
    if not settings.GEMINI_API_KEY:
        logger.info("GEMINI_API_KEY not configured. Using deterministic extractor.")
        return parse_deterministic(text)

    try:
        # Attempt Gemini structured extraction
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        system_instruction = (
            "You are an expert NLP parser for an Indian travel itinerary recommendation system. "
            "Extract travel intent strictly into the specified JSON format. "
            "Rules:\n"
            "1. origin_city: Departure/starting city in India (e.g., Delhi, Mumbai, Bangalore). Do NOT confuse with destination.\n"
            "2. preferred_destination: Destination city or place user specifically wants to visit (e.g. Manali, Jaipur, Goa, Agra, Shimla, Udaipur, Varanasi). Set to null if user does not specify a destination and just wants suggestions.\n"
            "3. total_budget_inr: Total budget in integer INR for the entire trip and all travellers. If user says '20k', that is 20000. If stated 'per person' and travellers is known, calculate total. If ambiguous whether it is per person or total for 2+ travellers, set is_budget_ambiguous_or_per_person to true.\n"
            "4. duration_days: Number of trip days (integer). 'with one friend' means 2 travellers.\n"
            "5. travellers_count: Total travellers (integer). 'solo'=1, 'me and my wife'=2, 'with one friend'=2.\n"
            "6. interests: List of interests (nature, food, adventure, culture, spirituality, beach, nightlife).\n"
            "7. accommodation_tier: 'Budget', 'Mid-range', or 'Luxury' if specified or implied by keywords (resort, 5-star, etc.), else null.\n"
            "8. transport_preference: 'Flight', 'Train', 'Bus', or 'Any' if mentioned, else null.\n"
            "9. If origin, budget, duration, or travellers cannot be reliably found, set missing_field and provide ONE concise follow-up question. Do not guess or assume."
        )

        prompt = f"Extract trip details from this travel request: \"{text}\""
        
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=ExtractedTripPreferences,
                temperature=0.1
            )
        )

        if response.text:
            extracted = ExtractedTripPreferences.model_validate_json(response.text)
            # Sanity-check extracted output with deterministic checks
            det = parse_deterministic(text)
            if not extracted.preferred_destination and det.preferred_destination:
                extracted.preferred_destination = det.preferred_destination
            if not extracted.origin_city and det.origin_city:
                extracted.origin_city = det.origin_city
            if not extracted.total_budget_inr and det.total_budget_inr:
                extracted.total_budget_inr = det.total_budget_inr
            if not extracted.duration_days and det.duration_days:
                extracted.duration_days = det.duration_days
            if not extracted.travellers_count and det.travellers_count:
                extracted.travellers_count = det.travellers_count
            
            # Recheck completeness
            if not extracted.origin_city:
                extracted.missing_field = "origin_city"
                if extracted.preferred_destination:
                    extracted.follow_up_question = f"Which city in India will you be travelling from to reach {extracted.preferred_destination}?"
                else:
                    extracted.follow_up_question = "Which city in India will you be travelling from?"
                extracted.is_complete = False
            elif not extracted.total_budget_inr:
                extracted.missing_field = "total_budget_inr"
                extracted.follow_up_question = "What is your total budget in INR for the entire trip?"
                extracted.is_complete = False
            elif extracted.is_budget_ambiguous_or_per_person:
                extracted.missing_field = "budget_scope"
                extracted.follow_up_question = f"Is your stated budget of ₹{extracted.total_budget_inr:,} the total budget for all travellers or per person?"
                extracted.is_complete = False
            elif not extracted.duration_days or extracted.duration_days <= 0:
                extracted.missing_field = "duration_days"
                extracted.follow_up_question = "How many days are you planning for this trip?"
                extracted.is_complete = False
            elif not extracted.travellers_count or extracted.travellers_count <= 0:
                extracted.missing_field = "travellers_count"
                extracted.follow_up_question = "How many travellers will be going on this trip?"
                extracted.is_complete = False
            else:
                extracted.is_complete = True
                extracted.missing_field = None
                extracted.follow_up_question = None

            return extracted

    except Exception as e:
        logger.warning(f"Gemini extraction call failed ({e}). Falling back to deterministic extractor.")
    
    return parse_deterministic(text)
