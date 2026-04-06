'use client'

import { useEffect, useState } from "react";
import { Search, Filter, ChevronDown } from "lucide-react";
import Nav from "../nav";
import { getPresets, createOrder } from "@/utils/api";
import { PRESETS } from "../moks/moks";
import { usePresetOrderConfirmation } from "@/components/orders/usePresetOrderConfirmation";

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
    const [expandedPresetId, setExpandedPresetId] = useState(null);
    const { openConfirm, ConfirmModal, SuccessModal } = usePresetOrderConfirmation({ createOrder });

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

    useEffect(() => {
        if (expandedPresetId) {
            setTimeout(() => {
                const expandedElement = document.getElementById(`preset-${expandedPresetId}`);
                if (expandedElement) {
                    expandedElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start',
                        inline: 'nearest'
                    });
                }
            }, 100);
        }
    }, [expandedPresetId]);

    const displayedPresets = availablePresets.filter(preset =>
        preset.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        preset.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (preset.flavors || []).some(flavor => flavor.flavor?.name.toLowerCase().includes(searchQuery.toLowerCase()))
    );

    const togglePreset = (presetId) => {
        setExpandedPresetId(expandedPresetId === presetId ? null : presetId);
    };

    const getStrengthLabel = (strength) => {
        return { label: strength, color: 'text-neutral-400', bg: 'bg-neutral-500/10', border: 'border-neutral-500/30' };
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
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full">
                            {displayedPresets.map((preset) => {
                                const isOpen = expandedPresetId === preset.id;
                                const strengthInfo = getStrengthLabel(preset.strength);

                                return (
                                    <div
                                        id={`preset-${preset.id}`}
                                        key={preset.id}
                                        className="relative bg-white/5 border rounded-2xl hover:bg-white/8 flex flex-col h-full"
                                        style={{
                                            borderColor: preset.hex_color
                                                ? `${preset.hex_color}60`
                                                : 'rgba(255,255,255,0.1)'
                                        }}
                                    >
                                        {/* Card Header - Always visible */}
                                        <button
                                            onClick={() => togglePreset(preset.id)}
                                            className="w-full p-5 flex justify-between items-center gap-3 hover:bg-white/5 transition-colors group text-left"
                                        >
                                            <div className="flex-1">
                                                <h3 className="text-base font-bold text-white group-hover:text-cyan-400 transition-colors leading-snug">
                                                    {preset.name || 'Без названия'}
                                                </h3>
                                            </div>
                                            <div className="flex flex-col items-end gap-1 flex-shrink-0">
                                                <div className="flex items-center gap-3">
                                                    <span className="text-xl font-bold text-white tracking-tight leading-none">
                                                        {preset.price ?? '—'}<span className="text-neutral-400 text-base font-semibold">₽</span>
                                                    </span>
                                                    <ChevronDown
                                                        className={`w-5 h-5 text-neutral-400 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
                                                    />
                                                </div>
                                            </div>
                                        </button>

                                        {/* Expanded Content - Absolute positioning */}
                                        {isOpen && (
                                            <div className="absolute left-0 right-0 top-full mt-2 z-20 bg-neutral-900 border border-white/10 rounded-xl p-5 shadow-2xl animate-fadeIn">
                                                <div className="space-y-4">
                                                    {/* Full Description */}
                                                    {preset.description && (
                                                        <div>
                                                            <p className="text-sm text-neutral-400 leading-relaxed">
                                                                {preset.description}
                                                            </p>
                                                        </div>
                                                    )}

                                                    {/* Flavors */}
                                                    <div>
                                                        <h4 className="text-xs uppercase tracking-wider text-neutral-500 font-semibold mb-3">
                                                            Состав микса
                                                        </h4>
                                                        <div className="space-y-2">
                                                            {(preset.flavors || []).length === 0 ? (
                                                                <p className="text-xs text-neutral-600 italic">Вкусы не указаны</p>
                                                            ) : (
                                                                (preset.flavors || []).map((ing, i) => (
                                                                    <div key={i} className="flex justify-between items-center py-1 border-b border-white/5">
                                                                        <span className="text-sm font-medium text-white">
                                                                            {ing.flavor?.name || <span className="text-neutral-600 italic">Неизвестный вкус</span>}
                                                                        </span>
                                                                        <span className="text-sm font-mono text-cyan-400 tabular-nums font-semibold">
                                                                            {ing.percent}%
                                                                        </span>
                                                                    </div>
                                                                ))
                                                            )}
                                                        </div>
                                                    </div>

                                                    <div>
                                                        <h4 className="text-xs uppercase tracking-wider text-neutral-500 font-semibold mb-2">
                                                            Крепость
                                                        </h4>
                                                        <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-semibold ${strengthInfo.bg} ${strengthInfo.border} border`}>
                                                            <span className={`text-base ${strengthInfo.color}`}>⚡</span>
                                                            <span className={strengthInfo.color}>{strengthInfo.label}</span>
                                                        </div>
                                                    </div>

                                                    {/* Bowl and Liquid */}
                                                    <div className="flex flex-wrap gap-2 pt-2">
                                                        {preset.bowl && (
                                                            <div className="flex flex-col gap-1 flex-1 min-w-[100px]">
                                                                <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium pl-1">Чаша</span>
                                                                <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-fuchsia-500/15 border border-fuchsia-500/30 text-fuchsia-300">
                                                                    <span className="text-base">{preset.bowl.icon}</span>
                                                                    <span className="truncate">{preset.bowl.name}</span>
                                                                </span>
                                                            </div>
                                                        )}
                                                        {preset.liquid && (
                                                            <div className="flex flex-col gap-1 flex-1 min-w-[100px]">
                                                                <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium pl-1">Колба</span>
                                                                <span
                                                                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border text-cyan-300"
                                                                    style={{
                                                                        backgroundColor: preset.liquid.hex_color
                                                                            ? `${preset.liquid.hex_color}20`
                                                                            : 'rgba(6,182,212,0.1)',
                                                                        borderColor: preset.liquid.hex_color
                                                                            ? `${preset.liquid.hex_color}50`
                                                                            : 'rgba(6,182,212,0.3)',
                                                                    }}
                                                                >
                                                                    <span className="text-base">💧</span>
                                                                    <span className="truncate">{preset.liquid.name}</span>
                                                                </span>
                                                            </div>
                                                        )}
                                                    </div>

                                                    {/* Order Button */}
                                                    <div className="pt-2">
                                                        <button
                                                            onClick={() => openConfirm({ preset })}
                                                            className="w-full px-4 py-2.5 bg-gradient-to-r from-fuchsia-600 to-cyan-600 hover:from-fuchsia-700 hover:to-cyan-700 text-white rounded-lg text-sm font-semibold tracking-tight transition-all shadow-lg"
                                                        >
                                                            Заказать микс
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                );
                            })}
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

            {ConfirmModal}
            {SuccessModal}
        </section>
    );
};

export default MainPresetsPage;