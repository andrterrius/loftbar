"use client";

import { useCallback, useRef, useState } from "react";
import { X } from "lucide-react";
import { useToast } from "@/components/shared/ToastProvider";

export function useImageModal() {
  const { showError } = useToast();
  const [modalImage, setModalImage] = useState(null); // { url, title }
  const [isOpen, setIsOpen] = useState(false);
  const preloadedRef = useRef(new Set());

  const close = useCallback(() => setIsOpen(false), []);

  const preloadImage = useCallback(async (url) => {
    if (!url) return null;
    if (preloadedRef.current.has(url)) return true;

    await new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = resolve;
      img.onerror = reject;
      img.src = url;
    });

    preloadedRef.current.add(url);
    return true;
  }, []);

  const openImageModal = useCallback((imageUrl, title) => {
    if (imageUrl) {
      setModalImage({ url: imageUrl, title });
      setIsOpen(true);
    } else {
      showError("Изображение не добавлено");
    }
  }, [showError]);

  const ImageModal =
    isOpen && modalImage ? (
      <div
        className="fixed inset-0 z-[80] flex items-center justify-center bg-black/80 backdrop-blur-md p-4"
        onClick={close}
      >
        <div
          className="relative max-w-3xl max-h-[90vh] w-full bg-neutral-900 rounded-2xl overflow-hidden border border-white/10 shadow-2xl"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex justify-between items-center p-4 border-b border-white/10">
            <h3 className="text-lg font-semibold text-white">{modalImage.title}</h3>
            <button
              onClick={close}
              className="p-2 rounded-lg hover:bg-white/10 transition-colors text-neutral-400 hover:text-white"
            >
              <X size={20} />
            </button>
          </div>
          <div className="p-4 flex justify-center items-center bg-neutral-950/50">
            <img
              src={modalImage.url}
              alt={modalImage.title}
              className="max-w-full max-h-[70vh] object-contain rounded-lg"
              onError={(e) => {
                e.currentTarget.src = "https://placehold.co/600x400?text=Image+not+found";
              }}
            />
          </div>
        </div>
      </div>
    ) : null;

  return { openImageModal, preloadImage, ImageModal, close, isOpen };
}

