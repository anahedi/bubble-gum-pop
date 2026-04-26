"use client";

import { useUserStore } from "@/store/userStore";
import { User, Briefcase, MapPin, Activity, Wallet, ArrowUpRight, ArrowDownRight } from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

export default function LeftPanel() {
  const user = useUserStore((state) => state.selectedUser);

  if (!user) return null;

  const chartData = [
    { name: "Ingresos", value: user.income, color: "#CDFF00" }, // hey-green
    { name: "Gastos", value: user.expenses, color: "#FF453A" },  // red
  ];

  return (
    <div className="w-80 bg-hey-gray border-r border-hey-lightGray h-full flex flex-col p-6 overflow-y-auto">
      <div className="mb-8 flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Hey Contexto</h2>
        <span className="px-2 py-1 bg-hey-lightGray rounded text-xs text-gray-300 border border-gray-700">
          {user.id}
        </span>
      </div>

      {/* Perfil Header */}
      <div className="flex items-center gap-4 mb-6">
        <div className="h-16 w-16 bg-hey-black rounded-full border-2 border-hey-green flex items-center justify-center">
          <User className="text-hey-green w-8 h-8" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-white">{user.name}</h3>
          <p className="text-sm text-hey-green font-medium">{user.status}</p>
        </div>
      </div>

      {/* Info Demográfica */}
      <div className="space-y-3 mb-8 bg-hey-black p-4 rounded-xl border border-hey-lightGray">
        <div className="flex items-center text-sm text-gray-400">
          <Briefcase className="w-4 h-4 mr-3 text-gray-500" />
          {user.education}
        </div>
        <div className="flex items-center text-sm text-gray-400">
          <MapPin className="w-4 h-4 mr-3 text-gray-500" />
          {user.city}, {user.age} años
        </div>
      </div>

      {/* Salud Financiera */}
      <div className="mb-8">
        <h4 className="text-sm font-semibold text-white mb-4 flex items-center">
          <Activity className="w-4 h-4 mr-2 text-hey-green" />
          Salud Financiera
        </h4>
        
        <div className="bg-hey-black p-4 rounded-xl border border-hey-lightGray relative h-40 flex items-center justify-center">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                innerRadius={40}
                outerRadius={55}
                paddingAngle={5}
                dataKey="value"
                stroke="none"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ backgroundColor: '#1C1C1E', border: '1px solid #2C2C2E', borderRadius: '8px', color: '#fff' }}
                itemStyle={{ color: '#fff' }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
            <span className="text-xs text-gray-400">Balance</span>
            <span className="text-sm font-bold text-white">${(user.balance / 1000).toFixed(1)}k</span>
          </div>
        </div>

        <div className="flex gap-2 mt-3">
          <div className="flex-1 bg-hey-black p-3 rounded-lg border border-hey-lightGray">
            <div className="flex items-center text-xs text-gray-400 mb-1">
              <ArrowUpRight className="w-3 h-3 mr-1 text-hey-green" /> Ingresos
            </div>
            <p className="text-sm font-semibold text-white">${(user.income / 1000).toFixed(1)}k</p>
          </div>
          <div className="flex-1 bg-hey-black p-3 rounded-lg border border-hey-lightGray">
            <div className="flex items-center text-xs text-gray-400 mb-1">
              <ArrowDownRight className="w-3 h-3 mr-1 text-red-500" /> Gastos
            </div>
            <p className="text-sm font-semibold text-white">${(user.expenses / 1000).toFixed(1)}k</p>
          </div>
        </div>
      </div>

      {/* Cluster Detectado */}
      <div className="mt-auto">
        <h4 className="text-sm font-semibold text-white mb-3">Clasificación BERT</h4>
        <div className="p-3 bg-hey-green/10 border border-hey-green/30 rounded-lg">
          <p className="text-xs text-hey-green font-mono break-words leading-relaxed">
            {user.mainNeed}
          </p>
        </div>
      </div>
    </div>
  );
}
