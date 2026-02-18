'use client'

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Image as ImageIcon, Heart, ShoppingCart, Filter } from "lucide-react";
import Nav from "../nav";

// Моки заменить на бэк (потом)
const TABS = ['All', 'Fruity', 'Minty', 'Tropical', 'Classic'];

const flavors = [
  { id: '1', name: 'Double Apple', color: '#dc2626' },
  { id: '2', name: 'Mint', color: '#16a34a' },
  { id: '3', name: 'Mango', color: '#eab308' },
];

const liquids = [
  { id: 'water', name: 'Water' },
  { id: 'milk', name: 'Milk' },
];

const settings = {
  basePrice: 20
};

const mockPresets = [
  {
    id: '1',
    name: 'Apple Freeze',
    category: 'Fruity',
    description: 'A refreshing blend of sweet double apple and icy mint.',
    imageUrl: null,
    liquidId: 'water',
    ingredients: [
      { flavorId: '1', percentage: 70 },
      { flavorId: '2', percentage: 30 }
    ]
  },
  {
    id: '2',
    name: 'Tropical Breeze',
    category: 'Tropical',
    description: 'Summer vibes with a sweet mango base.',
    imageUrl: null,
    liquidId: 'water',
    ingredients: [
      { flavorId: '3', percentage: 80 },
      { flavorId: '2', percentage: 20 }
    ]
  }
];

const MainPresetsPage = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [activeTab, setActiveTab] = useState('All');

    // Логика фильтрации
    const displayedPresets = mockPresets.filter(preset => {
      const matchesSearch = preset.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                            preset.description.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesTab = activeTab === 'All' || preset.category === activeTab;
      
      return matchesSearch && matchesTab;
    });

    const handleOrder = (preset) => {
        alert(`Order placed for ${preset.name}! Total: $${settings.basePrice}`);
    };

    return (
        <section className="min-h-screen bg-neutral-950 flex flex-col items-center w-full overflow-hidden">
            <Nav />
            <div className="w-full max-w-7xl mx-auto px-5 pt-24 pb-12 space-y-8 flex flex-col items-center">
                <div className="w-full flex flex-col items-center gap-6 border-b border-white/10 pb-8 text-center">
                    <div>
                        <h1 className="text-4xl font-bold text-white mb-2">Галерея миксов</h1>
                        <p className="text-neutral-400">Исследуй вкусы сообщества</p>
                    </div>
                    
                    <div className="flex justify-center w-full">
                        <div className="relative group w-full max-w-sm">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-neutral-500 group-focus-within:text-cyan-400 transition-colors" size={18} />
                            <input 
                                type="text" 
                                placeholder="Поиск миксов..." 
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full bg-neutral-900 border border-white/10 rounded-xl pl-10 pr-4 py-2.5 text-white focus:outline-none focus:border-cyan-500/50 focus:bg-neutral-800 transition-all"
                            />
                        </div>
                    </div>
                </div>

                <div className="w-full border-b border-white/10 pb-4"> 
                    <div className="flex overflow-x-auto gap-2 px-5 scrollbar-hide justify-start md:justify-center">
                        {TABS.map((tab) => (
                            <button
                                key={tab}
                                onClick={() => setActiveTab(tab)}
                                className={`relative px-6 py-2 rounded-full text-sm font-medium transition-colors whitespace-nowrap 
                                    ${
                                        activeTab === tab ? 'text-white' : 'text-neutral-400 hover:text-white'
                                    }`
                                }
                            >
                                {activeTab === tab && (
                                    <motion.div
                                        layoutId="activeTab"
                                        className="absolute inset-0 bg-white/10 rounded-full"
                                        transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                                    />
                                )}
                                <span className="relative z-10">{tab}</span>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Grid */}
                <motion.div 
                    layout
                    className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full text-left"
                >
                    <AnimatePresence mode='popLayout'>
                        {displayedPresets.map((preset) => {
                            const liquid = liquids.find(l => l.id === preset.liquidId);
                            
                            return (
                                <motion.div
                                    layout
                                    initial={{ opacity: 0, scale: 0.9 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    exit={{ opacity: 0, scale: 0.9 }}
                                    key={preset.id}
                                    className="group relative bg-white/5 border border-white/10 rounded-2xl overflow-hidden hover:border-white/20 transition-all hover:-translate-y-1 hover:shadow-xl flex flex-col w-full"
                                >

                                    <div className="h-48 bg-neutral-800 relative overflow-hidden">
                                        {preset.imageUrl ? (
                                            <img 
                                                src={preset.imageUrl} 
                                                alt={preset.name} 
                                                className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                                            />
                                        ) : (
                                            <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-neutral-800 to-neutral-900">
                                                <ImageIcon className="text-neutral-700" size={48} />
                                            </div>
                                        )}
                                        
                                        <div className="absolute inset-0 bg-gradient-to-t from-neutral-900 via-transparent to-transparent opacity-90" />
                                        
                                        <div className="absolute top-4 left-4 right-4 flex justify-between items-start z-10">
                                            <span className="px-2 py-1 rounded-md bg-black/60 text-xs text-white backdrop-blur-md border border-white/10">
                                                {preset.category}
                                            </span>
                                            <button className="p-2 rounded-full bg-black/40 text-white hover:bg-fuchsia-500 hover:text-white transition-colors backdrop-blur-md border border-white/10">
                                                <Heart size={16} />
                                            </button>
                                        </div>
                                        
                                        <div className="absolute bottom-4 left-4 flex -space-x-2 z-10">
                                            {preset.ingredients.map((ing, i) => {
                                                const f = flavors.find(fl => fl.id === ing.flavorId);
                                                return (
                                                    <div 
                                                        key={i}
                                                        className="w-8 h-8 rounded-full border-2 border-neutral-900 bg-neutral-800 flex items-center justify-center text-[10px] text-white font-bold shadow-lg"
                                                        style={{ backgroundColor: f?.color }}
                                                        title={`${f?.name} (${ing.percentage}%)`}
                                                    >
                                                        {f?.name?.[0] || '?'}
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </div>

                                    <div className="p-5 flex-1 flex flex-col space-y-4">
                                        <div>
                                            <h3 className="text-lg font-bold text-white group-hover:text-cyan-400 transition-colors">{preset.name}</h3>
                                            <p className="text-xs text-neutral-400 mt-1 line-clamp-2">{preset.description}</p>
                                        </div>

                                        <div className="space-y-2 flex-1">
                                            {preset.ingredients.slice(0, 3).map((ing, i) => {
                                                const f = flavors.find(fl => fl.id === ing.flavorId);
                                                return (
                                                    <div key={i} className="flex justify-between text-xs text-neutral-300">
                                                        <span>{f?.name || 'Unknown flavor'}</span>
                                                        <span className="text-neutral-500">{ing.percentage}%</span>
                                                    </div>
                                                );
                                            })}
                                        </div>

                                        <div className="pt-4 border-t border-white/5 flex justify-between items-center mt-auto">
                                            <div className="flex flex-col">
                                                <span className="text-[10px] text-neutral-500">Price</span>
                                                <span className="text-lg font-bold text-white">${settings.basePrice}</span>
                                            </div>
                                            <button 
                                                onClick={() => handleOrder(preset)}
                                                className="px-4 py-2 bg-white/10 hover:bg-fuchsia-600 hover:text-white text-neutral-300 rounded-lg text-sm font-medium transition-all flex items-center gap-2"
                                            >
                                                <ShoppingCart size={16} /> Заказ
                                            </button>
                                        </div>
                                    </div>
                                </motion.div>
                            );
                        })}
                    </AnimatePresence>
                </motion.div>
                
                {displayedPresets.length === 0 && (
                    <div className="py-20 text-center text-neutral-500 w-full">
                        <Filter size={48} className="mx-auto mb-4 opacity-20" />
                        <p>Не найдено шаблонов по запросу.</p>
                    </div>
                )}
            </div>
        </section>
    );
}
 
export default MainPresetsPage;