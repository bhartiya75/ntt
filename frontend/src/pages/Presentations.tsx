import { useState, useEffect } from 'react'
import { getStakeholders, getCompanies, getCampaigns } from '../services/api'
import api from '../services/api'

type PresentationType = 'stakeholder_briefing' | 'company_analysis' | 'campaign_summary' | 'outreach_strategy'

interface Entity {
  id: number
  name: string
}

interface GeneratedFile {
  filename: string
  download_url: string
  slides_count?: number
  size_bytes?: number
}

const TYPES: { value: PresentationType; label: string; needsId: boolean; entityLabel: string }[] = [
  { value: 'stakeholder_briefing', label: 'Stakeholder Briefing', needsId: true, entityLabel: 'Stakeholder' },
  { value: 'company_analysis', label: 'Company Analysis', needsId: true, entityLabel: 'Company' },
  { value: 'campaign_summary', label: 'Campaign Summary', needsId: true, entityLabel: 'Campaign' },
  { value: 'outreach_strategy', label: 'Outreach Strategy', needsId: false, entityLabel: '' },
]

export default function Presentations() {
  const [type, setType] = useState<PresentationType>('stakeholder_briefing')
  const [entityId, setEntityId] = useState<number | null>(null)
  const [title, setTitle] = useState('')
  const [entities, setEntities] = useState<Entity[]>([])
  const [loading, setLoading] = useState(false)
  const [generated, setGenerated] = useState<GeneratedFile | null>(null)
  const [history, setHistory] = useState<GeneratedFile[]>([])
  const [error, setError] = useState('')

  const selectedType = TYPES.find(t => t.value === type)!

  useEffect(() => {
    loadEntities()
    loadHistory()
  }, [type])

  async function loadEntities() {
    try {
      if (type === 'stakeholder_briefing') {
        const res = await getStakeholders({ limit: 100 })
        setEntities(res.data.map((s: any) => ({ id: s.id, name: s.full_name })))
      } else if (type === 'company_analysis') {
        const res = await getCompanies({ limit: 100 })
        setEntities(res.data.map((c: any) => ({ id: c.id, name: c.name })))
      } else if (type === 'campaign_summary') {
        const res = await getCampaigns({ limit: 100 })
        setEntities(res.data.map((c: any) => ({ id: c.id, name: c.name })))
      } else {
        setEntities([])
      }
    } catch {
      setEntities([])
    }
    setEntityId(null)
  }

  async function loadHistory() {
    try {
      const res = await api.get('/presentations/list')
      setHistory(res.data.presentations || [])
    } catch {
      setHistory([])
    }
  }

  async function handleGenerate() {
    if (selectedType.needsId && !entityId) {
      setError(`Please select a ${selectedType.entityLabel.toLowerCase()}.`)
      return
    }
    setLoading(true)
    setError('')
    setGenerated(null)
    try {
      const res = await api.post('/presentations/generate', {
        type,
        id: entityId,
        title: title || undefined,
        ai_provider: 'ollama',
      })
      setGenerated(res.data)
      loadHistory()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate presentation.')
    } finally {
      setLoading(false)
    }
  }

  function downloadUrl(url: string) {
    return `/api${url}`
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Presentations</h2>

      {/* Generator Card */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Generate PowerPoint Presentation</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          {/* Type selector */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Presentation Type</label>
            <select
              value={type}
              onChange={e => setType(e.target.value as PresentationType)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-blue-500 focus:border-blue-500"
            >
              {TYPES.map(t => (
                <option key={t.value} value={t.value}>{t.label}</option>
              ))}
            </select>
          </div>

          {/* Entity selector */}
          {selectedType.needsId && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Select {selectedType.entityLabel}
              </label>
              <select
                value={entityId ?? ''}
                onChange={e => setEntityId(e.target.value ? Number(e.target.value) : null)}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">-- Select --</option>
                {entities.map(e => (
                  <option key={e.id} value={e.id}>{e.name}</option>
                ))}
              </select>
            </div>
          )}
        </div>

        {/* Custom title */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">Custom Title (optional)</label>
          <input
            type="text"
            value={title}
            onChange={e => setTitle(e.target.value)}
            placeholder="Leave blank for auto-generated title"
            className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {error && <p className="text-red-600 text-sm mb-3">{error}</p>}

        <button
          onClick={handleGenerate}
          disabled={loading}
          className="bg-blue-700 text-white px-6 py-2 rounded-md text-sm font-medium hover:bg-blue-800 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Generating...' : 'Generate Presentation'}
        </button>

        {/* Generated result */}
        {generated && (
          <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-md">
            <p className="text-green-800 font-medium text-sm">
              Presentation generated! ({generated.slides_count} slides)
            </p>
            <a
              href={downloadUrl(generated.download_url)}
              className="inline-block mt-2 bg-green-600 text-white px-4 py-1.5 rounded text-sm hover:bg-green-700"
            >
              Download {generated.filename}
            </a>
          </div>
        )}
      </div>

      {/* History */}
      {history.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Generated Presentations</h3>
          <div className="space-y-2">
            {history.map(f => (
              <div key={f.filename} className="flex items-center justify-between py-2 px-3 bg-gray-50 rounded">
                <span className="text-sm text-gray-700">{f.filename}</span>
                <a
                  href={downloadUrl(f.download_url)}
                  className="text-blue-600 text-sm hover:underline"
                >
                  Download
                </a>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
