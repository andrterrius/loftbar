'use client'

import Link from "next/link";
import { useState } from "react";
import { Flame, Grid, Home, Menu, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";


const Nav = () => {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    const navItems = [
        { label: 'Главный экран', path: '/', icon: <Home size={20} /> },
        { label: 'Конструктор Миксов', path: '/builder', icon: <Flame size={20} /> },
        { label: 'Готовые миксы', path: '/presets', icon: <Grid size={20} /> }
    ];

    return (
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
                {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} strokeWidth={1.5}/>}
                </button>
            </div>
            </div>

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
                    <Link
                        key={item.label}
                        href={item.path}
                        onClick={() => setIsMobileMenuOpen(false)}
                        className="flex items-center gap-3 px-4 py-3 rounded-xl text-neutral-400 hover:bg-white/5 hover:text-white transition-all active:scale-95"
                    >
                        {item.icon}
                        <span className="font-medium">{item.label}</span>
                    </Link>
                    ))}
                </div>
                </motion.div>
            )}
            </AnimatePresence>
        </nav>
    );
}
 
export default Nav;