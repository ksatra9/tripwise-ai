import pytest
from unittest.mock import patch
from backend.app.services.extractor import parse_deterministic, extract_preferences

def test_extract_example_input():
    prompt = "I am travelling from Delhi with one friend for 3 days. Our total budget is ₹20,000. We like nature and local food."
    extracted = parse_deterministic(prompt)

    assert extracted.origin_city == "Delhi"
    assert extracted.travellers_count == 2
    assert extracted.duration_days == 3
    assert extracted.total_budget_inr == 20000
    assert "nature" in extracted.interests
    assert "food" in extracted.interests
    assert extracted.is_complete is True
    assert extracted.missing_field is None
    assert extracted.follow_up_question is None

def test_missing_budget():
    prompt = "I am travelling from Delhi with one friend for 3 days. We like nature and local food."
    extracted = parse_deterministic(prompt)

    assert extracted.origin_city == "Delhi"
    assert extracted.travellers_count == 2
    assert extracted.duration_days == 3
    assert extracted.total_budget_inr is None
    assert extracted.is_complete is False
    assert extracted.missing_field == "total_budget_inr"
    assert "total budget" in extracted.follow_up_question.lower()

def test_ambiguous_budget_scope():
    # When budget is stated for group without explicitly saying 'total' or 'per person'
    prompt = "Travelling from Delhi with 2 friends for 4 days. Budget is 15000. We like culture."
    extracted = parse_deterministic(prompt)

    assert extracted.origin_city == "Delhi"
    assert extracted.travellers_count == 3
    assert extracted.duration_days == 4
    assert extracted.is_budget_ambiguous_or_per_person is True
    assert extracted.is_complete is False
    assert extracted.missing_field == "budget_scope"
    assert "per person" in extracted.follow_up_question.lower()

def test_missing_origin_city():
    prompt = "Trip with one friend for 3 days. Our total budget is ₹25,000. We like trekking."
    extracted = parse_deterministic(prompt)

    assert extracted.origin_city is None
    assert extracted.is_complete is False
    assert extracted.missing_field == "origin_city"
    assert "city" in extracted.follow_up_question.lower()

def test_missing_duration():
    prompt = "Travelling from Delhi with one friend. Our total budget is ₹20,000. We like beaches."
    extracted = parse_deterministic(prompt)

    assert extracted.duration_days is None
    assert extracted.is_complete is False
    assert extracted.missing_field == "duration_days"
    assert "how many days" in extracted.follow_up_question.lower()

def test_missing_travellers():
    prompt = "Travelling from Delhi for 4 days. Our total budget is ₹20,000. We like nature."
    extracted = parse_deterministic(prompt)

    assert extracted.travellers_count is None
    assert extracted.is_complete is False
    assert extracted.missing_field == "travellers_count"
    assert "how many travellers" in extracted.follow_up_question.lower()

@pytest.mark.asyncio
async def test_llm_failure_fallback():
    # Simulate Gemini API failure and assert fallback to deterministic parser
    prompt = "I am travelling from Delhi with one friend for 3 days. Our total budget is ₹20,000. We like nature and local food."
    
    with patch("backend.app.config.settings.GEMINI_API_KEY", "mock-key"):
        with patch("google.genai.Client", side_effect=Exception("API connection timeout")):
            extracted = await extract_preferences(prompt)
            assert extracted.origin_city == "Delhi"
            assert extracted.travellers_count == 2
            assert extracted.duration_days == 3
            assert extracted.total_budget_inr == 20000
            assert extracted.is_complete is True

def test_extract_preferred_destination():
    prompt = "I want to visit Jaipur from Delhi with 1 friend for 3 days. Total budget is 20000."
    extracted = parse_deterministic(prompt)
    assert extracted.origin_city == "Delhi"
    assert extracted.preferred_destination == "Jaipur"
    assert extracted.duration_days == 3
    assert extracted.travellers_count == 2
    assert extracted.total_budget_inr == 20000

def test_extract_destination_with_trip_to():
    prompt = "Trip to Manali from Delhi for 4 days with 2 travellers. Total budget ₹25,000."
    extracted = parse_deterministic(prompt)
    assert extracted.origin_city == "Delhi"
    assert extracted.preferred_destination == "Manali"
    assert extracted.duration_days == 4
    assert extracted.travellers_count == 2
    assert extracted.total_budget_inr == 25000
