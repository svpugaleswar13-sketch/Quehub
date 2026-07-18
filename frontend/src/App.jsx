import { Route, Routes } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'

import Landing from './pages/Landing.jsx'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'

import CustomerDashboard from './pages/customer/Dashboard.jsx'
import DomainOrganizations from './pages/customer/DomainOrganizations.jsx'
import OrganizationPage from './pages/customer/OrganizationPage.jsx'
import ServiceDetails from './pages/customer/ServiceDetails.jsx'
import BookingSuccess from './pages/customer/BookingSuccess.jsx'
import LiveQueue from './pages/customer/LiveQueue.jsx'
import BookingHistory from './pages/customer/BookingHistory.jsx'

import OrganizationDashboard from './pages/organization/Dashboard.jsx'
import QueueManagement from './pages/organization/QueueManagement.jsx'
import WalkInBooking from './pages/organization/WalkInBooking.jsx'
import ManageServices from './pages/organization/ManageServices.jsx'
import Reports from './pages/organization/Reports.jsx'

export default function App() {
  return (
    <div className="min-h-screen bg-bg">
      <Navbar />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Customer */}
        <Route path="/dashboard" element={<ProtectedRoute role="customer"><CustomerDashboard /></ProtectedRoute>} />
        <Route path="/domains/:domain" element={<ProtectedRoute role="customer"><DomainOrganizations /></ProtectedRoute>} />
        <Route path="/organizations/:organizationId" element={<ProtectedRoute role="customer"><OrganizationPage /></ProtectedRoute>} />
        <Route path="/services/:serviceId" element={<ProtectedRoute role="customer"><ServiceDetails /></ProtectedRoute>} />
        <Route path="/booking-success" element={<ProtectedRoute role="customer"><BookingSuccess /></ProtectedRoute>} />
        <Route path="/live-queue/:serviceId" element={<ProtectedRoute role="customer"><LiveQueue /></ProtectedRoute>} />
        <Route path="/bookings" element={<ProtectedRoute role="customer"><BookingHistory /></ProtectedRoute>} />

        {/* Organization */}
        <Route path="/org/dashboard" element={<ProtectedRoute role="organization"><OrganizationDashboard /></ProtectedRoute>} />
        <Route path="/org/queue/:serviceId" element={<ProtectedRoute role="organization"><QueueManagement /></ProtectedRoute>} />
        <Route path="/org/walk-in" element={<ProtectedRoute role="organization"><WalkInBooking /></ProtectedRoute>} />
        <Route path="/org/services" element={<ProtectedRoute role="organization"><ManageServices /></ProtectedRoute>} />
        <Route path="/org/reports" element={<ProtectedRoute role="organization"><Reports /></ProtectedRoute>} />
      </Routes>
    </div>
  )
}
