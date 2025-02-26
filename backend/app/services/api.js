// frontend/src/services/api.js
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Tratamento centralizado de erros
    const errorMessage = error.response?.data?.erro || 'Ocorreu um erro na comunicação com o servidor';
    console.error('API Error:', errorMessage);
    return Promise.reject(errorMessage);
  }
);

export default api;