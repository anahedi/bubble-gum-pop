"use client";

import { useUserStore } from "@/store/userStore";
import { Send, Bot, User, Sparkles, ArrowRight, ShieldCheck, CreditCard } from "lucide-react";
import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";

type Message = {
  id: string;
  sender: 'user' | 'bot';
  text?: string;
  isActionCard?: boolean;
  actionType?: 'insurance' | 'credit' | 'pro';
};

export default function ChatPanel() {
  const user = useUserStore((state) => state.selectedUser);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!user) return;
    
    // Simulate initial proactive greeting
    setMessages([]);
    setIsTyping(true);
    
    const timer = setTimeout(() => {
      let initialMsg = "Hola, soy Havi. Estoy analizando tu perfil...";
      let actionCard: Message | null = null;

      if (user.mainNeed.includes("Auto, Crédito")) {
        initialMsg = `Hola ${user.name.split(' ')[0]}. Noté que estás buscando información sobre créditos automotrices. Tenemos una tasa preferencial pre-aprobada para tu perfil Negocios.`;
        actionCard = { id: 'card-1', sender: 'bot', isActionCard: true, actionType: 'credit' };
      } else if (user.mainNeed.includes("Crédito, Personal")) {
        initialMsg = `Hola ${user.name.split(' ')[0]}, vi que tienes dudas sobre créditos personales. Dado tu buen balance, tienes un crédito pre-aprobado.`;
        actionCard = { id: 'card-1', sender: 'bot', isActionCard: true, actionType: 'credit' };
      } else {
        initialMsg = `Hola ${user.name.split(' ')[0]}, ¿en qué puedo ayudarte hoy?`;
      }

      setMessages([{ id: 'msg-1', sender: 'bot', text: initialMsg }]);
      
      if (actionCard) {
        setTimeout(() => {
          setMessages(prev => [...prev, actionCard!]);
          setIsTyping(false);
        }, 800);
      } else {
        setIsTyping(false);
      }
      
    }, 1500);

    return () => clearTimeout(timer);
  }, [user]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const newMsg: Message = { id: Date.now().toString(), sender: 'user', text: inputText };
    setMessages(prev => [...prev, newMsg]);
    setInputText("");
    setIsTyping(true);

    setTimeout(() => {
      setMessages(prev => [...prev, { 
        id: (Date.now() + 1).toString(), 
        sender: 'bot', 
        text: "Entiendo. Estoy registrando esta solicitud en tu perfil para darle seguimiento." 
      }]);
      setIsTyping(false);
    }, 2000);
  };

  if (!user) return null;

  return (
    <div className="flex-1 flex flex-col bg-black relative">
      {/* Header */}
      <div className="h-16 border-b border-hey-lightGray bg-hey-gray/50 backdrop-blur-md flex items-center px-6 justify-between shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-hey-green/20 flex items-center justify-center">
            <Bot className="w-5 h-5 text-hey-green" />
          </div>
          <div>
            <h2 className="text-white font-semibold">Havi Pro</h2>
            <p className="text-xs text-hey-green flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-hey-green animate-pulse" />
              En línea
            </p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        <AnimatePresence initial={false}>
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.sender === 'bot' && !msg.isActionCard && (
                <div className="w-8 h-8 rounded-full bg-hey-gray flex items-center justify-center mr-3 shrink-0">
                  <Bot className="w-4 h-4 text-gray-400" />
                </div>
              )}
              
              {msg.isActionCard ? (
                <div className="ml-11 max-w-[80%] bg-hey-gray border border-hey-lightGray rounded-2xl p-5 overflow-hidden relative group">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-hey-green/5 rounded-full blur-3xl -mr-10 -mt-10 transition-transform group-hover:scale-150" />
                  <div className="flex items-start gap-4 relative z-10">
                    <div className="p-3 bg-hey-black rounded-xl">
                      {msg.actionType === 'credit' ? <CreditCard className="w-6 h-6 text-hey-green" /> : <ShieldCheck className="w-6 h-6 text-hey-green" />}
                    </div>
                    <div>
                      <h4 className="text-white font-semibold mb-1">
                        {msg.actionType === 'credit' ? 'Crédito Pre-aprobado' : 'Mejora tu cuenta'}
                      </h4>
                      <p className="text-sm text-gray-400 mb-4">
                        {msg.actionType === 'credit' 
                          ? `Tienes hasta $${(user.income * 1.5).toLocaleString()} disponibles a una tasa preferencial del 12%.`
                          : 'Activa Hey Pro para acceder a mejores rendimientos en tu inversión.'}
                      </p>
                      <button className="flex items-center gap-2 px-4 py-2 bg-hey-green text-black text-sm font-semibold rounded-lg hover:bg-[#a6cc00] transition-colors">
                        Revisar Oferta <ArrowRight className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ) : (
                <div className={`max-w-[75%] px-5 py-3 rounded-2xl ${
                  msg.sender === 'user' 
                    ? 'bg-hey-green text-black rounded-tr-sm' 
                    : 'bg-hey-gray text-white rounded-tl-sm border border-hey-lightGray'
                }`}>
                  <p className="text-[15px] leading-relaxed">{msg.text}</p>
                </div>
              )}
            </motion.div>
          ))}
          
          {isTyping && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
              <div className="w-8 h-8 rounded-full bg-hey-gray flex items-center justify-center mr-3 shrink-0">
                <Bot className="w-4 h-4 text-gray-400" />
              </div>
              <div className="bg-hey-gray border border-hey-lightGray px-5 py-4 rounded-2xl rounded-tl-sm flex gap-1.5 items-center">
                <motion.div animate={{ y: [0, -5, 0] }} transition={{ repeat: Infinity, duration: 0.6, delay: 0 }} className="w-2 h-2 bg-gray-400 rounded-full" />
                <motion.div animate={{ y: [0, -5, 0] }} transition={{ repeat: Infinity, duration: 0.6, delay: 0.2 }} className="w-2 h-2 bg-gray-400 rounded-full" />
                <motion.div animate={{ y: [0, -5, 0] }} transition={{ repeat: Infinity, duration: 0.6, delay: 0.4 }} className="w-2 h-2 bg-gray-400 rounded-full" />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-6 bg-gradient-to-t from-black to-transparent">
        <form onSubmit={handleSend} className="relative">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Escribe tu consulta..."
            className="w-full bg-hey-gray border border-hey-lightGray rounded-xl py-4 pl-4 pr-14 text-white focus:outline-none focus:border-hey-green transition-colors"
          />
          <button 
            type="submit"
            disabled={!inputText.trim() || isTyping}
            className="absolute right-2 top-2 p-2 bg-hey-green text-black rounded-lg disabled:opacity-50 hover:bg-[#a6cc00] transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
        <div className="flex gap-2 mt-3 overflow-x-auto pb-2 scrollbar-none">
          <button onClick={() => setInputText("¿Cuáles son mis beneficios?")} className="shrink-0 px-3 py-1.5 rounded-full border border-hey-lightGray bg-hey-gray text-xs text-gray-300 hover:text-white hover:border-gray-500 transition-colors flex items-center gap-1.5">
            <Sparkles className="w-3 h-3 text-hey-green" /> ¿Cuáles son mis beneficios?
          </button>
          <button onClick={() => setInputText("Quiero cancelar mi tarjeta")} className="shrink-0 px-3 py-1.5 rounded-full border border-hey-lightGray bg-hey-gray text-xs text-gray-300 hover:text-white hover:border-gray-500 transition-colors">
            Quiero cancelar mi tarjeta
          </button>
        </div>
      </div>
    </div>
  );
}
