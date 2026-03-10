'use client'
import { apiRequest } from "@/utils/api";
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
                const res = await apiRequest('/users/login', {
                    method: "POST",
                    headers: { "X-Init-Data": tgDataInit }
                })
                const data = await res.json();
                localStorage.setItem('jwt', data.access_token);
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