'use client'
import { apiRequest, simpleLogin } from "@/utils/api";
import { useEffect, useState } from "react";
import { QrCode } from "lucide-react";

const InitTelegramAuth = () => {
    const [mounted, setMounted] = useState(false);
    const [showNameInput, setShowNameInput] = useState(false);
    const [showQrScan, setShowQrScan] = useState(false);
    const [name, setName] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        setMounted(true);
        const initAuth = async () => {
            const tableId = window.Telegram?.WebApp?.initDataUnsafe?.start_param
                || new URLSearchParams(window.location.search).get('table_id');
            
            if (!tableId) {
                setShowQrScan(true);
                return;
            }

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

    if (!mounted) return null;

    const handleNameSubmit = async () => {
        if (!name.trim()) return;
        setIsLoading(true);
        try {
            await simpleLogin(name);
            setShowNameInput(false);
        } catch (err) {
            console.log("Ошибка при логине:", err);
        } finally {
            setIsLoading(false);
        }
    };

    if (!mounted) return null;
    if (!showNameInput && !showQrScan) return null;

    if (showQrScan) {
        return (
            <div className="fixed inset-0 z-[70] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="bg-neutral-900 border border-white/10 rounded-2xl p-8 w-full max-w-sm shadow-2xl flex flex-col items-center text-center">
            <div className="w-16 h-16 rounded-full bg-fuchsia-500/20 flex items-center justify-center mb-4">
              <QrCode size={32} className="text-fuchsia-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Отсканируй QR-код</h3>
            <p className="text-neutral-400 text-sm mb-6">
              Для оформления заказа необходимо отсканировать QR-код на вашем столе.
            </p>
            <div className="w-full py-3 px-4 rounded-xl bg-white/5 border border-white/10 text-neutral-500 text-xs text-center">
              📍 QR-код находится на столике
            </div>
          </div>
        </div>
        );
    }

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