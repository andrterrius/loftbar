const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export async function login() {
    const tgData = window.Telegram?.WebApp?.initData || '';
    const res = await fetch(`${BASE_URL}/users/login`, {
        method: 'POST',
        headers: { 'X-Init-Data': tgData },
    });
    if (!res.ok) throw new Error('Login failed');
    const data = await res.json();
    localStorage.setItem('jwt', data.access_token);
    return data.access_token;
}

export async function simpleLogin(name) {
    const res = await fetch(`${BASE_URL}/users/login/simple`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name.trim() }),
    });
    if (!res.ok) throw new Error('login failed');
    const data = await res.json();
    localStorage.setItem('jwt', data.access_token);
    return data.access_token;
}

function refreshToken() {
    let isTg = !!window.Telegram?.WebApp.initData;
    if (isTg) {
        return login();
    }
    throw new Error('no auto refresh bro');
}

export async function apiRequest(endpoint, options = {}, attempt = 1) {
    const MAX_ATTEMPTS = 3;
    let token = localStorage.getItem('jwt');
    if (!token) return

    const config = {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...(token && { Authorization: `Bearer ${token}` }),
            ...options.headers,
        },
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, config);

    // если 401 — запускаем retry
    if (response.status === 401) {
        if (attempt >= MAX_ATTEMPTS) {
            // все попытки исчерпаны закрываем приложение
            window.Telegram?.WebApp?.close();
            localStorage.removeItem("jwt");
            window.dispatchEvent(new Event('unauthorized'));
            return;
        }

        try {
            await refreshToken(); // обновляем токен
        } catch {
            // если чел не с телеги, то просто дальше идем, а если с тг то все гут
        }

        // рекурсивный повтор запроса
        return apiRequest(endpoint, options, attempt + 1);
    }

    if (response.status === 422) {
      const errorData = await response.json();
      const err = new Error('Validation error');
      err.status = 422;
      err.detail = errorData.detail;
      throw err;
    }

    if (!response.ok) throw new Error('Ошибка запроса');
    return response.json();
}



export const getFlavours = () => apiRequest('/flavors', { method: 'GET' });
export const getFlavoursCategories = () => apiRequest('/flavors/categories', { method: 'GET' });
export const getAvailablePresets = () => apiRequest('/presets/available', { method: 'GET' });
export const getLiquids = () => apiRequest('/liquids', { method: 'GET' });
export const getPresets = () => apiRequest('/presets', { method: 'GET' });
export const getBowls = () => apiRequest('/bowls', { method: 'GET' });
export const createOrder = (data) => apiRequest('/orders', { method: 'POST', body: JSON.stringify(data) });
export const getBasePrice = () => apiRequest('/presets/price', { method: 'GET' });
export const getSettingsImages = () => apiRequest('/settings/images', { method: 'GET' });