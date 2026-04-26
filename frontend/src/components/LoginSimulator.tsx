"use client";

import { motion } from "framer-motion";
import { UserProfile, MOCK_USERS, useUserStore } from "@/store/userStore";
import { UserCircle2 } from "lucide-react";

export default function LoginSimulator() {
  const setSelectedUser = useUserStore((state) => state.setSelectedUser);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen flex items-center justify-center p-4 bg-hey-black"
    >
      <div className="max-w-md w-full bg-hey-gray rounded-2xl border border-hey-lightGray p-8 shadow-2xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Hey Banco</h1>
          <p className="text-gray-400">Motor de Inteligencia Proactiva</p>
          <div className="mt-4 inline-block px-3 py-1 bg-hey-green/10 text-hey-green rounded-full text-sm font-medium">
            Simulador de Entorno
          </div>
        </div>

        <div className="space-y-4">
          <p className="text-sm text-gray-400 mb-4 text-center">Selecciona un perfil de prueba para cargar su contexto híbrido</p>
          
          {MOCK_USERS.map((user) => (
            <button
              key={user.id}
              onClick={() => setSelectedUser(user)}
              className="w-full flex items-center p-4 rounded-xl border border-hey-lightGray bg-hey-black hover:border-hey-green transition-all group"
            >
              <div className="h-12 w-12 rounded-full bg-hey-gray flex items-center justify-center group-hover:bg-hey-green/20 transition-colors">
                <UserCircle2 className="w-6 h-6 text-gray-400 group-hover:text-hey-green" />
              </div>
              <div className="ml-4 text-left flex-1">
                <h3 className="font-semibold text-white group-hover:text-hey-green transition-colors">{user.id}</h3>
                <p className="text-sm text-gray-400">{user.status} • {user.name}</p>
              </div>
            </button>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
