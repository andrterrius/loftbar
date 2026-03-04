export async function apiRequest(endpoint, options = {}) {
  let token = '';
  let tgData = '';

  if (typeof window !== 'undefined') {
    token = localStorage.getItem('jwt') || '';
    tgData = window.Telegram?.WebApp?.initData || '';
  }

  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...(tgData && { 'X-Telegram-Init-Data': tgData }),
      ...options.headers
    },
  };


  const response = await fetch(`https://andrterrius.lol/api/v1${endpoint}`, config);

  if (!response.ok) throw new Error('Ошибка запроса');

  return response.json();
}

export const getFlavours = () => apiRequest('/flavors/', { method: 'GET' });
export const getAvailablePresets = () => apiRequest('/presets/available', { method: 'GET' });
export const getLiquids = () => apiRequest('/liquids/', { method: 'GET' });
export const getPresets = () => apiRequest('/presets/', { method: 'GET' });
export const getBowls = () => apiRequest('/bowls/', { method: 'GET' });