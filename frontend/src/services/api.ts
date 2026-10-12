import { PlanResponse, Destination } from '../types/travel';

const API_BASE = '/api';

export async function planTrip(prompt: string): Promise<PlanResponse> {
  try {
    const response = await fetch(`${API_BASE}/plan`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || `Server responded with status ${response.status}`);
    }

    const data: PlanResponse = await response.json();
    return data;
  } catch (err: any) {
    console.error('API Error planTrip:', err);
    throw new Error(
      err.message || 'Could not communicate with the backend server. Please verify backend is running on http://localhost:8000.'
    );
  }
}

export async function fetchDestinations(): Promise<Destination[]> {
  try {
    const res = await fetch(`${API_BASE}/destinations`);
    if (!res.ok) return [];
    return await res.json();
  } catch (err) {
    console.error('Failed to fetch destinations:', err);
    return [];
  }
}

export async function fetchHealth(): Promise<any> {
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}
