"use client";

import { useUserStore } from "@/store/userStore";
import { BrainCircuit, Info, Target, Zap, LayoutList } from "lucide-react";
import { motion } from "framer-motion";

export default function RightPanel() {
  const user = useUserStore((state) => state.selectedUser);

  if (!user) return null;

  return (
    <div className="w-80 bg-hey-gray border-l border-hey-lightGray h-full flex flex-col overflow-y-auto">
      {/* Header */}
      <div className="p-6 border-b border-hey-lightGray bg-hey-black/50">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <BrainCircuit className="w-5 h-5 text-hey-green" />
          Explainability AI
        </h2>
        <p className="text-xs text-gray-400 mt-1">
          Por qué la Inteligencia Proactiva tomó esta decisión
        </p>
      </div>

      <div className="p-6 space-y-8">
        {/* Why I see this */}
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.1 }}>
          <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
            <Info className="w-4 h-4 text-hey-green" />
            ¿Por qué Havi actuó así?
          </h3>
          <div className="bg-hey-black rounded-xl p-4 border border-hey-lightGray text-sm text-gray-300 space-y-3">
            <p>
              El modelo semántico <span className="text-white font-medium">BERT</span> y el clusterer <span className="text-white font-medium">HDBSCAN</span> detectaron que este usuario pertenece al segmento:
            </p>
            <div className="px-3 py-2 bg-hey-gray rounded border border-gray-700 font-mono text-xs text-hey-green">
              "{user.mainNeed.split(',')[0]}, {user.mainNeed.split(',')[1]}"
            </div>
            <p>
              Además, el historial transaccional indica que el nivel de ingresos actual permite aprobar un producto de mayor nivel.
            </p>
          </div>
        </motion.div>

        {/* NLP Stats */}
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }}>
          <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
            <Target className="w-4 h-4 text-hey-green" />
            Métricas de Interacción NLP
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center text-sm">
              <span className="text-gray-400">Ratio de Ruido</span>
              <span className={`font-mono font-medium ${parseFloat(user.noiseRatio) > 50 ? 'text-red-400' : 'text-hey-green'}`}>
                {user.noiseRatio}
              </span>
            </div>
            
            <div className="pt-2">
              <span className="text-xs text-gray-500 uppercase font-semibold tracking-wider">Top Clusters Históricos</span>
              <div className="mt-2 space-y-2">
                {Object.entries(user.frequentClusters).map(([cluster, freq], idx) => (
                  <div key={idx} className="flex justify-between items-center bg-hey-black px-3 py-2 rounded border border-hey-lightGray">
                    <span className="text-xs text-gray-300 truncate w-4/5">{cluster}</span>
                    <span className="text-xs font-mono text-hey-green bg-hey-green/10 px-1.5 py-0.5 rounded">{freq}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>

        {/* Suggested Products */}
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }}>
          <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
            <LayoutList className="w-4 h-4 text-hey-green" />
            Portafolio Sugerido
          </h3>
          <div className="bg-hey-black rounded-xl border border-hey-lightGray overflow-hidden">
            <div className="p-3 border-b border-hey-lightGray flex justify-between items-center hover:bg-hey-gray transition-colors cursor-pointer">
              <span className="text-sm text-white font-medium">Cuenta Hey Pro</span>
              <Zap className="w-4 h-4 text-hey-green" />
            </div>
            <div className="p-3 border-b border-hey-lightGray flex justify-between items-center hover:bg-hey-gray transition-colors cursor-pointer">
              <span className="text-sm text-gray-300">Seguro de Auto</span>
              <span className="text-xs text-gray-500">Pendiente</span>
            </div>
            <div className="p-3 flex justify-between items-center hover:bg-hey-gray transition-colors cursor-pointer">
              <span className="text-sm text-gray-300">Inversión a 7 días</span>
              <span className="text-xs text-hey-green">Activo</span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
