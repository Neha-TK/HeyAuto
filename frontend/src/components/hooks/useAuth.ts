import { useState, useEffect } from 'react';
import api from '../api/api';
import type { User } from '../types';

export function useAuth() {
  const [user, setUser] = useState<User | null>(() => {
    const raw = localStorage.getItem('me');
    return raw ? JSON.parse(raw) : null;
  });

  useEffect(() => {
    if (user) localStorage.setItem('me', JSON.stringify(user));
    else localStorage.removeItem('me');
  }, [user]);

  const login = async (email: string, password: string) => {
    const resp = await api.post('/auth/login', { email, password });
    const token = resp.data.access_token;
    localStorage.setItem('access_token', token);
    // fetch profile
    const profile = (await api.get('/auth/me')).data;
    setUser(profile);
    return profile;
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('me');
    setUser(null);
  };

  const register = async (name: string, email: string, password: string) => {
    const resp = await api.post('/auth/register', { name, email, password });
    return resp.data;
  };

  return { user, setUser, login, logout, register };
}
