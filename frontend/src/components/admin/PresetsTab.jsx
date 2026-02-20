'use client'

import { useState } from "react";
import { motion } from "framer-motion";
import { Trash2, Image as ImageIcon, Save, X } from "lucide-react";

const PresetsTab = ({ presets, onDelete, onUpdateImage }) => {
    const [editingId, setEditingId] = useState(null);
    const [imageUrl, setImageUrl] = useState('');

    const handleSaveImage = (presetId) => {
        onUpdateImage(presetId, imageUrl);
        setEditingId(null);
        setImageUrl('');
    };

    const handleStartEdit = (preset) => {
        setEditingId(preset.id);
        setImageUrl(preset.imageUrl || '');
    };

    const handleCancel = () => {
        setEditingId(null);
        setImageUrl('');
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold text-white">Готовые миксы <span className="text-neutral-500 font-normal text-base">({presets.length})</span></h2>
                <p className="text-xs text-neutral-500">Управляйте пресетами и их изображениями</p>
            </div>

            <div className="space-y-3">
                {presets.map(preset => (
                    <motion.div
                        layout
                        key={preset.id}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex flex-col sm:flex-row items-start sm:items-center gap-4 p-4 bg-white/5 border border-white/10 rounded-xl hover:border-white/20 transition-all group"
                    >
                        <div className="w-16 h-16 rounded-xl bg-neutral-800 overflow-hidden shrink-0 flex items-center justify-center">
                            {preset.imageUrl ? (
                                <img src={preset.imageUrl} alt={preset.name} className="w-full h-full object-cover" />
                            ) : (
                                <ImageIcon size={22} className="text-neutral-600" />
                            )}
                        </div>

                        <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-0.5">
                                <h3 className="font-bold text-white text-sm">{preset.name}</h3>
                                <span className="px-2 py-0.5 text-[10px] bg-white/10 rounded-full text-neutral-400">{preset.category}</span>
                            </div>
                            <p className="text-xs text-neutral-500 truncate">{preset.description}</p>
                        </div>

                        <div className="flex items-center gap-2 w-full sm:w-auto">
                            {editingId === preset.id ? (
                                <div className="flex gap-2 flex-1 sm:flex-none">
                                    <input
                                        type="text"
                                        placeholder="Ссылка на изображение"
                                        value={imageUrl}
                                        onChange={e => setImageUrl(e.target.value)}
                                        autoFocus
                                        className="bg-neutral-900 border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:border-cyan-500 w-full sm:w-52 transition-colors placeholder-neutral-600"
                                    />
                                    <button
                                        onClick={() => handleSaveImage(preset.id)}
                                        className="p-2 text-green-400 hover:bg-green-400/10 rounded-lg transition-colors"
                                        title="Сохранить"
                                    >
                                        <Save size={16} />
                                    </button>
                                    <button
                                        onClick={handleCancel}
                                        className="p-2 text-neutral-500 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                                        title="Отмена"
                                    >
                                        <X size={16} />
                                    </button>
                                </div>
                            ) : (
                                <button
                                    onClick={() => handleStartEdit(preset)}
                                    className="p-2 text-cyan-400 hover:bg-cyan-400/10 rounded-lg transition-colors"
                                    title="Изменить изображение"
                                >
                                    <ImageIcon size={16} />
                                </button>
                            )}
                            <button
                                onClick={() => onDelete(preset.id)}
                                className="p-2 text-neutral-600 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-all"
                                title="Удалить"
                            >
                                <Trash2 size={16} />
                            </button>
                        </div>
                    </motion.div>
                ))}

                {presets.length === 0 && (
                    <div className="py-20 text-center text-neutral-600">
                        <ImageIcon size={40} className="mx-auto mb-3 opacity-30" />
                        <p className="text-sm">Нет пресетов</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default PresetsTab;
