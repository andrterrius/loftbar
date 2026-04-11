'use client'

import { useCallback, useState } from "react";
import { useSearchParams } from 'next/navigation';
import { getUrlWithParams } from '../../utils/urlParams';
import { useToast } from '@/components/shared/ToastProvider';

function cn(...classes) {
  return classes.filter(Boolean).join(" ");
}

function getTableId() {
  return (
    window.Telegram?.WebApp?.initDataUnsafe?.start_param ||
    new URLSearchParams(window.location.search).get("table_id") ||
    "unknown_table"
  );
}

function getStrengthLabel(strength) {
  return {
    label: strength,
    color: "text-neutral-400",
    bg: "bg-neutral-500/10",
    border: "border-neutral-500/30",
  };
}

function StrengthBadge({ strength }) {
  if (!strength && strength !== 0) return null;
  const meta = getStrengthLabel(strength);
  return (
    <div className={`inline-flex items-center gap-1.5 px-3 h-9 rounded-xl text-[12px] font-semibold border ${meta.bg} ${meta.border}`}>
      <span className={`text-base leading-none ${meta.color}`}>⚡</span>
      <span className={meta.color}>{meta.label}</span>
    </div>
  );
}

export function usePresetOrderConfirmation({ createOrder } = {}) {
  const searchParams = useSearchParams();
  const { showError } = useToast();
  
  const [confirmState, setConfirmState] = useState(null); // { preset, title, subtitle, priceLabel }
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successOrderId, setSuccessOrderId] = useState(null);
  const [submitHooks, setSubmitHooks] = useState({ onBeforeSubmit: null, onAfterSubmit: null, onSuccess: null });

  const openConfirm = useCallback(({ preset, title, subtitle, onBeforeSubmit, onAfterSubmit, onSuccess, getOrderPayload }) => {
    if (!preset) return;
    setConfirmState({
      preset,
      title: title || "Подтвердить заказ",
      subtitle: subtitle || "Вы заказываете",
      getOrderPayload: getOrderPayload || null,
    });
    setSubmitHooks({
      onBeforeSubmit: onBeforeSubmit || null,
      onAfterSubmit: onAfterSubmit || null,
      onSuccess: onSuccess || null,
    });
  }, []);

  const closeConfirm = useCallback(() => setConfirmState(null), []);

  const submit = useCallback(async () => {
    if (!confirmState?.preset || !createOrder) return;
    const useCustomPayload = typeof confirmState.getOrderPayload === "function";
    if (!useCustomPayload && !confirmState.preset.id) return;

    setIsSubmitting(true);
    try {
      submitHooks.onBeforeSubmit?.();
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
    }
    const tableId = getTableId();
    const orderData = useCustomPayload
      ? { table_id: tableId, ...confirmState.getOrderPayload() }
      : { table_id: tableId, preset_id: confirmState.preset.id };
    try {
      const result = await createOrder(orderData);
      try {
        submitHooks.onSuccess?.();
      } catch (e) {
        // eslint-disable-next-line no-console
        console.error(e);
      }
      setConfirmState(null);
      setSuccessOrderId(result?.daily_number || "");
      setTimeout(() => window.Telegram?.WebApp?.close(), 4000);
    } catch (error) {
      showError('Ошибка при оформлении заказа. Пожалуйста, попробуйте снова.');
      // eslint-disable-next-line no-console
      console.error(error);
    } finally {
      try {
        submitHooks.onAfterSubmit?.();
      } catch (e) {
        // eslint-disable-next-line no-console
        console.error(e);
      }
      setIsSubmitting(false);
    }
  }, [confirmState, createOrder, submitHooks, showError]);

  const preset = confirmState?.preset;
  const ConfirmModal = preset ? (
    <div
      className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={(e) => e.target === e.currentTarget && closeConfirm()}
    >
      <div className="bg-neutral-900 border border-white/10 rounded-2xl p-6 w-full max-w-sm shadow-2xl">
        <h3 className="text-xl font-bold tracking-tight text-white mb-0.5">{confirmState.title}</h3>
        <p className="text-[11px] uppercase tracking-widest text-neutral-600 font-medium mb-1">{confirmState.subtitle}</p>
        <p className="text-white font-bold text-base tracking-tight mb-4">{preset.name || "Заказ"}</p>

        {(preset.flavors || []).length > 0 && (
          <div className="space-y-2 mb-4 bg-white/5 rounded-xl p-3">
            {preset.flavors.map((ing, i) => (
              <div key={i} className="flex justify-between items-center">
                <span className="text-[14px] font-semibold text-white">{ing.flavor?.name || "Неизвестный вкус"}</span>
                <span className="font-mono text-[12px] text-neutral-300 tabular-nums">{ing.percent}%</span>
              </div>
            ))}
          </div>
        )}

        <div className="flex gap-2 flex-wrap mb-4">
          {preset.bowl && (
            <div className="flex flex-col gap-1">
              <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium pl-1">Чаша</span>
              <span className="h-9 flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[12px] font-semibold bg-fuchsia-500/15 border border-fuchsia-500/30 text-fuchsia-300 min-w-0">
                <span className="inline-flex h-4 w-4 shrink-0 items-center justify-center overflow-hidden">
                  {preset.bowl.image_url ? (
                    <img
                      src={preset.bowl.image_url}
                      alt=""
                      className="max-h-full max-w-full object-contain pointer-events-none select-none"
                      draggable={false}
                    />
                  ) : (
                    <span className="text-base leading-none">{preset.bowl.icon || "🍲"}</span>
                  )}
                </span>
                <span className="truncate">{preset.bowl.name}</span>
              </span>
            </div>
          )}
          {preset.liquid && (
            <div className="flex flex-col gap-1">
              <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium pl-1">Колба</span>
              <span
                className="h-9 flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[12px] font-semibold border text-cyan-300"
                style={{
                  backgroundColor: preset.liquid.hex_color ? `${preset.liquid.hex_color}20` : "rgba(6,182,212,0.1)",
                  borderColor: preset.liquid.hex_color ? `${preset.liquid.hex_color}50` : "rgba(6,182,212,0.3)",
                }}
              >
                <span className="text-base leading-none">💧</span> {preset.liquid.name}
              </span>
            </div>
          )}
          {preset.strength !== undefined && preset.strength !== null && (
            <div className="flex flex-col gap-1">
              <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium pl-1">Крепость</span>
              <StrengthBadge strength={preset.strength} />
            </div>
          )}
        </div>

        <div className="flex items-center justify-between mb-6 pt-4 border-t border-white/5">
          <span className="text-[10px] uppercase tracking-widest text-neutral-600 font-medium">Итого</span>
          <span className="text-white font-bold text-2xl tracking-tight leading-none">
            {preset.price ?? "—"}
            <span className="text-neutral-400 text-lg font-semibold">₽</span>
          </span>
        </div>

        <div className="flex gap-3">
          <button
            onClick={closeConfirm}
            disabled={isSubmitting}
            className="flex-1 py-3 rounded-xl bg-white/5 border border-white/10 text-neutral-400 hover:bg-white/10 transition-all text-[13px] font-semibold disabled:opacity-50"
          >
            Отмена
          </button>
          <button
            onClick={submit}
            disabled={isSubmitting}
            className={cn(
              "flex-1 py-3 rounded-xl bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white font-bold text-[13px] tracking-tight shadow-[0_0_20px_rgba(192,38,211,0.3)] active:scale-95 transition-transform",
              isSubmitting ? "opacity-60" : ""
            )}
          >
            {isSubmitting ? "Отправка..." : "Заказать"}
          </button>
        </div>
      </div>
    </div>
  ) : null;

  const SuccessModal = successOrderId !== null ? (
    <div className="fixed inset-0 z-[70] flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
      <div className="bg-neutral-900 border border-white/10 rounded-2xl p-8 w-full max-w-sm shadow-2xl flex flex-col items-center text-center">
        <div className="w-16 h-16 rounded-full bg-green-500/20 flex items-center justify-center mb-4">
          <span className="text-3xl">✅</span>
        </div>
        <h3 className="text-xl font-bold text-white mb-2">Заказ принят!</h3>
        <p className="text-neutral-400 text-sm mb-1">
          {successOrderId ? `Заказ` : "Ваш заказ"} успешно оформлен.
        </p>
        <p className="text-neutral-500 text-xs mb-6">Ожидайте — ваш микс уже готовится 🔥</p>
        <a
          href={getUrlWithParams('/orders', searchParams)}
          className="w-full py-3 rounded-xl bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white font-bold text-sm shadow-[0_0_20px_rgba(192,38,211,0.3)] text-center block no-underline"
        >
          Отлично
        </a>
      </div>
    </div>
  ) : null;

  return {
    openConfirm,
    closeConfirm,
    isSubmitting,
    ConfirmModal,
    SuccessModal,
    successOrderId,
    setSuccessOrderId,
  };
}

