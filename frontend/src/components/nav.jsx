// components/nav.jsx
'use client'

import Link from "next/link";
import { useState, Suspense, useEffect } from "react";
import { History, Flame, Grid, Home, LogOut, Menu, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useSearchParams } from 'next/navigation';
import { getUrlWithParams } from '../utils/urlParams';
import { getNonTelegramUserProfile } from '../utils/nonTelegramUser';

// Отдельный компонент, который использует useSearchParams
const NavContent = () => {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const [telegramEnv, setTelegramEnv] = useState(null);
    const [phoneNumber, setPhoneNumber] = useState(
        () => getNonTelegramUserProfile()?.phone_number ?? null
    );
    const searchParams = useSearchParams();

    useEffect(() => {
        setTelegramEnv(!!window.Telegram?.WebApp?.initData);
    }, []);

    useEffect(() => {
        if (telegramEnv) return;
        const onUserMe = (e) => setPhoneNumber(e.detail?.phone_number ?? null);
        window.addEventListener('user-me', onUserMe);
        setPhoneNumber(getNonTelegramUserProfile()?.phone_number ?? null);
        return () => window.removeEventListener('user-me', onUserMe);
    }, [telegramEnv]);

    const showBrowserSession = telegramEnv === false;

    const handleLogout = () => {
        localStorage.removeItem('jwt');
        setPhoneNumber(null);
        window.dispatchEvent(new Event('unauthorized'));
        window.dispatchEvent(new Event('logged-out'));
    };

    const navItems = [
        { label: 'Главный экран', path: '/', icon: <Home size={20} /> },
        { label: 'Конструктор кальяна', path: '/builder', icon: <Flame size={20} /> },
        { label: 'Готовые кальяны', path: '/presets', icon: <Grid size={20} /> },
        { label: 'История заказов', path: '/orders', icon: <History size={20} /> }
    ];

    return (
        <>
            <div className="mx-auto flex h-14 max-w-sm items-center gap-2 px-4">
                <div className="shrink-0 text-lg font-bold text-white tracking-tight">
                    <Link href={getUrlWithParams('/', searchParams)}>
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-fuchsia-500 via-purple-500 to-cyan-500">
                            {process.env.NEXT_PUBLIC_NAME}
                        </span>
                    </Link>
                </div>
                {showBrowserSession && (
                    <div className="flex min-w-0 flex-1 items-center justify-center gap-2">
                        <span className="truncate text-center text-xs text-neutral-300 tabular-nums">
                            {phoneNumber || '—'}
                        </span>
                        <button
                            type="button"
                            onClick={handleLogout}
                            aria-label="Выйти"
                            className="shrink-0 rounded-lg border border-white/15 bg-white/5 p-2 text-neutral-300 transition-colors hover:bg-white/10 hover:text-white active:scale-95"
                        >
                            <LogOut size={18} strokeWidth={1.75} />
                        </button>
                    </div>
                )}
                {!showBrowserSession && <div className="flex-1" aria-hidden />}
                <div className="flex shrink-0 items-center">
                    <button 
                        className="p-2 text-neutral-400 transition-colors"
                        onClick={() => setIsMobileMenuOpen(prev => !prev)}
                    >
                        {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} strokeWidth={1.5}/>}
                    </button>
                </div>
            </div>

            <AnimatePresence>
                {isMobileMenuOpen && (
                    <motion.div
                        key="nav-mobile-menu"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="overflow-hidden border-t border-white/10 bg-neutral-900"
                    >
                        <div className="px-4 py-4 space-y-2">
                            {navItems.map((item) => (
                                <Link
                                    key={item.label}
                                    href={getUrlWithParams(item.path, searchParams)}
                                    onClick={() => setIsMobileMenuOpen(false)}
                                    className="flex items-center gap-3 px-4 py-3 rounded-xl text-neutral-400 hover:bg-white/5 hover:text-white transition-all active:scale-95"
                                >
                                    {item.icon}
                                    <span className="font-medium">{item.label}</span>
                                </Link>
                            ))}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </>
    );
};

// Основной компонент с Suspense
const Nav = () => {
    return (
        <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/10 bg-neutral-950/80 backdrop-blur-md">
            <Suspense fallback={
                <div className="mx-auto flex h-14 max-w-sm items-center justify-between px-4">
                    <div className="text-lg font-bold text-white tracking-tight">
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-fuchsia-500 via-purple-500 to-cyan-500">
                            Loft bar
                        </span>
                    </div>
                    <div className="w-8 h-8 bg-neutral-800 rounded animate-pulse" />
                </div>
            }>
                <NavContent />
            </Suspense>
        </nav>
    );
}
 
export default Nav;