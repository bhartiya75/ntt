import { useEffect, useState } from 'react'
import { getStats } from '../services/api'

interface Stats {
  total_stakeholders: number
  total_companies: number
  total_campaigns: number
  active_campaigns: number
  total_messages: number
  messages_sent: number
  replies_received: number
}

function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null)

  useEffect(() => {
    getStats().then((res) => setStats(res.data)).catch(() => {})
  }, [])

  const cards = stats
    ? [
        { label: 'Total Stakeholders', value: stats.total_stakeholders, color: 'blue' },
        { label: 'Companies', value: stats.total_companies, color: 'indigo' },
        { label: 'Active Campaigns', value: stats.active_campaigns, color: 'green' },
        { label: 'Messages Generated', value: stats.total_messages, color: 'purple' },
        { label: 'Messages Sent', value: stats.messages_sent, color: 'orange' },
        { label: 'Replies Received', value: stats.replies_received, color: 'emerald' },
      ]
    : []

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h2>

      {stats ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {cards.map((card) => (
            <div
              key={card.label}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
            >
              <p className="text-sm font-medium text-gray-500">{card.label}</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {card.value}
              </p>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Welcome to SAP Sales Outreach Engine
          </h3>
          <p className="text-gray-500 mb-6">
            Get started by importing your LinkedIn contacts or adding stakeholders manually.
          </p>
          <div className="space-y-3 text-left max-w-lg mx-auto">
            <div className="flex items-start space-x-3">
              <span className="text-blue-600 font-bold">1.</span>
              <p className="text-gray-700">
                <strong>Import</strong> — Upload your LinkedIn CSV export or Sales Navigator list
              </p>
            </div>
            <div className="flex items-start space-x-3">
              <span className="text-blue-600 font-bold">2.</span>
              <p className="text-gray-700">
                <strong>Profile</strong> — Run AI analysis on stakeholders to understand their needs
              </p>
            </div>
            <div className="flex items-start space-x-3">
              <span className="text-blue-600 font-bold">3.</span>
              <p className="text-gray-700">
                <strong>Campaign</strong> — Create 1-to-1 or 1-to-many outreach campaigns
              </p>
            </div>
            <div className="flex items-start space-x-3">
              <span className="text-blue-600 font-bold">4.</span>
              <p className="text-gray-700">
                <strong>Outreach</strong> — Generate personalized messages with AI and send
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard
