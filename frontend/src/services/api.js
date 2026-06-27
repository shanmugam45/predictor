import axios from 'axios'

const apiBaseUrl = import.meta.env.VITE_API_URL 
  || import.meta.env.VITE_API_BASE_URL 
  || 'https://predictor-ep5n.onrender.com'  // fallback for safety

const api = axios.create({
  baseURL: apiBaseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api  