'use client'

import { useEffect, useState } from "react";
import { AnimatePresence } from "framer-motion";
import { X, Search, Plus, RussianRuble } from "lucide-react";
import FlavorCard from "./flavorCard";
import Nav from "../nav";
import { getBowls, getFlavours, getBasePrice, getLiquids, createOrder } from "@/utils/api";

const BowlSkeleton = () => (
    <div className="aspect-square rounded-lg bg-white/5 animate-pulse border border-white/5" />
);

const MainBuilderPage = () => {
    const [flavors, setFlavors] = useState([]);
    const [flavorsLoading, setFlavorsLoading] = useState(true);
    const [selectedFlavors, setSelectedFlavors] = useState([]);
    const [selectedLiquid, setSelectedLiquid] = useState(null);
    const [selectedBowl, setSelectedBowl] = useState(null);
    const [isSearchOpen, setIsSearchOpen] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [bowlOptions, setBowlOptions] = useState([]);
    const [bowlsLoading, setBowlsLoading] = useState(true);
    const [basePrice, setBasePrice] = useState(0);
    const [liquids, setLiquids] = useState([]);

    useEffect(() => {
        getFlavours()
            .then(data => setFlavors(data))
            .finally(() => setFlavorsLoading(false));
        getBowls()
            .then(data => { setBowlOptions(data); setSelectedBowl(data[0]?.id || null); })
            .catch(console.error)
            .finally(() => setBowlsLoading(false));
        getBasePrice()
            .then(data => setBasePrice(data.base_price))
            .catch(console.error);
        getLiquids()
            .then(data => {
                setLiquids(data);
                setSelectedLiquid(data[0]?.id || null);
            })
            .catch(console.error);
    }, []);

    const handlePercentageChange = (id, newPercentage) => {
        if (selectedFlavors.length <= 1) return;
        const targetPct = Math.max(0, Math.min(100, newPercentage));
        const remainder = 100 - targetPct;
        const others = selectedFlavors.filter(f => f.flavorId !== id);
        const sumOthers = others.reduce((acc, f) => acc + f.percentage, 0);
        const updated = selectedFlavors.map(f => {
            if (f.flavorId === id) return { ...f, percentage: targetPct };
            const newPct = sumOthers === 0
                ? remainder / others.length
                : (f.percentage / sumOthers) * remainder;
            return { ...f, percentage: newPct };
        });
        setSelectedFlavors(updated);
    };

    const addFlavorToMix = (flavor) => {
        if (selectedFlavors.find(f => f.flavorId === flavor.id)) return alert('Flavor already added');
        if (selectedFlavors.length >= 5) return alert('Max 5 flavors allowed');
        if (selectedFlavors.length === 0) {
            setSelectedFlavors([{ flavorId: flavor.id, percentage: 100 }]);
        } else {
            const count = selectedFlavors.length + 1;
            const newPct = 100 / count;
            const updated = selectedFlavors.map(f => ({ ...f, percentage: newPct }));
            updated.push({ flavorId: flavor.id, percentage: newPct });
            setSelectedFlavors(updated);
        }
        setIsSearchOpen(false);
    };

    const removeFlavorFromMix = (id) => {
        const remaining = selectedFlavors.filter(f => f.flavorId !== id);
        if (remaining.length === 0) return setSelectedFlavors([]);
        const currentSum = remaining.reduce((acc, f) => acc + f.percentage, 0);
        setSelectedFlavors(remaining.map(f => ({ ...f, percentage: (f.percentage / currentSum) * 100 })));
    };
    const calculatePrice = () => {
        const bowl = bowlOptions.find(b => b.id === selectedBowl);
        return basePrice + (bowl?.price ?? 0) + liquids.find(l => l.id === selectedLiquid)?.price || 0;
    };

    const handleOrder = async () => {
        if (selectedFlavors.length === 0) return alert('Mix is empty!');
        if (!selectedLiquid) return alert('Select base liquid!');
        setIsSubmitting(true);
        const orderData = {
            table_id: window.Telegram?.WebApp?.initDataUnsafe?.user?.id || 'unknown_table',
            preset: {
                liquid_id: selectedLiquid,
                bowl_id: selectedBowl,
                flavors: selectedFlavors.map(f => ({ flavor_id: f.flavorId, percent: f.percentage }))
            }
        };
        try {
            const result = await createOrder(orderData);
            alert(`Заказ #${result.id || ''} успешно оформлен!`);
            setSelectedFlavors([]);
            setSelectedLiquid(null);
        } catch (error) {
            console.error("Order error:", error);
            alert('Не удалось отправить заказ. Попробуйте позже.');
        } finally {
            setIsSubmitting(false);
        }
    };

    const filteredFlavors = flavors.filter(f =>
        f.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        f.brand.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const selectedBowlData = bowlOptions.find(b => b.id === selectedBowl);

    return (
        <section className="min-h-screen bg-neutral-950 flex flex-col items-center">
            <Nav/>

            <div className="w-full max-w-6xl mx-auto px-5 pt-24 pb-12 space-y-8">

                <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-white/10 pb-6 text-left">
                    <div>
                        <h1 className="text-3xl font-bold text-white mb-2">Конструктор Миксов</h1>
                        <p className="text-neutral-400 text-sm md:text-base">Создай свою идеальную чашу</p>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 text-left">

                    <div className="lg:col-span-2 space-y-6">
                        <div className="space-y-4">
                            {selectedFlavors.map((sf) => {
                                const flavor = flavors.find(f => f.id === sf.flavorId);
                                if (!flavor) return null;
                                return (
                                    <FlavorCard
                                        key={sf.flavorId}
                                        item={flavor}
                                        percentage={sf.percentage}
                                        color={flavor.hex_color}
                                        onRemove={() => removeFlavorFromMix(sf.flavorId)}
                                        onChange={(val) => handlePercentageChange(sf.flavorId, val)}
                                    />
                                );
                            })}

                            {selectedFlavors.length === 0 && (
                                <div className="p-8 border-2 border-dashed border-white/10 rounded-xl flex flex-col items-center justify-center text-neutral-500 h-64">
                                    <Plus size={48} className="mb-4 opacity-50" />
                                    <p>Выберите вкус</p>
                                </div>
                            )}

                            {selectedFlavors.length < 5 && (
                                <button
                                    onClick={() => setIsSearchOpen(true)}
                                    className="w-full py-4 border border-white/10 rounded-xl hover:bg-white/5 transition-colors text-cyan-400 flex items-center justify-center gap-2 font-medium active:scale-95"
                                >
                                    <Plus size={20} /> Добавить вкус
                                </button>
                            )}
                        </div>
                    </div>

                    <div className="space-y-6">

                        <div className="bg-white/5 border border-white/10 rounded-xl p-6 backdrop-blur-sm text-left">
                            <h3 className="text-lg font-semibold text-white mb-4">Вид Чаши</h3>
                            {bowlsLoading ? (
                                <div className="grid grid-cols-4 gap-2">
                                    {Array.from({ length: 8 }).map((_, i) => <BowlSkeleton key={i} />)}
                                </div>
                            ) : bowlOptions.length === 0 ? (
                                <div className="flex flex-col items-center justify-center py-8 text-neutral-600 gap-2">
                                    <span className="text-3xl">🏺</span>
                                    <p className="text-sm text-center">Чаши не добавлены администратором</p>
                                </div>
                            ) : (
                                <>
                                    <div className="grid grid-cols-4 gap-2">
                                        {bowlOptions.map((bowl) => (
                                            <button
                                                key={bowl.id}
                                                onClick={() => setSelectedBowl(bowl.id)}
                                                className={`flex flex-col items-center justify-center p-2 rounded-lg border transition-all aspect-square ${
                                                    selectedBowl === bowl.id
                                                        ? 'bg-fuchsia-600 border-fuchsia-500 text-white shadow-[0_0_15px_rgba(192,38,211,0.5)]'
                                                        : 'bg-white/5 border-transparent hover:bg-white/10 text-neutral-400'
                                                }`}
                                                title={bowl.name}
                                            >
                                                <span className="text-2xl mb-1">{bowl.icon}</span>
                                                <span className="text-[10px] text-center leading-tight truncate w-full">{bowl.name}</span>
                                            </button>
                                        ))}
                                    </div>
                                    {selectedBowlData?.category === 'fruit' && (
                                        <div className="mt-4 text-xs text-fuchsia-300 text-center font-medium bg-fuchsia-500/10 py-2 rounded-lg">
                                            +{selectedBowlData.price}₽ Fruit Bowl
                                        </div>
                                    )}
                                </>
                            )}
                        </div>

                        <div className="bg-white/5 border border-white/10 rounded-xl p-6 backdrop-blur-sm text-left">
                            <h3 className="text-lg font-semibold text-white mb-4">Стандартное наполнение</h3>
                            {liquids.length === 0 ? (
                                <div className="flex flex-col items-center justify-center py-6 text-neutral-600 gap-2">
                                    <span className="text-3xl">💧</span>
                                    <p className="text-sm text-center">Жидкости не добавлены</p>
                                </div>
                            ) : (
                                <div className="grid grid-cols-2 gap-2">
                                    {liquids.map((liquid) => (
                                        <button
                                            key={liquid.id}
                                            onClick={() => setSelectedLiquid(liquid.id)}
                                            className={`flex flex-col items-start p-3 rounded-lg border transition-all ${
                                                selectedLiquid === liquid.id
                                                    ? 'bg-cyan-500/20 border-cyan-500 text-cyan-300'
                                                    : 'bg-transparent border-white/5 hover:bg-white/5 text-neutral-400'
                                            }`}
                                        >
                                            <span className="text-sm font-medium">{liquid.name}</span>
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>

                        <div className="bg-gradient-to-br from-neutral-900 to-neutral-800 border border-white/10 rounded-xl p-6 shadow-xl">
                            <div className="flex justify-between items-center mb-4">
                                <span className="text-neutral-400">Итоговая цена</span>
                                <span className="text-3xl font-bold text-white flex items-center">
                                    {calculatePrice()}
                                    <RussianRuble size={28} className="text-green-500" />
                                </span>
                            </div>
                            <button
                                onClick={handleOrder}
                                disabled={isSubmitting}
                                className="w-full py-4 bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white rounded-xl font-bold text-lg shadow-[0_0_20px_rgba(192,38,211,0.3)] active:scale-95 transition-transform flex items-center justify-center gap-2 disabled:opacity-60"
                            >
                                Сделать заказ
                            </button>
                        </div>
                    </div>
                </div>

                <AnimatePresence>
                    {isSearchOpen && (
                        <div
                            className="fixed inset-0 z-[60] flex items-end sm:items-center justify-center bg-black/60 backdrop-blur-sm sm:p-4"
                            onClick={(e) => e.target === e.currentTarget && setIsSearchOpen(false)}
                        >
                            <div className="w-full h-[85vh] sm:h-auto sm:max-h-[80vh] sm:max-w-lg bg-neutral-900 border-t sm:border border-white/10 rounded-t-3xl sm:rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-[slideUp_0.3s_ease]">
                                <div className="w-full flex justify-center pt-3 pb-1 sm:hidden">
                                    <div className="w-12 h-1.5 bg-neutral-700 rounded-full" />
                                </div>

                                <div className="p-4 border-b border-white/10 flex items-center gap-3">
                                    <Search className="text-neutral-500" />
                                    <input
                                        type="text"
                                        placeholder="Поиск вкуса..."
                                        autoFocus
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        className="flex-1 bg-transparent border-none outline-none text-white placeholder-neutral-500"
                                    />
                                    <button onClick={() => setIsSearchOpen(false)} className="p-2 -mr-2 text-neutral-500 hover:text-white transition-colors">
                                        <X size={20} />
                                    </button>
                                </div>

                                <div className="flex-1 overflow-y-auto p-2">
                                    {flavorsLoading ? (
                                        <div className="space-y-1 p-2">
                                            {Array.from({ length: 5 }).map((_, i) => (
                                                <div key={i} className="flex items-center gap-3 p-3 rounded-lg animate-pulse">
                                                    <div className="w-10 h-10 rounded-full bg-white/10 shrink-0" />
                                                    <div className="space-y-2 flex-1">
                                                        <div className="h-3 w-24 bg-white/10 rounded" />
                                                        <div className="h-2 w-32 bg-white/5 rounded" />
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    ) : filteredFlavors.length === 0 ? (
                                        <div className="p-8 text-center text-neutral-500">Вкусы не найдены.</div>
                                    ) : (
                                        <div className="grid grid-cols-1 gap-1">
                                            {filteredFlavors.map(flavor => (
                                                <button
                                                    key={flavor.id}
                                                    onClick={() => addFlavorToMix(flavor)}
                                                    disabled={selectedFlavors.some(f => f.flavorId === flavor.id)}
                                                    className="flex items-center justify-between p-3 rounded-lg hover:bg-white/5 disabled:opacity-50 disabled:cursor-not-allowed group transition-colors text-left w-full"
                                                >
                                                    <div className="flex items-center gap-3">
                                                        <div
                                                            className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold text-black/60 shrink-0"
                                                            style={{ backgroundColor: flavor.hex_color || '#ccc' }}
                                                        >
                                                            {flavor.name[0]}
                                                        </div>
                                                        <div>
                                                            <div className="font-medium text-white group-hover:text-cyan-400 transition-colors">{flavor.name}</div>
                                                            <div className="text-xs text-neutral-500">{flavor.brand} • {flavor.category}</div>
                                                        </div>
                                                    </div>
                                                    <Plus size={18} className="text-neutral-500 group-hover:text-white shrink-0" />
                                                </button>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    )}
                </AnimatePresence>
            </div>
        </section>
    );
};

export default MainBuilderPage;