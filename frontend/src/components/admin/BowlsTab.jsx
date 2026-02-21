'use client'

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const BowlsTab = ({ bowls, onAdd, onDelete }) => {
    const [showForm, setShowForm] = useState(false);
    const [form, setForm] = useState({ type: '', icon: '', isFruit: false });
    const [error, setError] = useState('');

    const handleAdd = () => {
        if (!form.type.trim()) return setError('Введите название чаши');
        if (!form.icon.trim()) return setError('Введите иконку (эмодзи)');
        if (bowls.find(b => b.type.toLowerCase() === form.type.trim().toLowerCase())) {
            return setError('Чаша с таким названием уже существует');
        }

        onAdd({ type: form.type.trim(), icon: form.icon.trim(), isFruit: form.isFruit });
        setForm({ type: '', icon: '', isFruit: false });
        setError('');
        setShowForm(false);
    };

    const handleCancel = () => {
        setForm({ type: '', icon: '', isFruit: false });
        setError('');
        setShowForm(false);
    };

    return (
        <div className="space-y-6">
            {/* Header row */}
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-lg font-semibold text-white">Чаши</h2>
                    <p className="text-xs text-neutral-500 mt-0.5">{bowls.length} чаш добавлено</p>
                </div>
                {!showForm && (
                    <button
                        onClick={() => setShowForm(true)}
                        className="flex items-center gap-2 px-4 py-2 text-sm font-medium bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 rounded-xl hover:bg-cyan-500/20 transition-colors"
                    >
                        <span className="text-base leading-none">+</span>
                        Добавить чашу
                    </button>
                )}
            </div>

            {/* Add Form */}
            <AnimatePresence>
                {showForm && (
                    <motion.div
                        initial={{ opacity: 0, y: -8 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -8 }}
                        transition={{ duration: 0.2 }}
                        className="bg-neutral-900 border border-white/10 rounded-2xl p-5 space-y-4"
                    >
                        <h3 className="text-sm font-medium text-white">Новая чаша</h3>

                        <div className="grid grid-cols-2 gap-3">
                            {/* Icon */}
                            <div className="space-y-1.5">
                                <label className="text-xs text-neutral-400">Иконка (эмодзи)</label>
                                <input
                                    type="text"
                                    value={form.icon}
                                    onChange={e => setForm(prev => ({ ...prev, icon: e.target.value }))}
                                    placeholder="🏺"
                                    maxLength={4}
                                    className="w-full bg-neutral-800 border border-white/10 rounded-xl px-3 py-2.5 text-white text-sm placeholder-neutral-600 focus:outline-none focus:border-cyan-500/50 transition-colors"
                                />
                            </div>

                            {/* Name */}
                            <div className="space-y-1.5">
                                <label className="text-xs text-neutral-400">Название</label>
                                <input
                                    type="text"
                                    value={form.type}
                                    onChange={e => setForm(prev => ({ ...prev, type: e.target.value }))}
                                    placeholder="Classic"
                                    className="w-full bg-neutral-800 border border-white/10 rounded-xl px-3 py-2.5 text-white text-sm placeholder-neutral-600 focus:outline-none focus:border-cyan-500/50 transition-colors"
                                />
                            </div>
                        </div>

                        {/* isFruit toggle */}
                        <button
                            onClick={() => setForm(prev => ({ ...prev, isFruit: !prev.isFruit }))}
                            className={`flex items-center gap-2.5 px-3 py-2 rounded-xl text-sm transition-colors border ${
                                form.isFruit
                                    ? 'bg-orange-500/10 border-orange-500/30 text-orange-400'
                                    : 'bg-neutral-800 border-white/10 text-neutral-400 hover:text-neutral-300'
                            }`}
                        >
                            <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center transition-colors ${
                                form.isFruit ? 'border-orange-400 bg-orange-400' : 'border-neutral-600'
                            }`}>
                                {form.isFruit && <div className="w-1.5 h-1.5 bg-white rounded-full" />}
                            </div>
                            Фруктовая чаша
                        </button>

                        {error && (
                            <p className="text-xs text-red-400">{error}</p>
                        )}

                        <div className="flex gap-2 pt-1">
                            <button
                                onClick={handleAdd}
                                className="flex-1 py-2.5 text-sm font-medium bg-cyan-500 text-neutral-950 rounded-xl hover:bg-cyan-400 transition-colors"
                            >
                                Добавить
                            </button>
                            <button
                                onClick={handleCancel}
                                className="flex-1 py-2.5 text-sm text-neutral-400 bg-neutral-800 rounded-xl hover:text-white transition-colors"
                            >
                                Отмена
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Bowl list */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <AnimatePresence>
                    {bowls.map((bowl) => (
                        <motion.div
                            key={bowl.type}
                            initial={{ opacity: 0, scale: 0.96 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.96 }}
                            transition={{ duration: 0.15 }}
                            className="flex items-center justify-between px-4 py-3 bg-neutral-900 border border-white/10 rounded-2xl group"
                        >
                            <div className="flex items-center gap-3">
                                <span className="text-2xl">{bowl.icon}</span>
                                <div>
                                    <p className="text-sm font-medium text-white">{bowl.type}</p>
                                    <p className="text-xs text-neutral-500">
                                        {bowl.isFruit ? 'Фруктовая' : 'Обычная'}
                                    </p>
                                </div>
                            </div>

                            <button
                                onClick={() => onDelete(bowl.type)}
                                className="p-2 text-neutral-600 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-all"
                                title="Удалить"
                            >
                                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M9 7h6m2 0a1 1 0 00-1-1h-4a1 1 0 00-1 1H5" />
                                </svg>
                            </button>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>

            {bowls.length === 0 && (
                <div className="text-center py-16 text-neutral-600">
                    <p className="text-4xl mb-3">🏺</p>
                    <p className="text-sm">Нет чаш. Добавьте первую.</p>
                </div>
            )}
        </div>
    );
};

export default BowlsTab;