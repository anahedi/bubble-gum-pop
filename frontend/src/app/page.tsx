"use client";

import { useUserStore } from "@/store/userStore";
import LoginSimulator from "@/components/LoginSimulator";
import LeftPanel from "@/components/LeftPanel";
import ChatPanel from "@/components/ChatPanel";
import RightPanel from "@/components/RightPanel";
import { LogOut } from "lucide-react";

export default function Home() {
  const user = useUserStore((state) => state.selectedUser);
  const setSelectedUser = useUserStore((state) => state.setSelectedUser);

  if (!user) {
    return <LoginSimulator />;
  }

  return (
    <main className="flex h-screen w-full bg-black overflow-hidden font-sans">
      {/* Absolute Header for Logout */}
      <div className="absolute top-4 left-4 z-50">
        <button 
          onClick={() => setSelectedUser(null)}
          className="p-2 bg-hey-gray rounded-full border border-hey-lightGray hover:border-red-500 hover:text-red-500 transition-colors text-gray-400"
          title="Cerrar Sesión / Cambiar Perfil"
        >
          <LogOut className="w-5 h-5" />
        </button>
      </div>

      {/* Left Panel: Financial Context */}
      <LeftPanel />

      {/* Center Panel: Proactive Chatbot */}
      <ChatPanel />

      {/* Right Panel: Explainability & Insights */}
      <RightPanel />
    </main>
  );
}
