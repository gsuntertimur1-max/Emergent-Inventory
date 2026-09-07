import axios from 'axios';

const api = axios.create({
  baseURL: `${process.env.REACT_APP_BACKEND_URL}/api`,
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('bulog_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const setToken = (token) => {
  if (token) localStorage.setItem('bulog_token', token);
  else localStorage.removeItem('bulog_token');
};

export const apiError = (e) => {
  const detail = e?.response?.data?.detail;
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) return detail.map((d) => d?.msg || JSON.stringify(d)).join(' ');
  return e?.message || 'Terjadi kesalahan';
};

export default api;
