import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models import PlanningRequestLog
from backend.app.schemas import TripQuery, PlanResponse
from backend.app.services.extractor import extract_preferences
from backend.app.services.recommendation_engine import find_recommendations
from backend.app.services.explainer import generate_trip_explanation

logger = logging.getLogger("tripwise.plan")
router = APIRouter(prefix="/api", tags=["Trip Planning"])

@router.post("/plan", response_model=PlanResponse)
async def plan_trip(query: TripQuery, db: Session = Depends(get_db)):
    """
    Main endpoint: takes a single free-text travel query, extracts validated preferences,
    filters affordable destinations strictly in Python, builds day-by-day itineraries
    from real database entities, and returns transparent cost breakdowns.
    """
    raw_prompt = query.prompt.strip()
    if not raw_prompt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trip description cannot be empty."
        )

    logger.info(f"Received trip planning prompt: {raw_prompt}")

    # 1. Structured text extraction (Gemini with deterministic fallback)
    preferences = await extract_preferences(raw_prompt)

    # 2. Check for missing essential information
    if not preferences.is_complete:
        # Log planning request diagnostic
        log_entry = PlanningRequestLog(
            prompt=raw_prompt,
            origin_city=preferences.origin_city,
            budget_inr=preferences.total_budget_inr,
            days=preferences.duration_days,
            travellers=preferences.travellers_count,
            status="clarification_required"
        )
        db.add(log_entry)
        db.commit()

        return PlanResponse(
            status="clarification_needed",
            clarification_question=preferences.follow_up_question or "Could you clarify the starting city and total budget for your trip?",
            extracted_preferences=preferences,
            recommended_trip=None,
            alternatives=[],
            ai_explanation=None,
            budget_adjustment_suggestions=[]
        )

    # 3. Recommendation engine (hard affordability filter + interpretable scoring)
    recommended, alternatives, adjustment_suggestions, diagnostics = find_recommendations(
        db, preferences, return_diagnostics=True
    )

    # 4. Handle no affordable options or missing routes
    if not recommended:
        log_entry = PlanningRequestLog(
            prompt=raw_prompt,
            origin_city=preferences.origin_city,
            budget_inr=preferences.total_budget_inr,
            days=preferences.duration_days,
            travellers=preferences.travellers_count,
            status="no_affordable_options"
        )
        db.add(log_entry)
        db.commit()

        return PlanResponse(
            status="no_affordable_options",
            clarification_question=None,
            extracted_preferences=preferences,
            recommended_trip=None,
            alternatives=[],
            ai_explanation=None,
            budget_adjustment_suggestions=adjustment_suggestions,
            diagnostics=diagnostics
        )

    # 5. Conversational Explanation grounded strictly in approved data
    ai_explanation = await generate_trip_explanation(recommended, preferences)

    # 6. Log success
    log_entry = PlanningRequestLog(
        prompt=raw_prompt,
        origin_city=preferences.origin_city,
        budget_inr=preferences.total_budget_inr,
        days=preferences.duration_days,
        travellers=preferences.travellers_count,
        status="processed",
        recommended_destination=recommended.destination.name
    )
    db.add(log_entry)
    db.commit()

    return PlanResponse(
        status="success",
        clarification_question=None,
        extracted_preferences=preferences,
        recommended_trip=recommended,
        alternatives=alternatives,
        ai_explanation=ai_explanation,
        budget_adjustment_suggestions=adjustment_suggestions,
        diagnostics=diagnostics
    )
