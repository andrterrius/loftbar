'use client'

import { useState } from "react";
import { DollarSign, Check } from "lucide-react";

const SettingsTab = ({ settings, onSave }) => {
    const [form, setForm] = useState(settings);
    const [saved, setSaved] = useState(false);

    const handleSave = () => {
        onSave(form);
        setSaved(true);
        setTimeout(() => setSaved(false), 2000);
    };

    return (
        <div className="space-y-6">
            <h2 className="text-xl font-semibold text-white">Настройки</h2>

            <div className="max-w-md p-6 rounded-xl bg-white/5 border border-white/10 space-y-5">
                <div className="flex items-center gap-3 mb-2">
                    <div className="w-8 h-8 rounded-lg bg-green-500/10 flex items-center justify-center">
                        <DollarSign size={16} className="text-green-400" />
                    </div>
                    <h3 className="font-semibold text-white">Цены</h3>
                </div>

                <div className="space-y-4">
                    <div>
                        <label className="block text-sm text-neutral-400 mb-2">Базовая цена ($)</label>
                        <input
                            type="number"
                            value={form.basePrice}
                            onChange={e => setForm({ ...form, basePrice: Number(e.target.value) })}
                            className="w-full bg-neutral-900 border border-white/10 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-cyan-500 transition-colors"
                        />
                    </div>
                    <div>
                        <label className="block text-sm text-neutral-400 mb-2">Надбавка за фруктовую чашу ($)</label>
                        <input
                            type="number"
                            value={form.fruitBowlSurcharge}
                            onChange={e => setForm({ ...form, fruitBowlSurcharge: Number(e.target.value) })}
                            className="w-full bg-neutral-900 border border-white/10 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-cyan-500 transition-colors"
                        />
                    </div>
                </div>

                <button
                    onClick={handleSave}
                    className={`w-full py-2.5 rounded-lg font-medium text-sm transition-all flex items-center justify-center gap-2 active:scale-95 ${
                        saved
                            ? 'bg-green-600 text-white'
                            : 'bg-white/10 hover:bg-white/15 text-white'
                    }`}
                >
                    {saved ? <><Check size={16} /> Сохранено!</> : 'Сохранить изменения'}
                </button>
            </div>
        </div>
    );
};

export default SettingsTab;
