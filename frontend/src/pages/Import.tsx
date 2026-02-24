import { useState } from 'react'
import { importCSV } from '../services/api'

function Import() {
  const [file, setFile] = useState<File | null>(null)
  const [importing, setImporting] = useState(false)
  const [result, setResult] = useState<{
    imported: number
    skipped: number
    companies_created: number
    errors: { row: number; error: string }[]
  } | null>(null)

  const handleImport = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return

    setImporting(true)
    setResult(null)

    try {
      const res = await importCSV(file)
      setResult(res.data)
    } catch {
      alert('Import failed. Check your CSV format.')
    }

    setImporting(false)
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Import Contacts</h2>

      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          LinkedIn CSV Import
        </h3>
        <p className="text-sm text-gray-500 mb-4">
          Upload a CSV exported from LinkedIn, Sales Navigator, or Apollo.io.
          The system will automatically map columns to stakeholder fields and
          create companies.
        </p>

        <div className="bg-gray-50 rounded-md p-4 mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">
            Supported columns:
          </h4>
          <div className="grid grid-cols-3 gap-2 text-xs text-gray-600">
            <span>First Name / Last Name</span>
            <span>Email / Phone</span>
            <span>Job Title / Position</span>
            <span>Company / Organization</span>
            <span>LinkedIn URL</span>
            <span>Headline / Summary</span>
            <span>Location / City</span>
            <span>Industry</span>
            <span>Company Size / Employees</span>
            <span>Seniority / Department</span>
            <span>Connections</span>
            <span>Tags</span>
          </div>
        </div>

        <form onSubmit={handleImport} className="flex items-end space-x-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              CSV File
            </label>
            <input
              type="file"
              accept=".csv"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
            />
          </div>
          <button
            type="submit"
            disabled={!file || importing}
            className="bg-blue-600 text-white px-6 py-2 rounded-md text-sm hover:bg-blue-700 disabled:opacity-50"
          >
            {importing ? 'Importing...' : 'Import'}
          </button>
        </form>
      </div>

      {result && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            Import Results
          </h3>
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="bg-green-50 rounded-md p-4 text-center">
              <p className="text-2xl font-bold text-green-700">
                {result.imported}
              </p>
              <p className="text-sm text-green-600">Imported</p>
            </div>
            <div className="bg-yellow-50 rounded-md p-4 text-center">
              <p className="text-2xl font-bold text-yellow-700">
                {result.skipped}
              </p>
              <p className="text-sm text-yellow-600">Skipped (duplicates)</p>
            </div>
            <div className="bg-blue-50 rounded-md p-4 text-center">
              <p className="text-2xl font-bold text-blue-700">
                {result.companies_created}
              </p>
              <p className="text-sm text-blue-600">Companies Created</p>
            </div>
          </div>
          {result.errors.length > 0 && (
            <div className="bg-red-50 rounded-md p-4">
              <h4 className="text-sm font-medium text-red-700 mb-2">Errors:</h4>
              {result.errors.map((err, i) => (
                <p key={i} className="text-xs text-red-600">
                  Row {err.row}: {err.error}
                </p>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Import
