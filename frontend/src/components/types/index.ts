export type Role = 'user' | 'driver';

export interface User {
  id: string;
  email: string;
  name?: string;
  role?: Role;
}

export interface Driver {
  id: string;
  user_id: string;
  name: string;
  stand_id?: string | null;
  is_present: boolean;
  is_available: boolean;
  location?: { lat: number; lng: number };
}

export interface AutoStand {
  id: string;
  name: string;
  location: { lat: number; lng: number };
}

export interface Ride {
  id: string;
  user_id: string;
  driver_id?: string | null;
  origin: { lat: number; lng: number};
  destination: { lat: number; lng: number};
  status: 'requested'|'assigned'|'ongoing'|'completed'|'cancelled';
  created_at: string;
}

export interface QueueUpdate {
  stand_id: string;
  queue: string[]; // driver ids in order
}
