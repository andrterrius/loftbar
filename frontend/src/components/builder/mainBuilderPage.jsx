'use client'

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
        X, Save, Search, Plus, ShoppingCart, DollarSign 
    } from "lucide-react";
import FlavorCard from "./flavorCard";
import { apiRequest } from "@/utils/api";
import Nav from "../nav";

const mockFlavors = [
  { id: '1', name: 'Double Apple', brand: 'Al Fakher', category: 'Classic', color: '#dc2626' },
  { id: '2', name: 'Mint', brand: 'Tangiers', category: 'Minty', color: '#16a34a' },
  { id: '3', name: 'Mango', brand: 'Darkside', category: 'Fruity', color: '#eab308' },
  { id: '4', name: 'Peach', brand: 'MustHave', category: 'Fruity', color: '#f97316' },
  { id: '5', name: 'Pinkman', brand: 'MustHave', category: 'Berry', color: '#ec4899' },
  { id: '6', name: 'Pineapple', brand: 'Burn', category: 'Tropical', color: '#facc15' },
];

const mockLiquids = [
  { id: 'water', name: 'Water' },
  { id: 'milk', name: 'Milk' },
  { id: 'green_tea', name: 'Green Tea' },
  { id: 'juice', name: 'Juice' },
];

const mockSettings = {
  basePrice: 20,
  fruitBowlSurcharge: 5
};

const BOWL_OPTIONS = [
  { type: 'Classic', icon: '🏺', isFruit: false },
  { type: 'Silicon', icon: '⚫', isFruit: false },
  { type: 'Grapefruit', icon: '🍊', isFruit: true },
  { type: 'Lemon', icon: '🍋', isFruit: true },
  { type: 'Orange', icon: '🍊', isFruit: true },
  { type: 'Coconut', icon: '🥥', isFruit: true },
  { type: 'Pineapple', icon: '🍍', isFruit: true },
  { type: 'Pitahaya', icon: '🐉', isFruit: true },
];


const MainBuilderPage = () => {
    const [selectedFlavors, setSelectedFlavors] = useState([]);
    const [selectedLiquid, setSelectedLiquid] = useState(null);
    const [selectedBowl, setSelectedBowl] = useState('Classic');
    const [isSearchOpen, setIsSearchOpen] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [mixName, setMixName] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Функции
    const handlePercentageChange = (id, newPercentage) => {
      if (selectedFlavors.length <= 1) return;
  
      const index = selectedFlavors.findIndex(f => f.flavorId === id);
      if (index === -1) return;
  
      let targetPct = Math.max(0, Math.min(100, newPercentage));
      
      const others = selectedFlavors.filter(f => f.flavorId !== id);
      const sumOthers = others.reduce((acc, f) => acc + f.percentage, 0);
  
      const remainder = 100 - targetPct;
      let newOthers = [];
  
      if (sumOthers === 0) {
        const share = remainder / others.length;
        newOthers = others.map(f => ({ ...f, percentage: share }));
      } else {
        newOthers = others.map(f => ({
          ...f,
          percentage: (f.percentage / sumOthers) * remainder
        }));
      }
  
      const updated = selectedFlavors.map(f => {
        if (f.flavorId === id) return { ...f, percentage: targetPct };
        const other = newOthers.find(o => o.flavorId === f.flavorId);
        return other || f;
      });
      
      setSelectedFlavors(updated);
    };
  
    const addFlavorToMix = (flavor) => {
      if (selectedFlavors.find(f => f.flavorId === flavor.id)) {
        alert('Flavor already added');
        return;
      }
      if (selectedFlavors.length >= 5) {
        alert('Max 5 flavors allowed');
        return;
      }
  
      if (selectedFlavors.length === 0) {
        setSelectedFlavors([{ flavorId: flavor.id, percentage: 100 }]);
      } else {
        const count = selectedFlavors.length + 1;
        const newPct = 100 / count;
        const updated = selectedFlavors.map(f => ({ ...f, percentage: newPct }));
        updated.push({ flavorId: flavor.id, percentage: newPct });
        setSelectedFlavors(updated);
      }
      setIsSearchOpen(false);
    };
  
    const removeFlavorFromMix = (id) => {
      const remaining = selectedFlavors.filter(f => f.flavorId !== id);
      if (remaining.length === 0) {
        setSelectedFlavors([]);
        return;
      }
      const currentSum = remaining.reduce((acc, f) => acc + f.percentage, 0);
      const scaled = remaining.map(f => ({
        ...f,
        percentage: (f.percentage / currentSum) * 100
      }));
      setSelectedFlavors(scaled);
    };
  
    const calculatePrice = () => {
      const isFruit = BOWL_OPTIONS.find(b => b.type === selectedBowl)?.isFruit;
      return mockSettings.basePrice + (isFruit ? mockSettings.fruitBowlSurcharge : 0);
    };
  
    const handleSave = () => {
        if (!mixName) return alert('Please name your mix');
        if (selectedFlavors.length === 0) return alert('Add flavors first');
        if (!selectedLiquid) return alert('Select a base liquid');

        // Имитация сохранения
        const savedMix = {
            name: mixName,
            ingredients: selectedFlavors,
            liquidId: selectedLiquid,
            bowlType: selectedBowl
        };
        console.log('Mix saved to DB:', savedMix);
        
        alert('Mix saved successfully!');
        setMixName('');
        setSelectedFlavors([]);
        setSelectedLiquid(null);
        setSelectedBowl('Classic');
    };

    const handleOrder = async () => {
        if (selectedFlavors.length === 0) return alert('Mix is empty!');
        if (!selectedLiquid) return alert('Select base liquid!');
        setIsSubmitting(true);
        
        const orderData = {
            name: mixName || "Unnamed Mix",
            ingredients: selectedFlavors.map(f => ({
                flavorId: f.flavorId,
                percentage: f.percentage,
            })),
            liquidId: selectedLiquid,
            bowlType: selectedBowl,
            totalPrice: calculatePrice(),
            createdAt: new Date().toISOString()
        };

        try {
            const response = await apiRequest('api/orders', {
                method: "POST", 
                body: JSON.stringify(orderData),
            });
            if (!response.ok) {
                throw new Error("Ошибка при создании заказа")
            }
            const result = response.json()

            alert(`Заказ #${result.id || ''} успешно оформлен!`);

            setSelectedFlavors([]);
            setSelectedLiquid(null);
            setMixName('');

        } catch (error) {
            console.error("Order error:", error);
            alert('Не удалось отправить заказ. Попробуйте позже.');
        } finally {
            setIsSubmitting(false);
        }
    };

    const filteredFlavors = mockFlavors.filter(f => 
      f.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      f.brand.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return ( 
        <section className="min-h-screen bg-neutral-950 flex flex-col items-center">
            <Nav/>

            <div className="w-full max-w-6xl mx-auto px-5 pt-24 pb-12 space-y-8">
                
                <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-white/10 pb-6 text-left">
                    <div>
                        <h1 className="text-3xl font-bold text-white mb-2">Конструктор Миксов</h1>
                        <p className="text-neutral-400 text-sm md:text-base">Создай свою идеальную чашу</p>
                    </div>
                    <div className="flex flex-col sm:flex-row gap-2 w-full md:w-auto">
                        <input 
                            type="text" 
                            placeholder="Название микса..." 
                            value={mixName}
                            onChange={(e) => setMixName(e.target.value)}
                            className="flex-1 sm:w-64 bg-neutral-900 border border-white/10 rounded-lg px-4 py-3 sm:py-2 text-white focus:outline-none focus:border-cyan-500"
                        />
                        <button 
                            onClick={handleSave}
                            className="flex items-center justify-center gap-2 px-6 py-3 sm:py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg font-medium transition-colors active:scale-95"
                        >
                            <Save size={18} /> Сохранить
                        </button>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 text-left">
                    
                    <div className="lg:col-span-2 space-y-6">
                        <div className="space-y-4">
                            <AnimatePresence>
                            {selectedFlavors.map((sf) => {
                                const flavor = mockFlavors.find(f => f.id === sf.flavorId);
                                if (!flavor) return null;
                                return (
                                <FlavorCard 
                                    key={sf.flavorId}
                                    item={flavor}
                                    percentage={sf.percentage}
                                    color={flavor.color}
                                    onRemove={() => removeFlavorFromMix(sf.flavorId)}
                                    onChange={(val) => handlePercentageChange(sf.flavorId, val)}
                                />
                                );
                            })}
                            </AnimatePresence>
                            
                            {selectedFlavors.length === 0 && (
                            <div className="p-8 border-2 border-dashed border-white/10 rounded-xl flex flex-col items-center justify-center text-neutral-500 h-64">
                                <Plus size={48} className="mb-4 opacity-50" />
                                <p>Выберите вкус</p>
                            </div>
                            )}
                            
                            {selectedFlavors.length < 5 && (
                            <button
                                onClick={() => setIsSearchOpen(true)}
                                className="w-full py-4 border border-white/10 rounded-xl hover:bg-white/5 transition-colors text-cyan-400 flex items-center justify-center gap-2 font-medium active:scale-95"
                            >
                                <Plus size={20} /> Добавить вкус
                            </button>
                            )}
                        </div>
                    </div>

                    <div className="space-y-6">
                        
                        <div className="bg-white/5 border border-white/10 rounded-xl p-6 backdrop-blur-sm text-left">
                            <h3 className="text-lg font-semibold text-white mb-4">Вид Чаши</h3>
                            <div className="grid grid-cols-4 gap-2">
                            {BOWL_OPTIONS.map((bowl) => (
                                <button
                                key={bowl.type}
                                onClick={() => setSelectedBowl(bowl.type)}
                                className={`flex flex-col items-center justify-center p-2 rounded-lg border transition-all aspect-square ${
                                    selectedBowl === bowl.type
                                    ? 'bg-fuchsia-600 border-fuchsia-500 text-white shadow-[0_0_15px_rgba(192,38,211,0.5)]'
                                    : 'bg-white/5 border-transparent hover:bg-white/10 text-neutral-400'
                                }`}
                                title={bowl.type}
                                >
                                <span className="text-2xl mb-1">{bowl.icon}</span>
                                <span className="text-[10px] text-center leading-tight truncate w-full">{bowl.type}</span>
                                </button>
                            ))}
                            </div>
                            {BOWL_OPTIONS.find(b => b.type === selectedBowl)?.isFruit && (
                            <div className="mt-4 text-xs text-fuchsia-300 text-center font-medium bg-fuchsia-500/10 py-2 rounded-lg">
                                +${mockSettings.fruitBowlSurcharge} Fruit Bowl Surcharge
                            </div>
                            )}
                        </div>

                        <div className="bg-white/5 border border-white/10 rounded-xl p-6 backdrop-blur-sm text-left">
                            <h3 className="text-lg font-semibold text-white mb-4">Стандартное наполнение</h3>
                            <div className="grid grid-cols-2 gap-2">
                            {mockLiquids.map((liquid) => (
                                <button
                                key={liquid.id}
                                onClick={() => setSelectedLiquid(liquid.id)}
                                className={`flex flex-col items-start p-3 rounded-lg border transition-all ${
                                    selectedLiquid === liquid.id 
                                    ? 'bg-cyan-500/20 border-cyan-500 text-cyan-300' 
                                    : 'bg-transparent border-white/5 hover:bg-white/5 text-neutral-400'
                                }`}
                                >
                                <span className="text-sm font-medium">{liquid.name}</span>
                                </button>
                            ))}
                            </div>
                        </div>

                        <div className="bg-gradient-to-br from-neutral-900 to-neutral-800 border border-white/10 rounded-xl p-6 shadow-xl">
                            <div className="flex justify-between items-center mb-4">
                            <span className="text-neutral-400">Итоговая цена</span>
                            <span className="text-3xl font-bold text-white flex items-center">
                                <DollarSign size={24} className="text-green-500" />
                                {calculatePrice()}
                            </span>
                            </div>
                            
                            <motion.button
                                whileTap={{ scale: 0.96 }}
                                onClick={handleOrder}
                                className="w-full py-4 bg-gradient-to-r from-fuchsia-600 to-purple-600 text-white rounded-xl font-bold text-lg shadow-[0_0_20px_rgba(192,38,211,0.3)] transition-all flex items-center justify-center gap-2 active:scale-95"
                                disabled={isSubmitting}
                            >
                            <ShoppingCart size={20} /> Сделать заказ
                            </motion.button>
                        </div>
                    </div>
                </div>

                <AnimatePresence>
                    {isSearchOpen && (
                    <div className="fixed inset-0 z-[60] flex items-end sm:items-center justify-center bg-black/60 backdrop-blur-sm sm:p-4">
                        <motion.div
                        initial={{ opacity: 0, y: '100%' }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: '100%' }}
                        transition={{ type: 'spring', damping: 25, stiffness: 300 }}
                        className="w-full h-[85vh] sm:h-auto sm:max-h-[80vh] sm:max-w-lg bg-neutral-900 border-t sm:border border-white/10 rounded-t-3xl sm:rounded-2xl shadow-2xl flex flex-col overflow-hidden"
                        >
                        {/* Drag Handle for mobile */}
                        <div className="w-full flex justify-center pt-3 pb-1 sm:hidden">
                            <div className="w-12 h-1.5 bg-neutral-700 rounded-full"></div>
                        </div>

                        <div className="p-4 border-b border-white/10 flex items-center gap-3">
                            <Search className="text-neutral-500" />
                            <input
                            type="text"
                            placeholder="Поиск вкуса..."
                            autoFocus
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="flex-1 bg-transparent border-none outline-none text-white placeholder-neutral-500"
                            />
                            <button onClick={() => setIsSearchOpen(false)} className="p-2 -mr-2 text-neutral-500 hover:text-white transition-colors">
                                <X size={20} />
                            </button>
                        </div>

                        <div className="flex-1 overflow-y-auto p-2">
                            {filteredFlavors.length === 0 ? (
                            <div className="p-8 text-center text-neutral-500">Вкусы не найдены.</div>
                            ) : (
                            <div className="grid grid-cols-1 gap-1">
                                {filteredFlavors.map(flavor => (
                                <button
                                    key={flavor.id}
                                    onClick={() => addFlavorToMix(flavor)}
                                    disabled={selectedFlavors.some(f => f.flavorId === flavor.id)}
                                    className="flex items-center justify-between p-3 rounded-lg hover:bg-white/5 disabled:opacity-50 disabled:cursor-not-allowed group transition-colors text-left w-full"
                                >
                                    <div className="flex items-center gap-3">
                                    <div 
                                        className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold text-black/60 shrink-0"
                                        style={{ backgroundColor: flavor.color || '#ccc' }}
                                    >
                                        {flavor.name[0]}
                                    </div>
                                    <div>
                                        <div className="font-medium text-white group-hover:text-cyan-400 transition-colors">{flavor.name}</div>
                                        <div className="text-xs text-neutral-500">{flavor.brand} • {flavor.category}</div>
                                    </div>
                                    </div>
                                    <Plus size={18} className="text-neutral-500 group-hover:text-white shrink-0" />
                                </button>
                                ))}
                            </div>
                            )}
                        </div>
                        </motion.div>
                    </div>
                    )}
                </AnimatePresence>
            </div>
        </section>
  );
};
 
export default MainBuilderPage;