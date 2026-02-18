"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Flame, ArrowRight, Droplets, Menu, X, Home, Grid } from "lucide-react";

const MainSection = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Данные для навигации
  const navItems = [
    { label: 'Home', path: '/', icon: <Home size={20} /> },
    { label: 'Mix Builde', path: '/builder', icon: <Flame size={20} /> },
    { label: 'Presets', path: '/presets', icon: <Grid size={20} /> }
  ];

  return (
    <section className="mt-8 px-5 flex flex-col items-center text-center">
      {/* Навигация */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/10 bg-neutral-950/80 backdrop-blur-md">
        <div className="mx-auto flex h-14 max-w-sm items-center justify-between px-4">
          <div className="text-lg font-bold text-white tracking-tight">
            LOFT<span className="text-transparent bg-clip-text bg-gradient-to-r from-fuchsia-500 via-purple-500 to-cyan-500">BAR</span>
          </div>
          <div className="flex items-center">
            <button 
              className="p-2 text-neutral-400 transition-colors"
              onClick={() => setIsMobileMenuOpen(prev => !prev)}
            >
              {/* Меняем иконку в зависимости от состояния */}
              {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} strokeWidth={1.5}/>}
            </button>
          </div>
        </div>

        {/* Выпадающее меню */}
        <AnimatePresence>
          {isMobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="overflow-hidden border-t border-white/10 bg-neutral-900"
            >
              <div className="px-4 py-4 space-y-2">
                {navItems.map((item) => (
                  <a
                    key={item.label}
                    href={item.path}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className="flex items-center gap-3 px-4 py-3 rounded-xl text-neutral-400 hover:bg-white/5 hover:text-white transition-all active:scale-95"
                  >
                    {item.icon}
                    <span className="font-medium">{item.label}</span>
                  </a>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>

      {/* главный контент */}
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
        <motion.button
          whileTap={{
            scale: 0.96,
            boxShadow: "0px 0px 25px 5px rgba(192, 38, 211, 0.6)",
            filter: "brightness(1.1)"
          }}
          className="flex items-center justify-center gap-2 py-4 bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white font-bold rounded-2xl shadow-lg"
        >
          <span>Start Mixing</span>
          <Flame className="w-5 h-5 fill-white" />
        </motion.button>

        <button className="flex items-center justify-center gap-2 py-4 bg-zinc-900/50 border border-zinc-800 text-white font-semibold rounded-2xl active:scale-95 transition-transform">
          <span>Explore Presets</span>
          <ArrowRight className="w-5 h-5 text-zinc-500" />
        </button>
      </div>

      <div className="mt-12 w-full max-w-[400px]">
        <div className="flex flex-col gap-4">
          {[
            { title: 'Smart Balancer', desc: 'Auto-adjust percentages for perfect ratios.', icon: <Droplets className="text-cyan-400" /> },
            { title: 'Community Driven', desc: 'Share and discover top-rated mixes.', icon: <Flame className="text-fuchsia-400" /> },
            { title: 'Flavor Library', desc: 'Extensive database of premium tobaccos.', icon: <ArrowRight className="text-purple-400" /> },
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