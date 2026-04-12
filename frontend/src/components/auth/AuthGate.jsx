'use client'
import { useState, useEffect } from "react";
import { ToastProvider } from "@/components/shared/ToastProvider";
import { getMe } from "@/utils/api";
import { setNonTelegramUserProfile } from "@/utils/nonTelegramUser";

async function loadMeIfBrowserSession() {
    const isTelegramMiniApp =
        typeof window !== 'undefined' && !!window.Telegram?.WebApp?.initData;
    if (isTelegramMiniApp) return;
    const jwt = localStorage.getItem('jwt');
    if (!jwt) return;
    try {
        const me = await getMe();
        if (me) {
            setNonTelegramUserProfile(me);
            window.dispatchEvent(new CustomEvent('user-me', { detail: me }));
        }
    } catch {
        /* сеть или прочие ошибки */
    }
}

export default function AuthGate({ children }) {
    const [isReady, setIsReady] = useState(false);
    const [authState, setAuthState] = useState(0);

    useEffect(() => {
        let cancelled = false;

        const boot = async () => {
            const jwt = localStorage.getItem('jwt');
            if (jwt) {
                await loadMeIfBrowserSession();
                if (!cancelled && localStorage.getItem('jwt')) {
                    setIsReady(true);
                }
            }
        };

        boot();

        const handler = async () => {
            await loadMeIfBrowserSession();
            if (!cancelled && localStorage.getItem('jwt')) {
                setIsReady(true);
                setAuthState((prev) => prev + 1);
            }
        };

        const loggedOutHandler = () => {
            setNonTelegramUserProfile(null);
            setIsReady(false);
            setAuthState((prev) => prev + 1);
        };

        window.addEventListener('auth-ready', handler);
        window.addEventListener('logged-out', loggedOutHandler);

        return () => {
            cancelled = true;
            window.removeEventListener('auth-ready', handler);
            window.removeEventListener('logged-out', loggedOutHandler);
        };
    }, []);

    if (!isReady) {
        return null;
    }

    return (
        <div key={authState}>
            <ToastProvider>
                {children}
            </ToastProvider>
        </div>
    );
}