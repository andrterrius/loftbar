'use client'

import { useEffect, useState } from "react";
import { X, Search, Plus, RussianRuble, Info } from "lucide-react";
import FlavorCard from "./flavorCard";
import Nav from "../nav";
import { getBowls, getFlavours, getFlavoursCategories, getBasePrice, getLiquids, createOrder, getSettingsImages } from "@/utils/api";
import { usePresetOrderConfirmation } from "@/components/orders/usePresetOrderConfirmation";
import { FLAVORS, FLAVORS_CATEGORIES, BOWL_OPTIONS, LIQUIDS, SETTINGS, SETTINGS_IMAGES } from "../moks/moks";
import { useImageModal } from "../shared/useImageModal";
import { useToast } from "@/components/shared/ToastProvider";

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
    const { openConfirm, ConfirmModal, SuccessModal, isSubmitting } = usePresetOrderConfirmation({ createOrder });
    const [bowlOptions, setBowlOptions] = useState([]);
    const [bowlsLoading, setBowlsLoading] = useState(true);
    const [basePrice, setBasePrice] = useState(0);
    const [addedStrengthPrice, setAddedStrengthPrice] = useState(0);
    const [liquids, setLiquids] = useState([]);
    const [strength, setStrength] = useState(5);
    const [comment, setComment] = useState('');

    // Изображения настроек
    const [settingsImages, setSettingsImages] = useState({ liquids_image_url: null, bowls_image_url: null });
    const { openImageModal, preloadImage, ImageModal } = useImageModal();
    const { showError } = useToast();

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
            .then(async  (data) => {
                if (data) {
                    setSettingsImages({
                        liquids_image_url: data.liquids_image_url || null,
                        bowls_image_url: data.bowls_image_url || null
                    });
                    await preloadImage(data.liquids_image_url);
                    await preloadImage(data.bowls_image_url);
                }
            })
            .catch(async () => {
                setSettingsImages({
                    liquids_image_url: SETTINGS_IMAGES?.liquids_image_url || null,
                    bowls_image_url: SETTINGS_IMAGES?.bowls_image_url || null
                });
                await preloadImage(SETTINGS_IMAGES?.liquids_image_url);
                await preloadImage(SETTINGS_IMAGES?.bowls_image_url);
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

        // Если выбрано ровно 2 вкуса — второй автоматически становится 100 - targetPct
        // Для 3+ вкусов оставляем текущее поведение (ручная корректировка суммарных процентов)
        const newFlavors = selectedFlavors.map(f => {
            if (f.flavorId === id) return { ...f, percentage: targetPct };
            if (selectedFlavors.length === 2) return { ...f, percentage: 100 - targetPct };
            return f;
        });

        const total = newFlavors.reduce((sum, f) => sum + f.percentage, 0);
        if (total > 100) {
            console.warn('Сумма процентов превышает 100');
        }

        setSelectedFlavors(newFlavors);
    };

    const addFlavorToMix = (flavor) => {
        if (selectedFlavors.find(f => f.flavorId === flavor.id)) return showError('Вкус уже добавлен');
        if (selectedFlavors.length >= 5) return showError('Доступно максимум 5 вкусов');
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

        return basePrice + addedPrice + (bowl?.price ?? 0) + (bowl?.added_price ?? 0) + (liquid?.price ?? 0);
    };

    const selectedBowlData = bowlOptions.find(b => b.id === selectedBowl);
    const selectedLiquidData = liquids.find(l => l.id === selectedLiquid);

    const handleOrder = () => {
        if (selectedFlavors.length === 0) return showError('Выберите вкусы!');
        if (!selectedLiquid) return showError('Выберите наполнение колбы!');
        const total = selectedFlavors.reduce((acc, f) => acc + f.percentage, 0);
        if (total > 100.01) return showError('Сумма процентов превышает 100%. Скорректируйте микс.');
        if (total < 99.99) return showError('Сумма процентов должна быть равна 100%. Скорректируйте микс.');

        const displayPreset = {
            name: 'Кастомный микс',
            flavors: selectedFlavors.map((sf) => {
                const flavor = flavors.find(f => f.id === sf.flavorId);
                return { flavor: { name: flavor?.name }, percent: Math.round(sf.percentage) };
            }),
            bowl: selectedBowlData,
            liquid: selectedLiquidData,
            strength,
            price: calculatePrice(),
        };

        openConfirm({
            preset: displayPreset,
            title: 'Подтвердить заказ',
            subtitle: 'Ваш микс',
            getOrderPayload: () => ({
                special_requests: comment.trim() || undefined,
                preset: {
                    liquid_id: selectedLiquid,
                    bowl_id: selectedBowl,
                    flavors: selectedFlavors.map(f => ({ flavor_id: f.flavorId, percent: f.percentage })),
                    strength,
                },
            }),
            onSuccess: () => {
                setSelectedFlavors([]);
                setSelectedLiquid(null);
            },
        });
    };

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

    return (
    <section className="min-h-screen bg-neutral-950 flex flex-col items-center">
        <Nav/>

        <div className="w-full max-w-6xl mx-auto px-5 pt-24 pb-32 sm:pb-28 space-y-8">

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
                                    isLocked={selectedFlavors.length === 1}
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
                                            <div className="mb-1 flex h-9 w-9 shrink-0 items-center justify-center overflow-hidden">
                                                {bowl.image_url ? (
                                                    <img
                                                        src={bowl.image_url}
                                                        alt={bowl.name}
                                                        className="max-h-full max-w-full object-contain pointer-events-none select-none"
                                                        draggable={false}
                                                    />
                                                ) : (
                                                    <span className="text-2xl leading-none">{bowl.icon}</span>
                                                )}
                                            </div>
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
                </div>
            </div>

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
                                                            className="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                                                            loading="lazy"
                                                            decoding="async"
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
        </div>

        <div
            className="fixed bottom-0 left-0 right-0 z-40 pointer-events-none"
            style={{ paddingBottom: 'max(0.75rem, env(safe-area-inset-bottom, 0px))' }}
        >
            <div className="w-full max-w-6xl mx-auto px-5 pb-3 pointer-events-auto">
                <div className="bg-gradient-to-br from-neutral-900 to-neutral-800 border border-white/10 rounded-xl p-4 sm:p-5 backdrop-blur-md shadow-[0_-8px_32px_rgba(0,0,0,0.45)] flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                    <div className="flex justify-between items-center sm:justify-start sm:gap-4">
                        <span className="text-neutral-400 text-sm sm:text-base">Итоговая цена</span>
                        <span className="text-2xl sm:text-3xl font-bold text-white flex items-center tabular-nums">
                            {calculatePrice()}
                            <RussianRuble size={26} className="text-green-500 sm:w-7 sm:h-7 shrink-0" />
                        </span>
                    </div>
                    <button
                        type="button"
                        onClick={handleOrder}
                        disabled={isSubmitting}
                        className="w-full sm:w-auto sm:min-w-[200px] shrink-0 py-3.5 sm:py-3 px-6 bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white rounded-xl font-bold text-base sm:text-lg shadow-[0_0_20px_rgba(192,38,211,0.3)] active:scale-[0.98] transition-transform flex items-center justify-center gap-2 disabled:opacity-60"
                    >
                        Сделать заказ
                    </button>
                </div>
            </div>
        </div>

        {ConfirmModal}
        {SuccessModal}

        {ImageModal}
    </section>
    );
};

export default MainBuilderPage;