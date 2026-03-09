import { Routes, Route, Link, useLocation } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Stakeholders from './pages/Stakeholders'
import StakeholderDetail from './pages/StakeholderDetail'
import Companies from './pages/Companies'
import Campaigns from './pages/Campaigns'
import Outreach from './pages/Outreach'
import Import from './pages/Import'
import Presentations from './pages/Presentations'

const navItems = [
  { path: '/', label: 'Dashboard' },
  { path: '/stakeholders', label: 'Stakeholders' },
  { path: '/companies', label: 'Companies' },
  { path: '/campaigns', label: 'Campaigns' },
  { path: '/outreach', label: 'Outreach' },
  { path: '/import', label: 'Import' },
  { path: '/presentations', label: 'Presentations' },
]

function App() {
  const location = useLocation()

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <h1 className="text-xl font-bold text-blue-900">
                SAP Sales Outreach Engine
              </h1>
            </div>
            <nav className="flex space-x-1">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    location.pathname === item.path
                      ? 'bg-blue-100 text-blue-800'
                      : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  }`}
                >
                  {item.label}
                </Link>
              ))}
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/stakeholders" element={<Stakeholders />} />
          <Route path="/stakeholders/:id" element={<StakeholderDetail />} />
          <Route path="/companies" element={<Companies />} />
          <Route path="/campaigns" element={<Campaigns />} />
          <Route path="/outreach" element={<Outreach />} />
          <Route path="/import" element={<Import />} />
          <Route path="/presentations" element={<Presentations />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
