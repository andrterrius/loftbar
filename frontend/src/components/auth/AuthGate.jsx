'use client'
import { useState, useEffect } from "react";

export default function AuthGate({ children }) {
    const [isReady, setIsReady] = useState(false);

    useEffect(() => {
        if (localStorage.getItem('jwt')) {
            setIsReady(true);
            return;
        }
        const handler = () => setIsReady(true);
        window.addEventListener('auth-ready', handler);
        return () => window.removeEventListener('auth-ready', handler);
    }, []);

    return isReady ? children : null;
}