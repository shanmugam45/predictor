import api from './api'

export const predictionService = {
  predict: (data) => api.post('/predictions/predict', data).then((r) => r.data),
  predictBatch: (records) =>
    api.post('/predictions/predict/batch', { records }).then((r) => r.data),
  list: (params) => api.get('/predictions/', { params }).then((r) => r.data),  // ← trailing slash added
}