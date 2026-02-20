'use client'
import { useEffect } from "react";

const InitTelegramAuth = () => {
    useEffect(() => {
        const initAuth = async () => {
        const existingToken = localStorage.getItem('jwt') 
        if (existingToken) {
            return;
        }
        let tgDataInit = window.Telegram?.WebApp?.initData;

        if (!tgDataInit) {
            console.log("Не открыто в Telegram");
            return;
        }

        try {
            const res = await fetch('api/auth/tg', {
                method: "POST",
                headers: 
                    {
                        "Content-Type": "application/json"
                    },
                body: JSON.stringify({
                    initData: tgDataInit
                })
            })
            const data = await res.json();
            localStorage.setItem('jwt', data.token);
        } catch (err) {
            console.log("Ошибка", err)
        }
        }
        initAuth()
    }, [])
    return ( 
        null
     );
}
 
export default InitTelegramAuth;