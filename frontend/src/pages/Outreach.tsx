import { useEffect, useState } from 'react'
import { getMessages } from '../services/api'

interface Message {
  id: number
  stakeholder_id: number
  campaign_id: number | null
  channel: string
  subject: string | null
  body: string
  personalization_context: string | null
  sap_solutions_referenced: string[]
  ai_model_used: string | null
  variant: string | null
  status: string
  created_at: string
}

function Outreach() {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getMessages({ limit: 50 })
      .then((res) => setMessages(res.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="text-gray-500">Loading...</p>

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        Outreach Messages
      </h2>

      {messages.length === 0 ? (
        <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
          <p className="text-gray-500">
            No messages generated yet. Go to a stakeholder profile and click
            "Generate Outreach" to create personalized messages.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {messages.map((m) => (
            <div
              key={m.id}
              className="bg-white rounded-lg border border-gray-200 p-6"
            >
              <div className="flex justify-between items-start mb-3">
                <div className="flex space-x-3 text-sm">
                  <span
                    className={`px-2 py-0.5 rounded text-xs font-medium ${
                      m.status === 'approved'
                        ? 'bg-green-100 text-green-800'
                        : m.status === 'sent'
                        ? 'bg-blue-100 text-blue-800'
                        : m.status === 'replied'
                        ? 'bg-purple-100 text-purple-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {m.status}
                  </span>
                  <span className="text-gray-500">{m.channel}</span>
                  {m.variant && (
                    <span className="text-gray-400">Variant {m.variant}</span>
                  )}
                  {m.ai_model_used && (
                    <span className="text-gray-400">via {m.ai_model_used}</span>
                  )}
                </div>
                <button
                  onClick={() => navigator.clipboard.writeText(m.body)}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  Copy
                </button>
              </div>

              {m.subject && (
                <p className="font-medium text-gray-900 mb-2">
                  Subject: {m.subject}
                </p>
              )}

              <div className="bg-gray-50 rounded-md p-4">
                <p className="text-sm text-gray-800 whitespace-pre-wrap">
                  {m.body}
                </p>
              </div>

              {m.personalization_context && (
                <p className="text-xs text-gray-400 mt-2 italic">
                  Personalization: {m.personalization_context}
                </p>
              )}

              {m.sap_solutions_referenced.length > 0 && (
                <div className="flex space-x-2 mt-2">
                  {m.sap_solutions_referenced.map((sol) => (
                    <span
                      key={sol}
                      className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full text-xs"
                    >
                      {sol}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Outreach
