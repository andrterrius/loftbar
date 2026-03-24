'use client'
import { apiRequest } from "@/utils/api";
import { useEffect, useState } from "react";

const InitTelegramAuth = () => {
    const [showNameInput, setShowNameInput] = useState(false);
    const [name, setName] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const initAuth = async () => {
            if (localStorage.getItem('jwt')) return;

            const tgDataInit = window.Telegram?.WebApp?.initData;

            if (!tgDataInit) {
                setShowNameInput(true);
                return;
            }

            try {
                const data = await apiRequest('/users/login', {
                    method: "POST",
                    headers: { "X-Init-Data": tgDataInit }
                });
                localStorage.setItem('jwt', data.access_token);
            } catch (err) {
                console.log("Ошибка", err);
            }
        };
        initAuth();
    }, []);

    const handleNameSubmit = async () => {
        if (!name.trim()) return;
        setIsLoading(true);
        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/users/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: name.trim() })
            });

            if (!res.ok) {
                const err = await res.json();
                console.log("Ошибка сервера:", err);
                alert('Не удалось войти. Попробуйте другое имя.');
                return;
            }

            const data = await res.json();
            localStorage.setItem('jwt', data.access_token);
            setShowNameInput(false);
        } catch (err) {
            console.log("Ошибка регистрации", err);
            alert('Не удалось подключиться к серверу.');
        } finally {
            setIsLoading(false);
        }
    };

    if (!showNameInput) return null;

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
            <div className="bg-neutral-900 border border-white/10 rounded-2xl p-6 w-full max-w-sm shadow-2xl">
                <h3 className="text-xl font-bold text-white mb-1">Добро пожаловать</h3>
                <p className="text-neutral-400 text-sm mb-5">Введите ваше имя, чтобы продолжить</p>

                <input
                    type="text"
                    placeholder="Ваше имя..."
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleNameSubmit()}
                    autoFocus
                    className="w-full bg-neutral-800 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-neutral-500 text-sm outline-none focus:border-fuchsia-500/50 transition-colors mb-4"
                />

                <button
                    onClick={handleNameSubmit}
                    disabled={isLoading || !name.trim()}
                    className="w-full py-3 bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white rounded-xl font-bold text-sm shadow-[0_0_20px_rgba(192,38,211,0.3)] active:scale-95 transition-transform disabled:opacity-60"
                >
                    {isLoading ? 'Входим...' : 'Продолжить'}
                </button>
            </div>
        </div>
    );
};

export default InitTelegramAuth;