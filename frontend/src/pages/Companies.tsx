import { useEffect, useState } from 'react'
import { getCompanies, analyzeCompany } from '../services/api'

interface Company {
  id: number
  name: string
  industry: string | null
  employee_count: string | null
  current_erp: string | null
  current_sap_products: string[]
  sap_maturity_level: string
  priority_tier: number
  ai_company_analysis: string | null
}

function Companies() {
  const [companies, setCompanies] = useState<Company[]>([])
  const [loading, setLoading] = useState(true)
  const [analyzingId, setAnalyzingId] = useState<number | null>(null)

  useEffect(() => {
    getCompanies({ limit: 100 })
      .then((res) => setCompanies(res.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const handleAnalyze = async (id: number) => {
    setAnalyzingId(id)
    try {
      await analyzeCompany(id)
      const res = await getCompanies({ limit: 100 })
      setCompanies(res.data)
    } catch {
      alert('Failed to analyze company.')
    }
    setAnalyzingId(null)
  }

  if (loading) return <p className="text-gray-500">Loading...</p>

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Companies</h2>

      {companies.length === 0 ? (
        <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
          <p className="text-gray-500">
            No companies yet. Import stakeholders to auto-create companies.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {companies.map((c) => (
            <div
              key={c.id}
              className="bg-white rounded-lg border border-gray-200 p-6"
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {c.name}
                  </h3>
                  <div className="flex space-x-4 mt-1 text-sm text-gray-500">
                    {c.industry && <span>{c.industry}</span>}
                    {c.employee_count && <span>{c.employee_count} employees</span>}
                    <span className="bg-gray-100 px-2 py-0.5 rounded text-xs">
                      Tier {c.priority_tier}
                    </span>
                    <span className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs">
                      SAP: {c.sap_maturity_level}
                    </span>
                  </div>
                  {c.current_sap_products.length > 0 && (
                    <div className="flex space-x-2 mt-2">
                      {c.current_sap_products.map((p) => (
                        <span
                          key={p}
                          className="bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full text-xs"
                        >
                          {p}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                <button
                  onClick={() => handleAnalyze(c.id)}
                  disabled={analyzingId === c.id}
                  className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700 disabled:opacity-50"
                >
                  {analyzingId === c.id ? 'Analyzing...' : 'AI Analyze'}
                </button>
              </div>
              {c.ai_company_analysis && (
                <div className="mt-4 pt-4 border-t border-gray-100">
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">
                    {c.ai_company_analysis}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Companies
