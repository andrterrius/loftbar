'use client'

import { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { ChevronDown, History, RotateCcw } from "lucide-react";
import Nav from "../nav";
import { createOrder, getOrders } from "@/utils/api";
import { usePresetOrderConfirmation } from "./usePresetOrderConfirmation";
import { useSearchParams } from 'next/navigation';
import { getUrlWithParams } from '../../utils/urlParams';
import { useToast } from '@/components/shared/ToastProvider';

function cn(...classes) {
    return classes.filter(Boolean).join(" ");
}

function formatDateTime(value) {
    if (!value) return "—";
    
    // Добавляем Z, чтобы явно указать, что время в UTC
    const d = new Date(value + "Z");
    
    if (Number.isNaN(d.getTime())) return "—";
    
    return new Intl.DateTimeFormat("ru-RU", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    }).format(d);
}

function getStrengthLabel(strength) {
    return { label: strength, color: 'text-neutral-400', bg: 'bg-neutral-500/10', border: 'border-neutral-500/30' };
}

function statusMeta(status) {
    const emojiMap = {
        "pending": "⏳ В ожидании",
        "in_progress": "👨‍🍳 В процессе",
        "ready": "✅ Готов",
        "completed": "✨ Завершен",
        "cancelled": "❌ Отменен"
    };

    switch (status) {
        case "pending":
            return { label: emojiMap.pending, className: "bg-white/5 border-white/10 text-neutral-200" };
        case "in_progress":
            return { label: emojiMap.in_progress, className: "bg-indigo-500/15 border-indigo-500/30 text-indigo-200" };
        case "ready":
            return { label: emojiMap.ready, className: "bg-emerald-500/15 border-emerald-500/30 text-emerald-200" };
        case "completed":
            return { label: emojiMap.completed, className: "bg-neutral-500/15 border-neutral-500/30 text-neutral-200" };
        case "cancelled":
            return { label: emojiMap.cancelled, className: "bg-rose-500/15 border-rose-500/30 text-rose-200" };
        default:
            return { label: status || "—", className: "bg-white/5 border-white/10 text-neutral-200" };
    }
}

const OrderCardSkeleton = () => (
    <div className="bg-white/5 border border-white/10 rounded-2xl overflow-hidden flex flex-col w-full animate-pulse">
        <div className="p-5 flex-1 flex flex-col gap-4">
            <div className="flex items-start justify-between gap-3">
                <div className="space-y-2 flex-1">
                    <div className="h-4 w-40 bg-white/10 rounded" />
                    <div className="h-3 w-56 bg-white/5 rounded" />
                </div>
                <div className="h-6 w-24 bg-white/10 rounded-full" />
            </div>
            <div className="space-y-2">
                <div className="h-3 w-2/3 bg-white/5 rounded" />
                <div className="h-3 w-1/2 bg-white/5 rounded" />
            </div>
            <div className="pt-4 border-t border-white/5 flex items-center justify-between gap-3">
                <div className="h-4 w-32 bg-white/10 rounded" />
                <div className="h-9 w-28 bg-white/10 rounded-xl" />
            </div>
        </div>
    </div>
);

function OrderStatusBadge({ status }) {
    const meta = statusMeta(status);
    return (
        <span className={cn("inline-flex items-center px-3 py-1.5 rounded-full text-[12px] font-semibold border", meta.className)}>
            {meta.label}
        </span>
    );
}

function priceText(v) {
    if (v === null || v === undefined || v === "") return "—";
    return `${v} ₽`;
}

function OrderCard({ order, orderNumber, isExpanded, onToggleExpanded, onReorder, isReordering }) {
    const number = order?.daily_number ? `#${order.daily_number}` : (order?.id ? `#${order.id}` : "");

    const title = order?.is_custom
        ? (order?.custom_name || "Кастомный заказ")
        : (order?.preset?.name || "Заказ");

    const hasPreset = !!order?.preset;
    const canReorder = !!order?.can_reorder && hasPreset;

    const total = order?.total_price;
    const actual = order?.actual_price;
    const pricesDiffer = total !== null && total !== undefined && actual !== null && actual !== undefined && total !== actual;

    const flavors = order?.preset?.flavors || [];
    const strengthInfo = order?.preset?.strength !== undefined && order?.preset?.strength !== null
        ? getStrengthLabel(order.preset.strength)
        : null;

    return (
        <div className="bg-white/5 border border-white/10 rounded-2xl overflow-hidden flex flex-col w-full">
            <div className="p-5 flex flex-col gap-4">
                <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                        <div className="flex items-center gap-2 flex-wrap">
                            <h3 className="text-base font-bold text-white tracking-tight leading-snug">
                                Заказ #{orderNumber}
                            </h3>
                            {number && (
                                <span className="text-xs text-neutral-500 bg-white/5 px-2 py-0.5 rounded-full">
                                    {number}
                                </span>
                            )}
                        </div>
                        <p className="text-neutral-300 font-semibold text-[15px] mt-1 truncate">{title}</p>
                        <p className="text-neutral-500 text-xs mt-1">{formatDateTime(order?.created_at)}</p>
                    </div>
                    <OrderStatusBadge status={order?.status} />
                </div>

                <div className="flex items-center justify-between gap-3">
                    <div className="flex flex-col gap-1">
                        <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium">Цена</span>
                        <div className="flex items-center gap-2 flex-wrap">
                            <span className={cn("text-sm font-semibold", pricesDiffer ? "text-neutral-500 line-through" : "text-white")}>
                                {priceText(total)}
                            </span>
                            <span className={cn("text-sm font-semibold", pricesDiffer ? "text-emerald-300" : "text-neutral-400")}>
                                {pricesDiffer ? `Сейчас: ${priceText(actual)}` : (actual !== total ? `Сейчас: ${priceText(actual)}` : "")}
                            </span>
                        </div>
                    </div>

                    <button
                        onClick={onToggleExpanded}
                        className="inline-flex items-center gap-2 px-3 py-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-neutral-200 text-xs font-semibold transition-colors"
                    >
                        Состав
                        <ChevronDown className={cn("w-4 h-4 transition-transform", isExpanded ? "rotate-180" : "")} />
                    </button>
                </div>

                {isExpanded && (
                    <div className="bg-neutral-900/40 border border-white/10 rounded-xl p-4 space-y-3">
                        {!hasPreset ? (
                            <p className="text-sm text-neutral-400">Состав недоступен.</p>
                        ) : (
                            <>
                                <div className="flex flex-wrap gap-2 pt-2 items-stretch">
                                    {strengthInfo ? (
                                        <div className="flex flex-col gap-1 flex-1 min-w-[100px]">
                                            <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium pl-1">Крепость</span>
                                            <span className={`h-9 inline-flex items-center gap-2 px-3 rounded-lg text-sm font-semibold ${strengthInfo.bg} ${strengthInfo.border} border`}>
                                                <span className={`text-base ${strengthInfo.color}`}>⚡</span>
                                                <span className={strengthInfo.color}>{strengthInfo.label}</span>
                                            </span>
                                        </div>
                                    ) : null}

                                    {order?.preset?.bowl ? (
                                        <div className="flex flex-col gap-1 flex-1 min-w-[100px]">
                                            <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium pl-1">Чаша</span>
                                            <span className="h-9 flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-fuchsia-500/15 border border-fuchsia-500/30 text-fuchsia-300">
                                                <span className="inline-flex h-6 w-6 shrink-0 items-center justify-center overflow-hidden">
                                                    {order.preset.bowl.image_url ? (
                                                        <img
                                                            src={order.preset.bowl.image_url}
                                                            alt=""
                                                            className="max-h-full max-w-full object-contain pointer-events-none select-none"
                                                            draggable={false}
                                                        />
                                                    ) : (
                                                        <span className="text-base leading-none">{order.preset.bowl.icon || "🍲"}</span>
                                                    )}
                                                </span>
                                                <span className="truncate">{order.preset.bowl.name}</span>
                                            </span>
                                        </div>
                                    ) : null}

                                    {order?.preset?.liquid ? (
                                        <div className="flex flex-col gap-1 flex-1 min-w-[100px]">
                                            <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium pl-1">Колба</span>
                                            <span
                                                className="h-9 flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border text-cyan-300"
                                                style={{
                                                    backgroundColor: order.preset.liquid.hex_color
                                                        ? `${order.preset.liquid.hex_color}20`
                                                        : 'rgba(6,182,212,0.1)',
                                                    borderColor: order.preset.liquid.hex_color
                                                        ? `${order.preset.liquid.hex_color}50`
                                                        : 'rgba(6,182,212,0.3)',
                                                }}
                                            >
                                                <span className="text-base">💧</span>
                                                <span className="truncate">{order.preset.liquid.name}</span>
                                            </span>
                                        </div>
                                    ) : null}
                                </div>

                                <div>
                                    <p className="text-[11px] uppercase tracking-widest text-neutral-600 font-medium mb-2">Вкусы</p>
                                    {flavors.length === 0 ? (
                                        <p className="text-sm text-neutral-500 italic">Вкусы не указаны</p>
                                    ) : (
                                        <div className="space-y-2">
                                            {flavors.map((ing, i) => (
                                                <div key={i} className="flex items-center justify-between gap-3 border-b border-white/5 pb-2 last:border-b-0 last:pb-0">
                                                    <span className="text-sm font-semibold text-neutral-100">
                                                        {ing?.flavor?.name || <span className="text-neutral-500 italic">Неизвестный вкус</span>}
                                                    </span>
                                                    <span className="text-sm font-mono text-cyan-300 tabular-nums font-semibold">
                                                        {ing?.percent ?? "—"}%
                                                    </span>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </>
                        )}
                    </div>
                )}

                <div className="pt-4 border-t border-white/5 flex items-center justify-end gap-3">
                    {canReorder ? (
                        <button
                            onClick={onReorder}
                            disabled={isReordering}
                            className={cn(
                                "inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all",
                                "bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white shadow-[0_0_20px_rgba(192,38,211,0.25)] active:scale-95",
                                isReordering ? "opacity-70" : ""
                            )}
                        >
                            <RotateCcw className="w-4 h-4" />
                            {isReordering ? "Повторяем..." : "Повторить"}
                        </button>
                    ) : (
                        <div className="w-full flex items-center justify-center px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-neutral-400 text-sm font-semibold">
                            Недоступно для повторного заказа
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

const MainOrdersPage = () => {
    const searchParams = useSearchParams();

    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const { showError } = useToast();
    const [expandedOrderId, setExpandedOrderId] = useState(null);
    const [isReorderingById, setIsReorderingById] = useState({});
    const { openConfirm, ConfirmModal, SuccessModal } = usePresetOrderConfirmation({ createOrder });
    const didLoadRef = useRef(false);

    const sortedOrders = useMemo(() => {
        const arr = Array.isArray(orders) ? [...orders] : [];
        arr.sort((a, b) => {
            const at = new Date(a?.created_at || 0).getTime();
            const bt = new Date(b?.created_at || 0).getTime();
            return bt - at;
        });
        return arr;
    }, [orders]);

    useEffect(() => {
        if (didLoadRef.current) return;
        didLoadRef.current = true;

        getOrders()
            .then(data => {
                setOrders(Array.isArray(data) ? data : []);
            })
            .catch(e => {
                showError(e?.message || "Не удалось загрузить историю заказов");
                setOrders([]);
            })
            .finally(() => {
                setLoading(false);
            });
    }, [showError]);

    const handleReorder = async (order) => {
        const presetId = order?.preset?.id;
        if (!order?.can_reorder || !presetId) return;

        const id = order?.id ?? order?.daily_number ?? presetId;
        order.preset.price = order.actual_price;
        openConfirm({
            preset: order.preset,
            title: "Повторить заказ?",
            subtitle: "Вы уверены, что хотите заказать ещё раз?",
            onBeforeSubmit: () => {
                setIsReorderingById(prev => ({ ...prev, [id]: true }));
            },
            onAfterSubmit: () => {
                setIsReorderingById(prev => ({ ...prev, [id]: false }));
            },
        });
    };

    return (
        <section className="min-h-screen bg-neutral-950 flex flex-col items-center w-full overflow-hidden">
            <Nav />

            <div className="w-full max-w-7xl mx-auto px-5 pt-24 pb-12 space-y-8">
                <div className="w-full flex flex-col items-center gap-3 border-b border-white/10 pb-8 text-center">
                    <div>
                        <h1 className="text-4xl font-bold text-white mb-2">История заказов</h1>
                        <p className="text-neutral-400">Ваши заказы, начиная с самых свежих.</p>
                    </div>
                </div>

                {loading ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 w-full items-start">
                        {Array.from({ length: 6 }).map((_, i) => (
                            <OrderCardSkeleton key={i} />
                        ))}
                    </div>
                ) : sortedOrders.length === 0 ? (
                    <div className="py-16 text-center text-neutral-300">
                        <p className="text-lg font-semibold text-white mb-2">Заказов пока нет</p>
                        <p className="text-neutral-500 mb-6">Начните с готовых миксов или соберите свой микс.</p>
                        <div className="flex flex-wrap items-center justify-center gap-3">
                            <Link
                                href={getUrlWithParams('/presets', searchParams)}
                                className="inline-flex items-center justify-center px-5 py-3 rounded-xl bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white font-bold shadow-[0_0_20px_rgba(192,38,211,0.25)] active:scale-95 transition-transform"
                            >
                                Перейти к готовым миксам
                            </Link>
                            <Link
                                href={getUrlWithParams('/builder', searchParams)}
                                className="inline-flex items-center justify-center px-5 py-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-white font-semibold transition-colors"
                            >
                                Собрать микс
                            </Link>
                        </div>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 w-full items-start">
                        {sortedOrders.map((order, index) => {
                            const orderNumber = sortedOrders.length - index;
                            const key = order?.id ?? order?.daily_number ?? order?.created_at ?? `order-${Math.random().toString(16).slice(2)}`;
                            const idForBusy = order?.id ?? order?.daily_number ?? order?.preset?.id ?? key;
                            const expandedKey = order?.id ?? order?.daily_number ?? null;
                            const isExpanded = expandedKey !== null && expandedOrderId === expandedKey;

                            return (
                                <div key={key} id={expandedKey ? `order-${expandedKey}` : undefined}>
                                    <OrderCard
                                        order={order}
                                        orderNumber={orderNumber}
                                        isExpanded={isExpanded}
                                        onToggleExpanded={() => setExpandedOrderId(isExpanded ? null : expandedKey)}
                                        onReorder={() => handleReorder(order)}
                                        isReordering={!!isReorderingById[idForBusy]}
                                    />
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>

            {ConfirmModal}
            {SuccessModal}
        </section>
    );
};

export default MainOrdersPage;