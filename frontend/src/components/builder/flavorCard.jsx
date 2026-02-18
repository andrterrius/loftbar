'use client'

import { motion } from "framer-motion";
import { X } from "lucide-react";

const FlavorCard = ({ item, percentage, onRemove, onChange, color }) => {
    return ( 
        <motion.div
            layout
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="relative p-4 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm group hover:border-white/20 transition-all text-left"
        >
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="font-bold text-white text-lg">{item.name}</h3>
                    <p className="text-xs text-neutral-400">{item.brand}</p>
                </div>
                <button onClick={onRemove} className="text-neutral-500 hover:text-red-400 transition-colors">
                    <X size={18} />
                </button>
            </div>

            <div className="space-y-2">
                <div className="flex justify-between text-sm">
                    <span className="text-neutral-300">Ratio</span>
                    <span className="font-mono text-cyan-400">{Math.round(percentage)}%</span>
                </div>
                <input
                    type="range"
                    min="0"
                    max="100"
                    value={percentage}
                    onChange={(e) => onChange(parseInt(e.target.value))}
                    className="w-full h-2 bg-neutral-800 rounded-lg appearance-none cursor-pointer accent-cyan-500 hover:accent-cyan-400"
                    style={{
                        background: `linear-gradient(to right, ${color} 0%, ${color} ${percentage}%, #262626 ${percentage}%, #262626 100%)`
                    }}
                />
            </div>
        
            <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-bl from-white/5 to-transparent rounded-tr-xl pointer-events-none" />
            <div 
                className="absolute bottom-0 left-0 w-full h-1 rounded-b-xl opacity-50"
                style={{ backgroundColor: color }}
            />
        </motion.div>
    );
}
 
export default FlavorCard;