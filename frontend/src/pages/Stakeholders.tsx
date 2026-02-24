import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getStakeholders } from '../services/api'

interface Stakeholder {
  id: number
  full_name: string
  job_title: string | null
  company_name: string | null
  seniority_level: string | null
  department: string | null
  linkedin_url: string | null
  fit_score: number
  engagement_score: number
  ai_profile_summary: string | null
  tags: string[]
}

function Stakeholders() {
  const [stakeholders, setStakeholders] = useState<Stakeholder[]>([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)

  const fetchStakeholders = (searchTerm?: string) => {
    setLoading(true)
    const params: Record<string, string | number> = { limit: 100 }
    if (searchTerm) params.search = searchTerm
    getStakeholders(params)
      .then((res) => setStakeholders(res.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchStakeholders()
  }, [])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    fetchStakeholders(search)
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Stakeholders</h2>
        <form onSubmit={handleSearch} className="flex space-x-2">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by name, title, company..."
            className="border border-gray-300 rounded-md px-3 py-2 text-sm w-64"
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700"
          >
            Search
          </button>
        </form>
      </div>

      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : stakeholders.length === 0 ? (
        <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
          <p className="text-gray-500">
            No stakeholders yet. Import a LinkedIn CSV to get started.
          </p>
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Title
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Company
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Seniority
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Fit Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Profiled
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {stakeholders.map((s) => (
                <tr key={s.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <Link
                      to={`/stakeholders/${s.id}`}
                      className="text-blue-600 hover:text-blue-800 font-medium"
                    >
                      {s.full_name}
                    </Link>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {s.job_title || '—'}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {s.company_name || '—'}
                  </td>
                  <td className="px-6 py-4 text-sm">
                    {s.seniority_level ? (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {s.seniority_level}
                      </span>
                    ) : (
                      '—'
                    )}
                  </td>
                  <td className="px-6 py-4 text-sm">
                    {s.fit_score > 0 ? (
                      <span
                        className={`font-medium ${
                          s.fit_score >= 70
                            ? 'text-green-600'
                            : s.fit_score >= 40
                            ? 'text-yellow-600'
                            : 'text-gray-400'
                        }`}
                      >
                        {s.fit_score}
                      </span>
                    ) : (
                      <span className="text-gray-400">—</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-sm">
                    {s.ai_profile_summary ? (
                      <span className="text-green-600">Yes</span>
                    ) : (
                      <span className="text-gray-400">No</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default Stakeholders
