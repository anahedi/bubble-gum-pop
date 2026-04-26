import { create } from 'zustand';

export type UserProfile = {
  id: string;
  name: string;
  age: number;
  education: string;
  city: string;
  status: 'Hey Pro' | 'Negocios' | 'Estándar';
  mainNeed: string;
  frequentClusters: Record<string, number>;
  noiseRatio: string;
  balance: number;
  income: number;
  expenses: number;
};

type StoreState = {
  selectedUser: UserProfile | null;
  setSelectedUser: (user: UserProfile | null) => void;
};

// MOCK DATA based on the clustering pipeline output
export const MOCK_USERS: UserProfile[] = [
  {
    id: 'USR-00005',
    name: 'Ana Martínez',
    age: 28,
    education: 'Licenciatura',
    city: 'Monterrey',
    status: 'Hey Pro',
    mainNeed: 'Crédito, Personal, Credito, Puedo, Quiero',
    frequentClusters: {
      "Ruido": 3,
      "Crédito, Personal, Credito, Puedo, Quiero": 1,
      "Meses, 000, Enganche, 60, 36": 1
    },
    noiseRatio: '60.0%',
    balance: 45000,
    income: 32000,
    expenses: 28000,
  },
  {
    id: 'USR-00002',
    name: 'Carlos Garza',
    age: 35,
    education: 'Maestría',
    city: 'CDMX',
    status: 'Negocios',
    mainNeed: 'Auto, Crédito, Quiero, Automotriz, Credito',
    frequentClusters: {
      "Ruido": 2,
      "Auto, Crédito, Quiero, Automotriz, Credito": 1
    },
    noiseRatio: '66.67%',
    balance: 120500,
    income: 85000,
    expenses: 40000,
  }
];

export const useUserStore = create<StoreState>((set) => ({
  selectedUser: null,
  setSelectedUser: (user) => set({ selectedUser: user }),
}));
