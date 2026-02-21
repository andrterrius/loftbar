"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Flame, ArrowRight, Droplets, Menu, X, Home, Grid } from "lucide-react";
import Nav from "./nav";

const MainSection = () => {
  return (
    <section className="mt-8 px-5 flex flex-col items-center text-center">
      {/* --- Navigation --- */}
      <Nav/>

      {/* --- Main Content --- */}
      <motion.h1
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="mt-20 text-4xl font-bold text-white leading-tight"
      >
        <span className="block">Craft Your Perfect</span>
        <span className="block text-transparent bg-clip-text bg-gradient-to-r from-fuchsia-500 via-purple-500 to-cyan-400">
          Shisha Mix
        </span>
      </motion.h1>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.9 }}
        transition={{ delay: 0.2 }}
        className="mt-4 max-w-sm text-zinc-400 text-sm leading-relaxed"
      >
        Discover thousands of flavor combinations and explore community favorites.
      </motion.p>

      <div className="mt-10 flex flex-col gap-4 w-full max-w-[300px]">
        <Link href="/builder" className="w-full">
          <motion.button
            whileTap={{
              scale: 0.96,
              boxShadow: "0px 0px 25px 5px rgba(192, 38, 211, 0.6)",
              filter: "brightness(1.1)"
            }}
            className="flex items-center justify-center gap-2 py-4 w-full bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white font-bold rounded-2xl shadow-lg"
          >
            <span>Собрать Свой Микс</span>
            <Flame className="w-5 h-5 fill-white" />
          </motion.button>
        </Link>

        <Link href="/presets" className="w-full">
          <button className="flex items-center justify-center gap-2 py-4 w-full bg-zinc-900/50 border border-zinc-800 text-white font-semibold rounded-2xl active:scale-95 transition-all hover:bg-zinc-800">
            <span>Готовые миксы</span>
            <ArrowRight className="w-5 h-5 text-zinc-500" />
          </button>
        </Link>
      </div>

      {/* --- Features --- */}
      <div className="mt-12 w-full max-w-[400px] mb-10">
        <div className="flex flex-col gap-4">
          {[
            { title: 'Большая библиотека', desc: 'Более 50 вкусов на выбор', icon: <Droplets className="text-cyan-400" /> },
            { title: 'Сохранение вкусов', desc: 'Сохраняйте любимые комбинации', icon: <Flame className="text-fuchsia-400" /> },
            { title: 'Уникальная подача', desc: 'Чаши в виде фруктов', icon: <ArrowRight className="text-purple-400" /> },
          ].map((item, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="p-6 rounded-[28px] bg-white/5 border border-white/5 text-left active:bg-white/10 transition-colors"
            >
              <div className="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center mb-4">
                {item.icon}
              </div>
              <h3 className="text-xl font-bold mb-2 text-white tracking-tight">{item.title}</h3>
              <p className="text-neutral-400 text-[15px] leading-relaxed">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default MainSection;