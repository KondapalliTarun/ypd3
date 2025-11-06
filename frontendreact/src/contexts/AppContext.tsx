import { createContext, useContext, useState, ReactNode } from 'react';
import { Routine, Asana } from '../types';

interface AppContextType {
  selectedRoutine: Routine | null;
  setSelectedRoutine: (routine: Routine | null) => void;
  selectedAsana: Asana | null;
  setSelectedAsana: (asana: Asana | null) => void;
  isFullRoutine: boolean;
  setIsFullRoutine: (value: boolean) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [selectedRoutine, setSelectedRoutine] = useState<Routine | null>(null);
  const [selectedAsana, setSelectedAsana] = useState<Asana | null>(null);
  const [isFullRoutine, setIsFullRoutine] = useState(false);

  return (
    <AppContext.Provider
      value={{
        selectedRoutine,
        setSelectedRoutine,
        selectedAsana,
        setSelectedAsana,
        isFullRoutine,
        setIsFullRoutine,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
}
