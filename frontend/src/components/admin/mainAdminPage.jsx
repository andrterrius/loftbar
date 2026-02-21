'use client'

import { useState } from "react";
import { motion } from "framer-motion";
import Nav from "../nav";
import AdminLogin from "./AdminLogin";
import FlavorsTab from "./FlavorsTab";
import LiquidsTab from "./LiquidsTab";
import PresetsTab from "./PresetsTab";
import SettingsTab from "./SettingsTab";
import BowlsTab from "./BowlsTab";

const INITIAL_FLAVORS = [
    { id: '1', name: 'Double Apple', brand: 'Al Fakher', category: 'Classic', color: '#dc2626' },
    { id: '2', name: 'Mint', brand: 'Tangiers', category: 'Minty', color: '#16a34a' },
    { id: '3', name: 'Mango', brand: 'Darkside', category: 'Fruity', color: '#eab308' },
    { id: '4', name: 'Peach', brand: 'MustHave', category: 'Fruity', color: '#f97316' },
    { id: '5', name: 'Pinkman', brand: 'MustHave', category: 'Berry', color: '#ec4899' },
    { id: '6', name: 'Pineapple', brand: 'Burn', category: 'Tropical', color: '#facc15' },
];

const INITIAL_BOWL_OPTIONS = [
    { type: 'Classic',    icon: '🏺', isFruit: false },
    { type: 'Silicon',    icon: '⚫', isFruit: false },
    { type: 'Grapefruit', icon: '🍊', isFruit: true  },
    { type: 'Lemon',      icon: '🍋', isFruit: true  },
    { type: 'Orange',     icon: '🍊', isFruit: true  },
    { type: 'Coconut',    icon: '🥥', isFruit: true  },
    { type: 'Pineapple',  icon: '🍍', isFruit: true  },
    { type: 'Pitahaya',   icon: '🐉', isFruit: true  },
    { type: 'Watermelon', icon: '🍉', isFruit: true  },
];

const INITIAL_LIQUIDS = [
    { id: 'water', name: 'Water', description: 'Обычная вода' },
    { id: 'milk', name: 'Milk', description: 'Молоко' },
    { id: 'green_tea', name: 'Green Tea', description: 'Зелёный чай' },
    { id: 'juice', name: 'Juice', description: 'Сок' },
];

const INITIAL_PRESETS = [
    {
        id: '1',
        name: 'Apple Freeze',
        category: 'Fruity',
        description: 'Освежающий бленд двойного яблока и мятного льда.',
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
        description: 'Летнее настроение со сладким манго.',
        imageUrl: null,
        liquidId: 'water',
        ingredients: [
            { flavorId: '3', percentage: 80 },
            { flavorId: '2', percentage: 20 }
        ]
    }
];

const INITIAL_SETTINGS = {
    basePrice: 20,
    fruitBowlSurcharge: 5
};

const TABS = [
    { id: 'flavors', label: 'Вкусы' },
    { id: 'liquids', label: 'Жидкости' },
    { id: 'presets', label: 'Миксы' },
    { id: 'bowls', label: "Чаши"},
    { id: 'settings', label: 'Настройки' },
];

const MainAdminPage = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [activeTab, setActiveTab] = useState('flavors');

    const [flavors, setFlavors] = useState(INITIAL_FLAVORS);
    const [liquids, setLiquids] = useState(INITIAL_LIQUIDS);
    const [presets, setPresets] = useState(INITIAL_PRESETS);
    const [bowls, setBowls] = useState(INITIAL_BOWL_OPTIONS); 
    const [settings, setSettings] = useState(INITIAL_SETTINGS);

    // Flavors
    const addFlavor = (flavor) => setFlavors(prev => [...prev, flavor]);
    const removeFlavor = (id) => setFlavors(prev => prev.filter(f => f.id !== id));

    // Liquids
    const addLiquid = (liquid) => setLiquids(prev => [...prev, liquid]);
    const removeLiquid = (id) => setLiquids(prev => prev.filter(l => l.id !== id));

    // Presets
    const deletePreset = (id) => setPresets(prev => prev.filter(p => p.id !== id));
    const updatePresetImage = (id, imageUrl) => {
        setPresets(prev => prev.map(p => p.id === id ? { ...p, imageUrl } : p));
    };

    // Bowls
    const addBowl = (bowl) => setBowls((prev) => [...prev, bowl])
    const deleteBowl = (bowlType) => setBowls((prev) => prev.filter(b => b.type !== bowlType));

    if (!isAuthenticated) {
        return (
            <section className="min-h-screen bg-neutral-950 flex flex-col">
                <Nav />
                <AdminLogin onLogin={() => setIsAuthenticated(true)} />
            </section>
        );
    }

    return (
        <section className="min-h-screen bg-neutral-950 flex flex-col">
            <Nav />

            <div className="w-full max-w-5xl mx-auto px-4 pt-20 pb-12">
                {/* Header */}
                <div className="flex justify-between items-end py-6 mb-6 border-b border-white/10">
                    <div>
                        <h1 className="text-2xl font-bold text-white">Панель управления</h1>
                        <p className="text-sm text-neutral-500 mt-0.5">Управляйте вкусами, миксами и настройками</p>
                    </div>
                    <button
                        onClick={() => setIsAuthenticated(false)}
                        className="text-xs text-red-400 hover:text-red-300 transition-colors px-3 py-1.5 rounded-lg hover:bg-red-400/10"
                    >
                        Выйти
                    </button>
                </div>

                {/* Tabs */}
                <div className="flex border-b border-white/10 mb-8 overflow-x-auto">
                    {TABS.map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`relative px-5 py-3 text-sm font-medium transition-colors whitespace-nowrap ${
                                activeTab === tab.id
                                    ? 'text-white'
                                    : 'text-neutral-500 hover:text-neutral-300'
                            }`}
                        >
                            {activeTab === tab.id && (
                                <motion.div
                                    layoutId="adminTab"
                                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-cyan-500 rounded-full"
                                />
                            )}
                            {tab.label}
                        </button>
                    ))}
                </div>

                {/* Tab Content */}
                <motion.div
                    key={activeTab}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.2 }}
                >
                    {activeTab === 'flavors' && (
                        <FlavorsTab
                            flavors={flavors}
                            onAdd={addFlavor}
                            onRemove={removeFlavor}
                        />
                    )}
                    {activeTab === 'liquids' && (
                        <LiquidsTab
                            liquids={liquids}
                            onAdd={addLiquid}
                            onRemove={removeLiquid}
                        />
                    )}
                    {activeTab === 'presets' && (
                        <PresetsTab
                            presets={presets}
                            onDelete={deletePreset}
                            onUpdateImage={updatePresetImage}
                        />
                    )}
                    {activeTab === 'bowls' && (
                        <BowlsTab
                            onDelete={deleteBowl}
                            onAdd={addBowl}
                            bowls={bowls}
                        />
                    )}
                    {activeTab === 'settings' && (
                        <SettingsTab
                            settings={settings}
                            onSave={setSettings}
                        />
                    )}
                </motion.div>
            </div>
        </section>
    );
};

export default MainAdminPage;