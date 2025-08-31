import axios from 'axios'

export const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  withCredentials: true,
})

// Note: Les intercepteurs sont maintenant gérés dans le store auth pour éviter les doublons
