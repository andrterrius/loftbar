'use client'
import { login, apiRequest, simpleLogin } from "@/utils/api";
import { useEffect, useState } from "react";
import { QrCode } from "lucide-react";

const InitTelegramAuth = () => {
    const [mounted, setMounted] = useState(false);
    const [showNameInput, setShowNameInput] = useState(false);
    const [showQrScan, setShowQrScan] = useState(false);
    const [name, setName] = useState('');
    const [phone, setPhone] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [phoneError, setPhoneError] = useState('');

    // Валидация номера телефона
    const validatePhone = (phoneNumber) => {
        // Удаляем все非цифровые символы
        const cleaned = phoneNumber.replace(/\D/g, '');
        
        // Проверяем различные форматы
        const phoneRegex = /^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$/;
        const cleanRegex = /^[0-9]{10,11}$/;
        
        if (!phoneNumber.trim()) {
            return { isValid: false, error: 'Номер телефона обязателен' };
        }
        
        if (!phoneRegex.test(phoneNumber) && !cleanRegex.test(cleaned)) {
            return { isValid: false, error: 'Введите корректный номер телефона' };
        }
        
        if (cleaned.length < 10 || cleaned.length > 11) {
            return { isValid: false, error: 'Номер должен содержать 10-11 цифр' };
        }
        
        return { isValid: true, error: '' };
    };

    // Форматирование номера телефона при вводе
    const formatPhoneNumber = (value) => {
        // Удаляем все цифровые символы
        const cleaned = value.replace(/\D/g, '');
        
        // Ограничиваем длину 11 символами
        const limited = cleaned.slice(0, 11);
        
        // Форматируем в зависимости от количества цифр
        if (limited.length === 0) return '';
        if (limited.length <= 4) return `+7 ${limited.slice(1)}`;
        if (limited.length <= 7) return `+7 ${limited.slice(1, 4)} ${limited.slice(4)}`;
        if (limited.length <= 9) return `+7 ${limited.slice(1, 4)} ${limited.slice(4, 7)} ${limited.slice(7)}`;
        return `+7 ${limited.slice(1, 4)} ${limited.slice(4, 7)} ${limited.slice(7, 9)} ${limited.slice(9, 11)}`;
    };

    const handlePhoneChange = (e) => {
        const rawValue = e.target.value;
        const formattedValue = formatPhoneNumber(rawValue);
        setPhone(formattedValue);
        
        // Валидация при изменении
        const validation = validatePhone(formattedValue);
        setPhoneError(validation.error);
    };

    useEffect(() => {
        const handleUnauthorized = () => {
            setShowNameInput(true);
        };

        window.addEventListener('unauthorized', handleUnauthorized);

        return () => {
            window.removeEventListener('unauthorized', handleUnauthorized);
        };
    }, []);
    
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
                await login();
                window.dispatchEvent(new Event('auth-ready'));
            } catch (err) {
                console.log("Ошибка", err);
            }
        };
        initAuth();
    }, []);

    if (!mounted) return null;

    const handleSubmit = async () => {
        // Валидация перед отправкой
        const nameValidation = name.trim() ? { isValid: true } : { isValid: false, error: 'Имя обязательно' };
        const phoneValidation = validatePhone(phone);
        
        if (!nameValidation.isValid) {
            // Можно добавить ошибку для имени
            return;
        }
        
        if (!phoneValidation.isValid) {
            setPhoneError(phoneValidation.error);
            return;
        }
        
        // Очищаем номер от форматирования для отправки на сервер
        const cleanPhone = phone.replace(/\D/g, '');
        const formattedPhoneForServer = cleanPhone.startsWith('7') ? `+${cleanPhone}` : `+7${cleanPhone}`;
        
        setIsLoading(true);
        try {
            await simpleLogin(name, formattedPhoneForServer);
            
            window.dispatchEvent(new Event('auth-ready'));
            setShowNameInput(false);
        } catch (err) {
            console.log("Ошибка при логине:", err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && name.trim() && validatePhone(phone).isValid) {
            handleSubmit();
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
                <p className="text-neutral-400 text-sm mb-5">Введите ваши данные, чтобы продолжить</p>

                <input
                    type="text"
                    placeholder="Ваше имя..."
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    onKeyDown={handleKeyDown}
                    autoFocus
                    className="w-full bg-neutral-800 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-neutral-500 text-sm outline-none focus:border-fuchsia-500/50 transition-colors mb-4"
                />

                <div className="relative mb-4">
                    <input
                        type="tel"
                        placeholder="+7 XXX XXX XX XX"
                        value={phone}
                        onChange={handlePhoneChange}
                        onKeyDown={handleKeyDown}
                        className={`w-full bg-neutral-800 border rounded-xl px-4 py-3 text-white placeholder-neutral-500 text-sm outline-none transition-colors ${
                            phoneError 
                                ? 'border-red-500 focus:border-red-500' 
                                : 'border-white/10 focus:border-fuchsia-500/50'
                        }`}
                    />
                    {phoneError && (
                        <p className="text-red-500 text-xs mt-1 ml-2">
                            {phoneError}
                        </p>
                    )}
                </div>

                <button
                    onClick={handleSubmit}
                    disabled={isLoading || !name.trim() || !validatePhone(phone).isValid}
                    className="w-full py-3 bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white rounded-xl font-bold text-sm shadow-[0_0_20px_rgba(192,38,211,0.3)] active:scale-95 transition-transform disabled:opacity-60 disabled:cursor-not-allowed"
                >
                    {isLoading ? 'Входим...' : 'Продолжить'}
                </button>
            </div>
        </div>
    );
};

export default InitTelegramAuth;