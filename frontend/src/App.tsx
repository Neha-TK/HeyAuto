import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import RideBooking from './pages/RideBooking';
import RideHistory from './pages/RideHistory';
import DriverDashboard from './components/Driver/DriverDashboard';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" />} />
        <Route path="/login" element={<Login/>} />
        <Route path="/register" element={<Register/>} />
        <Route path="/dashboard" element={<Dashboard/>} />
        <Route path="/book" element={<RideBooking/>} />
        <Route path="/history" element={<RideHistory/>} />
        <Route path="/driver" element={<DriverDashboard/>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
