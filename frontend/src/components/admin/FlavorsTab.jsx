'use client'

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Plus, Trash2 } from "lucide-react";

const CATEGORIES = ['Fruity', 'Sweet', 'Mint', 'Spicy', 'Floral', 'Dessert', 'Tobacco', 'Classic', 'Berry', 'Tropical', 'Minty'];

const FlavorsTab = ({ flavors, onAdd, onRemove }) => {
    const [isAdding, setIsAdding] = useState(false);
    const [form, setForm] = useState({ name: '', brand: '', category: 'Fruity', color: '#dc2626' });

    const handleAdd = () => {
        if (!form.name.trim() || !form.brand.trim()) return;
        onAdd({ ...form, id: Date.now().toString() });
        setForm({ name: '', brand: '', category: 'Fruity', color: '#dc2626' });
        setIsAdding(false);
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold text-white">Вкусы <span className="text-neutral-500 font-normal text-base">({flavors.length})</span></h2>
                <button
                    onClick={() => setIsAdding(prev => !prev)}
                    className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg transition-colors text-sm font-medium active:scale-95"
                >
                    <Plus size={16} /> Добавить
                </button>
            </div>

            <AnimatePresence>
                {isAdding && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="overflow-hidden"
                    >
                        <div className="bg-white/5 border border-white/10 rounded-xl p-5 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
                            <input
                                placeholder="Название"
                                value={form.name}
                                onChange={e => setForm({ ...form, name: e.target.value })}
                                className="bg-neutral-900 border border-white/10 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-cyan-500 transition-colors placeholder-neutral-600"
                            />
                            <input
                                placeholder="Бренд"
                                value={form.brand}
                                onChange={e => setForm({ ...form, brand: e.target.value })}
                                className="bg-neutral-900 border border-white/10 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-cyan-500 transition-colors placeholder-neutral-600"
                            />
                            <select
                                value={form.category}
                                onChange={e => setForm({ ...form, category: e.target.value })}
                                className="bg-neutral-900 border border-white/10 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-cyan-500 transition-colors"
                            >
                                {CATEGORIES.map(cat => <option key={cat} value={cat}>{cat}</option>)}
                            </select>
                            <div className="flex gap-2 items-center">
                                <div className="relative">
                                    <input
                                        type="color"
                                        value={form.color}
                                        onChange={e => setForm({ ...form, color: e.target.value })}
                                        className="h-10 w-10 cursor-pointer rounded-lg overflow-hidden border border-white/10 bg-transparent"
                                    />
                                </div>
                                <button
                                    onClick={handleAdd}
                                    className="flex-1 bg-green-600 hover:bg-green-500 text-white rounded-lg font-medium py-2.5 text-sm transition-colors active:scale-95"
                                >
                                    Сохранить
                                </button>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {flavors.map(flavor => (
                    <motion.div
                        layout
                        key={flavor.id}
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.9 }}
                        className="flex items-center justify-between p-4 bg-white/5 border border-white/10 rounded-xl hover:bg-white/8 hover:border-white/20 transition-all group"
                    >
                        <div className="flex items-center gap-3">
                            <div
                                className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold text-black/60 shrink-0"
                                style={{ backgroundColor: flavor.color }}
                            >
                                {flavor.name[0]}
                            </div>
                            <div>
                                <p className="font-medium text-white text-sm">{flavor.name}</p>
                                <p className="text-xs text-neutral-500">{flavor.brand} · {flavor.category}</p>
                            </div>
                        </div>
                        <button
                            onClick={() => onRemove(flavor.id)}
                            className="p-2 text-neutral-600 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-all opacity-0 group-hover:opacity-100"
                        >
                            <Trash2 size={16} />
                        </button>
                    </motion.div>
                ))}
            </div>
        </div>
    );
};

export default FlavorsTab;
