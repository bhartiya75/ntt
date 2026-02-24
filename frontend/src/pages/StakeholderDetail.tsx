import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getStakeholder, profileStakeholder, generateOutreach } from '../services/api'

interface Stakeholder {
  id: number
  full_name: string
  first_name: string | null
  last_name: string | null
  email: string | null
  job_title: string | null
  company_name: string | null
  seniority_level: string | null
  department: string | null
  linkedin_url: string | null
  linkedin_headline: string | null
  linkedin_summary: string | null
  linkedin_location: string | null
  ai_profile_summary: string | null
  ai_need_analysis: string | null
  ai_gap_analysis: string | null
  pain_points: string[]
  recommended_sap_solutions: string[]
  conversation_starters: string[]
  best_outreach_channel: string | null
  fit_score: number
  engagement_score: number
}

function StakeholderDetail() {
  const { id } = useParams<{ id: string }>()
  const [stakeholder, setStakeholder] = useState<Stakeholder | null>(null)
  const [profiling, setProfiling] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [generatedMessage, setGeneratedMessage] = useState<string | null>(null)

  useEffect(() => {
    if (id) {
      getStakeholder(Number(id)).then((res) => setStakeholder(res.data))
    }
  }, [id])

  const handleProfile = async () => {
    if (!stakeholder) return
    setProfiling(true)
    try {
      await profileStakeholder(stakeholder.id, {
        ai_provider: 'ollama',
        include_need_analysis: true,
        include_gap_analysis: true,
        include_conversation_starters: true,
        include_solution_matching: true,
      })
      const res = await getStakeholder(stakeholder.id)
      setStakeholder(res.data)
    } catch {
      alert('Failed to generate profile. Is Ollama running? (ollama serve)')
    }
    setProfiling(false)
  }

  const handleGenerateOutreach = async () => {
    if (!stakeholder) return
    setGenerating(true)
    try {
      const res = await generateOutreach({
        stakeholder_ids: [stakeholder.id],
        ai_provider: 'ollama',
        tone: 'professional',
        message_type: 'initial_connect',
        channel: 'linkedin_message',
      })
      const msg = res.data.results?.[0]?.message?.body
      setGeneratedMessage(msg || 'Message generated — check Outreach tab.')
    } catch {
      alert('Failed to generate outreach. Is Ollama running? (ollama serve)')
    }
    setGenerating(false)
  }

  if (!stakeholder) return <p className="text-gray-500">Loading...</p>

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              {stakeholder.full_name}
            </h2>
            <p className="text-gray-600 mt-1">
              {stakeholder.job_title || 'No title'} at{' '}
              {stakeholder.company_name || 'Unknown company'}
            </p>
            {stakeholder.linkedin_headline && (
              <p className="text-gray-500 text-sm mt-1">
                {stakeholder.linkedin_headline}
              </p>
            )}
            <div className="flex space-x-4 mt-3 text-sm text-gray-500">
              {stakeholder.seniority_level && (
                <span className="bg-blue-50 text-blue-700 px-2 py-1 rounded">
                  {stakeholder.seniority_level}
                </span>
              )}
              {stakeholder.department && (
                <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded">
                  {stakeholder.department}
                </span>
              )}
              {stakeholder.linkedin_location && (
                <span>{stakeholder.linkedin_location}</span>
              )}
            </div>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={handleProfile}
              disabled={profiling}
              className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700 disabled:opacity-50"
            >
              {profiling ? 'Analyzing...' : 'Run AI Profile'}
            </button>
            <button
              onClick={handleGenerateOutreach}
              disabled={generating}
              className="bg-green-600 text-white px-4 py-2 rounded-md text-sm hover:bg-green-700 disabled:opacity-50"
            >
              {generating ? 'Generating...' : 'Generate Outreach'}
            </button>
          </div>
        </div>

        {/* Scores */}
        {(stakeholder.fit_score > 0 || stakeholder.engagement_score > 0) && (
          <div className="flex space-x-6 mt-4 pt-4 border-t border-gray-100">
            <div>
              <span className="text-sm text-gray-500">Fit Score</span>
              <p className="text-2xl font-bold text-blue-600">
                {stakeholder.fit_score}
              </p>
            </div>
            <div>
              <span className="text-sm text-gray-500">Engagement Score</span>
              <p className="text-2xl font-bold text-green-600">
                {stakeholder.engagement_score}
              </p>
            </div>
            {stakeholder.best_outreach_channel && (
              <div>
                <span className="text-sm text-gray-500">Best Channel</span>
                <p className="text-lg font-medium text-gray-900">
                  {stakeholder.best_outreach_channel}
                </p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* AI Profile Summary */}
      {stakeholder.ai_profile_summary && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            AI Profile Summary
          </h3>
          <p className="text-gray-700 whitespace-pre-wrap">
            {stakeholder.ai_profile_summary}
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Need Analysis */}
        {stakeholder.ai_need_analysis && (
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Need Analysis
            </h3>
            <p className="text-gray-700 whitespace-pre-wrap text-sm">
              {stakeholder.ai_need_analysis}
            </p>
          </div>
        )}

        {/* Gap Analysis */}
        {stakeholder.ai_gap_analysis && (
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Gap Analysis
            </h3>
            <p className="text-gray-700 whitespace-pre-wrap text-sm">
              {stakeholder.ai_gap_analysis}
            </p>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Pain Points */}
        {stakeholder.pain_points.length > 0 && (
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Pain Points
            </h3>
            <ul className="space-y-2">
              {stakeholder.pain_points.map((pp, i) => (
                <li key={i} className="text-sm text-gray-700 flex items-start">
                  <span className="text-red-500 mr-2 mt-1">&#9679;</span>
                  {pp}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommended SAP Solutions */}
        {stakeholder.recommended_sap_solutions.length > 0 && (
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Recommended SAP Solutions
            </h3>
            <ul className="space-y-2">
              {stakeholder.recommended_sap_solutions.map((sol, i) => (
                <li key={i} className="text-sm text-gray-700 flex items-start">
                  <span className="text-blue-500 mr-2 mt-1">&#9679;</span>
                  {sol}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Conversation Starters */}
        {stakeholder.conversation_starters.length > 0 && (
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Conversation Starters
            </h3>
            <ul className="space-y-3">
              {stakeholder.conversation_starters.map((cs, i) => (
                <li
                  key={i}
                  className="text-sm text-gray-700 bg-gray-50 p-3 rounded-md italic"
                >
                  "{cs}"
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Generated Outreach Message */}
      {generatedMessage && (
        <div className="bg-green-50 rounded-lg border border-green-200 p-6">
          <h3 className="text-lg font-semibold text-green-900 mb-3">
            Generated Outreach Message
          </h3>
          <div className="bg-white p-4 rounded-md border border-green-100">
            <p className="text-gray-800 whitespace-pre-wrap">{generatedMessage}</p>
          </div>
          <button
            onClick={() => navigator.clipboard.writeText(generatedMessage)}
            className="mt-3 text-sm text-green-700 hover:text-green-900 font-medium"
          >
            Copy to clipboard
          </button>
        </div>
      )}

      {/* LinkedIn Info */}
      {stakeholder.linkedin_summary && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            LinkedIn Summary
          </h3>
          <p className="text-gray-700 whitespace-pre-wrap text-sm">
            {stakeholder.linkedin_summary}
          </p>
          {stakeholder.linkedin_url && (
            <a
              href={stakeholder.linkedin_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline text-sm mt-3 inline-block"
            >
              View LinkedIn Profile
            </a>
          )}
        </div>
      )}
    </div>
  )
}

export default StakeholderDetail
