'use client'
import { useState, useEffect } from "react";
import { ToastProvider } from "@/components/shared/ToastProvider";

export default function AuthGate({ children }) {
    const [isReady, setIsReady] = useState(false);
    const [authState, setAuthState] = useState(0);

    useEffect(() => {
        if (localStorage.getItem('jwt')) {
            setIsReady(true);
        }

        const handler = () => {
            setIsReady(true);
            // Увеличиваем ключ, чтобы перерисовать детей
            setAuthState(prev => prev + 1);
        };

        window.addEventListener('auth-ready', handler);
        
        return () => window.removeEventListener('auth-ready', handler);
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