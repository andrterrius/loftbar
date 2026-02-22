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
import { FLAVORS, BOWL_OPTIONS, LIQUIDS, PRESETS, SETTINGS, TABS } from "../moks/moks";

const MainAdminPage = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [activeTab, setActiveTab] = useState('flavors');

    const [flavors, setFlavors] = useState(FLAVORS);
    const [liquids, setLiquids] = useState(LIQUIDS);
    const [presets, setPresets] = useState(PRESETS);
    const [bowls, setBowls] = useState(BOWL_OPTIONS); 
    const [settings, setSettings] = useState(SETTINGS);

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