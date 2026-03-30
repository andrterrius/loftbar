'use client'

import { useEffect, useState } from "react";
import { Search, Filter } from "lucide-react";
import Nav from "../nav";
import { getPresets, createOrder } from "@/utils/api";
import { PRESETS } from "../moks/moks";

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
    const [successOrderId, setSuccessOrderId] = useState(null);

    useEffect(() => {
        getPresets()
            .then(data => {
                if (!data || data.length === 0) throw new Error();
                setAvailablePresets(data);
            })
            .catch(() => {
                setAvailablePresets(PRESETS);
            })
            .finally(() => setPresetsLoading(false));
    }, []);

    const displayedPresets = availablePresets.filter(preset =>
        preset.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        preset.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (preset.flavors || []).some(flavor => flavor.flavor?.name.toLowerCase().includes(searchQuery.toLowerCase()))
    );

    const handleOrder = async (preset) => {
        setIsSubmitting(true);
        const orderData = {
            table_id: window.Telegram?.WebApp?.initDataUnsafe?.start_param
                || new URLSearchParams(window.location.search).get('table_id')
                || 'unknown_table',
            preset_id: preset.id
        };
        try {
            const result = await createOrder(orderData);
            setConfirmPreset(null);
            setSuccessOrderId(result.daily_number || '');
            setTimeout(() => window.Telegram?.WebApp?.close(), 4000);
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
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full text-left">
                            {displayedPresets.map((preset) => (
                                <div
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
                                            <h3 className="text-base font-bold tracking-tight text-white group-hover:text-cyan-400 transition-colors leading-snug">
                                                {preset.name || 'Без названия'}
                                            </h3>
                                            <p className="text-[11px] italic text-neutral-600 mt-1.5 line-clamp-2 min-h-[2rem] leading-relaxed">
                                                {preset.description || 'Описание не добавлено'}
                                            </p>
                                        </div>

                                        <div className="space-y-1.5 flex-1 min-h-[4rem]">
                                            {(preset.flavors || []).length === 0 ? (
                                                <p className="text-xs text-neutral-600 italic">Вкусы не указаны</p>
                                            ) : (
                                                (preset.flavors || []).map((ing, i) => (
                                                    <div key={i} className="flex justify-between items-center">
                                                        <span className="text-[14px] font-semibold text-white tracking-tight">{ing.flavor?.name || <span className="text-neutral-600 italic">Неизвестный вкус</span>}</span>
                                                        <span className="text-[12px] font-mono text-neutral-300 tabular-nums">{ing.percent}%</span>
                                                    </div>
                                                ))
                                            )}
                                        </div>

                                        <div className="flex gap-2 flex-wrap">
                                            {preset.bowl && (
                                                <div className="flex flex-col gap-1">
                                                    <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium pl-1">Чаша</span>
                                                    <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[12px] font-semibold bg-fuchsia-500/15 border border-fuchsia-500/30 text-fuchsia-300">
                                                        <span className="text-base leading-none">{preset.bowl.icon}</span> {preset.bowl.name}
                                                    </span>
                                                </div>
                                            )}
                                            {preset.liquid && (
                                                <div className="flex flex-col gap-1">
                                                    <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium pl-1">Колба</span>
                                                    <span
                                                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[12px] font-semibold border text-cyan-300"
                                                        style={{
                                                            backgroundColor: preset.liquid.hex_color
                                                                ? `${preset.liquid.hex_color}20`
                                                                : 'rgba(6,182,212,0.1)',
                                                            borderColor: preset.liquid.hex_color
                                                                ? `${preset.liquid.hex_color}50`
                                                                : 'rgba(6,182,212,0.3)',
                                                        }}
                                                    >
                                                        <span className="text-base leading-none">💧</span> {preset.liquid.name}
                                                    </span>
                                                </div>
                                            )}
                                        </div>

                                        <div className="pt-3 border-t border-white/5 flex justify-between items-center mt-auto">
                                            <div className="flex flex-col gap-0.5">
                                                <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium">Цена</span>
                                                <span className="text-xl font-bold text-white tracking-tight leading-none">{preset.price ?? '—'}<span className="text-neutral-400 text-base font-semibold">₽</span></span>
                                            </div>
                                            <button
                                                onClick={() => setConfirmPreset(preset)}
                                                className="px-5 py-2.5 hover:bg-fuchsia-600 hover:text-white text-white rounded-xl text-[13px] font-semibold tracking-tight transition-all border border-white/15 hover:border-fuchsia-500 bg-white/8"
                                            >
                                                Заказать
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

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
                        <h3 className="text-xl font-bold tracking-tight text-white mb-0.5">Подтвердить заказ</h3>
                        <p className="text-[11px] uppercase tracking-widest text-neutral-600 font-medium mb-1">Вы заказываете</p>
                        <p className="text-white font-bold text-base tracking-tight mb-4">{confirmPreset.name}</p>

                        {(confirmPreset.flavors || []).length > 0 && (
                            <div className="space-y-2 mb-4 bg-white/5 rounded-xl p-3">
                                {confirmPreset.flavors.map((ing, i) => (
                                    <div key={i} className="flex justify-between items-center">
                                        <span className="text-[14px] font-semibold text-white">{ing.flavor?.name || 'Неизвестный вкус'}</span>
                                        <span className="font-mono text-[12px] text-neutral-300 tabular-nums">{ing.percent}%</span>
                                    </div>
                                ))}
                            </div>
                        )}

                        <div className="flex gap-2 flex-wrap mb-4">
                            {confirmPreset.bowl && (
                                <div className="flex flex-col gap-1">
                                    <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium pl-1">Чаша</span>
                                    <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[12px] font-semibold bg-fuchsia-500/15 border border-fuchsia-500/30 text-fuchsia-300">
                                        <span className="text-base leading-none">{confirmPreset.bowl.icon}</span> {confirmPreset.bowl.name}
                                    </span>
                                </div>
                            )}
                            {confirmPreset.liquid && (
                                <div className="flex flex-col gap-1">
                                    <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium pl-1">Колба</span>
                                    <span
                                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[12px] font-semibold border text-cyan-300"
                                        style={{
                                            backgroundColor: confirmPreset.liquid.hex_color ? `${confirmPreset.liquid.hex_color}20` : 'rgba(6,182,212,0.1)',
                                            borderColor: confirmPreset.liquid.hex_color ? `${confirmPreset.liquid.hex_color}50` : 'rgba(6,182,212,0.3)',
                                        }}
                                    >
                                        <span className="text-base leading-none">💧</span> {confirmPreset.liquid.name}
                                    </span>
                                </div>
                            )}
                        </div>


                        <div className="flex items-center justify-between mb-6 pt-4 border-t border-white/5">
                            <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium">Итого</span>
                            <span className="text-white font-bold text-2xl tracking-tight leading-none">{confirmPreset.price ?? '—'}<span className="text-neutral-400 text-lg font-semibold">₽</span></span>
                        </div>

                        <div className="flex gap-3">
                            <button
                                onClick={() => setConfirmPreset(null)}
                                disabled={isSubmitting}
                                className="flex-1 py-3 rounded-xl bg-white/5 border border-white/10 text-neutral-400 hover:bg-white/10 transition-all text-[13px] font-semibold disabled:opacity-50"
                            >
                                Отмена
                            </button>
                            <button
                                onClick={() => handleOrder(confirmPreset)}
                                disabled={isSubmitting}
                                className="flex-1 py-3 rounded-xl bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white font-bold text-[13px] tracking-tight shadow-[0_0_20px_rgba(192,38,211,0.3)] active:scale-95 transition-transform disabled:opacity-60"
                            >
                                {isSubmitting ? 'Отправка...' : 'Заказать'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
            

            {successOrderId !== null && (
                <div className="fixed inset-0 z-[70] flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
                    <div className="bg-neutral-900 border border-white/10 rounded-2xl p-8 w-full max-w-sm shadow-2xl flex flex-col items-center text-center">
                        <div className="w-16 h-16 rounded-full bg-green-500/20 flex items-center justify-center mb-4">
                            <span className="text-3xl">✅</span>
                        </div>
                        <h3 className="text-xl font-bold text-white mb-2">Заказ принят!</h3>
                        <p className="text-neutral-400 text-sm mb-1">
                            {successOrderId ? `Заказ #${successOrderId}` : 'Ваш заказ'} успешно оформлен.
                        </p>
                        <p className="text-neutral-500 text-xs mb-6">Ожидайте — ваш микс уже готовится 🔥</p>
                        <button
                            onClick={() => window.Telegram?.WebApp?.close()}
                            className="w-full py-3 rounded-xl bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white font-bold text-sm shadow-[0_0_20px_rgba(192,38,211,0.3)] active:scale-95 transition-transform"
                        >
                            Закрыть
                        </button>
                    </div>
                </div>
            )}
        </section>
    );
};

export default MainPresetsPage;