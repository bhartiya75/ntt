import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

// Stakeholders
export const getStakeholders = (params?: Record<string, string | number>) =>
  api.get('/stakeholders/', { params })

export const getStakeholder = (id: number) =>
  api.get(`/stakeholders/${id}`)

export const createStakeholder = (data: Record<string, unknown>) =>
  api.post('/stakeholders/', data)

export const updateStakeholder = (id: number, data: Record<string, unknown>) =>
  api.patch(`/stakeholders/${id}`, data)

export const deleteStakeholder = (id: number) =>
  api.delete(`/stakeholders/${id}`)

export const profileStakeholder = (id: number, data: Record<string, unknown>) =>
  api.post(`/stakeholders/${id}/profile`, data)

export const enrichStakeholder = (id: number) =>
  api.post(`/stakeholders/${id}/enrich`)

// Companies
export const getCompanies = (params?: Record<string, string | number>) =>
  api.get('/companies/', { params })

export const getCompany = (id: number) =>
  api.get(`/companies/${id}`)

export const createCompany = (data: Record<string, unknown>) =>
  api.post('/companies/', data)

export const analyzeCompany = (id: number, provider?: string) =>
  api.post(`/companies/${id}/analyze`, null, { params: { provider } })

// Campaigns
export const getCampaigns = (params?: Record<string, string | number>) =>
  api.get('/campaigns/', { params })

export const getCampaign = (id: number) =>
  api.get(`/campaigns/${id}`)

export const createCampaign = (data: Record<string, unknown>) =>
  api.post('/campaigns/', data)

export const getCampaignStakeholders = (id: number) =>
  api.get(`/campaigns/${id}/stakeholders`)

// Outreach
export const generateOutreach = (data: Record<string, unknown>) =>
  api.post('/outreach/generate', data)

export const generateBulkOutreach = (data: Record<string, unknown>) =>
  api.post('/outreach/generate-bulk', data)

export const getMessages = (params?: Record<string, string | number>) =>
  api.get('/outreach/messages', { params })

// Import
export const importCSV = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/import/linkedin-csv', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

// Presentations
export const generatePresentation = (data: Record<string, unknown>) =>
  api.post('/presentations/generate', data)

export const listPresentations = () =>
  api.get('/presentations/list')

// Stats
export const getStats = () => api.get('/stats')

export default api
