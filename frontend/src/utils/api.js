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


  const response = await fetch(`https://andrterrius.lol${endpoint}`, config);

  if (!response.ok) throw new Error('Ошибка запроса');

  return response.json();
}

export const getFlavours = () => apiRequest('/api/v1/flavors/', { method: 'GET' });
export const getAvailableFlavours = () => apiRequest('/api/v1/flavors/available', { method: 'GET' }); 
export const getAvailablePresets = () => apiRequest('/api/v1/presets/available', { method: 'GET' });
export const savePreset = (presetData) => apiRequest('/api/v1/presets/', { method: 'POST', body: JSON.stringify(presetData) });