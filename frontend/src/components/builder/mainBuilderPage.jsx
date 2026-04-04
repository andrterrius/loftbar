'use client'

import { useEffect, useState } from "react";
import { AnimatePresence } from "framer-motion";
import { X, Search, Plus, RussianRuble, Info } from "lucide-react";
import FlavorCard from "./flavorCard";
import Nav from "../nav";
import { getBowls, getFlavours, getFlavoursCategories, getBasePrice, getLiquids, createOrder, getSettingsImages } from "@/utils/api";
import { FLAVORS, FLAVORS_CATEGORIES, BOWL_OPTIONS, LIQUIDS, SETTINGS, SETTINGS_IMAGES } from "../moks/moks";

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
    const [isConfirmOpen, setIsConfirmOpen] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [successOrderId, setSuccessOrderId] = useState(null);
    const [bowlOptions, setBowlOptions] = useState([]);
    const [bowlsLoading, setBowlsLoading] = useState(true);
    const [basePrice, setBasePrice] = useState(0);
    const [addedStrengthPrice, setAddedStrengthPrice] = useState(0);
    const [liquids, setLiquids] = useState([]);
    const [strength, setStrength] = useState(5);
    const [comment, setComment] = useState('');

    // Изображения настроек
    const [settingsImages, setSettingsImages] = useState({ liquids_image_url: null, bowls_image_url: null });
    const [modalImageUrl, setModalImageUrl] = useState(null);
    const [isImageModalOpen, setIsImageModalOpen] = useState(false);

    // Категории с бекенда
    const [categories, setCategories] = useState([]);
    const [selectedCategoryIds, setSelectedCategoryIds] = useState([]); // Массив ID выбранных категорий

    useEffect(() => {
        getFlavours()
            .then(data => {
                if (!data || data.length === 0) throw new Error();
                setFlavors(data);
            })
            .catch(() => {
                setFlavors(FLAVORS.map(f => ({ ...f, hex_color: f.color })));
            })
            .finally(() => setFlavorsLoading(false));

        getFlavoursCategories()
            .then(data => {
                if (data && data.length > 0) {
                    setCategories(data);
                } else {
                const fallbackCategories = FLAVORS_CATEGORIES.map((category, idx) => ({
                    id: category.id,
                    name: category.name
                }));
                setCategories(fallbackCategories);
            }
            })
            .catch(() => {
                const fallbackCategories = FLAVORS_CATEGORIES.map((category, idx) => ({
                    id: category.id,
                    name: category.name
                }));
                setCategories(fallbackCategories);
            });

        getBowls()
            .then(data => {
                if (!data || data.length === 0) throw new Error();
                setBowlOptions(data);
                setSelectedBowl(data[0]?.id || null);
            })
            .catch(() => {
                const fallbackBowls = BOWL_OPTIONS.map((b, i) => ({
                    ...b,
                    id: b.id || `mock-b-${i}`,
                    name: b.type,
                    category: b.isFruit ? 'fruit' : 'classic'
                }));
                setBowlOptions(fallbackBowls);
                setSelectedBowl(fallbackBowls[0]?.id);
            })
            .finally(() => setBowlsLoading(false));

        getBasePrice()
            .then(data => {
                setBasePrice(data?.base_price ?? SETTINGS.basePrice);
                setAddedStrengthPrice(data?.strength_added_price ?? SETTINGS.addedStrengthPrice);
            })
            .catch(() => {
                setBasePrice(SETTINGS.basePrice);
                setAddedStrengthPrice(SETTINGS.addedStrengthPrice);
            });

        getLiquids()
            .then(data => {
                if (!data || data.length === 0) throw new Error();
                setLiquids(data);
                setSelectedLiquid(data[0]?.id || null);
            })
            .catch(() => {
                setLiquids(LIQUIDS);
                setSelectedLiquid(LIQUIDS[0]?.id);
            });

        // Загрузка изображений настроек
        getSettingsImages()
            .then(data => {
                if (data) {
                    setSettingsImages({
                        liquids_image_url: data.liquids_image_url || null,
                        bowls_image_url: data.bowls_image_url || null
                    });
                }
            })
            .catch(() => {
                setSettingsImages({
                    liquids_image_url: SETTINGS_IMAGES?.liquids_image_url || null,
                    bowls_image_url: SETTINGS_IMAGES?.bowls_image_url || null
                });
            });
    }, []);

    const handlePercentageChange = (id, newPercentage, fromSlider = true) => {
        if (selectedFlavors.length <= 1) {
            setSelectedFlavors(prev => prev.map(f =>
                f.flavorId === id ? { ...f, percentage: 100 } : f
            ));
            return;
        }

        const targetPct = Math.max(0, Math.min(100, newPercentage));

        const newFlavors = selectedFlavors.map(f =>
            f.flavorId === id ? { ...f, percentage: targetPct } : f
        );

        const total = newFlavors.reduce((sum, f) => sum + f.percentage, 0);
        if (total > 100) {
            console.warn('Сумма процентов превышает 100');
        }

        setSelectedFlavors(newFlavors);
    };

    const addFlavorToMix = (flavor) => {
        if (selectedFlavors.find(f => f.flavorId === flavor.id)) return alert('Вкус уже добавлен');
        if (selectedFlavors.length >= 5) return alert('Доступно максимум 5 вкусов');
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
        const liquid = liquids.find(l => l.id === selectedLiquid);

        let addedPrice = strength >= 9 ? addedStrengthPrice : 0;

        return basePrice + addedPrice + (bowl?.price ?? 0) + (liquid?.price ?? 0);
    };

    const handleOrder = async () => {
        if (selectedFlavors.length === 0) return alert('Выберите вкусы!');
        if (!selectedLiquid) return alert('Выберите наполнение колбы!');
        const total = selectedFlavors.reduce((acc, f) => acc + f.percentage, 0);
        if (total > 100.01) return alert('Сумма процентов превышает 100%. Скорректируйте микс.');
        if (total < 99.99) return alert('Сумма процентов должна быть равна 100%. Скорректируйте микс.');
        setIsConfirmOpen(true);
    };

    const handleConfirmedOrder = async () => {
        setIsSubmitting(true);
        const orderData = {
            table_id: window.Telegram?.WebApp?.initDataUnsafe?.start_param
                || new URLSearchParams(window.location.search).get('table_id')
                || 'unknown_table',
            special_requests: comment.trim() || undefined,
            preset: {
                liquid_id: selectedLiquid,
                bowl_id: selectedBowl,
                flavors: selectedFlavors.map(f => ({ flavor_id: f.flavorId, percent: f.percentage })),
                strength: strength,
            }
        };
        try {
            const result = await createOrder(orderData);
            setSelectedFlavors([]);
            setSelectedLiquid(null);
            setIsConfirmOpen(false);
            setSuccessOrderId(result.daily_number || '');
            setTimeout(() => window.Telegram?.WebApp?.close(), 4000);
        } catch (error) {
            console.error("Order error:", error);
            alert('Не удалось отправить заказ. Попробуйте позже.');
        } finally {
            setIsSubmitting(false);
        }
    };

    const selectedBowlData = bowlOptions.find(b => b.id === selectedBowl);
    const selectedLiquidData = liquids.find(l => l.id === selectedLiquid);

    // Фильтрация вкусов по выбранным категориям (поддержка множественных категорий)
    const filteredFlavors = flavors.filter(flavor => {
        // Поиск
        const matchesSearch = searchQuery === '' ||
            flavor.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            (flavor.description && flavor.description.toLowerCase().includes(searchQuery.toLowerCase()));

        // Категории
        const matchesCategory = selectedCategoryIds.length === 0 ||
            selectedCategoryIds.some(catId => {
                const hasCategory = flavor.categories?.some(cat => cat.id == catId);
                console.log(`Category ${catId}:`, hasCategory, flavor.categories);
                return hasCategory;
            }
        );

        return matchesSearch && matchesCategory;
    });

    // Обработчик выбора категории (поддержка нескольких категорий)
    const toggleCategory = (categoryId) => {
        console.log(categoryId);
        setSelectedCategoryIds(prev => {
            if (prev.includes(categoryId)) {
                return prev.filter(id => id !== categoryId);
            } else {
                return [...prev, categoryId];
            }
        });
    };

    // Очистка всех выбранных категорий
    const clearCategories = () => {
        setSelectedCategoryIds([]);
    };

    // Открытие модального окна с изображением
    const openImageModal = (imageUrl, title) => {
        if (imageUrl) {
            setModalImageUrl({ url: imageUrl, title });
            setIsImageModalOpen(true);
        } else {
            alert('Изображение не добавлено');
        }
    };

    return (
    <section className="min-h-screen bg-neutral-950 flex flex-col items-center">
        <Nav/>

        <div className="w-full max-w-6xl mx-auto px-5 pt-24 pb-12 space-y-8">

            <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-white/10 pb-6 text-left">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-2">Конструктор кальяна</h1>
                    <p className="text-neutral-400 text-sm md:text-base">Создай свой идеальный кальян</p>
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
                                    color={flavor.color || flavor.hex_color || '#a21caf'}
                                    onRemove={() => removeFlavorFromMix(sf.flavorId)}
                                    onChange={(val, fromSlider) => handlePercentageChange(sf.flavorId, val, fromSlider)}
                                />
                            );
                        })}

                        {(() => {
                            const total = selectedFlavors.reduce((acc, f) => acc + f.percentage, 0);
                            const isOver = total > 100.01;
                            const isUnder = selectedFlavors.length > 0 && total < 99.99;
                            if (!isOver && !isUnder) return null;
                            return (
                                <div className={`flex items-center justify-between px-4 py-3 rounded-xl border text-sm font-medium ${
                                    isOver
                                        ? 'bg-red-500/10 border-red-500/30 text-red-400'
                                        : 'bg-yellow-500/10 border-yellow-500/30 text-yellow-400'
                                }`}>
                                    <span>
                                        {isOver ? '⚠ Сумма процентов превышает 100%' : 'ℹ Сумма процентов меньше 100%'}
                                    </span>
                                    <span className="font-mono font-bold">
                                        {Math.round(total)}%
                                    </span>
                                </div>
                            );
                        })()}

                        {selectedFlavors.length === 0 && (
                            <div
                              onClick={() => setIsSearchOpen(true)}
                              className="
                                p-8 border-2 border-dashed border-white/10 rounded-xl
                                flex flex-col items-center justify-center
                                text-neutral-500 h-64
                                cursor-pointer
                                transition-all duration-300
                                hover:border-white/40
                                hover:bg-white/5
                                hover:shadow-[0_0_15px_rgba(255,255,255,0.5)]
                                active:scale-95
                              "
                            >
                              <Plus size={48} className="mb-4 opacity-50 transition-opacity duration-300 group-hover:opacity-100" />
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
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="text-lg font-semibold text-white">Чаша</h3>
                            {settingsImages.bowls_image_url && (
                                <button
                                    onClick={() => openImageModal(settingsImages.bowls_image_url, 'Изображение чаш')}
                                    className="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 transition-colors text-neutral-400 hover:text-white"
                                    title="Посмотреть изображение"
                                >
                                    <Info size={16} />
                                </button>
                            )}
                        </div>
                        {bowlsLoading ? (
                            <div className="grid grid-cols-3 gap-2">
                                {Array.from({ length: 8 }).map((_, i) => <BowlSkeleton key={i} />)}
                            </div>
                        ) : bowlOptions.length === 0 ? (
                            <div className="flex flex-col items-center justify-center py-8 text-neutral-600 gap-2">
                                <span className="text-3xl">🏺</span>
                                <p className="text-sm text-center">Чаши не добавлены администратором</p>
                            </div>
                        ) : (
                            <>
                                <div className="grid grid-cols-3 gap-2">
                                    {bowlOptions.map((bowl) => (
                                        <button
                                            key={bowl.id}
                                            onClick={() => setSelectedBowl(bowl.id)}
                                            className={`flex flex-col items-center justify-center p-2 rounded-lg border transition-all min-w-0 ${
                                                selectedBowl === bowl.id
                                                    ? 'bg-fuchsia-600 border-fuchsia-500 text-white shadow-[0_0_15px_rgba(192,38,211,0.5)]'
                                                    : 'bg-white/5 border-transparent hover:bg-white/10 text-neutral-400'
                                            }`}
                                            title={bowl.name}
                                        >
                                            <span className="text-2xl mb-1">{bowl.icon}</span>
                                            <span className="text-[10px] text-center leading-tight w-full break-words whitespace-normal px-1">
                                                {bowl.name}
                                            </span>
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
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="text-lg font-semibold text-white">Наполнение колбы</h3>
                            {settingsImages.liquids_image_url && (
                                <button
                                    onClick={() => openImageModal(settingsImages.liquids_image_url, 'Изображение наполнений колб')}
                                    className="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 transition-colors text-neutral-400 hover:text-white"
                                    title="Посмотреть изображение"
                                >
                                    <Info size={16} />
                                </button>
                            )}
                        </div>
                        {liquids.length === 0 ? (
                            <div className="flex flex-col items-center justify-center py-6 text-neutral-600 gap-2">
                                <span className="text-3xl">💧</span>
                                <p className="text-sm text-center">Наполнения колбы не добавлены</p>
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

                    <div className="bg-white/5 border border-white/10 rounded-xl p-6 backdrop-blur-sm text-left">
                        <h3 className="text-lg font-semibold text-white mb-4">Крепость</h3>
                        <div className="space-y-3">
                            <div className="flex justify-between items-center">
                                <span className="text-neutral-400 text-sm">Лёгкий</span>
                                <span className="font-mono text-fuchsia-400 font-bold text-lg">{strength}</span>
                                <span className="text-neutral-400 text-sm">Крепкий</span>
                            </div>
                            <input
                                type="range"
                                min="1"
                                max="10"
                                value={strength}
                                onChange={(e) => setStrength(parseInt(e.target.value))}
                                className="w-full h-2 bg-neutral-800 rounded-lg appearance-none cursor-pointer accent-fuchsia-500"
                                style={{
                                    background: `linear-gradient(to right, #a21caf 0%, #a21caf ${(strength - 1) / 9 * 100}%, #262626 ${(strength - 1) / 9 * 100}%, #262626 100%)`
                                }}
                            />
                            <div className="flex justify-between text-[10px] text-neutral-600">
                                {[1,2,3,4,5,6,7,8,9,10].map(n => (
                                    <span key={n}>{n}</span>
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="bg-white/5 border border-white/10 rounded-xl p-6 backdrop-blur-sm text-left">
                        <h3 className="text-lg font-semibold text-white mb-4">Пожелания</h3>
                        <textarea
                            value={comment}
                            onChange={(e) => setComment(e.target.value)}
                            placeholder="Комментарий к заказу..."
                            rows={3}
                            maxLength={300}
                            className="w-full bg-neutral-900 border border-white/10 rounded-xl p-3 text-white placeholder-neutral-600 text-sm outline-none focus:border-fuchsia-500/50 transition-colors resize-none"
                        />
                        <p className="text-[10px] text-neutral-600 text-right mt-1">{comment.length}/300</p>
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
                        <div className="w-full h-[85vh] sm:h-auto sm:max-h-[80vh] sm:max-w-4xl bg-neutral-900 border-t sm:border border-white/10 rounded-t-3xl sm:rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-[slideUp_0.3s_ease]">
                            <div className="w-full flex justify-center pt-3 pb-1 sm:hidden">
                                <div className="w-12 h-1.5 bg-neutral-700 rounded-full" />
                            </div>

                            <div className="p-4 border-b border-white/10 flex items-center gap-3">
                                <Search className="text-neutral-500" />
                                <input
                                    type="text"
                                    placeholder="Поиск вкуса..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="flex-1 bg-transparent border-none outline-none text-white placeholder-neutral-500"
                                />
                                <button onClick={() => setIsSearchOpen(false)} className="p-2 -mr-2 text-neutral-500 hover:text-white transition-colors">
                                    <X size={20} />
                                </button>
                            </div>

                            {/* Category Selection - теперь с бекенда, поддержка множественного выбора */}
                            <div className="p-4 border-b border-white/10">
                                <div className="flex flex-wrap gap-2">
                                    {categories.map((category) => (
                                        <button
                                            key={category.id}
                                            onClick={() => toggleCategory(category.id)}
                                            className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                                                selectedCategoryIds.includes(category.id)
                                                    ? 'bg-fuchsia-600 text-white shadow-[0_0_10px_rgba(192,38,211,0.5)]'
                                                    : 'bg-white/5 text-neutral-400 hover:bg-white/10 hover:text-white'
                                            }`}
                                        >
                                            {category.name}
                                        </button>
                                    ))}
                                    {selectedCategoryIds.length > 0 && (
                                        <button
                                            onClick={clearCategories}
                                            className="px-4 py-2 rounded-full text-sm font-medium bg-red-500/20 text-red-400 hover:bg-red-500/30 transition-all duration-200"
                                        >
                                            Очистить ✕
                                        </button>
                                    )}
                                </div>
                                {selectedCategoryIds.length > 0 && (
                                    <div className="mt-2 text-xs text-neutral-500">
                                        Выбрано категорий: {selectedCategoryIds.length}
                                    </div>
                                )}
                            </div>

                            <div className="flex-1 overflow-y-auto p-4">
                                {flavorsLoading ? (
                                    <div className="grid gap-3" style={{ gridTemplateColumns: "repeat(4, minmax(0, 1fr))" }}>
                                        {Array.from({ length: 6 }).map((_, i) => (
                                            <div key={i} className="animate-pulse">
                                                <div className="aspect-square bg-white/10 rounded-xl mb-2" />
                                                <div className="h-3 bg-white/10 rounded w-3/4 mx-auto" />
                                            </div>
                                        ))}
                                    </div>
                                ) : filteredFlavors.length === 0 ? (
                                    <div className="p-8 text-center text-neutral-500">
                                        {searchQuery ? 'Вкусы не найдены' : 'В выбранных категориях пока нет вкусов'}
                                    </div>
                                ) : (
                                    <div className="grid gap-3" style={{ gridTemplateColumns: "repeat(4, minmax(0, 1fr))" }}>
                                        {filteredFlavors.map(flavor => (
                                            <button
                                                key={flavor.id}
                                                onClick={() => addFlavorToMix(flavor)}
                                                disabled={selectedFlavors.some(f => f.flavorId === flavor.id)}
                                                className="group flex flex-col items-center p-3 rounded-xl hover:bg-white/5 disabled:opacity-50 disabled:cursor-not-allowed transition-all text-center"
                                            >
                                                <div className="w-full aspect-square rounded-xl mb-2 overflow-hidden bg-neutral-800 flex items-center justify-center relative">
                                                    {flavor.image_url ? (
                                                        <img
                                                            src={flavor.image_url}
                                                            alt={flavor.name}
                                                            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                                                        />
                                                    ) : (
                                                        <div
                                                            className="w-full h-full flex items-center justify-center text-4xl font-bold"
                                                            style={{ backgroundColor: flavor.hex_color || flavor.color || '#333' }}
                                                        >
                                                            <span className="text-white/80">{flavor.name[0]}</span>
                                                        </div>
                                                    )}
                                                </div>
                                                <span className="text-sm font-bold text-white group-hover:text-cyan-400 transition-colors line-clamp-2">
                                                    {flavor.name}
                                                </span>
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

        {isConfirmOpen && (
            <div
                className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
                onClick={(e) => e.target === e.currentTarget && setIsConfirmOpen(false)}
            >
                <div className="bg-neutral-900 border border-white/10 rounded-2xl p-6 w-full max-w-sm shadow-2xl">
                    <h3 className="text-xl font-bold tracking-tight text-white mb-0.5">Подтвердить заказ</h3>
                    <p className="text-[11px] uppercase tracking-widest text-neutral-600 font-medium mb-4">Ваш микс</p>

                    <div className="space-y-2 mb-4 bg-white/5 rounded-xl p-3">
                        {selectedFlavors.map((sf) => {
                            const flavor = flavors.find(f => f.id === sf.flavorId);
                            return (
                                <div key={sf.flavorId} className="flex justify-between items-center">
                                    <span className="flex items-center gap-2 text-[14px] font-semibold text-white">
                                        <span
                                            className="w-2 h-2 rounded-full inline-block shrink-0"
                                            style={{ backgroundColor: flavor?.hex_color || flavor?.color || '#ccc' }}
                                        />
                                        {flavor?.name || 'Неизвестный вкус'}
                                    </span>
                                    <span className="font-mono text-[12px] text-neutral-300 tabular-nums">{Math.round(sf.percentage)}%</span>
                                </div>
                            );
                        })}
                    </div>

                    <div className="flex gap-4 mb-5">
                        <div className="flex flex-col gap-1.5">
                            <span className="text-[10px] uppercase tracking-widest text-neutral-500 font-medium">Чаша</span>
                            {selectedBowlData && (
                                <span className="flex items-center gap-1 px-2.5 py-1 rounded-full text-[12px] font-semibold bg-white/10 border border-white/15 text-white">
                                    {selectedBowlData.icon} {selectedBowlData.name}
                                </span>
                            )}
                        </div>
                        <div className="flex flex-col gap-1.5">
                            <span className="text-[10px] uppercase tracking-widest text-neutral-500 font-medium">Колба</span>
                            {selectedLiquidData && (
                                <span className="flex items-center gap-1 px-2.5 py-1 rounded-full text-[12px] font-semibold bg-white/10 border border-white/15 text-white">
                                    💧 {selectedLiquidData.name}
                                </span>
                            )}
                        </div>
                    </div>

                    <div className="flex items-center justify-between mb-6 pt-4 border-t border-white/5">
                        <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium">Итого</span>
                        <span className="text-white font-bold text-2xl tracking-tight leading-none">{calculatePrice()}<span className="text-neutral-400 text-lg font-semibold">₽</span></span>
                    </div>

                    <div className="flex gap-3">
                        <button
                            onClick={() => setIsConfirmOpen(false)}
                            disabled={isSubmitting}
                            className="flex-1 py-3 rounded-xl bg-white/5 border border-white/10 text-neutral-400 hover:bg-white/10 transition-all text-[13px] font-semibold disabled:opacity-50"
                        >
                            Отмена
                        </button>
                        <button
                            onClick={handleConfirmedOrder}
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
                    <p className="text-neutral-500 text-xs mb-6">
                        Ожидайте — ваш микс уже готовится 🔥
                    </p>
                    <button
                        onClick={() => window.Telegram?.WebApp?.close()}
                        className="w-full py-3 rounded-xl bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white font-bold text-sm shadow-[0_0_20px_rgba(192,38,211,0.3)] active:scale-95 transition-transform"
                    >
                        Закрыть
                    </button>
                </div>
            </div>
        )}

        {/* Модальное окно для изображений */}
        {isImageModalOpen && modalImageUrl && (
            <div
                className="fixed inset-0 z-[80] flex items-center justify-center bg-black/80 backdrop-blur-md p-4"
                onClick={() => setIsImageModalOpen(false)}
            >
                <div
                    className="relative max-w-3xl max-h-[90vh] w-full bg-neutral-900 rounded-2xl overflow-hidden border border-white/10 shadow-2xl"
                    onClick={(e) => e.stopPropagation()}
                >
                    <div className="flex justify-between items-center p-4 border-b border-white/10">
                        <h3 className="text-lg font-semibold text-white">{modalImageUrl.title}</h3>
                        <button
                            onClick={() => setIsImageModalOpen(false)}
                            className="p-2 rounded-lg hover:bg-white/10 transition-colors text-neutral-400 hover:text-white"
                        >
                            <X size={20} />
                        </button>
                    </div>
                    <div className="p-4 flex justify-center items-center bg-neutral-950/50">
                        <img
                            src={modalImageUrl.url}
                            alt={modalImageUrl.title}
                            className="max-w-full max-h-[70vh] object-contain rounded-lg"
                            onError={(e) => {
                                e.target.src = 'https://placehold.co/600x400?text=Image+not+found';
                            }}
                        />
                    </div>
                </div>
            </div>
        )}
    </section>
    );
};

export default MainBuilderPage;