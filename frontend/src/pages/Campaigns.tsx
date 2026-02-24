import { useEffect, useState } from 'react'
import { getCampaigns, createCampaign } from '../services/api'

interface Campaign {
  id: number
  name: string
  description: string | null
  campaign_type: string
  channel: string
  status: string
  total_contacts: number
  messages_sent: number
  replies_received: number
  sap_solution_focus: string[]
  created_at: string
}

function Campaigns() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreate, setShowCreate] = useState(false)
  const [form, setForm] = useState({
    name: '',
    description: '',
    campaign_type: 'one_to_one',
    channel: 'linkedin_message',
    value_proposition: '',
  })

  useEffect(() => {
    getCampaigns({ limit: 50 })
      .then((res) => setCampaigns(res.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await createCampaign({ ...form, stakeholder_ids: [] })
      const res = await getCampaigns({ limit: 50 })
      setCampaigns(res.data)
      setShowCreate(false)
      setForm({ name: '', description: '', campaign_type: 'one_to_one', channel: 'linkedin_message', value_proposition: '' })
    } catch {
      alert('Failed to create campaign.')
    }
  }

  if (loading) return <p className="text-gray-500">Loading...</p>

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Campaigns</h2>
        <button
          onClick={() => setShowCreate(!showCreate)}
          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700"
        >
          New Campaign
        </button>
      </div>

      {showCreate && (
        <form
          onSubmit={handleCreate}
          className="bg-white rounded-lg border border-gray-200 p-6 mb-6 space-y-4"
        >
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Campaign Name
              </label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Type
              </label>
              <select
                value={form.campaign_type}
                onChange={(e) => setForm({ ...form, campaign_type: e.target.value })}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
              >
                <option value="one_to_one">1-to-1 (High Touch)</option>
                <option value="one_to_many">1-to-Many (Scaled)</option>
              </select>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
              rows={2}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Value Proposition
            </label>
            <textarea
              value={form.value_proposition}
              onChange={(e) => setForm({ ...form, value_proposition: e.target.value })}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
              rows={2}
              placeholder="What unique value are you offering to this segment?"
            />
          </div>
          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={() => setShowCreate(false)}
              className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700"
            >
              Create Campaign
            </button>
          </div>
        </form>
      )}

      {campaigns.length === 0 ? (
        <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
          <p className="text-gray-500">No campaigns yet. Create one to start outreach.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {campaigns.map((c) => (
            <div
              key={c.id}
              className="bg-white rounded-lg border border-gray-200 p-6"
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {c.name}
                  </h3>
                  {c.description && (
                    <p className="text-sm text-gray-500 mt-1">{c.description}</p>
                  )}
                  <div className="flex space-x-4 mt-2 text-sm">
                    <span
                      className={`px-2 py-0.5 rounded text-xs font-medium ${
                        c.status === 'active'
                          ? 'bg-green-100 text-green-800'
                          : c.status === 'draft'
                          ? 'bg-gray-100 text-gray-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}
                    >
                      {c.status}
                    </span>
                    <span className="text-gray-500">
                      {c.campaign_type === 'one_to_one' ? '1-to-1' : '1-to-Many'}
                    </span>
                    <span className="text-gray-500">{c.channel}</span>
                  </div>
                </div>
                <div className="text-right text-sm">
                  <p className="text-gray-500">
                    {c.total_contacts} contacts
                  </p>
                  <p className="text-gray-500">
                    {c.messages_sent} sent / {c.replies_received} replies
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Campaigns
