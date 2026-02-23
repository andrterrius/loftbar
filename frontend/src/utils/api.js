export async function apiRequest(endpoint, options = {}) {
  let token = '';

  if (typeof window !== 'undefined') {
    token = localStorage.getItem('jwt') || '';
  }

  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  };

  const baseUrl =
    typeof window === 'undefined'
      ? process.env.NEXT_PUBLIC_API_URL
      : '';

  const response = await fetch(`${baseUrl}/api${endpoint}`, config);

  if (!response.ok) throw new Error('Ошибка запроса');

  return response.json();
}

const API_URL = 'http://localhost:8000/flavors'

// Получить все вкусы
export async function getFlavours() {
  const res = await fetch(`${API_URL}/`)
  if (!res.ok) throw new Error('Ошибка получения вкусов')
  return res.json()
}
