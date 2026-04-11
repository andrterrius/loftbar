'use client'

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { X } from "lucide-react";

const FlavorCard = ({ item, percentage, onRemove, onChange, color, isLocked = false }) => {
    const [inputValue, setInputValue] = useState(String(Math.round(percentage)));
    const [isFocused, setIsFocused] = useState(false);

    // Обновляем отображение только когда инпут не в фокусе
    useEffect(() => {
        if (!isFocused) {
            setInputValue(String(Math.round(percentage)));
        }
    }, [percentage, isFocused]);

    const handleCommit = () => {
        if (isLocked) return;
        setIsFocused(false);
        const parsed = parseInt(inputValue, 10);
        if (isNaN(parsed) || inputValue === '') {
            setInputValue(String(Math.round(percentage)));
            return;
        }
        const clamped = Math.max(1, Math.min(100, parsed));
        setInputValue(String(clamped));
        onChange(clamped, false); // ← ввод с клавиатуры: без авто-нормализации
    };

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="relative p-4 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm group hover:border-white/20 transition-all text-left"
        >
            <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-3">
                    <div
                        style={{
                            width: '40px', height: '40px', minWidth: '40px',
                            flex: 'none', borderRadius: '50%', overflow: 'hidden',
                            backgroundColor: color || '#ccc',
                            backgroundImage: item.image_url ? `url(${item.image_url})` : 'none',
                            backgroundSize: 'cover', backgroundPosition: 'center',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            fontSize: '14px', fontWeight: 'bold', color: 'rgba(0,0,0,0.6)',
                        }}
                    >
                        {!item.image_url && item.name[0]}
                    </div>
                    <div>
                        <h3 className="font-bold text-white text-lg leading-tight">{item.name}</h3>
                    </div>
                </div>
                <button onClick={onRemove} className="text-neutral-500 hover:text-red-400 transition-colors ml-2 mt-1">
                    <X size={18} />
                </button>
            </div>

            <div className="space-y-2">
                <div className="flex justify-between items-center text-sm">
                    <span className="text-neutral-300">Процент</span>

                    {/* Редактируемый процент */}
                    <div className="relative flex items-center">
                        <input
                            type="text"
                            inputMode="numeric"
                            value={inputValue}
                            readOnly={isLocked}
                            onFocus={(e) => {
                                if (isLocked) return;
                                setIsFocused(true);
                                e.target.select();
                            }}
                            onChange={(e) => {
                                if (isLocked) return;
                                const val = e.target.value.replace(/\D/g, '');
                                setInputValue(val);
                            }}
                            onBlur={handleCommit}
                            onKeyDown={(e) => {
                                if (isLocked) return;
                                if (e.key === 'Enter') e.target.blur();
                                if (e.key === 'Escape') {
                                    setInputValue(String(Math.round(percentage)));
                                    setIsFocused(false);
                                    e.target.blur();
                                }
                            }}
                            className={`w-14 text-center bg-neutral-800 border border-white/10 rounded-lg py-0.5 pr-4 text-sm font-mono text-cyan-400 outline-none focus:border-cyan-500/60 transition-colors ${isLocked ? 'opacity-60 cursor-not-allowed' : ''}`}
                        />
                        <span className="absolute right-2 text-xs text-neutral-500 pointer-events-none">%</span>
                    </div>
                </div>

                {/* Слайдер — перераспределяет остальные автоматически */}
                <input
                    type="range"
                    min="1"
                    max="99"
                    value={isFocused ? (parseInt(inputValue) || Math.round(percentage)) : Math.round(percentage)}
                    disabled={isLocked}
                    onChange={(e) => {
                        if (isLocked) return;
                        const val = parseInt(e.target.value);
                        setInputValue(String(val));
                        onChange(val, true); // ← ползунок: авто-нормализация
                    }}
                    className={`w-full h-2 rounded-lg appearance-none ${isLocked ? 'cursor-not-allowed opacity-60' : 'cursor-pointer'}`}
                    style={{
                        background: `linear-gradient(to right, ${color} 0%, ${color} ${Math.round(percentage)}%, #262626 ${Math.round(percentage)}%, #262626 100%)`
                    }}
                />
            </div>

            <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-bl from-white/5 to-transparent rounded-tr-xl pointer-events-none" />
            <div
                className="absolute bottom-0 left-0 w-full h-1 rounded-b-xl opacity-50"
                style={{ backgroundColor: color }}
            />
        </motion.div>
    );
}

export default FlavorCard;