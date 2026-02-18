'use client'

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X, Home, Flame, Grid, Save } from "lucide-react";



const MainBuilderPage = () => {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const [mixName, setMixName] = useState('');


    const handleSave = () => {
    if (!mixName) return toast.error('Please name your mix');
    if (selectedFlavors.length === 0) return toast.error('Add flavors first');
    if (!selectedLiquid) return toast.error('Select a base liquid');

    addPreset({
      name: mixName,
      description: `Custom mix with ${selectedBowl} bowl`,
      ingredients: selectedFlavors,
      liquidId: selectedLiquid,
      category: 'Classic',
      author: 'You',
      likes: 0,
      bowlType: selectedBowl
    });
    
    setMixName('');
    setSelectedFlavors([]);
    setSelectedLiquid(null);
    setSelectedBowl('Classic');
  };




    const navItems = [
        { label: 'Home', path: '/', icon: <Home size={20} /> },
        { label: 'Mix Builde', path: '/builder', icon: <Flame size={20} /> },
        { label: 'Presets', path: '/presets', icon: <Grid size={20} /> }
    ];

    return ( 
        <section className="mt-8 px-5 flex flex-col items-center text-center">
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
            <div className="mt-14 flex flex-col md:flex-row justify-between items-end gap-4 border-b border-white/10 pb-6">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-2">Mix Builder</h1>
                    <p className="text-neutral-400">Compose your perfect bowl. Auto-balanced ratios.</p>
                </div>
                <div className="flex gap-2 w-full md:w-auto">
                    <input 
                        type="text" 
                        placeholder="Name your mix..." 
                        value={mixName}
                        onChange={(e) => setMixName(e.target.value)}
                        className="flex-1 md:w-64 bg-neutral-900 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-cyan-500"
                    />
                    <button 
                        onClick={handleSave}
                        className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg font-medium transition-colors"
                    >
                        <Save size={18} /> Save
                    </button>
                </div>
            </div>
        </section>
  );
};
 
export default MainBuilderPage;