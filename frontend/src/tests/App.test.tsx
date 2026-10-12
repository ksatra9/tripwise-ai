import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';
import * as api from '../services/api';
import { PlanResponse } from '../types/travel';

describe('TripWise AI Frontend Application', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders home screen with title and single free-text input box', () => {
    render(<App />);
    expect(screen.getByText('TripWise AI')).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/I am travelling from Delhi with one friend/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Plan My Trip/i })).toBeInTheDocument();
  });

  it('handles loading state during text submission', async () => {
    // Mock API to return a delayed promise
    vi.spyOn(api, 'planTrip').mockImplementation(
      () => new Promise((resolve) => setTimeout(() => resolve({
        status: 'success',
        recommended_trip: null,
        alternatives: [],
        budget_adjustment_suggestions: [],
        disclaimer: 'Sample'
      } as any), 500))
    );

    render(<App />);
    const submitBtn = screen.getByRole('button', { name: /Plan My Trip/i });
    fireEvent.click(submitBtn);

    // Assert loading state
    expect(screen.getByText(/Calculating Your Affordable Itinerary/i)).toBeInTheDocument();
  });

  it('renders clarification card when essential information is missing', async () => {
    const mockClarification: PlanResponse = {
      status: 'clarification_needed',
      clarification_question: 'Which city in India will you be travelling from?',
      extracted_preferences: {
        is_budget_ambiguous_or_per_person: false,
        interests: ['nature'],
        is_complete: false,
        missing_field: 'origin_city',
        follow_up_question: 'Which city in India will you be travelling from?'
      },
      recommended_trip: null,
      alternatives: [],
      budget_adjustment_suggestions: [],
      disclaimer: 'Disclaimed'
    };

    vi.spyOn(api, 'planTrip').mockResolvedValue(mockClarification);

    render(<App />);
    const submitBtn = screen.getByRole('button', { name: /Plan My Trip/i });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(screen.getByText(/One quick detail needed/i)).toBeInTheDocument();
      expect(screen.getByText('Which city in India will you be travelling from?')).toBeInTheDocument();
    });
  });

  it('renders successful itinerary result with transparent cost breakdown', async () => {
    const mockSuccess: PlanResponse = {
      status: 'success',
      extracted_preferences: {
        origin_city: 'Delhi',
        total_budget_inr: 20000,
        is_budget_ambiguous_or_per_person: false,
        duration_days: 3,
        travellers_count: 2,
        interests: ['nature', 'food'],
        is_complete: true
      },
      recommended_trip: {
        destination: {
          id: 1,
          name: 'Rishikesh',
          state: 'Uttarakhand',
          ideal_days: 3,
          minimum_days: 2,
          maximum_days: 5,
          popularity_score: 9.2,
          safety_rating: 8.8,
          description: 'Yoga capital by the Ganges.',
          data_status: 'historical'
        },
        cost_breakdown: {
          round_trip_transport_inr: 2900,
          hotel_stay_inr: 3700,
          food_inr: 3000,
          attractions_inr: 400,
          local_transport_inr: 2100,
          subtotal_inr: 12100,
          contingency_inr: 1210,
          total_trip_cost_inr: 13310,
          budget_inr: 20000,
          remaining_budget_inr: 6690,
          is_within_budget: true,
          items: [
            {
              category: 'Round-Trip Transport',
              unit_cost_inr: 1450,
              units: 2,
              multiplier_description: '2 pax x 1450',
              total_inr: 2900,
              price_unit: 'per_person_round_trip',
              data_status: 'demo',
              verification_note: 'Verified train'
            }
          ]
        },
        recommended_hotel: {
          id: 1,
          destination_id: 1,
          name: 'Ganga Riverside Retreat [Sample Stay]',
          city: 'Rishikesh',
          stars: '3-star',
          rating: 4.4,
          tier: 'Budget',
          amount_inr: 1850,
          price_unit: 'per_room_per_night',
          data_status: 'demo',
          is_sample_entry: true
        },
        hotel_rooms_count: 1,
        hotel_nights_count: 2,
        transport_option: {
          id: 1,
          origin_city: 'Delhi',
          destination_id: 1,
          mode: 'Vande Bharat Express',
          duration_hours: 4.5,
          amount_inr: 1450,
          price_unit: 'per_person_round_trip',
          data_status: 'demo'
        },
        recommended_restaurants: [],
        visited_attractions: [],
        daily_plans: [
          {
            day_number: 1,
            title: 'Day 1: Discovering Rishikesh',
            area_cluster: 'Triveni Ghat',
            morning: {
              time_of_day: 'Morning',
              activity_name: 'River Walk',
              category: 'Nature',
              entry_fee_inr: 0,
              est_duration_hours: 2
            },
            afternoon: {
              time_of_day: 'Afternoon',
              activity_name: 'Ashram visit',
              category: 'Culture',
              entry_fee_inr: 50,
              est_duration_hours: 2
            },
            evening: {
              time_of_day: 'Evening',
              activity_name: 'Ganga Aarti',
              category: 'Spirituality',
              entry_fee_inr: 0,
              est_duration_hours: 1.5
            },
            estimated_day_cost_inr: 600
          }
        ],
        score: 92.5,
        score_breakdown: { interest_match: 95.0, budget_headroom: 90.0 },
        match_reasons: ['Strong match for nature and local food']
      },
      alternatives: [],
      ai_explanation: 'We recommend Rishikesh as it fits within your budget.',
      budget_adjustment_suggestions: [],
      disclaimer: 'Estimated prices.'
    };

    vi.spyOn(api, 'planTrip').mockResolvedValue(mockSuccess);

    render(<App />);
    const submitBtn = screen.getByRole('button', { name: /Plan My Trip/i });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      // Must display destination
      expect(screen.getByText('Rishikesh')).toBeInTheDocument();
      // Must display hotel
      expect(screen.getByText('Ganga Riverside Retreat [Sample Stay]')).toBeInTheDocument();
      // Must display cost breakdown items
      expect(screen.getByText('Round-Trip Transport')).toBeInTheDocument();
    });
  });

  it('renders graceful error state when network or API fails', async () => {
    vi.spyOn(api, 'planTrip').mockRejectedValue(new Error('Backend connection refused.'));

    render(<App />);
    const submitBtn = screen.getByRole('button', { name: /Plan My Trip/i });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(screen.getByText(/Unable to Complete Request/i)).toBeInTheDocument();
      expect(screen.getByText(/Backend connection refused/i)).toBeInTheDocument();
    });
  });
});
