function getTelegramHeaders() {
  const headers = {
    'Content-Type': 'application/json',
  };


  if (typeof window !== 'undefined' && window.Telegram?.WebApp?.initData) {
    headers['X-Telegram-Init-Data'] = window.Telegram.WebApp.initData;
  } else {
    console.warn('Telegram WebApp initData не найден. Работаем в режиме разработки или браузера.');
  }

  return headers;
}

export async function apiRequest(endpoint, options = {}) {
  const BASE_URL = '/api';

  const config = {
    ...options,
    headers: {
      ...getTelegramHeaders(),
      ...options.headers, 
    },
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, config);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || 'Ошибка сервера');
  }

  return response.json();
}