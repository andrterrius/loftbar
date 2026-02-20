'use client'

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Plus, Trash2, Droplets } from "lucide-react";

const LiquidsTab = ({ liquids, onAdd, onRemove }) => {
    const [isAdding, setIsAdding] = useState(false);
    const [form, setForm] = useState({ name: '', description: '' });

    const handleAdd = () => {
        if (!form.name.trim()) return;
        onAdd({ ...form, id: Date.now().toString() });
        setForm({ name: '', description: '' });
        setIsAdding(false);
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold text-white">Жидкости <span className="text-neutral-500 font-normal text-base">({liquids.length})</span></h2>
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
                        <div className="bg-white/5 border border-white/10 rounded-xl p-5 grid grid-cols-1 sm:grid-cols-3 gap-3">
                            <input
                                placeholder="Название"
                                value={form.name}
                                onChange={e => setForm({ ...form, name: e.target.value })}
                                className="bg-neutral-900 border border-white/10 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-cyan-500 transition-colors placeholder-neutral-600"
                            />
                            <input
                                placeholder="Описание (необязательно)"
                                value={form.description}
                                onChange={e => setForm({ ...form, description: e.target.value })}
                                className="bg-neutral-900 border border-white/10 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-cyan-500 transition-colors placeholder-neutral-600"
                            />
                            <button
                                onClick={handleAdd}
                                className="bg-green-600 hover:bg-green-500 text-white rounded-lg font-medium py-2.5 text-sm transition-colors active:scale-95"
                            >
                                Сохранить
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {liquids.map(liquid => (
                    <motion.div
                        layout
                        key={liquid.id}
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="flex items-center justify-between p-4 bg-white/5 border border-white/10 rounded-xl hover:border-white/20 transition-all group"
                    >
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-full bg-cyan-500/10 flex items-center justify-center shrink-0">
                                <Droplets size={18} className="text-cyan-400" />
                            </div>
                            <div>
                                <p className="font-medium text-white text-sm">{liquid.name}</p>
                                {liquid.description && <p className="text-xs text-neutral-500">{liquid.description}</p>}
                            </div>
                        </div>
                        <button
                            onClick={() => onRemove(liquid.id)}
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

export default LiquidsTab;
