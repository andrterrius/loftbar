export async function apiRequest(endpoint, options = {}) {
  let tgInitData = '';

  if (typeof window !== 'undefined') {
    // Мы на клиенте — берем из объекта Telegram
    tgInitData = window.Telegram?.WebApp?.initData || '';
  }

  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-TG-Data': tgInitData, 
      ...options.headers,
    },
  };

  // Важно: на сервере нужно указывать полный URL (http://localhost:3000...)
  // На клиенте достаточно относительного path (/api/...)
  const baseUrl = typeof window === 'undefined' ? process.env.NEXT_PUBLIC_API_URL : '';
  
  const response = await fetch(`${baseUrl}/api${endpoint}`, config);
  
  if (!response.ok) throw new Error('Ошибка запроса');
  return response.json();
}