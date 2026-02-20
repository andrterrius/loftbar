'use client'

import { useState } from "react";
import { motion } from "framer-motion";
import { Lock, LogIn } from "lucide-react";

const AdminLogin = ({ onLogin }) => {
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        await new Promise(r => setTimeout(r, 800));
        if (password === 'admin') {
            onLogin();
        } else {
            setError('Неверный пароль');
        }
        setIsLoading(false);
    };

    return (
        <div className="flex items-center justify-center min-h-[80vh] px-4">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="w-full max-w-sm p-8 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md text-center"
            >
                <div className="w-16 h-16 rounded-full bg-white/10 flex items-center justify-center mx-auto mb-6">
                    <Lock className="text-cyan-400" size={28} />
                </div>
                <h2 className="text-2xl font-bold text-white mb-1">Вход в Админку</h2>
                <p className="text-neutral-400 text-sm mb-6">Введите пароль для доступа</p>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <input
                        type="password"
                        placeholder="Пароль"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="w-full bg-neutral-900 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-cyan-500 transition-colors placeholder-neutral-600"
                    />
                    {error && <p className="text-red-400 text-sm">{error}</p>}
                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full py-3 bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white rounded-xl font-bold transition-all flex items-center justify-center gap-2 disabled:opacity-50 active:scale-95"
                    >
                        {isLoading
                            ? <span className="animate-spin w-5 h-5 border-2 border-white/30 border-t-white rounded-full" />
                            : <><LogIn size={18} /> Войти</>
                        }
                    </button>
                </form>
            </motion.div>
        </div>
    );
};

export default AdminLogin;
