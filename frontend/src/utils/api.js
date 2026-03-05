async function login() {
    const tgData = window.Telegram?.WebApp?.initData || '';
    const res = await fetch('https://andrterrius.lol/api/v1/users/login', {
        method: 'POST',
        headers: { 'X-Init-Data': tgData },
    });
    if (!res.ok) throw new Error('Login failed');
    const data = await res.json();
    localStorage.setItem('jwt', data.access_token);
    return data.access_token;
}

export async function apiRequest(endpoint, options = {}, attempt = 1) {
    const MAX_ATTEMPTS = 3;
    let token = localStorage.getItem('jwt') || '';

    const config = {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...(token && { Authorization: `Bearer ${token}` }),
            ...options.headers,
        },
    };

    const response = await fetch(`https://andrterrius.lol/api/v1${endpoint}`, config);

    // если 401 — запускаем retry
    if (response.status === 401) {
        if (attempt >= MAX_ATTEMPTS) {
            // все попытки исчерпаны закрываем приложение
            window.Telegram?.WebApp?.close();
            return;
        }

        try {
            await login(); // обновляем токен
        } catch {
            // логин не удался — следующая попытка
        }

        // рекурсивный повтор запроса
        return apiRequest(endpoint, options, attempt + 1);
    }

    if (!response.ok) throw new Error('Ошибка запроса');
    return response.json();
}



export const getFlavours = () => apiRequest('/flavors/', { method: 'GET' });
export const getAvailablePresets = () => apiRequest('/presets/available', { method: 'GET' });
export const getLiquids = () => apiRequest('/liquids/', { method: 'GET' });
export const getPresets = () => apiRequest('/presets/', { method: 'GET' });
export const getBowls = () => apiRequest('/bowls/', { method: 'GET' });