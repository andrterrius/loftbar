"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Flame, ArrowRight, Droplets } from "lucide-react";
import Nav from "./nav";

const MainSection = () => {
  return (
    <>
      <section className="mt-8 px-5 flex flex-col items-center text-center">
        <Nav/>

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
          <Link href="/builder" className="w-full">
            <button className="flex items-center justify-center gap-2 py-4 w-full bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white font-bold rounded-2xl shadow-lg active:scale-95 transition-transform">
              <span>Собрать Свой Кальян</span>
              <Flame className="w-5 h-5 fill-white" />
            </button>
          </Link>

          <Link href="/presets" className="w-full">
            <button className="flex items-center justify-center gap-2 py-4 w-full bg-zinc-900/50 border border-zinc-800 text-white font-semibold rounded-2xl active:scale-95 transition-transform hover:bg-zinc-800">
              <span>Готовые Кальяны</span>
              <ArrowRight className="w-5 h-5 text-zinc-500" />
            </button>
          </Link>
        </div>

        <div className="mt-12 w-full max-w-[400px] mb-10">
          <div className="flex flex-col gap-4">
            {[
              { title: 'Большая библиотека', desc: 'Более 50 вкусов на выбор', icon: <Droplets className="text-cyan-400" /> },
              { title: 'Сохранение вкусов', desc: 'Сохраняйте любимые комбинации', icon: <Flame className="text-fuchsia-400" /> },
              { title: 'Уникальная подача', desc: 'Чаши в виде фруктов', icon: <ArrowRight className="text-purple-400" /> },
            ].map((item, i) => (
              <div
                key={i}
                className="p-6 rounded-[28px] bg-white/5 border border-white/5 text-left active:bg-white/10 transition-colors"
              >
                <div className="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center mb-4">
                  {item.icon}
                </div>
                <h3 className="text-xl font-bold mb-2 text-white tracking-tight">{item.title}</h3>
                <p className="text-neutral-400 text-[15px] leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
};

export default MainSection;
