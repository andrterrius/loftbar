'use client'

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Filter } from "lucide-react";
import Nav from "../nav";
import { getPresets, createOrder } from "@/utils/api";

const PresetCardSkeleton = () => (
    <div className="bg-white/5 border border-white/10 rounded-2xl overflow-hidden flex flex-col w-full animate-pulse">
        <div className="p-5 flex-1 flex flex-col space-y-4">
            <div className="space-y-2">
                <div className="h-4 w-3/4 bg-white/10 rounded" />
                <div className="h-3 w-full bg-white/5 rounded" />
                <div className="h-3 w-2/3 bg-white/5 rounded" />
            </div>
            <div className="space-y-2 flex-1">
                {[1, 2, 3].map(i => (
                    <div key={i} className="flex justify-between">
                        <div className="h-3 w-24 bg-white/10 rounded" />
                        <div className="h-3 w-8 bg-white/5 rounded" />
                    </div>
                ))}
            </div>
            <div className="pt-4 border-t border-white/5 flex justify-between items-center">
                <div className="h-6 w-12 bg-white/10 rounded" />
                <div className="h-8 w-20 bg-white/10 rounded-lg" />
            </div>
        </div>
    </div>
);

const MainPresetsPage = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [availablePresets, setAvailablePresets] = useState([]);
    const [presetsLoading, setPresetsLoading] = useState(true);
    const [confirmPreset, setConfirmPreset] = useState(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    useEffect(() => {
        getPresets()
            .then(setAvailablePresets)
            .catch(console.error)
            .finally(() => setPresetsLoading(false));
    }, []);

    const displayedPresets = availablePresets.filter(preset =>
        preset.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        preset.description?.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const handleOrder = async (preset) => {
        setIsSubmitting(true);
        const orderData = {
            table_id: window.Telegram?.WebApp?.initDataUnsafe?.user?.id || 'unknown_table',
            preset_id: preset.id
        };
        try {
            const result = await createOrder(orderData);
            alert(`Заказ #${result.id || ''} успешно оформлен!`);
            setConfirmPreset(null);
        } catch (error) {
            alert('Ошибка при оформлении заказа. Пожалуйста, попробуйте снова.');
            console.error(error);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <section className="min-h-screen bg-neutral-950 flex flex-col items-center w-full overflow-hidden">
            <Nav />
            <div className="w-full max-w-7xl mx-auto px-5 pt-24 pb-12 space-y-8 flex flex-col items-center">
                <div className="w-full flex flex-col items-center gap-6 border-b border-white/10 pb-8 text-center">
                    <div>
                        <h1 className="text-4xl font-bold text-white mb-2">Галерея миксов</h1>
                        <p className="text-neutral-400">Исследуй вкусы сообщества</p>
                    </div>

                    <div className="flex justify-center w-full">
                        <div className="relative group w-full max-w-sm">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-neutral-500 group-focus-within:text-cyan-400 transition-colors" size={18} />
                            <input
                                type="text"
                                placeholder="Поиск миксов..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full bg-neutral-900 border border-white/10 rounded-xl pl-10 pr-4 py-2.5 text-white focus:outline-none focus:border-cyan-500/50 focus:bg-neutral-800 transition-all"
                            />
                        </div>
                    </div>
                </div>

                {presetsLoading ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full">
                        {Array.from({ length: 8 }).map((_, i) => (
                            <PresetCardSkeleton key={i} />
                        ))}
                    </div>
                ) : (
                    <>
                        <motion.div
                            layout
                            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full text-left"
                        >
                            <AnimatePresence mode='popLayout'>
                                {displayedPresets.map((preset) => (
                                    <motion.div
                                        layout
                                        initial={{ opacity: 0, scale: 0.9 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        exit={{ opacity: 0, scale: 0.9 }}
                                        key={preset.id}
                                        style={{
                                            borderColor: preset.hex_color
                                                ? `${preset.hex_color}60`
                                                : 'rgba(255,255,255,0.1)'
                                        }}
                                        className="group relative bg-white/5 border rounded-2xl overflow-hidden hover:-translate-y-1 hover:shadow-xl transition-all flex flex-col w-full"
                                    >
                                        <div className="p-5 flex-1 flex flex-col space-y-4">
                                            <div>
                                                <h3 className="text-lg font-bold text-white group-hover:text-cyan-400 transition-colors">
                                                    {preset.name || 'Без названия'}
                                                </h3>
                                                <p className="text-xs text-neutral-400 mt-1 line-clamp-2 min-h-[2rem]">
                                                    {preset.description || <span className="italic text-neutral-600">Описание не добавлено</span>}
                                                </p>
                                            </div>

                                            <div className="space-y-2 flex-1 min-h-[4rem]">
                                                {(preset.flavors || []).length === 0 ? (
                                                    <p className="text-xs text-neutral-600 italic">Вкусы не указаны</p>
                                                ) : (
                                                    (preset.flavors || []).slice(0, 3).map((ing, i) => (
                                                        <div key={i} className="flex justify-between text-xs text-neutral-300">
                                                            <span>{ing.flavor?.name || <span className="text-neutral-600 italic">Неизвестный вкус</span>}</span>
                                                            <span className="text-neutral-500">{ing.percent}%</span>
                                                        </div>
                                                    ))
                                                )}
                                            </div>

                                            <div className="flex gap-2 flex-wrap">
                                                {preset.bowl && (
                                                    <span className="flex items-center gap-1 px-2 py-1 rounded-full text-[10px] bg-white/5 border border-white/10 text-neutral-400">
                                                        {preset.bowl.icon} {preset.bowl.name}
                                                    </span>
                                                )}
                                                {preset.liquid && (
                                                    <span
                                                        className="flex items-center gap-1 px-2 py-1 rounded-full text-[10px] border text-white"
                                                        style={{
                                                            backgroundColor: preset.liquid.hex_color
                                                                ? `${preset.liquid.hex_color}30`
                                                                : 'rgba(255,255,255,0.05)',
                                                            borderColor: preset.liquid.hex_color
                                                                ? `${preset.liquid.hex_color}70`
                                                                : 'rgba(255,255,255,0.1)',
                                                        }}
                                                    >
                                                        💧 {preset.liquid.name}
                                                    </span>
                                                )}
                                            </div>

                                            <div className="pt-4 border-t border-white/5 flex justify-between items-center mt-auto">
                                                <div className="flex flex-col">
                                                    <span className="text-[10px] text-neutral-500">Цена</span>
                                                    <span className="text-lg font-bold text-white">{preset.price ?? '—'}₽</span>
                                                </div>
                                                <button
                                                    onClick={() => setConfirmPreset(preset)}
                                                    className="px-4 py-2 bg-white/10 hover:bg-fuchsia-600 hover:text-white text-neutral-300 rounded-lg text-sm font-medium transition-all"
                                                >
                                                    Заказать
                                                </button>
                                            </div>
                                        </div>
                                    </motion.div>
                                ))}
                            </AnimatePresence>
                        </motion.div>

                        {displayedPresets.length === 0 && (
                            <div className="py-20 text-center text-neutral-500 w-full">
                                <Filter size={48} className="mx-auto mb-4 opacity-20" />
                                <p>Не найдено миксов по запросу.</p>
                            </div>
                        )}
                    </>
                )}
            </div>

            {confirmPreset && (
                <div
                    className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
                    onClick={(e) => e.target === e.currentTarget && setConfirmPreset(null)}
                >
                    <div className="bg-neutral-900 border border-white/10 rounded-2xl p-6 w-full max-w-sm shadow-2xl">
                        <h3 className="text-lg font-bold text-white mb-1">Подтвердить заказ</h3>
                        <p className="text-neutral-400 text-sm mb-1">Вы хотите заказать:</p>
                        <p className="text-white font-semibold mb-4">{confirmPreset.name}</p>

                        {(confirmPreset.flavors || []).length > 0 && (
                            <div className="space-y-1 mb-4 bg-white/5 rounded-xl p-3">
                                {confirmPreset.flavors.map((ing, i) => (
                                    <div key={i} className="flex justify-between text-xs text-neutral-300">
                                        <span>{ing.flavor?.name || 'Неизвестный вкус'}</span>
                                        <span className="text-neutral-500">{ing.percent}%</span>
                                    </div>
                                ))}
                            </div>
                        )}

                        <div className="flex items-center justify-between mb-6">
                            <span className="text-neutral-500 text-sm">Итого</span>
                            <span className="text-white font-bold text-xl">{confirmPreset.price ?? '—'}₽</span>
                        </div>

                        <div className="flex gap-3">
                            <button
                                onClick={() => setConfirmPreset(null)}
                                disabled={isSubmitting}
                                className="flex-1 py-3 rounded-xl bg-white/5 border border-white/10 text-neutral-400 hover:bg-white/10 transition-all text-sm font-medium disabled:opacity-50"
                            >
                                Отмена
                            </button>
                            <button
                                onClick={() => handleOrder(confirmPreset)}
                                disabled={isSubmitting}
                                className="flex-1 py-3 rounded-xl bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white font-bold text-sm shadow-[0_0_20px_rgba(192,38,211,0.3)] active:scale-95 transition-transform disabled:opacity-60"
                            >
                                {isSubmitting ? 'Отправка...' : 'Заказать'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </section>
    );
};

export default MainPresetsPage;