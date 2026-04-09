// components/MainSection.jsx
"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { History, Flame, ArrowRight, Droplets } from "lucide-react";
import Nav from "./nav";
import { useSearchParams } from 'next/navigation';
import { getUrlWithParams } from '../utils/urlParams';
import { getSettingsImages } from "../utils/api";
import { SETTINGS_IMAGES } from "./moks/moks";
import { useImageModal } from "./shared/useImageModal";

// Отдельный компонент, который использует useSearchParams
const MainSectionContent = () => {
  const searchParams = useSearchParams();
  const { openImageModal, preloadImage, ImageModal } = useImageModal();
  const [settingsImages, setSettingsImages] = useState({ liquids_image_url: null, bowls_image_url: null });

  useEffect(() => {
    getSettingsImages()
      .then((data) => {
        if (data) {
          const next = {
            liquids_image_url: data.liquids_image_url || null,
            bowls_image_url: data.bowls_image_url || null
          };
          setSettingsImages(next);
          preloadImage(next.bowls_image_url);
        }
      })
      .catch(() => {
        const next = {
          liquids_image_url: SETTINGS_IMAGES?.liquids_image_url || null,
          bowls_image_url: SETTINGS_IMAGES?.bowls_image_url || null
        };
        setSettingsImages(next);
        preloadImage(next.bowls_image_url);
      });
  }, [preloadImage]);

  return (
    <>
      <h1 className="mt-20 text-4xl font-bold text-white leading-tight">
        <span className="block">Создай свой идеальный</span>
        <span className="block text-transparent bg-clip-text bg-gradient-to-r from-fuchsia-500 via-purple-500 to-cyan-400">
          кальян
        </span>
      </h1>

      <p className="mt-4 max-w-sm text-zinc-400 text-sm leading-relaxed">
        Открой для себя тысячи комбинаций вкусов
      </p>

      <div className="mt-10 flex flex-col gap-4 w-full max-w-[300px]">
        <Link href={getUrlWithParams('/builder', searchParams)} className="w-full">
          <button className="flex items-center justify-center gap-2 py-4 w-full bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white font-bold rounded-2xl shadow-lg active:scale-95 transition-transform">
            <span>Собрать Свой Кальян</span>
            <Flame className="w-5 h-5 fill-white" />
          </button>
        </Link>

        <Link href={getUrlWithParams('/presets', searchParams)} className="w-full">
          <button className="flex items-center justify-center gap-2 py-4 w-full bg-zinc-900/50 border border-zinc-800 text-white font-semibold rounded-2xl active:scale-95 transition-transform hover:bg-zinc-800">
            <span>Готовые Кальяны</span>
            <ArrowRight className="w-5 h-5 text-zinc-500" />
          </button>
        </Link>
      </div>

      <div className="mt-12 w-full max-w-[400px] mb-10">
        <div className="flex flex-col gap-4">
          {[
            { title: 'Большая библиотека вкусов', desc: 'Более 100 вкусов на выбор', icon: <Droplets className="text-cyan-400" />, href: '/builder' },
            {
              title: 'Уникальная подача',
              desc: 'Чаши в виде фруктов',
              icon: <Flame className="text-purple-400" />,
              href: '',
              onClick: (e) => {
                e.preventDefault();
                openImageModal(settingsImages.bowls_image_url, 'Изображение чаш');
              }
            },
            { title: 'Сохранение миксов', desc: 'История ваших заказов', icon: <History className="text-fuchsia-400" />, href: '/orders' },
          ].map((item, i) => (
            <a
              key={i}
              href={item.href ? getUrlWithParams(item.href, searchParams) : '#'}
              onClick={item.onClick}
              className="block p-6 rounded-[28px] bg-white/5 border border-white/5 text-left transition-all duration-300 hover:scale-[1.02] hover:bg-white/10 hover:border-cyan-400/50 hover:shadow-lg hover:shadow-cyan-400/10 cursor-pointer group"
            >
              <div className="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center mb-4 transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3">
                {item.icon}
              </div>
              <h3 className="text-xl font-bold mb-2 text-white tracking-tight transition-colors duration-300 group-hover:text-cyan-300">
                {item.title}
              </h3>
              <p className="text-neutral-400 text-[15px] leading-relaxed transition-colors duration-300 group-hover:text-neutral-300">
                {item.desc}
              </p>
            </a>
          ))}
        </div>
      </div>

      {ImageModal}
    </>
  );
};

// Основной компонент с Suspense
const MainSection = () => {
  return (
    <section className="mt-8 px-5 flex flex-col items-center text-center">
      <Nav />
      
      <Suspense fallback={
        <div className="mt-20">
          <div className="h-12 w-64 bg-neutral-800 rounded-lg animate-pulse mx-auto" />
          <div className="mt-4 h-6 w-48 bg-neutral-800 rounded-lg animate-pulse mx-auto" />
          <div className="mt-10 flex flex-col gap-4 w-full max-w-[300px] mx-auto">
            <div className="h-14 w-full bg-neutral-800 rounded-2xl animate-pulse" />
            <div className="h-14 w-full bg-neutral-800 rounded-2xl animate-pulse" />
          </div>
        </div>
      }>
        <MainSectionContent />
      </Suspense>
    </section>
  );
};

export default MainSection;